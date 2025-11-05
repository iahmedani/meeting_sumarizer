"""Command-line interface for meeting recorder."""
import sys
import time
from datetime import datetime
from audio_recorder import AudioRecorder
from transcriber import Transcriber
from summarizer import Summarizer
from database import Database


def print_header():
    """Print application header."""
    print("\n" + "="*60)
    print("  Meeting Recorder, Transcriber & Summarizer")
    print("="*60 + "\n")


def record_meeting(db):
    """Record a meeting."""
    print_header()
    print("📹 RECORD MEETING")
    print("-" * 60)

    # Get meeting title
    title = input("Enter meeting title: ").strip()
    if not title:
        title = f"Meeting {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    # Initialize recorder
    recorder = AudioRecorder()

    print(f"\nMeeting: {title}")
    print("\nPress ENTER to start recording...")
    input()

    # Start recording
    recorder.start_recording()
    start_time = time.time()

    print("\n🔴 Recording... Press ENTER to stop.")
    input()

    # Stop recording
    recorder.stop_recording()
    duration = int(time.time() - start_time)

    # Save recording
    audio_path = recorder.save_recording()

    # Save to database
    meeting = db.add_meeting(
        title=title,
        duration=duration,
        audio_file_path=audio_path
    )

    print(f"\n✅ Recording saved!")
    print(f"   Meeting ID: {meeting.id}")
    print(f"   Duration: {duration} seconds")
    print(f"   File: {audio_path}")

    return meeting.id


def transcribe_meeting(db, meeting_id=None):
    """Transcribe a meeting."""
    print_header()
    print("📝 TRANSCRIBE MEETING")
    print("-" * 60)

    if meeting_id is None:
        meeting_id = int(input("Enter meeting ID to transcribe: "))

    meeting = db.get_meeting(meeting_id)
    if not meeting:
        print("❌ Meeting not found!")
        return

    if not meeting.audio_file_path:
        print("❌ No audio file found for this meeting!")
        return

    print(f"\nTranscribing: {meeting.title}")
    print("This may take a few minutes...\n")

    # Initialize transcriber
    transcriber = Transcriber(model_size='base')

    # Transcribe
    transcript_path, transcript_text = transcriber.transcribe_and_save(
        meeting.audio_file_path
    )

    # Update database
    db.update_meeting(meeting_id, transcript_path=transcript_path)

    print(f"\n✅ Transcription complete!")
    print(f"   File: {transcript_path}")
    print(f"\n📄 Transcript preview:")
    print("-" * 60)
    print(transcript_text[:500] + "..." if len(transcript_text) > 500 else transcript_text)


def summarize_meeting(db, meeting_id=None):
    """Summarize a meeting."""
    print_header()
    print("🤖 SUMMARIZE MEETING")
    print("-" * 60)

    if meeting_id is None:
        meeting_id = int(input("Enter meeting ID to summarize: "))

    meeting = db.get_meeting(meeting_id)
    if not meeting:
        print("❌ Meeting not found!")
        return

    if not meeting.transcript_path:
        print("❌ No transcript found! Please transcribe first.")
        return

    print(f"\nSummarizing: {meeting.title}")
    print("Generating AI summary...\n")

    # Read transcript
    with open(meeting.transcript_path, 'r', encoding='utf-8') as f:
        transcript = f.read()

    # Initialize summarizer
    try:
        summarizer = Summarizer()
    except ValueError as e:
        print(f"❌ Error: {e}")
        return

    # Generate summary
    import os
    base_name = os.path.splitext(os.path.basename(meeting.audio_file_path))[0]
    filename = f"{base_name}_summary.txt"

    summary_path, summary_text = summarizer.summarize_and_save(
        transcript,
        meeting_title=meeting.title,
        filename=filename
    )

    # Update database
    db.update_meeting(meeting_id, summary=summary_text)

    print(f"\n✅ Summary generated!")
    print(f"   File: {summary_path}")
    print(f"\n📋 Summary:")
    print("=" * 60)
    print(summary_text)
    print("=" * 60)


def list_meetings(db):
    """List all meetings."""
    print_header()
    print("📚 ALL MEETINGS")
    print("-" * 60)

    meetings = db.get_all_meetings()

    if not meetings:
        print("No meetings found.")
        return

    for meeting in meetings:
        status_icons = []
        if meeting.audio_file_path:
            status_icons.append("🎤")
        if meeting.transcript_path:
            status_icons.append("📄")
        if meeting.summary:
            status_icons.append("📝")

        status = " ".join(status_icons) if status_icons else "❌"

        print(f"\n{status} ID: {meeting.id} - {meeting.title}")
        print(f"   Date: {meeting.date.strftime('%Y-%m-%d %H:%M:%S')}")
        if meeting.duration:
            print(f"   Duration: {meeting.duration} seconds")


def complete_workflow(db):
    """Complete workflow: record, transcribe, and summarize."""
    print_header()
    print("🚀 COMPLETE WORKFLOW")
    print("-" * 60)

    # Step 1: Record
    meeting_id = record_meeting(db)

    # Step 2: Transcribe
    print("\n\nContinuing to transcription...")
    time.sleep(2)
    transcribe_meeting(db, meeting_id)

    # Step 3: Summarize
    print("\n\nContinuing to summarization...")
    time.sleep(2)
    summarize_meeting(db, meeting_id)

    print("\n\n✅ Complete workflow finished!")


def main_menu():
    """Display main menu and handle user input."""
    db = Database()

    while True:
        print_header()
        print("MAIN MENU")
        print("-" * 60)
        print("1. Record Meeting")
        print("2. Transcribe Meeting")
        print("3. Summarize Meeting")
        print("4. List All Meetings")
        print("5. Complete Workflow (Record → Transcribe → Summarize)")
        print("6. Exit")
        print("-" * 60)

        choice = input("\nEnter your choice (1-6): ").strip()

        try:
            if choice == '1':
                record_meeting(db)
            elif choice == '2':
                transcribe_meeting(db)
            elif choice == '3':
                summarize_meeting(db)
            elif choice == '4':
                list_meetings(db)
            elif choice == '5':
                complete_workflow(db)
            elif choice == '6':
                print("\nGoodbye!")
                db.close()
                sys.exit(0)
            else:
                print("\n❌ Invalid choice. Please try again.")

            input("\nPress ENTER to continue...")

        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            input("\nPress ENTER to continue...")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPress ENTER to continue...")


if __name__ == "__main__":
    main_menu()
