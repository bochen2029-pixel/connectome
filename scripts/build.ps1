# build.ps1 - configure and build the native core.
#
# Bootstraps the MSVC environment and the VS-bundled Ninja, so a fresh clone needs
# nothing on PATH beyond Visual Studio 2022 with the C++ workload and the CUDA
# toolkit.  Mirrors the pattern in C:/backrooms/scripts/build.ps1.
#
#   scripts\build.ps1                 incremental Release build, archs 89;90;120
#   scripts\build.ps1 -Native         compile only for this machine's GPU (fast)
#   scripts\build.ps1 -Clean          wipe the build directory first
#   scripts\build.ps1 -NoCuda         CPU reference only; every gate still runs

[CmdletBinding()]
param(
    [switch]$Clean,
    [switch]$Native,
    [switch]$NoCuda,
    [ValidateSet('Release', 'Debug', 'RelWithDebInfo')]
    [string]$Config = 'Release'
)

$ErrorActionPreference = 'Stop'

$repo   = Split-Path -Parent $PSScriptRoot
$source = Join-Path $repo 'native'
$build  = Join-Path $repo 'build'

if ($Clean -and (Test-Path $build)) {
    Write-Host "clean: removing $build"
    Remove-Item -Recurse -Force $build
}

# --- Visual Studio ---------------------------------------------------------
$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
if (-not (Test-Path $vswhere)) {
    throw "vswhere.exe not found. Install Visual Studio 2022 with 'Desktop development with C++'."
}
$vsRoot = & $vswhere -latest -products * `
    -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
if (-not $vsRoot) { throw 'No Visual Studio 2022 with the C++ toolset was found.' }

$vcvars = Join-Path $vsRoot 'VC\Auxiliary\Build\vcvars64.bat'
if (-not (Test-Path $vcvars)) { throw "vcvars64.bat not found under $vsRoot" }

# --- CMake and Ninja (prefer PATH, fall back to the VS-bundled copies) ------
$cmakeCmd = Get-Command cmake -ErrorAction SilentlyContinue
$cmake = if ($cmakeCmd) { $cmakeCmd.Source } else {
    Join-Path $vsRoot 'Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe'
}
if (-not (Test-Path $cmake)) { throw 'CMake >= 3.27 not found on PATH or in Visual Studio.' }

$ninjaCmd = Get-Command ninja -ErrorAction SilentlyContinue
$ninja = if ($ninjaCmd) { $ninjaCmd.Source } else {
    Join-Path $vsRoot 'Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja\ninja.exe'
}
if (-not (Test-Path $ninja)) { throw 'Ninja not found on PATH or in Visual Studio.' }

# --- CUDA ------------------------------------------------------------------
$cudaFlag = if ($NoCuda) { 'OFF' } else { 'ON' }
if (-not $NoCuda -and -not (Get-Command nvcc -ErrorAction SilentlyContinue)) {
    Write-Warning 'nvcc is not on PATH; configure will fail unless CUDA is installed. Use -NoCuda for the CPU reference build.'
}
$archArg = if ($Native) { '-DCMAKE_CUDA_ARCHITECTURES=native' } else { '' }

$configure = @(
    "`"$cmake`"", '-S', "`"$source`"", '-B', "`"$build`"", '-G', 'Ninja',
    "-DCMAKE_BUILD_TYPE=$Config", "-DCX_WITH_CUDA=$cudaFlag",
    "-DCMAKE_MAKE_PROGRAM=`"$ninja`"", $archArg
) -join ' '

$compile = "`"$cmake`" --build `"$build`" --config $Config"

Write-Host "configure: $Config, CUDA=$cudaFlag$(if($Native){', arch=native'})"
cmd /c "`"$vcvars`" >nul && $configure && $compile"
if ($LASTEXITCODE -ne 0) { throw "build failed with exit code $LASTEXITCODE" }

$exe = Join-Path $build 'cx.exe'
Write-Host ''
Write-Host "built: $exe"
