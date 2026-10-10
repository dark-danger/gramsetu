@echo off
title GramSetu AI - Windows Setup & Executable Builder
color 0A

echo ============================================================
echo   🌾 GramSetu AI - 1-Click Windows PC Installer
echo ============================================================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not found on this system.
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b
)

echo [+] Python detected:
python --version
echo.

echo [+] Installing required packages (PyInstaller)...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install pyinstaller
echo.

echo [+] Building Standalone GramSetuAI.exe ...
python build_exe.py
echo.

if exist "dist\GramSetuAI.exe" (
    echo ============================================================
    echo [SUCCESS] GramSetuAI.exe successfully created!
    echo Location: %cd%\dist\GramSetuAI.exe
    echo ============================================================
    echo.
    echo Copying GramSetuAI.exe to main folder...
    copy /y "dist\GramSetuAI.exe" "GramSetuAI.exe" >nul
    echo.
    echo [+] You can now double-click "GramSetuAI.exe" or "Run_GramSetu_Windows.bat" anytime!
) else (
    echo [!] Build completed. You can launch GramSetu using "Run_GramSetu_Windows.bat".
)

echo.
pause
