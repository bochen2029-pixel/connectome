cmake_minimum_required(VERSION 3.27)

# ---------------------------------------------------------------------------
# CONNECTOME native core.  Build conventions are inherited verbatim from the
# operator's own native repos (C:/Buddhabrot_CUDA, C:/Booster_Lander_Simulator,
# C:/backrooms) and pinned by CONNECTOME v5.5 section 10.1:
#
#   RTX 40-series (Ada Lovelace) = compute_89
#   Hopper datacentre            = compute_90
#   RTX 50-series (Blackwell)    = compute_120
#
# Set BEFORE project() so CMake's CUDA detection uses them.  Pass
# -DCMAKE_CUDA_ARCHITECTURES=native for a fast local build.
# ---------------------------------------------------------------------------
if(NOT DEFINED CMAKE_CUDA_ARCHITECTURES)
    set(CMAKE_CUDA_ARCHITECTURES 89 90 120 CACHE STRING "")
endif()

option(CX_WITH_CUDA "Build the CUDA hot path (OFF: the CPU reference is the whole engine)" ON)

if(CX_WITH_CUDA)
    project(connectome VERSION 5.5.0 LANGUAGES CXX CUDA)
else()
    project(connectome VERSION 5.5.0 LANGUAGES CXX)
endif()

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(CX_WITH_CUDA)
    set(CMAKE_CUDA_STANDARD 20)
    set(CMAKE_CUDA_STANDARD_REQUIRED ON)
    # Static CUDA runtime: the executable ships without cudart64_*.dll beside it.
    set(CMAKE_CUDA_RUNTIME_LIBRARY Static)
endif()

# Static MSVC runtime: no VS redistributable required on the target machine.
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

if(MSVC)
    add_compile_definitions(_CRT_SECURE_NO_WARNINGS NOMINMAX WIN32_LEAN_AND_MEAN)
endif()

# ---------------------------------------------------------------------------
# cx_core - the library every surface links against.
# ---------------------------------------------------------------------------
set(CX_CORE_SOURCES
    src/scan_cpu.cpp
    src/doctor.cpp)

if(CX_WITH_CUDA)
    list(APPEND CX_CORE_SOURCES src/scan_gpu.cu)
else()
    list(APPEND CX_CORE_SOURCES src/scan_gpu_stub.cpp)
endif()

add_library(cx_core STATIC ${CX_CORE_SOURCES})
target_include_directories(cx_core PUBLIC include)

if(CX_WITH_CUDA)
    target_compile_definitions(cx_core PUBLIC CX_WITH_CUDA=1)
    # Determinism, per the booster core's house rules: no contraction on any path
    # whose result reaches a fingerprint, and never --use_fast_math.  The scan
    # itself is integer, so it is exact regardless; the flag is the standing
    # discipline for the float kernels that land at M3.
    target_compile_options(cx_core PRIVATE $<$<COMPILE_LANGUAGE:CUDA>:-fmad=false>)
endif()

if(WIN32)
    target_link_libraries(cx_core PRIVATE ws2_32)
endif()

# ---------------------------------------------------------------------------
# cx - the command line surface.
# ---------------------------------------------------------------------------
add_executable(cx src/main.cpp)
target_link_libraries(cx PRIVATE cx_core)

# ---------------------------------------------------------------------------
# Tests.  ctest is the gate; scripts/gate.ps1 -Milestone M0 wraps it.
# ---------------------------------------------------------------------------
enable_testing()

add_executable(cx_test_scan tests/test_scan.cpp)
target_link_libraries(cx_test_scan PRIVATE cx_core)

add_executable(cx_test_contracts tests/test_contracts.cpp)
target_link_libraries(cx_test_contracts PRIVATE cx_core)

add_test(NAME scan_parity       COMMAND cx_test_scan parity)
add_test(NAME scan_determinism  COMMAND cx_test_scan determinism)
add_test(NAME topk_tiebreak     COMMAND cx_test_scan topk)
add_test(NAME two_pass_exact    COMMAND cx_test_scan twopass)
add_test(NAME contracts_compile COMMAND cx_test_contracts)

message(STATUS "connectome ${PROJECT_VERSION}  CUDA=${CX_WITH_CUDA}  archs=${CMAKE_CUDA_ARCHITECTURES}")
