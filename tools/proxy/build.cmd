@echo off
rem Usage: build.cmd <dll name, e.g. xinput1_3> <target dir>
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
set PROXY_DLL=%1
cargo build --release --manifest-path "%~dp0Cargo.toml" --target-dir "%2"
