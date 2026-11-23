@echo off
title WorthIQ Launcher
echo ===================================================
echo           Starting WorthIQ Platform
echo ===================================================
echo.

:: 1. Check & start PostgreSQL container
echo [1/3] Ensuring PostgreSQL container is running...
docker inspect -f "{{.State.Running}}" worthiq_postgres 2>nul | findstr "true" >nul
if %errorlevel% neq 0 (
    echo Starting worthiq_postgres container...
    docker start worthiq_postgres 2>nul
    if %errorlevel% neq 0 (
        docker compose -f database\docker-compose.yml up -d
    )
) else (
    echo Postgres container is already active.
)

:: 2. Start Django Backend in a separate window
echo [2/3] Starting Django Backend (http://localhost:8000)...
start "WorthIQ Backend (Django)" cmd /k "cd /d %~dp0 && backend\venv\Scripts\python.exe backend\manage.py runserver 0.0.0.0:8000"

:: 3. Start React Vite Frontend in a separate window
echo [3/3] Starting React Vite Frontend (http://localhost:5180)...
start "WorthIQ Frontend (React/Vite)" cmd /k "cd /d %~dp0frontend && npm run dev"

:: 4. Open Browser
timeout /t 3 /nobreak >nul
start http://localhost:5180

echo.
echo ===================================================
echo WorthIQ is running!
echo Frontend: http://localhost:5180
echo Backend:  http://localhost:8000
echo Database: PostgreSQL port 5432
echo ===================================================
echo.
pause
