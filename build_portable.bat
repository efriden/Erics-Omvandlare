@echo off
REM Build script for Erics-Omvandlare portable executable
REM This script creates a standalone .exe with bundled pandoc

echo.
echo =================================================
echo    Building Erics-Omvandlare Portable Executable
echo =================================================
echo.

REM Check if PyInstaller is available
py -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: PyInstaller not found. Installing...
    py -m pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Check if pandoc.exe exists
if not exist "tools\pandoc-3.5\pandoc.exe" (
    echo Error: pandoc.exe not found in tools\pandoc-3.5\ directory!
    echo Please ensure pandoc is properly installed in the tools folder.
    pause
    exit /b 1
)

REM Clean up previous builds
if exist "dist" (
    echo Cleaning up previous builds...
    rmdir /s /q "dist"
)

if exist "build" (
    rmdir /s /q "build"
)

REM Install dependencies
echo Installing/verifying dependencies...
py -m pip install -r requirements.txt

echo.
echo Building executable...
echo.

REM Build with PyInstaller using our spec file
py -m PyInstaller --clean build_portable.spec

REM Check if build was successful
if exist "dist\Erics-Omvandlare.exe" (
    echo.
    echo =================================================
    echo    BUILD SUCCESSFUL!
    echo =================================================
    echo.
    echo Portable executable created: dist\Erics-Omvandlare.exe
    echo File size:
    dir "dist\Erics-Omvandlare.exe" | find ".exe"
    echo.
    echo You can now distribute this single .exe file!
    echo It includes Python, all dependencies, and pandoc.
    echo.
    
    REM Optional: Test the executable
    choice /M "Would you like to test the executable now"
    if %errorlevel% == 1 (
        echo Testing executable...
        start "Testing Erics-Omvandlare" "dist\Erics-Omvandlare.exe"
    )
) else (
    echo.
    echo BUILD FAILED!
    echo Check the output above for errors.
    echo.
)

echo.
pause
