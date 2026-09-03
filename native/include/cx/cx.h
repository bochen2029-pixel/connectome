// cx/cx.h - the vocabulary every module shares.
//
// CONNECTOME v5.5 - The Field.  See docs/CONNECTOME_v5.5_THE-FIELD_2026-09-03.md.
// Nothing in this header allocates, reads a file, or calls a model.

#pragma once

#include <cstdint>
#include <string>

namespace cx {

inline constexpr int  kVersionMajor = 5;
inline constexpr int  kVersionMinor = 5;
inline constexpr int  kVersionPatch = 0;
inline constexpr char kSpec[] =
    "CONNECTOME v5.5 - The Field (docs/CONNECTOME_v5.5_THE-FIELD_2026-09-03.md)";

using DocId   = std::int32_t;
using ChunkId = std::int32_t;

// The only coordinate system that can close a claim: character offsets into the
// NFC canonical text record identified by (doc, seq).  Spec section 4.1.  A quote
// is located in the tape by deterministic code or it is not a quote - model-emitted
// offsets measured 0% usable on this corpus.
struct Span {
    DocId        doc   = -1;
    std::int32_t seq   = 0;
    std::int32_t start = 0;
    std::int32_t end   = 0;
};

// Stamped at intake from the channel, never inferred from content (spec 4.1).
// An assistant's paraphrase never becomes a claim attributed to the operator.
enum class Origin : std::uint8_t {
    OperatorDoc = 0,
    TranscriptOperator = 1,
    TranscriptAssistant = 2,
    Imported = 3,
};

// Trust follows origin, and gates whether a relation may enter the backbone
// without a second independent witness (spec 6.2, support gating).
enum class Trust : std::uint8_t { Operator = 0, Trusted = 1, Narrative = 2, Untrusted = 3 };

constexpr Trust trust_of(Origin o) {
    switch (o) {
        case Origin::OperatorDoc:         return Trust::Operator;
        case Origin::TranscriptOperator:  return Trust::Trusted;
        case Origin::TranscriptAssistant: return Trust::Narrative;
        case Origin::Imported:            return Trust::Untrusted;
    }
    return Trust::Untrusted;
}

// A locator addresses a node without a learned index: (partition version,
// super-community, community, intra-community sequence).  Spec 6.1.
struct Locator {
    std::uint16_t partition_version = 0;
    std::uint16_t c1 = 0;   // super-community  (T3)
    std::uint32_t c2 = 0;   // community        (T2)
    std::uint32_t seq = 0;  // tape order within the community
};

inline std::string version_string() {
    return std::to_string(kVersionMajor) + "." + std::to_string(kVersionMinor) + "." +
           std::to_string(kVersionPatch);
}

} // namespace cx
