// cx/tape.h - cx-tape.  CONTRACT ONLY; implementation lands at M0/M1.
//
// The tape is truth (spec section 4.1): append-only, blake2b-128 hash-chained JSONL
// in Scriptorium's format, so the two organs share negatives and one fence.  Every
// structure above it - index, field, map, pages - is a rebuildable fold.  Delete the
// store and rebuild; delete the tape and you have lost the corpus.

#pragma once

#include <array>
#include <cstdint>
#include <string>
#include <vector>

#include "cx/cx.h"

namespace cx::tape {

enum class RecordKind : std::uint8_t {
    Doc,      // one source file: path, content hash, mtime, modality, extractor fingerprint
    Text,     // a canonical-text block; the span coordinate system lives here
    Journal,  // intake events: admitted / dedup-folded / quarantined / excluded
    Contact,  // the census row: tokens x period x source x modality
    Derived,  // a journaled model output: {op, model_fp, prompt_hash, inputs}
};

struct Record {
    RecordKind    kind = RecordKind::Journal;
    DocId         doc = -1;
    std::int32_t  seq = 0;
    Origin        origin = Origin::Imported;
    std::string   body;         // canonical text, or the JSON payload for Derived
    std::uint64_t t_event = 0;  // when it was true
    std::uint64_t t_tape  = 0;  // when it landed  (bi-temporal, spec 6.2)
    std::array<std::uint8_t, 16> prev_hash{};
    std::array<std::uint8_t, 16> hash{};
};

struct Chunk {
    ChunkId      id = -1;
    Span         span;
    Locator      locator;
    Origin       origin = Origin::Imported;
    std::int32_t tokens = 0;
    std::string  header;   // "{doc title} > {breadcrumb} - {era} - {origin}"  (spec 4.2)
};

// Append a record and extend the hash chain.  Returns the new head.
std::array<std::uint8_t, 16> append(const std::string& archive_root, const Record& r);

// Verify the whole chain; returns the sequence number of the first bad record, or -1.
std::int64_t verify(const std::string& archive_root);

// Byte-exact dedup before anything is embedded: conversational corpora measured ~80%
// redundant by bytes with zero quality regression (spec 4.1).
std::int64_t fold_duplicates(const std::string& archive_root);

// The chunker is called at its fixed path as a subprocess, never imported (spec 10.5).
std::vector<Chunk> chunk_document(const std::string& path, int budget_tokens, int overlap);

} // namespace cx::tape
