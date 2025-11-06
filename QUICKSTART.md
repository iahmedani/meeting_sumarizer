# Quick Start Guide 🚀

Get up and running with the Meeting Recorder in 10 minutes!

## Prerequisites

- Python 3.8+ installed
- Microphone connected to your computer
- **Ollama installed** (we'll guide you through this)
- 8GB+ RAM recommended

## Step 1: Install Ollama (5 minutes)

### Linux & macOS
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows
Download and install from: https://ollama.com/download/windows

### Verify Installation
```bash
ollama --version
```

## Step 2: Download AI Model (2 minutes)

Choose and download a model (pick one):

```bash
# Small & fast - recommended for most users
ollama pull llama3.2

# OR for better quality (if you have 16GB+ RAM)
ollama pull llama3.2:3b
```

**Wait for download to complete** (1-4GB depending on model)

## Step 3: Install FFmpeg (Required for Whisper)

FFmpeg is required for audio transcription with Whisper.

### macOS
```bash
brew install ffmpeg
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install ffmpeg
```

### Windows
```bash
choco install ffmpeg
# Or download from: https://ffmpeg.org/download.html
```

### Verify Installation
```bash
ffmpeg -version
```

## Step 4: Install Meeting Recorder (3 minutes)

```bash
# 1. Run the setup script
bash setup.sh

# 2. Activate virtual environment
source venv/bin/activate

# 3. (Optional) Configure model preference
cp .env.example .env
# Edit .env if you want to use a different model
```

## Step 5: Start Recording!

### Make sure Ollama is running:
```bash
ollama serve
```

### Launch the GUI:
```bash
python gui.py
```

## Using the Application

### Your First Meeting Recording

1. **Enter Meeting Title**
   - Default shows current date/time
   - Edit to something descriptive like "Team Standup" or "Client Call"

2. **Record**
   - Click "Start Recording" 🔴
   - Speak into your microphone
   - Click "Stop Recording" when done ⏹️

3. **Transcribe**
   - Click "Transcribe" button
   - Wait 1-2 minutes (processes locally with Whisper)
   - Transcript appears in output window

4. **Summarize**
   - Click "Summarize" button
   - Wait 10-30 seconds (processes locally with Ollama)
   - Read your structured meeting summary!

### Complete Workflow (One Button)

After recording:
- Click "Record → Transcribe → Summarize"
- Everything happens automatically!

## Using the CLI

```bash
# Launch CLI
python cli.py

# Choose option 5: Complete Workflow
# Follow the prompts:
# 1. Enter meeting title
# 2. Press ENTER to start recording
# 3. Press ENTER to stop
# 4. Wait for automatic transcription and summarization
```

## File Locations

After recording, you'll find:
- **Audio files**: `recordings/meeting_YYYYMMDD_HHMMSS.wav`
- **Transcripts**: `transcripts/meeting_YYYYMMDD_HHMMSS_transcript.txt`
- **Summaries**: `summaries/meeting_YYYYMMDD_HHMMSS_summary.txt`
- **Database**: `meetings.db`

## What Models Should I Use?

### For Summarization (Ollama):
- **8GB RAM**: `llama3.2` (small, fast)
- **16GB+ RAM**: `llama3.2:3b` or `mistral` (better quality)
- **32GB+ RAM**: `llama3.1:8b` (best quality)

### For Transcription (Whisper):
- **Quick meetings**: `tiny` or `base` (default)
- **Important meetings**: `small` or `medium`
- **Technical/Medical**: `medium` or `large`

Change Whisper model in gui.py:
```python
self.transcriber = Transcriber(model_size='small')
```

## Processing Times

For a 10-minute meeting:
- **Recording**: 10 minutes (real-time)
- **Transcription**: ~1-2 minutes (base model)
- **Summarization**: ~10-30 seconds (llama3.2)

**Total: ~12 minutes** for a 10-minute meeting

## Tips for Best Results

1. **Audio Quality**
   - Use a good microphone (built-in is okay, external is better)
   - Record in a quiet room
   - Speak clearly at normal pace

2. **First Run**
   - First transcription downloads Whisper model (~150MB)
   - This only happens once
   - Subsequent transcriptions are faster

3. **Performance**
   - Close unnecessary apps during processing
   - Use smaller models if processing is slow
   - Ensure Ollama is running before summarization

## Troubleshooting

### "Could not connect to Ollama"
```bash
# Start Ollama server
ollama serve

# Verify it's running
ollama list
```

### "Model not found"
```bash
# Download the model
ollama pull llama3.2

# Check available models
ollama list
```

### "No module named 'sounddevice'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "No audio devices found"
- Check your microphone is connected
- On macOS: Grant microphone permission in System Preferences
- On Linux: Ensure you're in the `audio` group

### Slow Processing
```bash
# Use smaller Whisper model
# Edit gui.py or cli.py:
self.transcriber = Transcriber(model_size='tiny')  # Fastest

# Use smaller Ollama model
ollama pull llama3.2  # Smallest, fastest
```

## Privacy Notice

🔒 **Everything runs locally on your machine!**
- No data sent to cloud services
- No API keys required
- Works completely offline (after initial setup)
- Your meetings stay 100% private

## What's Next?

- Try recording different types of meetings
- Experiment with different models
- Customize the summarization prompt in `summarizer.py`
- View past meetings in the GUI list
- Export your summaries to your note-taking app

## Available Ollama Models

List all available models:
```bash
ollama list
```

Browse more models:
```bash
# Visit: https://ollama.com/library

# Popular choices:
ollama pull llama3.2       # Recommended starter
ollama pull llama3.2:3b    # Better quality
ollama pull mistral        # Alternative
ollama pull qwen2.5:7b     # Multilingual
```

## Need More Help?

- Check the full [README.md](README.md) for detailed documentation
- Review the Troubleshooting section
- Make sure Ollama is running: `ollama serve`
- Make sure your model is downloaded: `ollama list`

## Quick Command Reference

```bash
# Setup
bash setup.sh
source venv/bin/activate

# Ollama
ollama serve              # Start Ollama server
ollama list               # List installed models
ollama pull llama3.2      # Download model

# Run Application
python gui.py             # Launch GUI
python cli.py             # Launch CLI

# Check Status
ollama --version          # Check Ollama installation
python --version          # Check Python version
pip list                  # Check installed packages
```

---

**Happy Recording! 🎙️**

**Remember: 100% Private. 100% Local. 100% Free.**
