import uuid
from typing import Optional
from src.models.schemas import CreateProfileRequest, StudentProfile
from src.services.storage_service import storage_service


class StudentController:
    """Controller for student profile operations."""
    
    def create_profile(self, request: CreateProfileRequest) -> StudentProfile:
        """Create a new student profile."""
        
        profile = StudentProfile(
            student_id=str(uuid.uuid4()),
            name=request.name,
            email=request.email,
            current_level=request.current_level,
            goals=request.goals,
            target_exam=request.target_exam,
            career_interest=request.career_interest
        )
        
        storage_service.save_profile(profile)
        return profile
    
    def get_profile(self, student_id: str) -> Optional[StudentProfile]:
        """Get a student profile by ID."""
        return storage_service.get_profile(student_id)
    
    def update_profile(self, student_id: str, updates: dict) -> Optional[StudentProfile]:
        """Update a student profile."""
        
        profile = storage_service.get_profile(student_id)
        if not profile:
            return None
        
        # Update fields
        for key, value in updates.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)
        
        storage_service.save_profile(profile)
        return profile


student_controller = StudentController()
