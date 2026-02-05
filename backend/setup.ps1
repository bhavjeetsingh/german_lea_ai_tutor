# GermanLeap Lea Backend Setup Script for Windows

Write-Host "🚀 Setting up GermanLeap Lea Python Backend..." -ForegroundColor Green

# Check Python installation
Write-Host "`n📦 Checking Python installation..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python installed: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found. Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`n🔨 Creating virtual environment..." -ForegroundColor Cyan
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`n🔄 Activating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "`n📥 Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

# Create .env file if it doesn't exist
Write-Host "`n⚙️  Setting up environment..." -ForegroundColor Cyan
if (Test-Path ".env") {
    Write-Host ".env file already exists." -ForegroundColor Yellow
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created from .env.example" -ForegroundColor Green
    Write-Host "⚠️  Please edit .env and add your API keys!" -ForegroundColor Yellow
}

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env and add your OpenAI or Anthropic API key"
Write-Host "2. Run: python main.py"
Write-Host "3. Visit: http://localhost:8000/docs"
