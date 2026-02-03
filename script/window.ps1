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

# Check if dependencies are already installed
Write-Host ""
Write-Host "Checking dependencies..."
Write-Host ""

$requirementsFile = "requirements.txt"
$allInstalled = $true

# Read requirements.txt and check each package
if (Test-Path $requirementsFile) {
    $packages = Get-Content $requirementsFile | Where-Object { $_ -and -not $_.StartsWith("#") }
    
    foreach ($package in $packages) {
        $packageName = $package.Split("==")[0].Split(">=")[0].Split("<=")[0].Split("<")[0].Split(">")[0].Trim()
        
        $checkOutput = python -m pip show $packageName 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Missing: $packageName"
            $allInstalled = $false
        } else {
            Write-Host "✅ Installed: $packageName"
        }
    }
}

Write-Host ""

if ($allInstalled) {
    Write-Host "All dependencies are already installed! ✅"
    Write-Host "Skipping installation..."
} else {
    Write-Host "Installing missing dependencies..."
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
}

Write-Host ""

# Start the application
Write-Host ""
Write-Host "========================================"
Write-Host "Starting HighTierBots..."
Write-Host "========================================"
Write-Host ""

python main.py
