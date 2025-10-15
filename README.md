# Meeting Summarizer — Assignment 4

Author: AYITHA VENKATA SAI CHARAN

## Objective

Transcribe meeting audio and produce action-oriented summaries. This project demonstrates ASR integration, an LLM-based summarizer, and a clean web UI for audio uploads and review.

## Scope of Work

- Input: Meeting audio files (wav, mp3, m4a, flac)
- Output: Transcript text, concise summary, major decisions, and action items
- Frontend: Static HTML/CSS/JS (suitable for GitHub Pages) to upload audio and view results

## Technical Stack

- Backend: FastAPI (Python)
- ASR: OpenAI Whisper (via OpenAI API) — replaceable with other providers (Google/Azure)
- LLM: OpenAI Chat completions
- Frontend: Static site (frontend/static) — suitable for GitHub Pages
- Containerization: Docker + docker-compose (included)

## Setup

1. Create a virtual environment and activate it.

Windows (PowerShell):

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r backend/requirements.txt
```

3. Set up Google Cloud:

a. Create a Google Cloud project and enable Speech-to-Text API
b. Create a service account and download the JSON key
c. Copy the JSON key to `backend/google-credentials.json`
d. Copy and set up environment:

```powershell
Copy-Item backend\.env.example backend\.env
# The .env will point to google-credentials.json by default
```

4. Run backend (from project root):

```powershell
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

5. (Optional) Run frontend locally (static):

```powershell
# Serve the static frontend (requires Python 3)
python -m http.server 8501 -d frontend/static
# Then open http://localhost:8501 in your browser
```

6. Or run with Docker Compose (local):

```powershell
docker-compose up --build -d
```

## Usage

- Health check: http://127.0.0.1:8000/health
- Upload audio via Streamlit UI (http://localhost:8501) or POST to /upload-audio

## LLM Prompt Guidance

Use a focused prompt to extract decisions and tasks. Example:

```
Summarize this meeting transcript into:
1) A concise meeting summary (3-5 sentences).
2) Major decisions (bullet list).
3) Action items as: [Action] — [Owner] — [Due date if mentioned or assign TBD].
4) Any open questions.

Transcript:
{transcript}
```

## Deliverables for the assignment

- GitHub repo (this repository)
- README (this file) explaining setup, usage and prompt
- Demo video (script provided in VIDEO_SCRIPT.md)
- Deployed demo URL (recommended: backend on Render, frontend on GitHub Pages)

## Evaluation focus

- Transcription accuracy (ASR)
- Summary quality and prompt effectiveness
- Clear code structure and reproducibility
- UX for uploading and viewing results

## Notes

- The project uses environment variables for API keys. Do not commit secrets.
- If the OpenAI client version differs, `backend/asr.py` and `backend/summarizer.py` include defensive code to handle the modern OpenAI SDK.

## Contact

Owner: AYITHA VENKATA SAI CHARAN
Email: (add your contact email here)

