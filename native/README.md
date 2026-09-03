# native — the C++/CUDA core

The hot path and the viewer, native. Spec section 10 of
[`docs/CONNECTOME_v5.5_THE-FIELD_2026-09-03.md`](../docs/CONNECTOME_v5.5_THE-FIELD_2026-09-03.md).

Build conventions are inherited from the operator's own native repos and not reinvented here:
CMake ≥ 3.27 with `CMAKE_CUDA_ARCHITECTURES 89 90 120` set before `project()`, C++20 / CUDA 20,
static CUDA and MSVC runtimes so the executable ships alone, Ninja from the VS 2022 developer
environment ([`C:/Buddhabrot_CUDA`](https://github.com/bochen2029-pixel)); no float atomics on any
reduction path, fixed-topology reductions, per-architecture bit-identity as the hard gate
(`C:/Booster_Lander_Simulator/core/guidance_mppi_cuda.cu`); machine-checkable milestone gates
(`C:/backrooms/scripts/gate.ps1`).

## Build and gate

```powershell
scripts\build.ps1 -Native          # this machine's GPU only, fast
scripts\build.ps1                  # archs 89;90;120, shippable
scripts\build.ps1 -NoCuda          # CPU reference only; every gate still runs
scripts\gate.ps1 -Milestone M0     # a milestone is done when its gate exits 0
```

```
build\cx.exe doctor [--json]                    what this machine has and is missing
build\cx.exe bench [--n N] [--d D] [--dc DC]    the two-pass scan, measured
build\cx.exe selftest [--seed S]                a fixed scan; prints the digest the gate compares
```

## M0 receipt — measured 2026-09-03

RTX 4070 Ti SUPER 16 GB, CUDA 13.1, MSVC 14.44, Windows. Gate: **PASS** (5/5 ctest, cross-process
digest `9574b5dae6191b39` identical in two separate processes).

| corpus | coarse pass | | | |
|---|---|---|---|---|
| chunks | CPU reference | GPU, re-uploaded per query | **GPU resident** | exactness |
| 250,000 (30.5 MiB) | 9.00 ms | 13.05 ms | **0.29 ms — 102 GiB/s** | bit-identical |
| 2,000,000 (244 MiB) | 68.37 ms | 88.61 ms | **2.02 ms — 118 GiB/s** | bit-identical |

Two things worth reading off that table. First, **the transfer is the whole cost** when the matrix
is copied per query — the naive GPU path *loses to the CPU*, which is exactly why the spec keeps the
coarse head resident in VRAM at every corpus scale (§4.3, §10.3) and why `bench` prints both rows.
Second, an exact brute-force scan of two million chunks takes **two milliseconds**, so there is no
ANN index to build, tune, or let rot — SCAN, DON'T SEEK is a measurement here, not a slogan.
Extrapolating the resident row to the spec's largest tier (2×10⁷ chunks, 2.5 GB coarse) gives
≈ 21 ms per query, still interactive, still exact.

**Determinism is by construction, not by tolerance.** Scores are int32 sums of int8 products, the
reduction is a fixed-topology warp shuffle, and no float atomic appears anywhere on the path. So the
GPU result equals the CPU reference *exactly*, every run, on every supported architecture — which is
what makes "byte-identical scans across runs and against the reference" a real gate rather than an
epsilon check.

## Modules

| Module | Status | Owns | Lands |
|---|---|---|---|
| `cx-index` (`scan.h`, `scan_cpu.cpp`, `scan_gpu.cu`) | **implemented, gated** | int8 two-pass scan, resident device matrix, deterministic top-k, digests | M0 ✓ |
| `doctor` (`doctor.cpp`) | **implemented** | device query, model-server ports, fixed-path organs, corpus presence | M0 ✓ |
| `cx-tape` (`tape.h`) | contract | hash-chained tape, spans, origin/trust, dedup, the chunker seam | M1 |
| `cx-field` (`field.h`) | contract | seven slices, frozen versioned partition, assignment, firing | M2 |
| `cx-map` (`map.h`) | contract | Lorentz coordinates, analytic placement, Procrustes + hysteresis | M3 |
| `cx-place` (`place.h`) | contract | residual, verdicts, priority r/v, fronts (CUSUM), habituation | M4 |
| `cx-view` | not started | GLFW + OpenGL 4.6, CUDA–GL interop, instanced quads, id picking, ImGui | M3 |
| `cx-serve` | not started | stateless MCP (2026-07-28), pricebook, meters | M5 |

A contract header declares the interface and nothing else. `cx_test_contracts` compiles every one of
them and asserts the invariants that cross module boundaries (a span is memcpy-able, a ball
coordinate is 16 bytes, trust follows origin), so a header cannot drift from the spec while nothing
links against it yet.

## Layout

```
native/
  CMakeLists.txt            one target set: cx_core (lib), cx (cli), two test binaries
  include/cx/
    cx.h                    spans, origin, trust, locators, version
    scan.h                  cx-index: the two-pass scan and the resident matrix
    synth.h                 the counter-based synthetic corpus (bench, selftest, tests)
    tape.h field.h map.h place.h    contracts for the modules that land at M1–M4
  src/
    scan_cpu.cpp            the reference implementation and the deterministic top-k
    scan_gpu.cu             warp-per-row __dp4a kernel, resident matrix, device info
    scan_gpu_stub.cpp       the CX_WITH_CUDA=OFF build
    doctor.cpp main.cpp
  tests/
    test_scan.cpp           parity, determinism, tie-break, planted-row two-pass
    test_contracts.cpp      every contract header compiles; cross-module invariants hold
```

Cold paths stay in Python at version events (UMAP-3 angles, consensus Leiden, page generation,
embedding); the seam between hot and cold is the store on disk. Nothing hot imports Python.
