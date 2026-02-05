import json
import os
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from src.models.schemas import StudentProfile, ChatSession, Message
from src.config.settings import settings


class StorageService:
    """Service for storing and retrieving data from JSON files."""
    
    def __init__(self):
        self.data_dir = Path(settings.data_dir)
        self.profiles_dir = self.data_dir / "profiles"
        self.sessions_dir = self.data_dir / "sessions"
        
        # Create directories if they don't exist
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
    
    def _json_serializer(self, obj):
        """Custom JSON serializer for datetime objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    def save_profile(self, profile: StudentProfile) -> None:
        """Save student profile to JSON file."""
        profile_path = self.profiles_dir / f"{profile.student_id}.json"
        profile.updated_at = datetime.utcnow()
        
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile.model_dump(), f, indent=2, default=self._json_serializer)
    
    def get_profile(self, student_id: str) -> Optional[StudentProfile]:
        """Retrieve student profile from JSON file."""
        profile_path = self.profiles_dir / f"{student_id}.json"
        
        if not profile_path.exists():
            return None
        
        with open(profile_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return StudentProfile(**data)
    
    def get_profile_by_email(self, email: str) -> Optional[StudentProfile]:
        """Retrieve student profile by email address."""
        for profile_file in self.profiles_dir.glob("*.json"):
            with open(profile_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('email', '').lower() == email.lower():
                    return StudentProfile(**data)
        return None
    
    def save_session(self, session: ChatSession) -> None:
        """Save chat session to JSON file."""
        session_path = self.sessions_dir / f"{session.session_id}.json"
        session.updated_at = datetime.utcnow()
        
        with open(session_path, 'w', encoding='utf-8') as f:
            json.dump(session.model_dump(), f, indent=2, default=self._json_serializer)
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Retrieve chat session from JSON file."""
        session_path = self.sessions_dir / f"{session_id}.json"
        
        if not session_path.exists():
            return None
        
        with open(session_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return ChatSession(**data)
    
    def get_student_sessions(self, student_id: str) -> List[ChatSession]:
        """Get all sessions for a student."""
        sessions = []
        
        for session_file in self.sessions_dir.glob("*.json"):
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('student_id') == student_id:
                    sessions.append(ChatSession(**data))
        
        return sorted(sessions, key=lambda s: s.created_at, reverse=True)


storage_service = StorageService()