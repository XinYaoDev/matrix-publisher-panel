@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   Matrix Publisher Panel
echo ============================================
echo.

:: Prefer social-auto-upload venv Python (has patchright)
set "PYTHON=python"
if exist "..\social-auto-upload\.venv\Scripts\python.exe" (
    set "PYTHON=..\social-auto-upload\.venv\Scripts\python.exe"
    echo [INFO] Using SAU venv Python
)

:: Check social-auto-upload
if not exist "..\social-auto-upload\sau_cli.py" (
    echo [WARN] social-auto-upload not found at ..\social-auto-upload\
    echo        Login and upload features will not work.
    echo        Set SAU_ROOT env var to its path if it's elsewhere.
    echo.
)

:: Install httpx into current environment if missing (patchright is in SAU venv)
%PYTHON% -c "import httpx" 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Installing httpx...
    %PYTHON% -m pip install httpx --quiet
)

echo [INFO] Starting server on http://127.0.0.1:8787
echo [INFO] Press Ctrl+C to stop.
echo.

%PYTHON% server.py
pause
