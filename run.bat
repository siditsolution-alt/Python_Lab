@echo off
REM Weather Data Analyzer - Windows Batch Runner
REM Double-click this file or run from command line to start the application

title Weather Data Analyzer

REM Get the directory where the batch file is located
cd /d "%~dp0"

echo ========================================
echo   Weather Data Analyzer
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if required directory exists
if not exist "Weather_Data_Analyzer" (
    echo [ERROR] Weather_Data_Analyzer directory not found
    echo.
    echo Please make sure you're running this from the project root directory
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

REM Check if .env file exists (optional but recommended)
if not exist ".env" (
    echo [WARNING] .env file not found
    echo.
    echo Make sure you have created a .env file with your WEATHER_API_KEY
    echo Example: WEATHER_API_KEY=your_api_key_here
    echo.
)

echo Starting Weather Data Analyzer...
echo.

REM Run the Python script
python run.py

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%

echo.
if %EXIT_CODE% EQU 0 (
    echo ========================================
    echo   Execution completed successfully!
    echo ========================================
) else (
    echo ========================================
    echo   Execution completed with errors
    echo   Exit code: %EXIT_CODE%
    echo ========================================
)

echo.
pause
