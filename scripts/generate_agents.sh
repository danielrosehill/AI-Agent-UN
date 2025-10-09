#!/bin/bash
# Generate agent directories and system prompts for all UN member states

set -e  # Exit on error

echo "🤖 Generating UN Delegate Agents"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "Please run ./scripts/setup.sh first"
    exit 1
fi

# Check if data file exists
if [ ! -f "data/united-nations-membership-status.json" ]; then
    echo "❌ Error: UN membership data not found"
    echo "Expected: data/united-nations-membership-status.json"
    exit 1
fi

# Run the generation script
echo "📁 Creating agent directories..."
.venv/bin/python3 generate_agents.py

echo ""
echo "✓ Agent generation complete"
echo ""
