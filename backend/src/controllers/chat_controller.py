import uuid
from datetime import datetime
from typing import Optional
from src.models.schemas import ChatRequest, ChatResponse, ChatSession, Message
from src.services.storage_service import storage_service
from src.services.ai_service import ai_service


class ChatController:
    """Controller for chat-related operations."""
    
    async def send_message(self, request: ChatRequest) -> ChatResponse:
        """Process a chat message and get AI response."""
        
        # Get student profile
        profile = storage_service.get_profile(request.student_id)
        if not profile:
            raise ValueError(f"Student profile not found: {request.student_id}")
        
        # Get or create session
        if request.session_id:
            session = storage_service.get_session(request.session_id)
            if not session:
                raise ValueError(f"Session not found: {request.session_id}")
        else:
            session = ChatSession(
                session_id=str(uuid.uuid4()),
                student_id=request.student_id,
                teaching_mode=request.teaching_mode
            )
        
        # Add user message to session
        user_message = Message(role="user", content=request.message)
        session.messages.append(user_message)
        
        # Get AI response
        ai_response_content = await ai_service.get_response(
            profile=profile,
            messages=session.messages,
            teaching_mode=request.teaching_mode or session.teaching_mode
        )
        
        # Add AI response to session
        ai_message = Message(role="assistant", content=ai_response_content)
        session.messages.append(ai_message)
        
        # Update teaching mode if specified
        if request.teaching_mode:
            session.teaching_mode = request.teaching_mode
        
        # Save session
        storage_service.save_session(session)
        
        return ChatResponse(
            session_id=session.session_id,
            message=ai_response_content,
            timestamp=ai_message.timestamp
        )
    
    def get_session_history(self, session_id: str) -> Optional[ChatSession]:
        """Get chat history for a session."""
        return storage_service.get_session(session_id)
    
    def get_student_sessions(self, student_id: str):
        """Get all sessions for a student."""
        return storage_service.get_student_sessions(student_id)


chat_controller = ChatController()
