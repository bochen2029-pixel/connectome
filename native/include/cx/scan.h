// cx/scan.h - cx-index: the two-pass exact scan.  Spec section 5.4.
//
// SCAN, DON'T SEEK.  There is no ANN index to build, tune, or let rot: the coarse
// pass is a brute-force int8 dot product against every row, and the fine pass is an
// exact rescoring of a few thousand gathered rows.  Vectors are Matryoshka heads of
// one embedding, L2-normalised then quantised to int8, so every score is an exact
// int32 dot product.  Consequences that matter:
//
//   * bit-identical across runs, across devices, and between CPU and GPU, because
//     integer addition is associative and the reduction topology is fixed;
//   * no float atomics anywhere on a reduction path (booster house rule);
//   * recall is exact, which removes an entire class of retrieval bugs.

#pragma once

#include <cstdint>
#include <string>
#include <vector>

#include "cx/cx.h"

namespace cx {

struct ScanHit {
    ChunkId      id    = -1;
    std::int32_t score = 0;
};

struct DeviceInfo {
    bool         present   = false;
    std::string  name      = "none";
    int          cc_major  = 0;
    int          cc_minor  = 0;
    std::size_t  mem_total = 0;
    std::size_t  mem_free  = 0;
    int          driver    = 0;
    int          runtime   = 0;
};

// Exact dot products of q against every row of X (n x d, row-major, int8).
// `out` must hold n int32 values.
void dot_i8_cpu(const std::int8_t* X, std::int64_t n, int d, const std::int8_t* q,
                std::int32_t* out);

// Same contract, on the GPU.  One warp per row, __dp4a over int8x4 lanes, then a
// fixed-topology shuffle reduction.  Requires d % 4 == 0.  Throws std::runtime_error
// on any CUDA failure or when the build has no CUDA.
void dot_i8_gpu(const std::int8_t* X, std::int64_t n, int d, const std::int8_t* q,
                std::int32_t* out);

bool       cuda_available();
DeviceInfo cuda_device_info();

// ---------------------------------------------------------------------------
// The resident matrix.  dot_i8_gpu above copies X to the device on every call,
// which is only ever right for a one-shot scan: measured on this box, a 30 MiB
// coarse pass spends more time on the transfer than the CPU spends on the whole
// scan.  The spec's design is the opposite - the coarse head lives in VRAM at
// every corpus scale (spec 4.3, 10.3) and a query touches it without moving it.
// Upload once, query for the life of the process.
// ---------------------------------------------------------------------------
struct GpuMatrix;

GpuMatrix* gpu_upload(const std::int8_t* X, std::int64_t n, int d);
void       gpu_free(GpuMatrix* m);
std::int64_t gpu_rows(const GpuMatrix* m);

// Exact dot products of q against every resident row.  Same kernel, same integer
// arithmetic, same bit-identical result as dot_i8_cpu - only the transfer is gone.
void dot_i8_resident(const GpuMatrix* m, const std::int8_t* q, std::int32_t* out);

// Deterministic top-k: score descending, chunk id ascending on ties.  A stable
// tie-break is not cosmetic - it is what makes the gate "byte-identical across
// runs" meaningful when many chunks share a score.
std::vector<ScanHit> topk(const std::int32_t* scores, std::int64_t n, int k);

// The two-pass scan: coarse pass over all n rows at dc dims, then exact rescoring
// of the coarse top-`coarse_k` rows at df dims, returning the final top-`final_k`.
// Spec 5.4 sizes this at dc = 128 (resident in VRAM at every corpus scale) and
// df = 1024 (resident to ~3.5 GB, NVMe-mapped beyond).
std::vector<ScanHit> two_pass(const std::int8_t* Xc, int dc,
                              const std::int8_t* Xf, int df,
                              const std::int8_t* qc, const std::int8_t* qf,
                              std::int64_t n, int coarse_k, int final_k,
                              bool use_gpu);

// FNV-1a over the (id, score) pairs of a result.  The gate runs a fixed selftest in
// two separate processes and compares this digest; equality is the M0 acceptance.
std::uint64_t digest(const std::vector<ScanHit>& hits);

} // namespace cx
