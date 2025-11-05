"""Transcription module using OpenAI Whisper."""
import os
import whisper
import torch


class Transcriber:
    """Transcriber for converting audio to text using Whisper."""

    def __init__(self, model_size='base'):
        """
        Initialize the transcriber.

        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
                       'tiny' - fastest, least accurate
                       'base' - good balance (default)
                       'small' - better accuracy
                       'medium' - very good accuracy
                       'large' - best accuracy, slowest
        """
        self.model_size = model_size
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

    def load_model(self):
        """Load the Whisper model."""
        if self.model is None:
            print(f"Loading Whisper model ({self.model_size})...")
            self.model = whisper.load_model(self.model_size, device=self.device)
            print("Model loaded successfully!")

    def transcribe_audio(self, audio_file_path, language='en'):
        """
        Transcribe audio file to text.

        Args:
            audio_file_path: Path to the audio file
            language: Language code (default: 'en' for English, None for auto-detect)

        Returns:
            Dictionary containing transcription and metadata
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        self.load_model()

        print(f"Transcribing audio file: {audio_file_path}")

        # Transcribe
        result = self.model.transcribe(
            audio_file_path,
            language=language,
            verbose=False
        )

        return result

    def save_transcript(self, result, output_path, include_timestamps=True):
        """
        Save transcription to a text file.

        Args:
            result: Transcription result from Whisper
            output_path: Path to save the transcript
            include_timestamps: Whether to include timestamps in the output

        Returns:
            Path to the saved transcript file
        """
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            # Write full text
            f.write("=== FULL TRANSCRIPT ===\n\n")
            f.write(result['text'].strip())
            f.write("\n\n")

            # Write segments with timestamps if requested
            if include_timestamps and 'segments' in result:
                f.write("=== DETAILED TRANSCRIPT WITH TIMESTAMPS ===\n\n")
                for segment in result['segments']:
                    start = self._format_timestamp(segment['start'])
                    end = self._format_timestamp(segment['end'])
                    text = segment['text'].strip()
                    f.write(f"[{start} --> {end}] {text}\n")

        print(f"Transcript saved to: {output_path}")
        return output_path

    @staticmethod
    def _format_timestamp(seconds):
        """Format seconds as HH:MM:SS."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def transcribe_and_save(self, audio_file_path, output_dir='transcripts', language='en'):
        """
        Convenience method to transcribe and save in one step.

        Args:
            audio_file_path: Path to the audio file
            output_dir: Directory to save transcripts
            language: Language code

        Returns:
            Tuple of (transcript_path, full_text)
        """
        # Generate output filename
        base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_transcript.txt")

        # Transcribe
        result = self.transcribe_audio(audio_file_path, language)

        # Save
        self.save_transcript(result, output_path)

        return output_path, result['text']
