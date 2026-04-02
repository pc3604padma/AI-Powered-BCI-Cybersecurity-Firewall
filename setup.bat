@echo off
REM SYNORA Setup Script for Windows Local Development
REM Built by Padmanathan and Oviya

setlocal enabledelayedexpansion

echo.
echo 🚀 SYNORA BCI Security - Windows Local Setup
echo =============================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "bci_env" (
    python -m venv bci_env
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call bci_env\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul
echo ✅ pip upgraded
echo.

REM Install requirements
echo Installing dependencies from requirements.txt...
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo ✅ Dependencies installed
) else (
    echo ❌ requirements.txt not found
    pause
    exit /b 1
)
echo.

REM Check MongoDB
echo Checking MongoDB...
where mongod >nul 2>&1
if errorlevel 1 (
    echo ⚠️  MongoDB not found in PATH
    echo    Please visit: https://www.mongodb.com/try/download/community
) else (
    echo ✅ MongoDB found
    tasklist /FI "IMAGENAME eq mongod.exe" 2>nul | find /I /N "mongod.exe" >nul
    if errorlevel 1 (
        echo.
        echo ⚠️  MongoDB not running. Start with: mongod.exe
    ) else (
        echo ✅ MongoDB is running
    )
)
echo.

REM Verify project files
echo Verifying project files...
setlocal enabledelayedexpansion
set "missing=0"

for %%F in (app.py database.py auth.py requirements.txt) do (
    if exist "%%F" (
        echo ✅ %%F
    ) else (
        echo ❌ %%F missing
        set "missing=1"
    )
)

if !missing! equ 1 (
    echo.
    echo ❌ Some required files are missing
    pause
    exit /b 1
)
echo.

REM Test imports
echo Testing Python imports...
python << 'PYTHON_EOF'
import sys
try:
    import streamlit
    import pandas
    import numpy
    import pymongo
    import plotly
    print("✅ All core imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
PYTHON_EOF

if errorlevel 1 (
    echo.
    echo ❌ Some imports failed
    pause
    exit /b 1
)
echo.

REM Display success message
echo ✅ Setup completed successfully!
echo.
echo 📋 Next steps:
echo.
echo 1. Make sure MongoDB is running:
echo    mongod.exe
echo.
echo 2. In a new terminal, activate environment and run the app:
echo    bci_env\Scripts\activate.bat
echo    streamlit run app.py
echo.
echo 3. Open browser to: http://localhost:8501
echo.
echo 📖 Documentation:
echo    - Quick Start: QUICK_START.md
echo    - Usage Guide: USAGE_GUIDE.md
echo    - Deployment: DEPLOYMENT_GUIDE.md
echo.
echo 🚀 Tips:
echo    - For Docker: docker-compose up
echo    - Test MongoDB: python test_mongodb.py
echo    - View MongoDB: Download MongoDB Compass
echo.
pause
