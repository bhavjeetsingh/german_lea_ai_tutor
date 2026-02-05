# GermanLeap Lea - Python Backend

FastAPI-based backend with AI integration for the GermanLeap Lea AI Tutor.

## Features

- 🚀 **FastAPI** - Modern, fast Python web framework
- 🤖 **AI Integration** - OpenAI GPT or Google Gemini
- 💾 **JSON Storage** - Simple file-based storage (easily upgradable)
- 🔒 **Type Safety** - Pydantic models for data validation
- 📝 **Auto Documentation** - Swagger UI at `/docs`

## Prerequisites

- Python 3.9 or higher
- pip or poetry
- OpenAI API key or Google Gemini API key

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
.\venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
copy .env.example .env

# Edit .env and add your API key
```

Example `.env`:
```
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
PORT=8000
```

### 4. Run the Server

```bash
# Development mode (auto-reload)
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── data/                  # JSON storage (auto-created)
│   ├── profiles/         # Student profiles
│   └── sessions/         # Chat sessions
└── src/
    ├── config/
    │   └── settings.py   # Configuration management
    ├── models/
    │   └── schemas.py    # Pydantic models
    ├── services/
    │   ├── ai_service.py       # AI integration
    │   └── storage_service.py  # Data persistence
    ├── controllers/
    │   ├── chat_controller.py    # Chat logic
    │   └── student_controller.py # Profile logic
    └── routes/
        ├── chat_routes.py    # Chat API endpoints
        └── student_routes.py # Student API endpoints
```

## API Endpoints

### Students

- `POST /api/students/profile` - Create student profile
- `GET /api/students/profile/{student_id}` - Get profile
- `PATCH /api/students/profile/{student_id}` - Update profile

### Chat

- `POST /api/chat/message` - Send message to Lea
- `GET /api/chat/session/{session_id}` - Get session history
- `GET /api/chat/student/{student_id}/sessions` - Get all student sessions

### System

- `GET /` - API info
- `GET /health` - Health check

## Example Usage

### Create a Student Profile

```bash
curl -X POST http://localhost:8000/api/students/profile \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alex",
    "email": "alex@example.com",
    "current_level": "A2",
    "goals": ["Pass Goethe B1 exam", "Move to Germany"],
    "target_exam": "Goethe B1",
    "career_interest": "Nursing"
  }'
```

### Send a Chat Message

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "your-student-id",
    "message": "Hallo Lea! Can you help me with German articles?",
    "teaching_mode": "grammar_practice"
  }'
```

## Teaching Modes

- `grammar_practice` - Structured grammar lessons
- `vocabulary_building` - Context-based vocab learning
- `speaking_practice` - Conversational practice
- `exam_preparation` - Goethe/Telc exam prep
- `interview_coaching` - Job interview scenarios
- `career_guidance` - Career advice for Germany

## Development

### Running Tests (TODO)

```bash
pytest
```

### Code Formatting

```bash
pip install black isort
black .
isort .
```

### Type Checking

```bash
pip install mypy
mypy src/
```

## Upgrading to Database

To upgrade from JSON to a database:

1. Install database driver (e.g., `pip install sqlalchemy asyncpg`)
2. Update `storage_service.py` to use SQLAlchemy
3. Create database models based on Pydantic schemas
4. No changes needed to controllers or routes!

## License

MIT
