#!/bin/bash

# AI Agent UN - Setup Script
# This script helps you set up the environment for running simulations

set -e

echo "=========================================="
echo "AI Agent UN - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "1. Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.12 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Check for virtual environment
echo "2. Checking virtual environment..."
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi
echo ""

# Activate virtual environment and install dependencies
echo "3. Installing dependencies..."
if command -v uv &> /dev/null; then
    echo "Using uv (faster)..."
    uv pip install -r requirements.txt
else
    echo "Using pip..."
    .venv/bin/python -m pip install -r requirements.txt
fi
echo "✓ Dependencies installed"
echo ""

# Check for .env file
echo "4. Checking configuration..."
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys"
    echo "   - For cloud: Add OPENAI_API_KEY or ANTHROPIC_API_KEY"
    echo "   - For local: Install Ollama and pull a model"
else
    echo "✓ .env file exists"
fi
echo ""

# Final instructions
echo "=========================================="
echo "Setup complete! 🎉"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure your API keys (if using cloud):"
echo "   nano .env"
echo ""
echo "2. Run a test simulation:"
echo "   python scripts/run_motion.py 01_gaza_ceasefire_resolution --sample 3"
echo ""
echo "3. Run a full simulation:"
echo "   python scripts/run_motion.py 01_gaza_ceasefire_resolution"
echo ""
echo "For more information, see docs/USAGE.md"
echo ""
