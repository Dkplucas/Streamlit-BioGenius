# AI Bioinformatics Assistant - Startup Script
# This script starts both FastAPI backend and Streamlit frontend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🧬 AI Bioinformatics Assistant" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ .env created. Please edit it and add your OPENROUTER_API_KEY" -ForegroundColor Yellow
    } else {
        Write-Host "❌ .env.example not found!" -ForegroundColor Red
        exit 1
    }
}

# Load environment variables
Get-Content ".env" | ForEach-Object {
    if ($_ -match '^\s*([^=]+)=(.*)$') {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
}

Write-Host "Checking Python installation..." -ForegroundColor Cyan
python --version | Write-Host

Write-Host ""
Write-Host "Checking required packages..." -ForegroundColor Cyan

# Check if requirements are installed
$requirements = @("fastapi", "uvicorn", "streamlit", "requests", "python-dotenv")
$missing = @()

foreach ($pkg in $requirements) {
    try {
        python -c "import $($pkg.replace('-', '_'))" 2>$null
        Write-Host "✅ $pkg" -ForegroundColor Green
    } catch {
        Write-Host "❌ $pkg" -ForegroundColor Red
        $missing += $pkg
    }
}

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "Installing missing packages..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting services..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📡 Backend URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "🖥️  Frontend URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting FastAPI backend..." -ForegroundColor Green
$backendProcess = Start-Process python -ArgumentList "backend/main.py" -PassThru -NoNewWindow
Write-Host "Backend PID: $($backendProcess.Id)" -ForegroundColor Cyan

Write-Host "Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Starting Streamlit frontend..." -ForegroundColor Green
Start-Process streamlit -ArgumentList "run frontend/app.py"

Write-Host ""
Write-Host "✅ Services started!" -ForegroundColor Green
Write-Host "Frontend will open in your browser shortly..." -ForegroundColor Green
Write-Host ""
Write-Host "To stop services, close this window or press Ctrl+C" -ForegroundColor Yellow
Write-Host ""

# Keep the script running
$backendProcess.WaitForExit()
