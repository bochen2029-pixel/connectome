// cx - the command line surface of the native core.
//
//   cx doctor [--json]                 what this machine has and is missing
//   cx bench  [--n N] [--d D] [--iters I]   the two-pass scan, measured
//   cx selftest [--seed S]             a fixed scan; prints a digest the gate compares
//   cx version
//
// Spec: docs/CONNECTOME_v5.5_THE-FIELD_2026-09-03.md

#include "cx/scan.h"
#include "cx/synth.h"

#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <stdexcept>
#include <string>
#include <vector>

namespace cx {
int doctor(bool json);
}

namespace {

using cx::fill_i8;

long long arg_num(int argc, char** argv, const char* flag, long long fallback) {
    for (int i = 1; i + 1 < argc; ++i) {
        if (std::strcmp(argv[i], flag) == 0) return std::atoll(argv[i + 1]);
    }
    return fallback;
}

bool has_flag(int argc, char** argv, const char* flag) {
    for (int i = 1; i < argc; ++i) {
        if (std::strcmp(argv[i], flag) == 0) return true;
    }
    return false;
}

int usage() {
    std::printf(
        "connectome %s\n\n"
        "  cx doctor [--json]                         probe this machine\n"
        "  cx bench [--n N] [--d D] [--iters I]       measure the two-pass scan\n"
        "  cx selftest [--seed S]                     fixed scan; prints a digest\n"
        "  cx version\n\n"
        "%s\n",
        cx::version_string().c_str(), cx::kSpec);
    return 2;
}

int bench(int argc, char** argv) {
    const long long n     = arg_num(argc, argv, "--n", 250000);
    const long long d     = arg_num(argc, argv, "--d", 1024);
    const long long dc    = arg_num(argc, argv, "--dc", 128);
    const long long iters = arg_num(argc, argv, "--iters", 5);
    if (d % 4 || dc % 4) {
        std::printf("d and dc must be multiples of 4\n");
        return 2;
    }

    std::printf("corpus: %lld chunks, coarse %lld-d, fine %lld-d  (%.2f MiB coarse, %.2f MiB fine)\n",
                n, dc, d, static_cast<double>(n * dc) / 1048576.0,
                static_cast<double>(n * d) / 1048576.0);

    std::vector<std::int8_t> Xc(static_cast<std::size_t>(n * dc));
    std::vector<std::int8_t> Xf(static_cast<std::size_t>(n * d));
    std::vector<std::int8_t> qc(static_cast<std::size_t>(dc));
    std::vector<std::int8_t> qf(static_cast<std::size_t>(d));
    fill_i8(Xc, 1); fill_i8(Xf, 2); fill_i8(qc, 3); fill_i8(qf, 4);

    const bool gpu = cx::cuda_available();
    std::printf("device: %s\n\n", gpu ? cx::cuda_device_info().name.c_str() : "cpu only");

    // Correctness before speed: the coarse pass on both paths must agree exactly.
    if (gpu) {
        std::vector<std::int32_t> a(static_cast<std::size_t>(n)), b(static_cast<std::size_t>(n));
        cx::dot_i8_cpu(Xc.data(), n, static_cast<int>(dc), qc.data(), a.data());
        cx::dot_i8_gpu(Xc.data(), n, static_cast<int>(dc), qc.data(), b.data());
        if (a != b) {
            std::printf("PARITY FAILED: gpu and cpu coarse scores differ\n");
            return 1;
        }
        std::printf("parity: gpu == cpu exactly on %lld coarse scores\n", n);
    }

    const auto run = [&](bool use_gpu, const char* label) {
        std::vector<cx::ScanHit> hits;
        double best_ms = 1e30;
        for (long long i = 0; i < iters; ++i) {
            const auto t0 = std::chrono::steady_clock::now();
            hits = cx::two_pass(Xc.data(), static_cast<int>(dc), Xf.data(), static_cast<int>(d),
                                qc.data(), qf.data(), n, 2048, 100, use_gpu);
            const auto t1 = std::chrono::steady_clock::now();
            best_ms = std::min(best_ms, std::chrono::duration<double, std::milli>(t1 - t0).count());
        }
        const double gib = static_cast<double>(n * dc + 2048 * d) / (1024.0 * 1024.0 * 1024.0);
        std::printf("%-10s %8.2f ms   %6.1f GiB/s scanned   top-1 id %d score %d   digest %016llx\n",
                    label, best_ms, gib / (best_ms / 1000.0), hits.empty() ? -1 : hits[0].id,
                    hits.empty() ? 0 : hits[0].score,
                    static_cast<unsigned long long>(cx::digest(hits)));
        return hits;
    };

    const std::vector<cx::ScanHit> cpu_hits = run(false, "cpu");
    if (gpu) {
        const std::vector<cx::ScanHit> gpu_hits = run(true, "gpu copy");
        if (cx::digest(cpu_hits) != cx::digest(gpu_hits)) {
            std::printf("\nDIGEST MISMATCH between cpu and gpu two-pass results\n");
            return 1;
        }

        // The coarse pass as the spec actually sizes it: the head lives in VRAM and a
        // query never moves it.  This is the number the design rests on.
        cx::GpuMatrix* resident = cx::gpu_upload(Xc.data(), n, static_cast<int>(dc));
        std::vector<std::int32_t> scores(static_cast<std::size_t>(n));
        cx::dot_i8_resident(resident, qc.data(), scores.data());   // warm

        double best_ms = 1e30;
        for (long long i = 0; i < iters; ++i) {
            const auto t0 = std::chrono::steady_clock::now();
            cx::dot_i8_resident(resident, qc.data(), scores.data());
            const auto t1 = std::chrono::steady_clock::now();
            best_ms = std::min(best_ms, std::chrono::duration<double, std::milli>(t1 - t0).count());
        }
        cx::gpu_free(resident);

        std::vector<std::int32_t> reference(static_cast<std::size_t>(n));
        cx::dot_i8_cpu(Xc.data(), n, static_cast<int>(dc), qc.data(), reference.data());
        const bool exact = (scores == reference);

        const double gib = static_cast<double>(n * dc) / (1024.0 * 1024.0 * 1024.0);
        std::printf("%-10s %8.2f ms   %6.1f GiB/s scanned   coarse pass only, %s\n", "gpu resident",
                    best_ms, gib / (best_ms / 1000.0),
                    exact ? "exact vs cpu" : "MISMATCH vs cpu");
        if (!exact) return 1;

        std::printf(
            "\ntwo-pass digests identical: the GPU path is the reference, exactly.\n"
            "note: 'gpu copy' re-uploads the matrix per query and is the wrong shape on\n"
            "purpose - it is what the design refuses.  'gpu resident' is the design.\n");
    }
    return 0;
}

int selftest(int argc, char** argv) {
    const long long seed = arg_num(argc, argv, "--seed", 20260903);
    constexpr long long n = 20000, d = 256, dc = 64;

    std::vector<std::int8_t> Xc(static_cast<std::size_t>(n * dc));
    std::vector<std::int8_t> Xf(static_cast<std::size_t>(n * d));
    std::vector<std::int8_t> qc(static_cast<std::size_t>(dc));
    std::vector<std::int8_t> qf(static_cast<std::size_t>(d));
    fill_i8(Xc, static_cast<std::uint64_t>(seed) + 1);
    fill_i8(Xf, static_cast<std::uint64_t>(seed) + 2);
    fill_i8(qc, static_cast<std::uint64_t>(seed) + 3);
    fill_i8(qf, static_cast<std::uint64_t>(seed) + 4);

    const bool gpu = cx::cuda_available();
    const std::vector<cx::ScanHit> hits =
        cx::two_pass(Xc.data(), static_cast<int>(dc), Xf.data(), static_cast<int>(d), qc.data(),
                     qf.data(), n, 512, 32, gpu);

    std::printf("seed %lld  path %s  hits %zu  digest %016llx\n", seed, gpu ? "gpu" : "cpu",
                hits.size(), static_cast<unsigned long long>(cx::digest(hits)));
    return hits.empty() ? 1 : 0;
}

} // namespace

int main(int argc, char** argv) {
    if (argc < 2) return usage();
    const std::string cmd = argv[1];
    try {
        if (cmd == "doctor")   return cx::doctor(has_flag(argc, argv, "--json"));
        if (cmd == "bench")    return bench(argc, argv);
        if (cmd == "selftest") return selftest(argc, argv);
        if (cmd == "version") {
            std::printf("%s\n%s\n", cx::version_string().c_str(), cx::kSpec);
            return 0;
        }
    } catch (const std::exception& e) {
        std::fprintf(stderr, "cx %s: %s\n", cmd.c_str(), e.what());
        return 1;
    }
    return usage();
}
