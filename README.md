# Meeting Summarizer

## Overview
Transcribes meeting audio then generates a short summary, decisions, and action items using OpenAI Whisper + Chat.

## Setup
1. Create a virtual environment and activate it.

Windows (PowerShell):

python -m venv .venv
.venv\Scripts\Activate.ps1

2. Install dependencies:

pip install -r backend/requirements.txt

3. Copy and fill environment:

cp backend/.env.example backend/.env
# open backend/.env and add your OPENAI_API_KEY

4. Run backend (from project root or inside backend/):

uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000

5. (Optional) Run frontend:

streamlit run frontend/streamlit_app.py

## Usage
- Health check: http://127.0.0.1:8000/health
- Upload audio via Streamlit UI or POST to /upload-audio

