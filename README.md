# Meeting Recorder, Transcriber & Summarizer 🎙️

A comprehensive desktop application for recording meetings, transcribing audio to text using AI (Whisper), and generating intelligent summaries using local Ollama models. Similar to Notion's meeting capabilities but runs **completely locally** on your laptop with full privacy!

## Features ✨

- 🎤 **Audio Recording**: High-quality audio recording with real-time timer
- 📝 **AI Transcription**: Automatic speech-to-text using OpenAI's Whisper model (local)
- 🤖 **Smart Summaries**: AI-powered meeting summaries using local Ollama models (Llama, Mistral, etc.)
- 💾 **Database Storage**: SQLite database to organize and track all your meetings
- 🖥️ **Dual Interface**: Both GUI (tkinter) and CLI interfaces available
- 📊 **Meeting Management**: View, organize, and search through past meetings
- 🔒 **100% Private**: All processing happens locally on your machine

## Requirements

- Python 3.8 or higher
- Microphone for audio recording
- 8GB+ RAM recommended (4GB minimum for small models)
- **FFmpeg** (required for audio processing)
- **Ollama** (for AI summarization)

## Installation

### 1. Install Ollama

First, install Ollama on your system:

#### Linux & macOS
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows
Download from: https://ollama.com/download/windows

#### Verify Ollama Installation
```bash
ollama --version
```

### 2. Download an AI Model

Pull a model for summarization (choose one):

```bash
# Small & fast (recommended for 8GB RAM)
ollama pull llama3.2

# Balanced performance (good for 16GB+ RAM)
ollama pull llama3.2:3b

# Better quality (requires 16GB+ RAM)
ollama pull llama3.1:8b

# Alternative: Mistral
ollama pull mistral

# Multilingual support
ollama pull qwen2.5:7b
```

### 3. Clone the Repository

```bash
git clone <repository-url>
cd meeting_sumarizer
```

### 4. Install System Dependencies

#### macOS
```bash
# Install audio dependencies and ffmpeg (required for Whisper)
brew install portaudio ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y python3-pyaudio portaudio19-dev ffmpeg
```

#### Windows
```bash
# Install ffmpeg using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**Note**: FFmpeg is required for Whisper to process audio files. Make sure it's installed before running transcription.

### 5. Run Setup Script (Automated)

```bash
bash setup.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 6. Configure (Optional)

Copy and edit the environment file if you want to use a different model:

```bash
cp .env.example .env
```

Edit `.env` to change the model:
```bash
OLLAMA_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
```

## Usage

### Start Ollama Server

Make sure Ollama is running (usually starts automatically):

```bash
ollama serve
```

### GUI Application (Recommended)

Launch the graphical interface:

```bash
source venv/bin/activate  # If not already activated
python gui.py
```

**GUI Features:**
- Click "Start Recording" to begin recording a meeting
- Enter a descriptive meeting title
- Click "Stop Recording" when done
- Click "Transcribe" to convert audio to text (runs locally with Whisper)
- Click "Summarize" to generate an AI summary (runs locally with Ollama)
- View all past meetings in the list below
- Select a meeting and click "View Details" to see full information

### CLI Application

Launch the command-line interface:

```bash
python cli.py
```

**CLI Menu Options:**
1. **Record Meeting** - Record a new meeting
2. **Transcribe Meeting** - Transcribe an existing recording
3. **Summarize Meeting** - Generate AI summary from transcript
4. **List All Meetings** - View all recorded meetings
5. **Complete Workflow** - Do all steps automatically (Record → Transcribe → Summarize)
6. **Exit**

## Project Structure

```
meeting_sumarizer/
├── audio_recorder.py      # Audio recording module
├── transcriber.py         # Speech-to-text transcription (Whisper)
├── summarizer.py          # AI-powered summarization (Ollama)
├── database.py            # SQLite database management
├── gui.py                 # Tkinter GUI application
├── cli.py                 # Command-line interface
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── setup.sh              # Automated setup script
└── README.md             # This file

# Generated folders (created automatically):
├── recordings/           # Audio files (.wav)
├── transcripts/          # Transcription files (.txt)
├── summaries/            # Summary files (.txt)
└── meetings.db           # SQLite database
```

## How It Works

### 1. Audio Recording
- Uses `sounddevice` library for cross-platform audio capture
- Records in 16kHz mono WAV format (optimal for Whisper)
- Saves recordings in the `recordings/` directory

### 2. Transcription (Local)
- Uses OpenAI's Whisper model for speech recognition
- Runs completely locally on your machine
- Supports multiple model sizes:
  - `tiny` - Fastest, least accurate (~40MB)
  - `base` - Good balance (default, ~150MB)
  - `small` - Better accuracy (~500MB)
  - `medium` - Very accurate (~1.5GB)
  - `large` - Best accuracy (~3GB)
- Generates timestamped transcripts
- Saves transcripts in the `transcripts/` directory

### 3. Summarization (Local with Ollama)
- Uses Ollama for running local LLMs (Llama, Mistral, etc.)
- **Completely private** - no data sent to external servers
- Generates structured summaries with:
  - Executive Summary
  - Key Discussion Points
  - Decisions Made
  - Action Items
  - Next Steps
- Saves summaries in the `summaries/` directory

### 4. Database
- SQLite database stores meeting metadata
- Tracks: title, date, duration, file paths, summaries
- Enables easy retrieval and organization

## Configuration

### Change Whisper Model Size

Edit the model size in `gui.py` or `cli.py`:

```python
self.transcriber = Transcriber(model_size='small')  # Change to tiny/base/small/medium/large
```

**Model Size Recommendations:**
- **tiny/base**: Fast, good for quick meetings or less critical content
- **small**: Balanced option for most use cases
- **medium/large**: High accuracy for important meetings, technical discussions

### Change Ollama Model

You can use different Ollama models for summarization:

```bash
# List available models
ollama list

# Pull a different model
ollama pull mistral

# Set in .env file
echo "OLLAMA_MODEL=mistral" > .env
```

Or pass it when initializing:
```python
summarizer = Summarizer(model_name='mistral')
```

**Recommended Ollama Models:**
- **llama3.2** - Small, fast (1-3B parameters)
- **llama3.2:3b** - Good balance
- **llama3.1:8b** - Better quality, needs more RAM
- **mistral** - Good alternative, efficient
- **qwen2.5:7b** - Multilingual support

### Customize Summarization Prompt

Edit the `_build_default_prompt()` method in `summarizer.py` to customize how summaries are generated.

## Troubleshooting

### Ollama Issues

**Problem**: "Could not connect to Ollama"
```bash
# Check if Ollama is running
ollama list

# Start Ollama server
ollama serve
```

**Problem**: "Model not found"
```bash
# List available models
ollama list

# Pull the model you need
ollama pull llama3.2
```

**Problem**: Summarization is slow
- Use a smaller model: `llama3.2` instead of `llama3.1:8b`
- Close other applications to free up RAM
- Ensure Ollama has enough memory allocated

### Audio Recording Issues

**Problem**: "No audio devices found"
```bash
# List available audio devices
python -c "from audio_recorder import AudioRecorder; AudioRecorder.list_audio_devices()"
```

**Problem**: Permission denied for microphone
- **macOS**: System Preferences → Security & Privacy → Microphone → Enable for Terminal/Python
- **Linux**: Ensure user is in `audio` group: `sudo usermod -a -G audio $USER`

### Transcription Issues

**Problem**: "[Errno 2] No such file or directory: 'ffmpeg'"
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg

# Windows
choco install ffmpeg
# Or download from https://ffmpeg.org/download.html

# Verify installation
ffmpeg -version
```

**Problem**: "Out of memory" error
- Use a smaller Whisper model (`tiny` or `base`)
- Close other applications to free up RAM

**Problem**: Transcription is slow
- Use GPU acceleration if available (requires CUDA setup)
- Use smaller model for faster processing

## Performance & System Requirements

### Minimum Requirements
- **CPU**: Dual-core processor
- **RAM**: 4GB (for tiny/base models)
- **Storage**: 5GB free space

### Recommended Specs
- **CPU**: Quad-core or better
- **RAM**: 8GB+ (16GB for larger models)
- **Storage**: 10GB+ free space
- **GPU**: Optional, but significantly speeds up transcription with CUDA support

### Processing Times (Approximate)
- **Recording**: Real-time
- **Transcription** (base model): ~1-2 minutes per 10 minutes of audio
- **Summarization** (llama3.2): ~10-30 seconds depending on transcript length

## Privacy & Security

- **100% Local Processing**: All audio recording, transcription, and summarization happens on your machine
- **No Internet Required**: After initial setup, works completely offline
- **Your Data Stays Private**: No data sent to external servers or APIs
- **Open Source Models**: Uses open-source Whisper and Ollama models

## Cost

**Completely FREE!**
- No API fees
- No subscriptions
- No cloud costs
- Open-source software

## Tips for Best Results

1. **Recording Quality**
   - Use a good microphone in a quiet environment
   - Speak clearly and minimize background noise
   - Keep recordings under 2 hours for optimal processing

2. **Transcription Accuracy**
   - Use higher quality models for technical/medical content
   - Specify language if not English: `transcriber.transcribe_audio(path, language='es')`

3. **Better Summaries**
   - Include meaningful meeting titles
   - Ensure transcription is accurate before summarizing
   - Use larger Ollama models for more detailed summaries

4. **Performance Optimization**
   - Close unnecessary applications during processing
   - Use SSD for faster file operations
   - Consider GPU acceleration for Whisper if available

## Future Enhancements

Potential features for future versions:
- [ ] Real-time transcription during recording
- [ ] Support for multiple languages
- [ ] Export to PDF/Markdown formats
- [ ] Integration with calendar apps
- [ ] Speaker diarization (identify different speakers)
- [ ] Search functionality across all meetings
- [ ] Cloud sync options (optional)
- [ ] Mobile app companion
- [ ] Web interface option

## Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and create pull requests.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section above
2. Ensure Ollama is installed and running: `ollama list`
3. Ensure your model is downloaded: `ollama pull llama3.2`
4. Search existing issues on GitHub
5. Create a new issue with detailed information

## Acknowledgments

- **OpenAI Whisper**: For the excellent open-source speech recognition model
- **Ollama**: For making local LLM inference accessible and easy
- **Meta (Llama)** & **Mistral AI**: For the open-source language models
- **Python Community**: For the amazing libraries that made this possible

---

**Happy Meeting Recording! 🎉**

**100% Private. 100% Local. 100% Free.**

If you find this useful, please give it a star ⭐
