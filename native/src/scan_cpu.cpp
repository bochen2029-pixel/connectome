#include "cx/scan.h"

#include <algorithm>
#include <cstring>
#include <numeric>

namespace cx {

void dot_i8_cpu(const std::int8_t* X, std::int64_t n, int d, const std::int8_t* q,
                std::int32_t* out) {
    for (std::int64_t r = 0; r < n; ++r) {
        const std::int8_t* row = X + r * static_cast<std::int64_t>(d);
        std::int32_t acc = 0;
        for (int k = 0; k < d; ++k) {
            acc += static_cast<std::int32_t>(row[k]) * static_cast<std::int32_t>(q[k]);
        }
        out[r] = acc;
    }
}

std::vector<ScanHit> topk(const std::int32_t* scores, std::int64_t n, int k) {
    std::vector<ScanHit> hits;
    if (k <= 0 || n <= 0) return hits;

    const std::int64_t kk = std::min<std::int64_t>(k, n);
    std::vector<ChunkId> idx(static_cast<std::size_t>(n));
    std::iota(idx.begin(), idx.end(), 0);

    // score descending, id ascending on ties - a total order, so the result is
    // independent of the partitioning algorithm's internal swaps.
    const auto better = [&](ChunkId a, ChunkId b) {
        if (scores[a] != scores[b]) return scores[a] > scores[b];
        return a < b;
    };

    std::nth_element(idx.begin(), idx.begin() + kk, idx.end(), better);
    std::sort(idx.begin(), idx.begin() + kk, better);

    hits.reserve(static_cast<std::size_t>(kk));
    for (std::int64_t i = 0; i < kk; ++i) hits.push_back(ScanHit{idx[static_cast<std::size_t>(i)],
                                                                scores[idx[static_cast<std::size_t>(i)]]});
    return hits;
}

std::vector<ScanHit> two_pass(const std::int8_t* Xc, int dc,
                              const std::int8_t* Xf, int df,
                              const std::int8_t* qc, const std::int8_t* qf,
                              std::int64_t n, int coarse_k, int final_k,
                              bool use_gpu) {
    const bool gpu = use_gpu && cuda_available();

    std::vector<std::int32_t> coarse(static_cast<std::size_t>(n));
    if (gpu) dot_i8_gpu(Xc, n, dc, qc, coarse.data());
    else     dot_i8_cpu(Xc, n, dc, qc, coarse.data());

    std::vector<ScanHit> cand = topk(coarse.data(), n, coarse_k);
    if (cand.empty()) return cand;

    // Gather the candidate rows of the fine matrix into one contiguous block so the
    // second pass is another dense scan rather than a strided walk.
    std::vector<std::int8_t> gathered(cand.size() * static_cast<std::size_t>(df));
    for (std::size_t i = 0; i < cand.size(); ++i) {
        std::memcpy(&gathered[i * static_cast<std::size_t>(df)],
                    Xf + static_cast<std::int64_t>(cand[i].id) * df,
                    static_cast<std::size_t>(df));
    }

    std::vector<std::int32_t> fine(cand.size());
    const std::int64_t m = static_cast<std::int64_t>(cand.size());
    if (gpu) dot_i8_gpu(gathered.data(), m, df, qf, fine.data());
    else     dot_i8_cpu(gathered.data(), m, df, qf, fine.data());

    std::vector<ScanHit> hits(cand.size());
    for (std::size_t i = 0; i < cand.size(); ++i) {
        hits[i] = ScanHit{cand[i].id, fine[i]};
    }
    std::sort(hits.begin(), hits.end(), [](const ScanHit& a, const ScanHit& b) {
        if (a.score != b.score) return a.score > b.score;
        return a.id < b.id;
    });
    if (static_cast<int>(hits.size()) > final_k) {
        hits.resize(static_cast<std::size_t>(final_k));
    }
    return hits;
}

std::uint64_t digest(const std::vector<ScanHit>& hits) {
    std::uint64_t h = 1469598103934665603ull;             // FNV-1a offset basis
    const auto mix = [&h](std::uint32_t v) {
        for (int b = 0; b < 4; ++b) {
            h ^= static_cast<std::uint64_t>((v >> (b * 8)) & 0xffu);
            h *= 1099511628211ull;                        // FNV-1a prime
        }
    };
    for (const ScanHit& x : hits) {
        mix(static_cast<std::uint32_t>(x.id));
        mix(static_cast<std::uint32_t>(x.score));
    }
    return h;
}

} // namespace cx
