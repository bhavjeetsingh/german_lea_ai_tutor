"""Authentication routes for signup and login."""
from fastapi import APIRouter, HTTPException
from src.models.schemas import SignupRequest, LoginRequest, AuthResponse
from src.controllers.auth_controller import auth_controller

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """Register a new user account."""
    try:
        response = auth_controller.signup(request)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.message)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during signup: {str(e)}")


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Login with existing credentials."""
    try:
        response = auth_controller.login(request)
        if not response.success:
            raise HTTPException(status_code=401, detail=response.message)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")
