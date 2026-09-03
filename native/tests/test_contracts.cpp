// Every contract header must parse and stay self-consistent, including the modules
// whose implementations land at M2-M4.  This is the cheapest possible guard against
// a header drifting away from the spec while nothing links against it yet.

#include "cx/cx.h"
#include "cx/field.h"
#include "cx/map.h"
#include "cx/place.h"
#include "cx/scan.h"
#include "cx/synth.h"
#include "cx/tape.h"

#include <cstdio>
#include <type_traits>

int main() {
    static_assert(cx::kVersionMajor == 5 && cx::kVersionMinor == 5, "version drift");
    static_assert(std::is_trivially_copyable_v<cx::Span>, "a span must be memcpy-able");
    static_assert(std::is_trivially_copyable_v<cx::Locator>, "a locator must be memcpy-able");
    static_assert(std::is_trivially_copyable_v<cx::ScanHit>, "a scan hit must be memcpy-able");
    static_assert(std::is_trivially_copyable_v<cx::map::Ball>, "ball coords go to the GPU");
    static_assert(sizeof(cx::map::Ball) == 16, "ball coords stay 16 bytes per instance");

    // Trust follows origin, always, and is never inferred from content (spec 4.1).
    static_assert(cx::trust_of(cx::Origin::OperatorDoc) == cx::Trust::Operator);
    static_assert(cx::trust_of(cx::Origin::TranscriptAssistant) == cx::Trust::Narrative);
    static_assert(cx::trust_of(cx::Origin::Imported) == cx::Trust::Untrusted);

    std::printf("contracts ok: cx %s\n%s\n", cx::version_string().c_str(), cx::kSpec);
    return 0;
}
