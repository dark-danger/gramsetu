@echo off
:: Set current directory to the folder where this batch file is located
cd /d "%~dp0"

title GramSetu AI - Kisan Assistant
color 0A

echo ============================================================
echo   🌾 GramSetu AI - Offline Assistant Launcher
echo ============================================================
echo.

:: 1. Check for standalone GramSetuAI.exe first
if exist "%~dp0GramSetuAI.exe" (
    echo [+] Launching Standalone GramSetuAI.exe...
    start "" "%~dp0GramSetuAI.exe" --open
    timeout /t 2 >nul
    exit /b
)

:: 2. Check for Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [+] Starting GramSetu Python Server...
    start "" http://localhost:8000
    python "%~dp0server.py" --open
    exit /b
)

:: 3. Direct Browser Launch (100% Offline, No Python Needed)
echo [+] Launching GramSetu AI in your default browser...
start "" "%~dp0index.html"

echo.
echo ============================================================
echo [SUCCESS] GramSetu AI has opened in your browser!
echo Aap is window ko band kar sakte hain.
echo ============================================================
echo.
pause
