# GermanLeap - Lea AI Tutor

India's premium, AI-first German language tutor helping students learn German (A1-B2), prepare for Goethe/Telc exams, and build confidence for careers in Germany.

## Features

- 🎓 **German Language Learning** (A1-B2 levels)
- 📝 **Exam Preparation** (Goethe/Telc style)
- 💼 **Interview Coaching** (Germany-specific)
- 🌍 **Career Guidance** (Ausbildung, Nursing, Skilled Jobs)
- 📊 **Progress Tracking** (Student profile & history)
- 🤖 **AI-Powered Tutoring** (Calm, structured, human-like mentor)

## Tech Stack

- **Frontend**: Python + Streamlit
- **Backend**: Python + FastAPI
- **AI**: OpenAI GPT / Google Gemini API
- **Database**: JSON file storage (easily upgradable to MongoDB/PostgreSQL)

## Project Structure

```
german_lea_ai_tutor/
├── backend/
│   ├── src/
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── models/
│   │   └── routes/
│   ├── data/
│   └── server.js
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   └── index.html
└── README.md
```

## Setup Instructions

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- OpenAI API key or Google Gemini API key

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
npm install
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Add your API key to `.env`:
```
AI_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
# OR for OpenAI
# AI_PROVIDER=openai
# OPENAI_API_KEY=your_key_here
PORT=8000
```

4. Start the backend:
```bash
npm run dev
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

2. Start the frontend:
```bash
streamlit run app.py
```

3. Open browser at `http://localhost:8501`

## Usage

1. Create a student profile with your German level and goals
2. Start chatting with Lea for personalized learning
3. Practice grammar, vocabulary, speaking, or prepare for exams
4. Track your progress over time

## Teaching Modes

- **Grammar Practice**: Structured lessons with examples
- **Vocabulary Building**: Context-based learning
- **Speaking Practice**: Realistic conversations (text-based)
- **Exam Preparation**: Goethe/Telc style questions
- **Interview Coaching**: Germany job interview scenarios
- **Career Guidance**: Safe, realistic advice for Germany pathways

## License

MIT

## Contact

For questions or support, contact GermanLeap team.
