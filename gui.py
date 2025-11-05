"""GUI application for meeting recorder, transcriber, and summarizer."""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import threading
import os
from datetime import datetime
from audio_recorder import AudioRecorder
from transcriber import Transcriber
from summarizer import Summarizer
from database import Database


class MeetingRecorderGUI:
    """GUI application for meeting recorder."""

    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Meeting Recorder & Summarizer")
        self.root.geometry("900x700")

        # Initialize components
        self.recorder = AudioRecorder()
        self.transcriber = Transcriber(model_size='base')
        try:
            self.summarizer = Summarizer()
            self.summarizer_available = True
        except ValueError as e:
            print(f"Summarizer not available: {e}")
            self.summarizer_available = False

        self.db = Database()

        # State variables
        self.is_recording = False
        self.current_meeting_id = None
        self.recording_start_time = None

        # Create UI
        self.create_widgets()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """Create GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Meeting Recorder & Summarizer",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=10)

        # Meeting title input
        title_frame = ttk.LabelFrame(main_frame, text="Meeting Details", padding="10")
        title_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        title_frame.columnconfigure(1, weight=1)

        ttk.Label(title_frame, text="Meeting Title:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.meeting_title_var = tk.StringVar(value=f"Meeting {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self.meeting_title_entry = ttk.Entry(title_frame, textvariable=self.meeting_title_var, width=50)
        self.meeting_title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        # Recording controls
        control_frame = ttk.LabelFrame(main_frame, text="Recording Controls", padding="10")
        control_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)

        self.record_button = ttk.Button(control_frame, text="Start Recording",
                                       command=self.toggle_recording, width=20)
        self.record_button.grid(row=0, column=0, padx=5)

        self.status_label = ttk.Label(control_frame, text="Ready", foreground="green")
        self.status_label.grid(row=0, column=1, padx=10)

        self.time_label = ttk.Label(control_frame, text="00:00:00", font=('Arial', 12, 'bold'))
        self.time_label.grid(row=0, column=2, padx=10)

        # Processing controls
        process_frame = ttk.LabelFrame(main_frame, text="Processing", padding="10")
        process_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)

        self.transcribe_button = ttk.Button(process_frame, text="Transcribe",
                                           command=self.transcribe_last_recording, width=15)
        self.transcribe_button.grid(row=0, column=0, padx=5)
        self.transcribe_button.config(state='disabled')

        self.summarize_button = ttk.Button(process_frame, text="Summarize",
                                          command=self.summarize_last_transcript, width=15)
        self.summarize_button.grid(row=0, column=1, padx=5)
        self.summarize_button.config(state='disabled')

        self.process_all_button = ttk.Button(process_frame, text="Record → Transcribe → Summarize",
                                            command=self.process_complete_workflow, width=30)
        self.process_all_button.grid(row=1, column=0, columnspan=2, pady=5)

        # Output display
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=15)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Meetings list
        meetings_frame = ttk.LabelFrame(main_frame, text="Recent Meetings", padding="10")
        meetings_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=5)
        meetings_frame.columnconfigure(0, weight=1)

        self.meetings_listbox = tk.Listbox(meetings_frame, height=5)
        self.meetings_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.meetings_listbox.bind('<<ListboxSelect>>', self.on_meeting_select)

        meetings_btn_frame = ttk.Frame(meetings_frame)
        meetings_btn_frame.grid(row=1, column=0, pady=5)

        ttk.Button(meetings_btn_frame, text="Refresh List",
                  command=self.refresh_meetings_list).grid(row=0, column=0, padx=5)
        ttk.Button(meetings_btn_frame, text="View Details",
                  command=self.view_meeting_details).grid(row=0, column=1, padx=5)

        # Initial load
        self.refresh_meetings_list()

        if not self.summarizer_available:
            self.log("Warning: Summarizer not configured. Please set ANTHROPIC_API_KEY in .env file")

    def toggle_recording(self):
        """Toggle recording on/off."""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Start recording."""
        self.is_recording = True
        self.recording_start_time = datetime.now()
        self.recorder.start_recording()

        self.record_button.config(text="Stop Recording")
        self.status_label.config(text="Recording...", foreground="red")
        self.meeting_title_entry.config(state='disabled')

        self.log(f"Started recording: {self.meeting_title_var.get()}")

        # Start timer update
        self.update_timer()

    def stop_recording(self):
        """Stop recording."""
        self.is_recording = False
        self.recorder.stop_recording()

        # Save recording
        audio_path = self.recorder.save_recording()
        duration = int(self.recorder.get_duration())

        # Save to database
        meeting = self.db.add_meeting(
            title=self.meeting_title_var.get(),
            duration=duration,
            audio_file_path=audio_path
        )
        self.current_meeting_id = meeting.id

        self.record_button.config(text="Start Recording")
        self.status_label.config(text="Recording saved", foreground="green")
        self.meeting_title_entry.config(state='normal')
        self.transcribe_button.config(state='normal')

        self.log(f"Recording stopped and saved: {audio_path}")
        self.log(f"Duration: {duration} seconds")

        self.refresh_meetings_list()

    def update_timer(self):
        """Update the recording timer."""
        if self.is_recording and self.recording_start_time:
            elapsed = (datetime.now() - self.recording_start_time).total_seconds()
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)
        else:
            self.time_label.config(text="00:00:00")

    def transcribe_last_recording(self):
        """Transcribe the last recording."""
        if not self.current_meeting_id:
            messagebox.showwarning("No Recording", "Please record audio first.")
            return

        meeting = self.db.get_meeting(self.current_meeting_id)
        if not meeting or not meeting.audio_file_path:
            messagebox.showerror("Error", "No audio file found for this meeting.")
            return

        self.log("Starting transcription... This may take a few minutes.")
        self.transcribe_button.config(state='disabled')

        # Run transcription in a separate thread
        def transcribe_thread():
            try:
                transcript_path, transcript_text = self.transcriber.transcribe_and_save(
                    meeting.audio_file_path
                )

                # Update database
                self.db.update_meeting(self.current_meeting_id, transcript_path=transcript_path)

                self.root.after(0, lambda: self.on_transcription_complete(transcript_text))

            except Exception as e:
                self.root.after(0, lambda: self.on_transcription_error(str(e)))

        thread = threading.Thread(target=transcribe_thread, daemon=True)
        thread.start()

    def on_transcription_complete(self, transcript_text):
        """Handle transcription completion."""
        self.log("Transcription completed!")
        self.log(f"Transcript preview: {transcript_text[:200]}...")
        self.transcribe_button.config(state='normal')
        self.summarize_button.config(state='normal')
        self.refresh_meetings_list()

    def on_transcription_error(self, error_msg):
        """Handle transcription error."""
        self.log(f"Transcription error: {error_msg}")
        messagebox.showerror("Transcription Error", f"Failed to transcribe: {error_msg}")
        self.transcribe_button.config(state='normal')

    def summarize_last_transcript(self):
        """Summarize the last transcript."""
        if not self.summarizer_available:
            messagebox.showwarning("Summarizer Not Available",
                                 "Please configure ANTHROPIC_API_KEY in .env file")
            return

        if not self.current_meeting_id:
            messagebox.showwarning("No Transcript", "Please transcribe audio first.")
            return

        meeting = self.db.get_meeting(self.current_meeting_id)
        if not meeting or not meeting.transcript_path:
            messagebox.showerror("Error", "No transcript found for this meeting.")
            return

        # Read transcript
        with open(meeting.transcript_path, 'r', encoding='utf-8') as f:
            transcript = f.read()

        self.log("Generating summary with AI... This may take a moment.")
        self.summarize_button.config(state='disabled')

        # Run summarization in a separate thread
        def summarize_thread():
            try:
                base_name = os.path.splitext(os.path.basename(meeting.audio_file_path))[0]
                filename = f"{base_name}_summary.txt"

                summary_path, summary_text = self.summarizer.summarize_and_save(
                    transcript,
                    meeting_title=meeting.title,
                    filename=filename
                )

                # Update database
                self.db.update_meeting(self.current_meeting_id, summary=summary_text)

                self.root.after(0, lambda: self.on_summarization_complete(summary_text))

            except Exception as e:
                self.root.after(0, lambda: self.on_summarization_error(str(e)))

        thread = threading.Thread(target=summarize_thread, daemon=True)
        thread.start()

    def on_summarization_complete(self, summary_text):
        """Handle summarization completion."""
        self.log("Summary generated successfully!")
        self.log(f"\n{summary_text}\n")
        self.summarize_button.config(state='normal')
        self.refresh_meetings_list()

    def on_summarization_error(self, error_msg):
        """Handle summarization error."""
        self.log(f"Summarization error: {error_msg}")
        messagebox.showerror("Summarization Error", f"Failed to generate summary: {error_msg}")
        self.summarize_button.config(state='normal')

    def process_complete_workflow(self):
        """Process complete workflow: record, transcribe, and summarize."""
        if self.is_recording:
            messagebox.showinfo("Info", "Please stop the current recording first.")
            return

        # Start new recording
        self.start_recording()

        # The rest will be triggered manually by the user

    def refresh_meetings_list(self):
        """Refresh the meetings list."""
        self.meetings_listbox.delete(0, tk.END)
        meetings = self.db.get_all_meetings()
        for meeting in meetings:
            status = "📝" if meeting.summary else ("📄" if meeting.transcript_path else "🎤")
            display_text = f"{status} {meeting.title} - {meeting.date.strftime('%Y-%m-%d %H:%M')}"
            self.meetings_listbox.insert(tk.END, display_text)

    def on_meeting_select(self, event):
        """Handle meeting selection."""
        selection = self.meetings_listbox.curselection()
        if selection:
            index = selection[0]
            meetings = self.db.get_all_meetings()
            if index < len(meetings):
                self.current_meeting_id = meetings[index].id

    def view_meeting_details(self):
        """View details of selected meeting."""
        if not self.current_meeting_id:
            messagebox.showwarning("No Selection", "Please select a meeting from the list.")
            return

        meeting = self.db.get_meeting(self.current_meeting_id)
        if not meeting:
            return

        # Clear output
        self.output_text.delete('1.0', tk.END)

        # Show details
        self.log(f"=== {meeting.title} ===")
        self.log(f"Date: {meeting.date.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"Duration: {meeting.duration} seconds" if meeting.duration else "Duration: Unknown")
        self.log(f"Audio: {meeting.audio_file_path}")

        if meeting.transcript_path:
            self.log(f"\nTranscript available at: {meeting.transcript_path}")

        if meeting.summary:
            self.log(f"\n=== SUMMARY ===\n")
            self.log(meeting.summary)

    def log(self, message):
        """Log message to output text widget."""
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()

    def on_closing(self):
        """Handle application closing."""
        if self.is_recording:
            if messagebox.askokcancel("Recording in Progress",
                                     "Recording is in progress. Stop and exit?"):
                self.stop_recording()
                self.db.close()
                self.root.destroy()
        else:
            self.db.close()
            self.root.destroy()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = MeetingRecorderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
