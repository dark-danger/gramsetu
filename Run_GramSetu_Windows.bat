@echo off
title GramSetu AI - Offline Kisan Assistant
color 0B

echo ============================================================
echo   🌾 GramSetu AI - Launching App
echo ============================================================
echo.

:: 1. Check for GramSetuAI.exe first
if exist "GramSetuAI.exe" (
    echo [+] Launching Standalone Executable GramSetuAI.exe...
    start "" "GramSetuAI.exe" --open
    exit /b
)

:: 2. Check for Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [+] Starting GramSetu local server on http://localhost:8000 ...
    start "" http://localhost:8000
    python server.py --open
    exit /b
)

:: 3. Direct Browser Launch (No Python needed)
echo [+] Opening GramSetu AI directly in your browser...
start "" index.html
exit /b
