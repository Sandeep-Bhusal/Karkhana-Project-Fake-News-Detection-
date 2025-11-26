# Quick Setup Script for Fake News Detection System
# Run this script to set up the project quickly

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fake News Detection System - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Step 2: Install dependencies
Write-Host ""
Write-Host "[2/4] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Step 3: Train model
Write-Host ""
Write-Host "[3/4] Training the model..." -ForegroundColor Yellow
Write-Host "(This uses sample data. For better accuracy, add Kaggle dataset to data/raw/)" -ForegroundColor Gray
python model/train_model.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Model trained successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Model training failed" -ForegroundColor Red
    exit 1
}

# Step 4: Instructions
Write-Host ""
Write-Host "[4/4] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the app locally:" -ForegroundColor White
Write-Host "  streamlit run app.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "To deploy on Streamlit Cloud:" -ForegroundColor White
Write-Host "  1. Push code to GitHub" -ForegroundColor Gray
Write-Host "  2. Go to share.streamlit.io" -ForegroundColor Gray
Write-Host "  3. Connect your repository" -ForegroundColor Gray
Write-Host "  4. Deploy!" -ForegroundColor Gray
Write-Host ""
Write-Host "For better accuracy:" -ForegroundColor White
Write-Host "  Download Kaggle dataset and place in data/raw/" -ForegroundColor Gray
Write-Host "  Then run: python model/train_model.py" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Happy detecting! 🔍" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
