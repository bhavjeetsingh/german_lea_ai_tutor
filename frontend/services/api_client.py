"""API client for communicating with the GermanLeap backend."""
import requests
from typing import Optional, Dict, List, Any


class APIClient:
    """Client for the GermanLeap Lea AI Tutor API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Cannot connect to the backend server. "
                "Please ensure the backend is running on " + self.base_url
            )
        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out. Please try again.")
        except requests.exceptions.HTTPError as e:
            error_detail = "Unknown error"
            try:
                error_detail = e.response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            raise Exception(f"API Error: {error_detail}")
    
    # Health check
    def health_check(self) -> Dict[str, Any]:
        """Check if the API is healthy."""
        return self._make_request("GET", "/health")
    
    # Authentication endpoints
    def signup(
        self,
        name: str,
        email: str,
        password: str,
        current_level: str,
        goals: List[str] = None,
        target_exam: Optional[str] = None,
        career_interest: Optional[str] = None
    ) -> Dict[str, Any]:
        """Sign up a new user."""
        data = {
            "name": name,
            "email": email,
            "password": password,
            "current_level": current_level,
            "goals": goals or [],
            "target_exam": target_exam,
            "career_interest": career_interest
        }
        return self._make_request("POST", "/api/auth/signup", data=data)
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login with existing credentials."""
        data = {
            "email": email,
            "password": password
        }
        return self._make_request("POST", "/api/auth/login", data=data)
    
    # Student Profile endpoints
    def create_profile(
        self,
        name: str,
        email: str,
        current_level: str,
        goals: List[str] = None,
        target_exam: Optional[str] = None,
        career_interest: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new student profile."""
        data = {
            "name": name,
            "email": email,
            "current_level": current_level,
            "goals": goals or [],
            "target_exam": target_exam,
            "career_interest": career_interest
        }
        return self._make_request("POST", "/api/students/profile", data=data)
    
    def get_profile(self, student_id: str) -> Dict[str, Any]:
        """Get a student profile by ID."""
        return self._make_request("GET", f"/api/students/profile/{student_id}")
    
    def update_profile(self, student_id: str, updates: Dict) -> Dict[str, Any]:
        """Update a student profile."""
        return self._make_request("PATCH", f"/api/students/profile/{student_id}", data=updates)
    
    # Chat endpoints
    def send_message(
        self,
        student_id: str,
        message: str,
        session_id: Optional[str] = None,
        teaching_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send a message to Lea and get a response."""
        data = {
            "student_id": student_id,
            "message": message,
            "session_id": session_id,
            "teaching_mode": teaching_mode
        }
        return self._make_request("POST", "/api/chat/message", data=data)
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get chat session by ID."""
        return self._make_request("GET", f"/api/chat/session/{session_id}")
    
    def get_student_sessions(self, student_id: str) -> Dict[str, Any]:
        """Get all chat sessions for a student."""
        return self._make_request("GET", f"/api/chat/student/{student_id}/sessions")


# Singleton instance
api_client = APIClient()
