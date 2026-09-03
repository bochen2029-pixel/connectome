// cx/field.h - cx-field.  CONTRACT ONLY; implementation lands at M2.
//
// Seven relation slices over the chunks, a partition that is a versioned artifact
// rather than a recomputable process, and firing that returns a read plan and never
// an answer (spec sections 6.2, 6.3, 6.6).

#pragma once

#include <cstdint>
#include <vector>

#include "cx/cx.h"

namespace cx::field {

enum class Slice : std::uint8_t {
    SemanticKnn   = 0,  // deterministic: top-10 cosine, mutual-kNN symmetrised
    Retelling     = 1,  // cosine >= the learned trough, or MinHash Jaccard >= 0.80
    Containment   = 2,  // chunk in doc in community
    Succession    = 3,  // tape order within a document; message order within a session
    Lexical       = 4,  // BM25 co-hits on rare terms, count-shrunk
    Provenance    = 5,  // transcript <-> document by exact 12-gram: what produced what
    Contradiction = 6,  // arithmetic over the typed position ledger
    Hebbian       = 7,  // verified use, difficulty-scaled, asymmetric decay, capped
};

// Compressed sparse row, both orientations resident (spec 6.2).
struct Csr {
    std::vector<std::int64_t> row_ptr;
    std::vector<ChunkId>      col;
    std::vector<float>        weight;
};

struct Partition {
    std::uint16_t            version = 0;
    std::vector<std::uint32_t> community_of;   // per chunk
    std::vector<std::uint16_t> super_of;       // per community
    std::vector<float>         centroids;      // n_communities x d, row-major
    double                     modularity = 0.0;
    double                     drift = 0.0;    // share whose nearest centroid != their community
};

// Assign a new chunk to the frozen partition: nearest centroid subject to size caps,
// overflow bucket when over cap.  O(1) in corpus size, never moves an existing node.
std::uint32_t assign(const Partition& p, const std::int8_t* vec, int d);

// Bounded local refinement, HIT-Leiden shaped: only nodes within 2 hops of new nodes
// may move, only on modularity gain, at most one pass per sleep (spec 6.3).
void refine_local(Partition& p, const Csr& backbone, const std::vector<ChunkId>& arrived);

// A version event: seeded Leiden + consensus over 10 seeds, size repair, re-induced
// names, an old->new map, and a re-anchored layout.  Never a side effect of ingest.
Partition repartition(const Csr& backbone, std::uint16_t new_version, std::uint64_t seed);

struct ReadPlan {
    std::vector<ChunkId>      spans;
    std::vector<float>        activation;
    std::vector<std::uint32_t> communities_at_centroid_only;  // the absence markers
};

// Firing returns a read plan, a salience annotation and an absence signal.  Never an
// answer.  Sparse frontier (SpMSpV), scope mask before any top-k, PPR restart, k-WTA,
// hub suppression by 1/log(degree), time decay (spec 6.6).
ReadPlan fire(const std::vector<Csr>& slices, const std::vector<ChunkId>& seed, int hops);

} // namespace cx::field
