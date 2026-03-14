@echo off
title Corporate Knowledge Nexus - Backend
echo.
echo  ============================================
echo   Corporate Knowledge Nexus - Starting...
echo  ============================================
echo.
cd /D "%~dp0backend"

IF NOT EXIST venv (
    echo [1/3] Creating virtual environment...
    python -m venv venv
)

echo [2/3] Activating venv and installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet

IF NOT EXIST ".env" (
    echo.
    echo  WARNING: No .env file found! Copying from .env.example
    echo  Please edit backend\.env and add your OPENAI_API_KEY
    echo.
    copy .env.example .env
)

echo [3/3] Seeding database and starting server...
python seed.py
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
