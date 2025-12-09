#!/bin/bash

# Workspace Setup Script for Mini Project 3
# This script helps set up your development environment

echo "🚀 Setting up Mini Project 3 workspace..."

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p data/raw data/processed data/output
mkdir -p logs
mkdir -p .vscode

# Check Python installation
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found: $(python3 --version)"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "🐍 Creating Python virtual environment..."
        python3 -m venv venv
        echo "✅ Virtual environment created!"
        echo "💡 Activate it with: source venv/bin/activate"
    else
        echo "✅ Virtual environment already exists"
    fi
else
    echo "⚠️  Python 3 not found. Please install Python 3.8+"
fi

# Check Node.js installation
if command -v node &> /dev/null; then
    echo "✅ Node.js found: $(node --version)"
    if [ -f "package.json" ]; then
        echo "📦 Installing Node.js dependencies..."
        npm install
    fi
else
    echo "⚠️  Node.js not found. Install if you plan to use JavaScript/TypeScript"
fi

# Copy example config if config doesn't exist
if [ ! -f "config/config.json" ] && [ -f "config/config.example.json" ]; then
    echo "📋 Creating config file from example..."
    cp config/config.example.json config/config.json
    echo "✅ Config file created. Please edit config/config.json with your settings."
fi

echo ""
echo "✨ Workspace setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate Python venv: source venv/bin/activate"
echo "2. Install Python dependencies: pip install -r requirements.txt"
echo "3. Configure your project in config/config.json"
echo "4. Start coding in the src/ directory"
