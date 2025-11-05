"""Audio recording module for capturing meeting audio."""
import os
import wave
import threading
import sounddevice as sd
import numpy as np
from datetime import datetime


class AudioRecorder:
    """Audio recorder for capturing meeting audio."""

    def __init__(self, sample_rate=16000, channels=1):
        """
        Initialize the audio recorder.

        Args:
            sample_rate: Sample rate in Hz (default: 16000 for Whisper compatibility)
            channels: Number of audio channels (default: 1 for mono)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.frames = []
        self.stream = None

    def start_recording(self):
        """Start recording audio."""
        if self.recording:
            print("Already recording!")
            return

        self.recording = True
        self.frames = []

        def callback(indata, frames, time, status):
            """Callback function for audio stream."""
            if status:
                print(f"Status: {status}")
            if self.recording:
                self.frames.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=callback,
            dtype='float32'
        )
        self.stream.start()
        print(f"Recording started... (Sample rate: {self.sample_rate} Hz)")

    def stop_recording(self):
        """Stop recording audio."""
        if not self.recording:
            print("Not currently recording!")
            return None

        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()

        print("Recording stopped.")
        return self.frames

    def save_recording(self, filename=None, output_dir='recordings'):
        """
        Save the recorded audio to a WAV file.

        Args:
            filename: Name of the output file (default: timestamp-based)
            output_dir: Directory to save recordings (default: 'recordings')

        Returns:
            Path to the saved file
        """
        if not self.frames:
            print("No audio recorded!")
            return None

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"meeting_{timestamp}.wav"

        filepath = os.path.join(output_dir, filename)

        # Concatenate all frames
        audio_data = np.concatenate(self.frames, axis=0)

        # Convert float32 to int16 for WAV file
        audio_data = np.int16(audio_data * 32767)

        # Save as WAV file
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 2 bytes for int16
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())

        print(f"Recording saved to: {filepath}")
        return filepath

    def get_duration(self):
        """Get the duration of the recording in seconds."""
        if not self.frames:
            return 0
        total_frames = sum(len(frame) for frame in self.frames)
        return total_frames / self.sample_rate

    @staticmethod
    def list_audio_devices():
        """List available audio input devices."""
        print("\nAvailable audio devices:")
        print(sd.query_devices())
        return sd.query_devices()
