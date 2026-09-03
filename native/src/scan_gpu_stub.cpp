// cx-index, GPU half, absent.  Built when -DCX_WITH_CUDA=OFF so the CPU reference
// is the whole engine: every gate still runs, more slowly, on a machine with no
// NVIDIA GPU.  The reference is not a mock - it is the definition the GPU path is
// held to (spec 5.4).

#include "cx/scan.h"

#include <stdexcept>

namespace cx {

bool cuda_available() { return false; }

DeviceInfo cuda_device_info() {
    DeviceInfo info;
    info.name = "none (built with CX_WITH_CUDA=OFF)";
    return info;
}

void dot_i8_gpu(const std::int8_t*, std::int64_t, int, const std::int8_t*, std::int32_t*) {
    throw std::runtime_error(
        "dot_i8_gpu: this build has no CUDA; configure with -DCX_WITH_CUDA=ON");
}

GpuMatrix* gpu_upload(const std::int8_t*, std::int64_t, int) {
    throw std::runtime_error(
        "gpu_upload: this build has no CUDA; configure with -DCX_WITH_CUDA=ON");
}

void gpu_free(GpuMatrix*) {}

std::int64_t gpu_rows(const GpuMatrix*) { return 0; }

void dot_i8_resident(const GpuMatrix*, const std::int8_t*, std::int32_t*) {
    throw std::runtime_error(
        "dot_i8_resident: this build has no CUDA; configure with -DCX_WITH_CUDA=ON");
}

} // namespace cx
