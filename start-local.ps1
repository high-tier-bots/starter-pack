# Local Start Script for HighTierBots (PowerShell Version)
# This script sets up the environment and starts the application locally

Write-Host ""
Write-Host "========================================"
Write-Host "HighTierBots - Local Start"
Write-Host "========================================"
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion"
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH"
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
    Write-Host "Virtual environment created successfully."
}

Write-Host "Virtual environment ready."

# Install requirements
Write-Host ""
Write-Host "Installing dependencies..."
Write-Host "This may take a few minutes..."
Write-Host ""

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to install dependencies"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Dependencies installed successfully!"

# Start the application
Write-Host ""
Write-Host "========================================"
Write-Host "Starting HighTierBots..."
Write-Host "========================================"
Write-Host ""

python main.py
