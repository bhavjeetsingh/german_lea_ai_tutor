"""Authentication controller for handling signup and login."""
import uuid
from passlib.context import CryptContext
from src.models.schemas import SignupRequest, LoginRequest, StudentProfile, AuthResponse
from src.services.storage_service import storage_service


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthController:
    """Controller for authentication operations."""
    
    def hash_password(self, password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def signup(self, request: SignupRequest) -> AuthResponse:
        """Register a new user."""
        # Check if email already exists
        existing_profile = storage_service.get_profile_by_email(request.email)
        if existing_profile:
            return AuthResponse(
                success=False,
                message="An account with this email already exists. Please login instead.",
                profile=None
            )
        
        # Create new profile with hashed password
        profile = StudentProfile(
            student_id=str(uuid.uuid4()),
            name=request.name,
            email=request.email,
            password_hash=self.hash_password(request.password),
            current_level=request.current_level,
            goals=request.goals,
            target_exam=request.target_exam,
            career_interest=request.career_interest
        )
        
        storage_service.save_profile(profile)
        
        # Return profile without password_hash for security
        return AuthResponse(
            success=True,
            message="Account created successfully!",
            profile=profile
        )
    
    def login(self, request: LoginRequest) -> AuthResponse:
        """Authenticate a user."""
        # Find profile by email
        profile = storage_service.get_profile_by_email(request.email)
        
        if not profile:
            return AuthResponse(
                success=False,
                message="No account found with this email. Please sign up first.",
                profile=None
            )
        
        # Check if profile has a password (for backward compatibility)
        if not profile.password_hash:
            return AuthResponse(
                success=False,
                message="This account was created without a password. Please sign up again.",
                profile=None
            )
        
        # Verify password
        if not self.verify_password(request.password, profile.password_hash):
            return AuthResponse(
                success=False,
                message="Incorrect password. Please try again.",
                profile=None
            )
        
        return AuthResponse(
            success=True,
            message="Login successful!",
            profile=profile
        )


auth_controller = AuthController()
