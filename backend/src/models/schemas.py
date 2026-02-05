from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class StudentProfile(BaseModel):
    """Student profile information."""
    student_id: str
    name: str
    email: str
    password_hash: Optional[str] = None  # Hashed password for authentication
    current_level: Literal["A1", "A2", "B1", "B2"]
    goals: List[str] = Field(default_factory=list)
    target_exam: Optional[str] = None
    career_interest: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Message(BaseModel):
    """Chat message."""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatSession(BaseModel):
    """Chat session with Lea."""
    session_id: str
    student_id: str
    teaching_mode: Optional[Literal[
        "grammar_practice",
        "vocabulary_building",
        "speaking_practice",
        "exam_preparation",
        "interview_coaching",
        "career_guidance"
    ]] = None
    messages: List[Message] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Request to send a message to Lea."""
    student_id: str
    session_id: Optional[str] = None
    message: str
    teaching_mode: Optional[str] = None


class ChatResponse(BaseModel):
    """Response from Lea."""
    session_id: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CreateProfileRequest(BaseModel):
    """Request to create a student profile."""
    name: str
    email: str
    current_level: Literal["A1", "A2", "B1", "B2"]
    goals: List[str] = Field(default_factory=list)
    target_exam: Optional[str] = None
    career_interest: Optional[str] = None


class SignupRequest(BaseModel):
    """Request to sign up a new user."""
    name: str
    email: str
    password: str
    current_level: Literal["A1", "A2", "B1", "B2"]
    goals: List[str] = Field(default_factory=list)
    target_exam: Optional[str] = None
    career_interest: Optional[str] = None


class LoginRequest(BaseModel):
    """Request to login."""
    email: str
    password: str


class AuthResponse(BaseModel):
    """Response after successful authentication."""
    success: bool
    message: str
    profile: Optional[StudentProfile] = None