from fastapi import APIRouter, HTTPException
from src.models.schemas import CreateProfileRequest, StudentProfile
from src.controllers.student_controller import student_controller

router = APIRouter(prefix="/api/students", tags=["students"])


@router.post("/profile", response_model=StudentProfile, status_code=201)
async def create_profile(request: CreateProfileRequest):
    """Create a new student profile."""
    try:
        return student_controller.create_profile(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating profile: {str(e)}")


@router.get("/profile/{student_id}", response_model=StudentProfile)
async def get_profile(student_id: str):
    """Get a student profile by ID."""
    profile = student_controller.get_profile(student_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.patch("/profile/{student_id}", response_model=StudentProfile)
async def update_profile(student_id: str, updates: dict):
    """Update a student profile."""
    profile = student_controller.update_profile(student_id, updates)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
