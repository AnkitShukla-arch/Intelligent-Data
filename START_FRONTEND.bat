@echo off
title Corporate Knowledge Nexus - Frontend
echo.
echo  ============================================
echo   Corporate Knowledge Nexus - Frontend
echo  ============================================
echo.
cd /D "%~dp0frontend"

IF NOT EXIST "node_modules" (
    echo Installing npm packages...
    call npm install
)

echo Starting frontend at http://localhost:3000
call npm run dev

pause
