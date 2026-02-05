# GermanLeap Frontend (Python/Streamlit)

A Python-based frontend for the GermanLeap Lea AI Tutor using Streamlit.

## Features

- 🎨 Clean, modern UI with German-themed styling
- 👤 Student profile creation and management
- 💬 Interactive chat interface with Lea
- 📚 Multiple teaching modes (Grammar, Vocabulary, Speaking, Exam Prep, etc.)
- 🔄 Session management and chat history

## Prerequisites

- Python 3.9 or higher
- Backend server running on `http://localhost:8000`

## Setup

1. **Create a virtual environment (recommended):**
   ```bash
   cd frontend
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Make sure the backend is running:**
   ```bash
   cd ../backend
   python main.py
   ```

4. **Run the frontend:**
   ```bash
   cd frontend
   streamlit run app.py
   ```

5. **Open in browser:**
   Navigate to `http://localhost:8501`

## Project Structure

```
frontend/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── services/
    ├── __init__.py
    └── api_client.py   # Backend API client
```

## Configuration

The frontend connects to the backend at `http://localhost:8000` by default. To change this, modify the `base_url` in `services/api_client.py`.

## Teaching Modes

- **Free Chat**: Open conversation with Lea
- **Grammar Practice**: Structured grammar lessons and exercises
- **Vocabulary Building**: Learn new words in context
- **Speaking Practice**: Conversation practice (text-based)
- **Exam Preparation**: Goethe/Telc style questions
- **Interview Coaching**: German job interview practice
- **Career Guidance**: Advice for Germany career pathways

## Troubleshooting

### Cannot connect to backend
- Ensure the backend is running: `cd backend && python main.py`
- Check that port 8000 is not blocked
- Verify CORS settings allow `http://localhost:8501`

### Streamlit not found
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt`
