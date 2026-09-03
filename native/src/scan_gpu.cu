// cx-index, GPU half.  Spec section 5.4 and 10.1.
//
// Determinism by construction, not by tolerance: the scores are int32 sums of int8
// products, the reduction is a fixed-topology warp shuffle, and no float atomic
// appears anywhere.  The same input therefore yields byte-identical output on every
// run, on every supported architecture, and identical to the CPU reference - which
// is what makes the M0 gate ("byte-identical scans across runs and against the
// reference") a real test rather than a tolerance check.

#include "cx/scan.h"

#include <cuda_runtime.h>

#include <stdexcept>
#include <string>

namespace {

void check(cudaError_t e, const char* what) {
    if (e != cudaSuccess) {
        throw std::runtime_error(std::string(what) + ": " + cudaGetErrorString(e));
    }
}

// RAII so a throw between allocations cannot leak device memory.
struct DevBuf {
    void* p = nullptr;
    explicit DevBuf(std::size_t bytes) { check(cudaMalloc(&p, bytes), "cudaMalloc"); }
    ~DevBuf() { if (p) cudaFree(p); }
    DevBuf(const DevBuf&) = delete;
    DevBuf& operator=(const DevBuf&) = delete;
};

// One warp per row; each lane strides over the row in int8x4 words.
__global__ void dot_i8_kernel(const int* __restrict__ X4, const int* __restrict__ q4,
                              int* __restrict__ out, long long n, int d4) {
    const long long warp =
        (static_cast<long long>(blockIdx.x) * blockDim.x + threadIdx.x) >> 5;
    const int lane = static_cast<int>(threadIdx.x) & 31;
    if (warp >= n) return;

    const int* row = X4 + warp * static_cast<long long>(d4);
    int acc = 0;
    for (int k = lane; k < d4; k += 32) {
        acc = __dp4a(row[k], q4[k], acc);   // four int8 products, accumulated in int32
    }
#pragma unroll
    for (int off = 16; off > 0; off >>= 1) {
        acc += __shfl_down_sync(0xffffffffu, acc, off);
    }
    if (lane == 0) out[warp] = acc;
}

} // namespace

namespace cx {

bool cuda_available() {
    int count = 0;
    return cudaGetDeviceCount(&count) == cudaSuccess && count > 0;
}

DeviceInfo cuda_device_info() {
    DeviceInfo info;
    int count = 0;
    if (cudaGetDeviceCount(&count) != cudaSuccess || count <= 0) return info;

    cudaDeviceProp prop{};
    if (cudaGetDeviceProperties(&prop, 0) != cudaSuccess) return info;

    info.present  = true;
    info.name     = prop.name;
    info.cc_major = prop.major;
    info.cc_minor = prop.minor;

    std::size_t freeB = 0, totalB = 0;
    if (cudaMemGetInfo(&freeB, &totalB) == cudaSuccess) {
        info.mem_free  = freeB;
        info.mem_total = totalB;
    }
    cudaDriverGetVersion(&info.driver);
    cudaRuntimeGetVersion(&info.runtime);
    return info;
}

// --- the resident matrix ---------------------------------------------------

struct GpuMatrix {
    std::int8_t*  X = nullptr;    // n x d, row-major, device memory
    std::int8_t*  q = nullptr;    // one query, device memory
    std::int32_t* out = nullptr;  // n scores, device memory
    std::int64_t  n = 0;
    int           d = 0;
};

GpuMatrix* gpu_upload(const std::int8_t* X, std::int64_t n, int d) {
    if (d % 4 != 0) {
        throw std::runtime_error("gpu_upload: d must be a multiple of 4");
    }
    auto* m = new GpuMatrix();
    m->n = n;
    m->d = d;
    try {
        const std::size_t bytesX = static_cast<std::size_t>(n) * static_cast<std::size_t>(d);
        check(cudaMalloc(reinterpret_cast<void**>(&m->X), bytesX), "cudaMalloc resident X");
        check(cudaMalloc(reinterpret_cast<void**>(&m->q), static_cast<std::size_t>(d)),
              "cudaMalloc resident q");
        check(cudaMalloc(reinterpret_cast<void**>(&m->out),
                         static_cast<std::size_t>(n) * sizeof(std::int32_t)),
              "cudaMalloc resident out");
        check(cudaMemcpy(m->X, X, bytesX, cudaMemcpyHostToDevice), "cudaMemcpy resident X");
    } catch (...) {
        gpu_free(m);
        throw;
    }
    return m;
}

void gpu_free(GpuMatrix* m) {
    if (!m) return;
    if (m->X) cudaFree(m->X);
    if (m->q) cudaFree(m->q);
    if (m->out) cudaFree(m->out);
    delete m;
}

std::int64_t gpu_rows(const GpuMatrix* m) { return m ? m->n : 0; }

void dot_i8_resident(const GpuMatrix* m, const std::int8_t* q, std::int32_t* out) {
    if (!m || m->n <= 0) return;
    check(cudaMemcpy(m->q, q, static_cast<std::size_t>(m->d), cudaMemcpyHostToDevice),
          "cudaMemcpy q");

    constexpr int kThreads = 256;
    const long long warps_per_block = kThreads / 32;
    const long long blocks = (m->n + warps_per_block - 1) / warps_per_block;

    dot_i8_kernel<<<static_cast<unsigned>(blocks), kThreads>>>(
        reinterpret_cast<const int*>(m->X), reinterpret_cast<const int*>(m->q), m->out,
        static_cast<long long>(m->n), m->d / 4);

    check(cudaGetLastError(), "dot_i8_kernel launch (resident)");
    check(cudaMemcpy(out, m->out, static_cast<std::size_t>(m->n) * sizeof(std::int32_t),
                     cudaMemcpyDeviceToHost),
          "cudaMemcpy scores");
}

void dot_i8_gpu(const std::int8_t* X, std::int64_t n, int d, const std::int8_t* q,
                std::int32_t* out) {
    if (d % 4 != 0) {
        throw std::runtime_error("dot_i8_gpu: d must be a multiple of 4 (got " +
                                 std::to_string(d) + ")");
    }
    if (n <= 0) return;

    const int d4 = d / 4;
    const std::size_t bytesX = static_cast<std::size_t>(n) * static_cast<std::size_t>(d);
    const std::size_t bytesQ = static_cast<std::size_t>(d);
    const std::size_t bytesO = static_cast<std::size_t>(n) * sizeof(std::int32_t);

    DevBuf dX(bytesX), dQ(bytesQ), dO(bytesO);
    check(cudaMemcpy(dX.p, X, bytesX, cudaMemcpyHostToDevice), "cudaMemcpy X");
    check(cudaMemcpy(dQ.p, q, bytesQ, cudaMemcpyHostToDevice), "cudaMemcpy q");

    constexpr int kThreads = 256;                 // 8 warps per block
    const long long warps_per_block = kThreads / 32;
    const long long blocks = (n + warps_per_block - 1) / warps_per_block;

    dot_i8_kernel<<<static_cast<unsigned>(blocks), kThreads>>>(
        static_cast<const int*>(dX.p), static_cast<const int*>(dQ.p),
        static_cast<int*>(dO.p), static_cast<long long>(n), d4);

    check(cudaGetLastError(), "dot_i8_kernel launch");
    check(cudaMemcpy(out, dO.p, bytesO, cudaMemcpyDeviceToHost), "cudaMemcpy out");
}

} // namespace cx
