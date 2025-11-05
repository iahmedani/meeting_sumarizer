# Meeting Recorder, Transcriber & Summarizer 🎙️

A comprehensive desktop application for recording meetings, transcribing audio to text using AI (Whisper), and generating intelligent summaries using Claude AI. Similar to Notion's meeting capabilities but runs entirely on your laptop!

## Features ✨

- 🎤 **Audio Recording**: High-quality audio recording with real-time timer
- 📝 **AI Transcription**: Automatic speech-to-text using OpenAI's Whisper model
- 🤖 **Smart Summaries**: AI-powered meeting summaries with key points, decisions, and action items
- 💾 **Database Storage**: SQLite database to organize and track all your meetings
- 🖥️ **Dual Interface**: Both GUI (tkinter) and CLI interfaces available
- 📊 **Meeting Management**: View, organize, and search through past meetings

## Requirements

- Python 3.8 or higher
- Microphone for audio recording
- 4GB+ RAM recommended (for Whisper model)
- Anthropic API key (for AI summarization)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd meeting_sumarizer
```

### 2. Install System Dependencies

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y python3-pyaudio portaudio19-dev
```

#### macOS
```bash
brew install portaudio
```

#### Windows
PyAudio will be installed via pip (may require Microsoft C++ Build Tools)

### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The first time you run the transcription, Whisper will download the model (~150MB for 'base' model).

### 5. Set Up API Keys

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

Get your API key from: https://console.anthropic.com/

## Usage

### GUI Application (Recommended)

Launch the graphical interface:

```bash
python gui.py
```

**GUI Features:**
- Click "Start Recording" to begin recording a meeting
- Enter a descriptive meeting title
- Click "Stop Recording" when done
- Click "Transcribe" to convert audio to text
- Click "Summarize" to generate an AI summary
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
├── transcriber.py         # Speech-to-text transcription
├── summarizer.py          # AI-powered summarization
├── database.py            # SQLite database management
├── gui.py                 # Tkinter GUI application
├── cli.py                 # Command-line interface
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
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

### 2. Transcription
- Uses OpenAI's Whisper model for speech recognition
- Supports multiple model sizes:
  - `tiny` - Fastest, least accurate (~40MB)
  - `base` - Good balance (default, ~150MB)
  - `small` - Better accuracy (~500MB)
  - `medium` - Very accurate (~1.5GB)
  - `large` - Best accuracy (~3GB)
- Generates timestamped transcripts
- Saves transcripts in the `transcripts/` directory

### 3. Summarization
- Uses Claude AI (Anthropic) for intelligent summarization
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

### Customize Summarization Prompt

Edit the `_build_default_prompt()` method in `summarizer.py` to customize how summaries are generated.

## Troubleshooting

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

**Problem**: "Out of memory" error
- Use a smaller Whisper model (`tiny` or `base`)
- Close other applications to free up RAM

**Problem**: Transcription is slow
- Use GPU acceleration if available (requires CUDA setup)
- Use smaller model for faster processing

### Summarization Issues

**Problem**: "API key not found"
- Ensure `.env` file exists with valid `ANTHROPIC_API_KEY`
- Run `source .env` or restart the application

**Problem**: API rate limits
- The application uses Claude 3.5 Sonnet model
- Check your API usage limits at console.anthropic.com

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
   - Edit summaries if needed for your specific use case

## Privacy & Security

- All processing happens locally except for AI summarization (which uses Anthropic's API)
- Audio files and transcripts are stored only on your computer
- API keys are stored in `.env` file (not committed to git)
- No data is shared with third parties beyond the summarization API

## Cost Considerations

- **Recording & Transcription**: Free (runs locally using Whisper)
- **Summarization**: Uses Anthropic Claude API (paid)
  - Typical cost: ~$0.003-0.015 per meeting summary
  - Based on transcript length and model used
  - Check current pricing at: https://www.anthropic.com/pricing

## Future Enhancements

Potential features for future versions:
- [ ] Real-time transcription during recording
- [ ] Support for multiple languages
- [ ] Export to PDF/Markdown formats
- [ ] Integration with calendar apps
- [ ] Speaker diarization (identify different speakers)
- [ ] Search functionality across all meetings
- [ ] Cloud sync options
- [ ] Mobile app companion

## Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and create pull requests.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information

## Acknowledgments

- **OpenAI Whisper**: For the excellent speech recognition model
- **Anthropic Claude**: For powerful AI summarization capabilities
- **Python Community**: For the amazing libraries that made this possible

---

**Happy Meeting Recording! 🎉**

If you find this useful, please give it a star ⭐
