@echo off
echo.
echo ========================================
echo   Restarting Festiva Planner AI
echo ========================================
echo.

REM Kill any existing Python processes on port 8000
echo Stopping existing server...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /F /PID %%a 2>nul

echo.
echo Starting server with new UI...
echo.

REM Activate virtual environment and run
call venv\Scripts\activate.bat
python run.py
