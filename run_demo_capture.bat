@echo off
REM Quick start script for demo capture (Windows)

echo ========================================
echo Demo Capture - Quick Start
echo ========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo WARNING: No .env file found!
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo Created .env file
    echo.
    echo IMPORTANT: You need to add your OpenAI API key to the .env file
    echo.
    echo Edit the .env file and replace 'your-openai-api-key-here' with your actual key:
    echo   notepad .env
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

REM Check if OPENAI_API_KEY is set in .env
findstr "your-openai-api-key-here" .env >nul
if %errorlevel% equ 0 (
    echo WARNING: OPENAI_API_KEY is not configured!
    echo.
    echo Please edit the .env file and add your OpenAI API key:
    echo   notepad .env
    echo.
    echo Replace 'your-openai-api-key-here' with your actual API key ^(starts with 'sk-'^)
    pause
    exit /b 1
)

REM Load environment variables from .env
for /f "usebackq tokens=1,* delims==" %%a in (.env) do (
    if not "%%a"=="" if not "%%a:~0,1%"=="#" (
        set "%%a=%%b"
    )
)

REM Check if API key is set
if "%OPENAI_API_KEY%"=="" (
    echo WARNING: OPENAI_API_KEY environment variable is empty!
    echo.
    echo Please add your OpenAI API key to the .env file:
    echo   notepad .env
    pause
    exit /b 1
)

echo Environment configured
echo.
echo Starting demo automation...
echo This will:
echo   1. Start the Streamlit server
echo   2. Load demo documents
echo   3. Capture 3 screenshots
echo   4. Record a demo video
echo   5. Save all assets to demo_tools\output\
echo.
echo Estimated time: 2-3 minutes
echo.

REM Run the demo capture script
python -m demo_tools.capture_demo

REM Check exit code
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Demo capture completed successfully!
    echo ========================================
    echo.
    echo Your demo assets are ready in:
    echo   demo_tools\output\[timestamp]\
    echo.
    echo Files generated:
    echo   * 01_indexed_files.png
    echo   * 02_answer.png
    echo   * 03_sources.png
    echo   * demo.mp4
    echo.
    echo These assets are ready for your product launch! 🚀
    echo.
) else (
    echo.
    echo Demo capture failed!
    echo.
    echo Please check the error messages above and try again.
    echo For help, see DEMO_CAPTURE_GUIDE.md
    pause
    exit /b 1
)

pause
