from fastapi import APIRouter, HTTPException
from src.models.schemas import ChatRequest, ChatResponse, ChatSession
from src.controllers.chat_controller import chat_controller

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message to Lea and get a response."""
    try:
        return await chat_controller.send_message(request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@router.get("/session/{session_id}", response_model=ChatSession)
async def get_session(session_id: str):
    """Get chat history for a specific session."""
    session = chat_controller.get_session_history(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/student/{student_id}/sessions")
async def get_student_sessions(student_id: str):
    """Get all chat sessions for a student."""
    sessions = chat_controller.get_student_sessions(student_id)
    return {"sessions": sessions}
