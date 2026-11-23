Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "          Starting WorthIQ Platform" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# 1. Start Docker Container if not running
Write-Host "[1/3] Checking PostgreSQL container..." -ForegroundColor Yellow
$isRunning = docker inspect -f "{{.State.Running}}" worthiq_postgres 2>$null
if ($isRunning -ne "true") {
    Write-Host "Starting worthiq_postgres container..." -ForegroundColor Green
    docker start worthiq_postgres 2>$null
    if ($LASTEXITCODE -ne 0) {
        docker compose -f database\docker-compose.yml up -d
    }
} else {
    Write-Host "Postgres container is already active." -ForegroundColor Green
}

# 2. Start Django Backend in new window
Write-Host "[2/3] Starting Django Backend (http://localhost:8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; .\backend\venv\Scripts\python.exe .\backend\manage.py runserver 0.0.0.0:8000"

# 3. Start Vite Frontend in new window
Write-Host "[3/3] Starting React Frontend (http://localhost:5180)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

# 4. Open Browser
Start-Sleep -Seconds 3
Start-Process "http://localhost:5180"

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "WorthIQ successfully launched!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5180" -ForegroundColor White
Write-Host "Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "===================================================" -ForegroundColor Cyan
