"""Database module for storing meeting records."""
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Meeting(Base):
    """Meeting model for database."""

    __tablename__ = 'meetings'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer)  # Duration in seconds
    audio_file_path = Column(String(500))
    transcript_path = Column(String(500))
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Meeting(id={self.id}, title='{self.title}', date='{self.date}')>"


class Database:
    """Database manager for meetings."""

    def __init__(self, db_path='meetings.db'):
        """Initialize database connection."""
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_meeting(self, title, duration=None, audio_file_path=None,
                   transcript_path=None, summary=None):
        """Add a new meeting to the database."""
        meeting = Meeting(
            title=title,
            duration=duration,
            audio_file_path=audio_file_path,
            transcript_path=transcript_path,
            summary=summary
        )
        self.session.add(meeting)
        self.session.commit()
        return meeting

    def update_meeting(self, meeting_id, **kwargs):
        """Update a meeting record."""
        meeting = self.session.query(Meeting).filter_by(id=meeting_id).first()
        if meeting:
            for key, value in kwargs.items():
                if hasattr(meeting, key):
                    setattr(meeting, key, value)
            self.session.commit()
        return meeting

    def get_meeting(self, meeting_id):
        """Get a meeting by ID."""
        return self.session.query(Meeting).filter_by(id=meeting_id).first()

    def get_all_meetings(self):
        """Get all meetings."""
        return self.session.query(Meeting).order_by(Meeting.date.desc()).all()

    def delete_meeting(self, meeting_id):
        """Delete a meeting."""
        meeting = self.session.query(Meeting).filter_by(id=meeting_id).first()
        if meeting:
            # Delete associated files
            if meeting.audio_file_path and os.path.exists(meeting.audio_file_path):
                os.remove(meeting.audio_file_path)
            if meeting.transcript_path and os.path.exists(meeting.transcript_path):
                os.remove(meeting.transcript_path)

            self.session.delete(meeting)
            self.session.commit()
            return True
        return False

    def close(self):
        """Close database connection."""
        self.session.close()
