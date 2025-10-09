#!/bin/bash
# Setup script for AI Agent UN project

set -e  # Exit on error

echo "🌐 AI Agent UN - Setup Script"
echo "================================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv is not installed"
    echo "Please install uv first: https://github.com/astral-sh/uv"
    exit 1
fi

echo "✓ Found uv package manager"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To generate agent directories, run:"
echo "  ./scripts/generate_agents.sh"
echo ""
