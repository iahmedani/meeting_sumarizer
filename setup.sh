#!/bin/bash

# Setup script for Meeting Recorder & Summarizer

echo "=================================="
echo "Meeting Recorder Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check for ffmpeg
echo ""
echo "Checking for ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ ffmpeg is installed"
    ffmpeg -version | head -n 1
else
    echo "⚠️  Warning: ffmpeg is not installed"
    echo "   ffmpeg is required for audio transcription with Whisper"
    echo ""
    echo "   To install ffmpeg:"
    echo "   macOS:   brew install ffmpeg"
    echo "   Linux:   sudo apt-get install ffmpeg"
    echo "   Windows: choco install ffmpeg"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for Ollama
echo ""
echo "Checking for Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    ollama --version
else
    echo "⚠️  Warning: Ollama is not installed"
    echo "   Ollama is required for AI summarization"
    echo ""
    echo "   To install Ollama:"
    echo "   Linux/macOS: curl -fsSL https://ollama.com/install.sh | sh"
    echo "   Windows:     https://ollama.com/download/windows"
    echo ""
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing Python dependencies..."
echo "This may take several minutes..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "ℹ️  You can edit .env to change the Ollama model (default: llama3.2)"
fi

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p recordings transcripts summaries

echo ""
echo "=================================="
echo "✅ Setup completed successfully!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Make sure ffmpeg is installed: ffmpeg -version"
echo "2. Make sure Ollama is installed: ollama --version"
echo "3. Download an Ollama model: ollama pull llama3.2"
echo "4. Start Ollama server: ollama serve"
echo "5. Activate the virtual environment: source venv/bin/activate"
echo "6. Run the GUI: python gui.py"
echo "   OR run the CLI: python cli.py"
echo ""
