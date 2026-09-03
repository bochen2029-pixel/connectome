// cx/place.h - cx-place.  CONTRACT ONLY; implementation lands at M4.
//
// The residual loop (spec section 7).  A new passage is scored against the field as
// it stands; the residual sets its priority; high-priority passages are read with
// their map slice; what changed is written back as typed deltas.  Thresholds are
// quantiles of the corpus's own distributions, re-estimated as it grows - never
// constants a person chose (spec 2.2).

#pragma once

#include <cstdint>
#include <string>
#include <vector>

#include "cx/cx.h"

namespace cx::place {

enum class Verdict : std::uint8_t {
    Retelling = 0,  // below the learned trough of the top-1 cosine distribution
    Routine   = 1,
    Related   = 2,
    Bridging  = 3,  // high community entropy across super-communities
    Novel     = 4,  // above the learned residual quantile
};

struct Placement {
    ChunkId      chunk = -1;
    float        residual = 0.f;      // 1 - max cosine, excluding the retelling slice
    float        entropy = 0.f;       // community entropy of the top-k neighbours
    float        volatility = 0.f;    // EMA of residuals from the same source lane
    float        priority = 0.f;      // residual / volatility  (measured: beats every arm)
    Verdict      verdict = Verdict::Routine;
    std::uint32_t nearest_community = 0;
    std::vector<ChunkId> bridges;
};

// Learned from the corpus, not configured: the quantiles that separate the verdicts.
struct Thresholds {
    float retelling_cosine = 0.97f;   // the trough of the bimodal top-1 distribution
    float novel_residual   = 0.f;     // 90th percentile of the trailing window
    float routine_residual = 0.f;     // 40th percentile
    float bridge_cosine    = 0.62f;   // where cross-community pairs beat chance
};

Thresholds estimate_thresholds(const std::vector<float>& residuals,
                               const std::vector<float>& top1_cosines);

Placement place_chunk(const std::int8_t* vec, int d, const Thresholds& t,
                      const std::string& lane);

// A corpus is a stream of fronts, not a stationary distribution (spec 2.5, measured).
// CUSUM on the per-lane residual series: a front opens when residual exceeds the
// trailing 90th percentile for m consecutive documents, and closes when the retelling
// share exceeds its own.  In a front, vigilance; out of one, habituation.
struct Front {
    bool          open = false;
    std::uint64_t opened_at = 0;
    double        cusum = 0.0;
    int           consecutive = 0;
};

Front update_front(Front prior, float residual, float retelling_share,
                   double k_sigma, double h_sigma);

// Habituation: P(observe) = 1 / EMA[residual^2] per lane, so a chatty source cannot
// monopolise attention and a frozen loop cannot fixate (measured in the eye harness).
float habituation(float ema_sq_residual);

} // namespace cx::place
