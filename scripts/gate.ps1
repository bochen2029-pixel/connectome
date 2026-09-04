# gate.ps1 - a milestone is done when its gate exits 0.  Nothing else counts.
#
#   scripts\gate.ps1 -Milestone M0
#
# M0 (spec section 13): the native skeleton stands, and the two-pass scan is exact,
# deterministic across runs, and identical between the GPU path and the CPU
# reference.  The cross-process arm is the one that matters: two separate `cx
# selftest` processes must print the same digest, which is what "byte-identical
# scans across runs" means when the scan later moves to a different machine.
#
# M1 (spec sections 2 and 12): the loss exists and is honest.  The harness must never
# look forward, must not depend on its own block size, must detect a planted front,
# and must survive the degenerate corpora that broke the first detector.  Then it is
# run on the real corpus, where F-CONVERGE either reproduces or refutes the finding
# the whole design rests on.

[CmdletBinding()]
param(
    [ValidateSet('M0','M1')]
    [string]$Milestone = 'M0',
    [switch]$SkipBuild
)

$ErrorActionPreference = 'Stop'

$repo  = Split-Path -Parent $PSScriptRoot
$build = Join-Path $repo 'build'
$cx    = Join-Path $build 'cx.exe'
$fail  = 0

function Step([string]$name, [scriptblock]$body) {
    Write-Host ''
    Write-Host "== $name"
    try {
        & $body
        if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) { throw "exit code $LASTEXITCODE" }
        Write-Host "   PASS  $name"
    } catch {
        Write-Host "   FAIL  $name : $_"
        $script:fail++
    }
}

Write-Host "gate: $Milestone"

if (-not $SkipBuild) {
    Step 'build' { & (Join-Path $PSScriptRoot 'build.ps1') -Native }
}

Step 'ctest' {
    Push-Location $build
    try { ctest --output-on-failure } finally { Pop-Location }
}

Step 'cross-process determinism' {
    $a = & $cx selftest --seed 20260903
    $b = & $cx selftest --seed 20260903
    Write-Host "   run A: $a"
    Write-Host "   run B: $b"
    $da = ($a -split 'digest ')[-1].Trim()
    $db = ($b -split 'digest ')[-1].Trim()
    if ($da -ne $db) { throw "digests differ: $da vs $db" }
    if ([string]::IsNullOrWhiteSpace($da)) { throw 'no digest printed' }
    $global:LASTEXITCODE = 0
}

Step 'doctor (informational)' {
    & $cx doctor
    # doctor's own exit code reports missing required organs; the M0 gate does not
    # depend on a running embedding server, so it is reported and not enforced.
    $global:LASTEXITCODE = 0
}

if ($Milestone -eq 'M1') {
    Step 'harness self-tests' {
        Push-Location $repo
        try { python -m harness.test_harness } finally { Pop-Location }
    }

    Step 'F-CONVERGE on the live corpus' {
        Push-Location $repo
        try {
            $out = python -m harness.run converge --shuffles 3 2>&1
            $out | ForEach-Object { Write-Host "   $_" }
            if ($LASTEXITCODE -ne 0) { throw 'converge failed' }
            # The finding, not a threshold: arrival order must beat an arbitrary one
            # at the head of the corpus, where the subject was still being laid down.
            $first = ($out | Select-String -Pattern '^\s+1\s').ToString()
            if ($first -notmatch '\+\s*\d') { throw "first decile shows no advantage: $first" }
        } finally { Pop-Location }
    }

    Step 'front detection' {
        Push-Location $repo
        try {
            $out = python -m harness.run fronts 2>&1
            $out | ForEach-Object { Write-Host "   $_" }
            if ($LASTEXITCODE -ne 0) { throw 'fronts failed' }
        } finally { Pop-Location }
    }
}

Write-Host ''
if ($fail -eq 0) {
    Write-Host "gate $Milestone : PASS"
    exit 0
} else {
    Write-Host "gate $Milestone : FAIL ($fail step(s))"
    exit 1
}
