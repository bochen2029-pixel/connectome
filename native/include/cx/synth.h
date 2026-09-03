// cx/synth.h - the synthetic corpus.
//
// A counter-based generator (splitmix64 over an index, not a stateful engine), so a
// seed reproduces the same bytes on every machine, every compiler and every standard
// library.  bench, selftest and the tests all draw from it, which is what lets a
// digest printed in one process be compared with a digest printed in another - the
// M0 gate.

#pragma once

#include <cstdint>
#include <vector>

namespace cx {

inline std::int8_t sample_i8(std::uint64_t counter, std::uint64_t seed) {
    std::uint64_t x = counter + 0x9e3779b97f4a7c15ull * (seed + 1);
    x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ull;
    x ^= x >> 27; x *= 0x94d049bb133111ebull;
    x ^= x >> 31;
    return static_cast<std::int8_t>(static_cast<std::int32_t>(x & 0xffu) - 128);
}

inline void fill_i8(std::vector<std::int8_t>& v, std::uint64_t seed) {
    for (std::size_t i = 0; i < v.size(); ++i) {
        v[i] = sample_i8(static_cast<std::uint64_t>(i), seed);
    }
}

} // namespace cx
