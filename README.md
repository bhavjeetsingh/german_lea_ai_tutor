# GermanLeap - Lea AI Tutor

India's premium, AI-first German language tutor helping students learn German (A1–B2), prepare for Goethe/Telc exams, and build confidence for careers in Germany.[page:1]

## Features

- 🎓 **German Language Learning** (A1–B2 levels)[page:1]
- 📝 **Exam Preparation** (Goethe/Telc style tasks and practice)[page:1]
- 💼 **Interview Coaching** (Germany-specific questions and scenarios)[page:1]
- 🌍 **Career Guidance** (Ausbildung, nursing, and other skilled jobs in Germany)[page:1]
- 📊 **Progress Tracking** (student profile and conversational history)[page:1]
- 🤖 **AI-Powered Tutoring** (calm, structured, human-like mentor persona)[page:1]

## Tech Stack

- **Frontend**: Python + Streamlit[page:1]
- **Backend**: Python + FastAPI[page:1]
- **AI**: OpenAI GPT / Google Gemini API[page:1]
- **Storage**: JSON file storage for profiles and history (upgradable to MongoDB/PostgreSQL)[page:1]

## Project Structure

```bash
german_lea_ai_tutor/
├── backend/
│   ├── src/
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── models/
│   │   └── routes/
│   ├── data/
│   └── tests/
├── data/
│   └── profiles/
├── frontend/
│   ├── app.py          # Streamlit entry point
│   ├── pages/
│   ├── components/
│   └── services/
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
└── README.md

python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
cd backend
pip install -r requirements.txt
# or, from repo root if using pyproject:
# pip install .

cp .env.example .env

AI_PROVIDER=gemini
GEMINI_API_KEY=your_key_here

# OR, for OpenAI:
# AI_PROVIDER=openai
# OPENAI_API_KEY=your_key_here

PORT=8000

cd frontend
pip install -r requirements.txt

streamlit run app.py
