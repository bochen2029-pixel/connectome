// cx/map.h - cx-map.  CONTRACT ONLY; implementation lands at M3.
//
// Radius is resolution (spec section 6.4).  Coordinates live on the Lorentz
// hyperboloid in float64 on the host; the GPU receives only the Poincare projection,
// which is strictly inside the unit ball for every hyperbolic distance - so adding
// documents can never overflow the map, and detail compresses toward the rim as
// 1/(1 - rho^2).  That is the slide rule, made a coordinate system.
//
// Placement is arithmetic, not an optimiser: no hyperbolic optimiser scales past
// ~10^5 points, and the corpus's own Gromov delta (measured: 0.054 of diameter at
// p99) says the embedding space is not a tree.  The hierarchy is imposed by the
// partition; the embeddings supply only the angle.

#pragma once

#include <cstdint>
#include <vector>

#include "cx/cx.h"

namespace cx::map {

// x0^2 - x1^2 - x2^2 - x3^2 = 1, x0 > 0.
struct Lorentz {
    double x0 = 1.0, x1 = 0.0, x2 = 0.0, x3 = 0.0;
};

// What the GPU gets: rho = tanh(r/2) < 1, plus the level for level-of-detail.
struct Ball {
    float x = 0.f, y = 0.f, z = 0.f;
    std::uint8_t level = 0;
};

enum class Level : std::uint8_t { Corpus = 0, Super = 1, Community = 2, Chunk = 3 };

// Delta = ln(b)/2 per level: in H^3 volume grows as e^{2r}, so each level holds b
// times the volume of the one above.  With b ~ 10 the display radii are
// 0 / 0.52 / 0.82 / 0.94.
double level_step(double branching_factor);
double level_radius(Level level, double delta);

// Within a level, radius encodes importance: r_i = r_level - 0.5 * ln(k_i / k_mean),
// clipped to +/- delta/2.  Krioukov's law - radius is expected degree, angle is
// similarity.
double radius_for(Level level, double delta, double importance, double mean_importance);

// The angle comes from the unit-normalised Euclidean UMAP-3 coordinate; children are
// constrained to their parent's hyperbolic cone (Munzner's H3 construction).
Lorentz place(Level level, double delta, double importance, double mean_importance,
              const double angle_unit_vector[3]);

Ball to_ball(const Lorentz& p);

// Focus-and-context: moving the focus is one Lorentz boost, a 4x4 uniform.  Nothing
// is re-uploaded when the operator looks somewhere else.
void boost_to_origin(const Lorentz& focus, double out_matrix[16]);

// Stability (F-LAYOUT-STABLE): after any re-fit, align the shared nodes to their
// previous coordinates by orthogonal Procrustes (rotation and uniform scale, never
// reflection), then move a node only if its hyperbolic displacement exceeds the
// hysteresis threshold.  Bar: median displacement <= 2% of the ball radius per build.
void procrustes_align(const std::vector<Lorentz>& previous,
                      std::vector<Lorentz>& current,
                      const std::vector<ChunkId>& shared);

double apply_hysteresis(std::vector<Lorentz>& coords,
                        const std::vector<Lorentz>& previous,
                        double threshold_in_delta);

} // namespace cx::map
