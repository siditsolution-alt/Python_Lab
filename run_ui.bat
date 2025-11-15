@echo off
REM Weather Data Analyzer - Web UI Launcher
REM Double-click this file to start the web UI server

title Weather Data Analyzer - Web UI

cd /d "%~dp0"

echo ========================================
echo   Weather Data Analyzer - Web UI
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    pause
    exit /b 1
)

REM Run the UI
python run_ui.py

pause
