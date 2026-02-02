#!/bin/bash
# Local Start Script for HighTierBots (Linux/macOS Version)
# This script sets up the environment and starts the application locally

set -e

echo ""
echo "========================================"
echo "HighTierBots - Local Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is not installed or not in PATH"
  exit 1
fi

echo "Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
  echo "Virtual environment created successfully."
fi

echo "Virtual environment ready."

# Install requirements
echo ""
echo "Installing dependencies..."
echo "This may take a few minutes..."
echo ""

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo ""
echo "Dependencies installed successfully!"

# Start the application
echo ""
echo "========================================"
echo "Starting HighTierBots..."
echo "========================================"
echo ""

python3 main.py
