// M0's acceptance tests.  The gate is: the scan is exact, deterministic across runs,
// and identical between the GPU path and the CPU reference.

#include "cx/scan.h"
#include "cx/synth.h"

#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

namespace {

int failures = 0;

void expect(bool cond, const char* what) {
    if (!cond) {
        std::printf("  FAIL  %s\n", what);
        ++failures;
    } else {
        std::printf("  ok    %s\n", what);
    }
}

struct Corpus {
    std::vector<std::int8_t> Xc, Xf, qc, qf;
    long long n = 0, dc = 0, d = 0;
};

Corpus make(long long n, long long dc, long long d, std::uint64_t seed) {
    Corpus c;
    c.n = n; c.dc = dc; c.d = d;
    c.Xc.resize(static_cast<std::size_t>(n * dc));
    c.Xf.resize(static_cast<std::size_t>(n * d));
    c.qc.resize(static_cast<std::size_t>(dc));
    c.qf.resize(static_cast<std::size_t>(d));
    cx::fill_i8(c.Xc, seed + 1);
    cx::fill_i8(c.Xf, seed + 2);
    cx::fill_i8(c.qc, seed + 3);
    cx::fill_i8(c.qf, seed + 4);
    return c;
}

int test_parity() {
    if (!cx::cuda_available()) {
        std::printf("  skip  no CUDA device; the CPU reference is the whole engine\n");
        return 0;
    }
    const Corpus c = make(5000, 128, 256, 11);
    std::vector<std::int32_t> a(static_cast<std::size_t>(c.n)), b(a.size());
    cx::dot_i8_cpu(c.Xc.data(), c.n, static_cast<int>(c.dc), c.qc.data(), a.data());
    cx::dot_i8_gpu(c.Xc.data(), c.n, static_cast<int>(c.dc), c.qc.data(), b.data());
    expect(a == b, "gpu coarse scores are bit-identical to the cpu reference");

    std::vector<std::int32_t> af(a.size()), bf(a.size());
    cx::dot_i8_cpu(c.Xf.data(), c.n, static_cast<int>(c.d), c.qf.data(), af.data());
    cx::dot_i8_gpu(c.Xf.data(), c.n, static_cast<int>(c.d), c.qf.data(), bf.data());
    expect(af == bf, "gpu fine scores are bit-identical to the cpu reference");
    return failures;
}

int test_determinism() {
    const Corpus c = make(4096, 64, 128, 23);
    const auto one = cx::two_pass(c.Xc.data(), static_cast<int>(c.dc), c.Xf.data(),
                                  static_cast<int>(c.d), c.qc.data(), c.qf.data(), c.n, 256, 32,
                                  false);
    const auto two = cx::two_pass(c.Xc.data(), static_cast<int>(c.dc), c.Xf.data(),
                                  static_cast<int>(c.d), c.qc.data(), c.qf.data(), c.n, 256, 32,
                                  false);
    expect(cx::digest(one) == cx::digest(two), "cpu two-pass repeats byte-identically");

    if (cx::cuda_available()) {
        const auto g1 = cx::two_pass(c.Xc.data(), static_cast<int>(c.dc), c.Xf.data(),
                                     static_cast<int>(c.d), c.qc.data(), c.qf.data(), c.n, 256, 32,
                                     true);
        const auto g2 = cx::two_pass(c.Xc.data(), static_cast<int>(c.dc), c.Xf.data(),
                                     static_cast<int>(c.d), c.qc.data(), c.qf.data(), c.n, 256, 32,
                                     true);
        expect(cx::digest(g1) == cx::digest(g2), "gpu two-pass repeats byte-identically");
        expect(cx::digest(g1) == cx::digest(one), "gpu and cpu two-pass agree exactly");
    } else {
        std::printf("  skip  no CUDA device for the gpu determinism arms\n");
    }
    return failures;
}

int test_topk() {
    // Ties everywhere: every even row scores 10, every odd row scores 10 as well,
    // so only the tie-break makes the order total.
    std::vector<std::int32_t> scores(64, 10);
    scores[7] = 99;
    scores[40] = 99;
    const auto hits = cx::topk(scores.data(), static_cast<std::int64_t>(scores.size()), 5);
    expect(hits.size() == 5, "topk returns exactly k hits");
    expect(hits[0].id == 7 && hits[1].id == 40, "score descending, then id ascending on ties");
    expect(hits[2].id == 0 && hits[3].id == 1 && hits[4].id == 2, "the tie-break is stable");

    const auto small = cx::topk(scores.data(), 3, 10);
    expect(small.size() == 3, "k larger than n is clamped, not an error");

    const auto none = cx::topk(scores.data(), 0, 5);
    expect(none.empty(), "an empty corpus returns no hits");
    return failures;
}

int test_twopass() {
    // Plant the query itself as row 1234 in both matrices: its score is sum(q_i^2),
    // which random rows cannot approach, so it must come first through both passes.
    Corpus c = make(8192, 64, 128, 31);
    const std::size_t row = 1234;
    std::memcpy(&c.Xc[row * static_cast<std::size_t>(c.dc)], c.qc.data(),
                static_cast<std::size_t>(c.dc));
    std::memcpy(&c.Xf[row * static_cast<std::size_t>(c.d)], c.qf.data(),
                static_cast<std::size_t>(c.d));

    const auto hits = cx::two_pass(c.Xc.data(), static_cast<int>(c.dc), c.Xf.data(),
                                   static_cast<int>(c.d), c.qc.data(), c.qf.data(), c.n, 512, 10,
                                   cx::cuda_available());
    expect(!hits.empty(), "two_pass returns hits");
    expect(!hits.empty() && hits[0].id == static_cast<cx::ChunkId>(row),
           "the planted row survives the coarse pass and wins the fine pass");

    // The fine score of the planted row must equal sum(q_i^2) exactly - the gather
    // must copy the right row, and int8 products must accumulate without overflow.
    std::int32_t expected = 0;
    for (long long k = 0; k < c.d; ++k) {
        expected += static_cast<std::int32_t>(c.qf[static_cast<std::size_t>(k)]) *
                    static_cast<std::int32_t>(c.qf[static_cast<std::size_t>(k)]);
    }
    expect(!hits.empty() && hits[0].score == expected, "the gathered row scores exactly sum(q^2)");
    return failures;
}

} // namespace

int main(int argc, char** argv) {
    const std::string which = argc > 1 ? argv[1] : "all";
    std::printf("cx_test_scan [%s]  device: %s\n", which.c_str(),
                cx::cuda_available() ? cx::cuda_device_info().name.c_str() : "cpu only");

    if (which == "parity" || which == "all")       test_parity();
    if (which == "determinism" || which == "all")  test_determinism();
    if (which == "topk" || which == "all")         test_topk();
    if (which == "twopass" || which == "all")      test_twopass();

    std::printf("%s: %d failure%s\n", which.c_str(), failures, failures == 1 ? "" : "s");
    return failures == 0 ? 0 : 1;
}
