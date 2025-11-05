# Quick Start Guide 🚀

Get up and running with the Meeting Recorder in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Microphone connected to your computer
- Anthropic API key (get one at https://console.anthropic.com/)

## Installation (Quick)

```bash
# 1. Run the setup script
bash setup.sh

# 2. Add your API key to .env file
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env

# 3. Activate virtual environment
source venv/bin/activate

# 4. Launch the GUI
python gui.py
```

## Using the GUI

### Record Your First Meeting

1. **Start the Application**
   ```bash
   python gui.py
   ```

2. **Enter Meeting Title**
   - The default title shows current date/time
   - Edit it to something descriptive like "Team Standup" or "Client Call"

3. **Record**
   - Click "Start Recording"
   - Speak into your microphone
   - Click "Stop Recording" when done

4. **Transcribe**
   - Click the "Transcribe" button
   - Wait a few minutes while Whisper processes the audio
   - The transcript will appear in the output window

5. **Summarize**
   - Click the "Summarize" button
   - Wait a moment for Claude AI to generate the summary
   - Read your structured meeting summary!

### Complete Workflow

For a faster experience after your first recording:
- Just record your meeting
- Click "Record → Transcribe → Summarize" button
- Everything happens automatically!

## Using the CLI

```bash
# Launch CLI
python cli.py

# Choose option 5: Complete Workflow
# This will guide you through:
# - Recording
# - Transcription
# - Summarization
```

## File Locations

After recording, you'll find:
- **Audio files**: `recordings/meeting_YYYYMMDD_HHMMSS.wav`
- **Transcripts**: `transcripts/meeting_YYYYMMDD_HHMMSS_transcript.txt`
- **Summaries**: `summaries/meeting_YYYYMMDD_HHMMSS_summary.txt`
- **Database**: `meetings.db`

## Tips for Best Results

1. **Audio Quality**
   - Use a good microphone (built-in is okay, external is better)
   - Record in a quiet room
   - Speak clearly

2. **Processing Time**
   - **Recording**: Real-time
   - **Transcription**: ~1-2 minutes per 10 minutes of audio (base model)
   - **Summarization**: ~5-10 seconds

3. **First Run**
   - The first transcription will download the Whisper model (~150MB)
   - This only happens once

## Troubleshooting

### "No module named 'sounddevice'"
```bash
pip install sounddevice
```

### "ANTHROPIC_API_KEY not found"
Make sure your `.env` file exists and contains:
```
ANTHROPIC_API_KEY=your_actual_key_here
```

### "No audio devices found"
- Check your microphone is connected
- On macOS: Grant microphone permission in System Preferences
- On Linux: Ensure you're in the `audio` group

### Slow transcription
- Use a smaller Whisper model:
  ```python
  # In gui.py or cli.py, change:
  self.transcriber = Transcriber(model_size='tiny')  # Fastest
  ```

## What's Next?

- Try recording different types of meetings
- Experiment with different Whisper models (tiny/base/small/medium/large)
- Customize the summarization prompt in `summarizer.py`
- Export your summaries to your note-taking app

## Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review the troubleshooting section
- Open an issue on GitHub

---

**Happy Recording! 🎙️**
