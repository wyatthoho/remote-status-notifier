@echo off
cd /d "%~dp0"

if not exist "venv" (
    py -m venv venv
    call .\venv\Scripts\activate
    pip install -e .
)

start "" ".\venv\Scripts\pythonw.exe" -m notifier.main