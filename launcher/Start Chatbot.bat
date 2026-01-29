@echo off
REM Windows launcher for Document Chatbot
REM Double-click this file to start the application
SETLOCAL ENABLEDELAYEDEXPANSION

echo ========================================
echo   Document Chatbot Launcher
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0\.."

REM Check for Python installation
set PYTHON_CMD=
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    REM Try py launcher with Python 3.10+
    py -3.10 --version >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        set PYTHON_CMD=py -3.10
        echo [OK] Found Python via py launcher
    ) else (
        py -3 --version >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            set PYTHON_CMD=py -3
            echo [OK] Found Python via py launcher
        )
    )
)

if "!PYTHON_CMD!"=="" (
    where python >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        set PYTHON_CMD=python
        echo [OK] Found Python
    ) else (
        echo [ERROR] Python not found!
        echo.
        echo Please install Python 3.10 or higher from:
        echo https://www.python.org/downloads/
        echo.
        echo Make sure to check "Add Python to PATH" during installation.
        echo.
        pause
        exit /b 1
    )
)

REM Verify Python version
echo Checking Python version...
!PYTHON_CMD! -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python 3.10 or higher is required!
    echo.
    !PYTHON_CMD! --version
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

!PYTHON_CMD! --version

REM Create virtual environment if it doesn't exist
if not exist ".venv\" (
    echo.
    echo Creating virtual environment...
    !PYTHON_CMD! -m venv .venv
    if !ERRORLEVEL! NEQ 0 (
        echo [ERROR] Failed to create virtual environment!
        echo.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Check if dependencies need to be installed
set NEED_INSTALL=0
if not exist ".venv\.requirements_hash" (
    set NEED_INSTALL=1
    echo First run detected - will install dependencies...
) else (
    REM Compare requirements.txt hash
    certutil -hashfile requirements.txt MD5 > .venv\.requirements_hash_new 2>nul
    fc .venv\.requirements_hash .venv\.requirements_hash_new >nul 2>&1
    if !ERRORLEVEL! NEQ 0 (
        set NEED_INSTALL=1
        echo Requirements changed - will update dependencies...
    )
    del .venv\.requirements_hash_new >nul 2>&1
)

REM Install/update dependencies if needed
if !NEED_INSTALL! EQU 1 (
    echo.
    echo Installing dependencies (this may take a few minutes)...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if !ERRORLEVEL! NEQ 0 (
        echo [ERROR] Failed to install dependencies!
        echo.
        pause
        exit /b 1
    )
    REM Save hash for next time
    certutil -hashfile requirements.txt MD5 > .venv\.requirements_hash 2>nul
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already up to date
)

REM Check for .env file and OPENAI_API_KEY if using OpenAI
echo.
echo Checking configuration...
if exist ".env" (
    echo [OK] Found .env file
) else (
    if exist "config\config.example.yaml" (
        findstr /C:"provider: \"openai\"" config\config.example.yaml >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            echo [WARNING] No .env file found!
            echo.
            echo If you're using OpenAI, you need to:
            echo 1. Copy .env.example to .env
            echo 2. Add your OPENAI_API_KEY to the .env file
            echo.
            echo Press any key to continue anyway, or Ctrl+C to exit...
            pause >nul
        )
    )
)

REM Start Streamlit
echo.
echo ========================================
echo   Starting Document Chatbot...
echo ========================================
echo.
echo The application will open in your browser automatically.
echo Keep this window open while using the chatbot.
echo Press Ctrl+C to stop the application.
echo.

REM Open browser after a short delay
start "" python scripts\open_browser.py http://localhost:8501

REM Run Streamlit
streamlit run app\app.py --server.headless true --server.address localhost --server.port 8501

echo.
echo Application stopped.
pause
