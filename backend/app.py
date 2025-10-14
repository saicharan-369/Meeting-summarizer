# app.py
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from .utils import OUTPUT_DIR
from .asr import transcribe_with_openai_whisper
from .summarizer import generate_summary_and_actions
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

app = FastAPI(title="Meeting Summarizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Accept audio file (wav, mp3). Returns transcript & summary.
    """
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="No file attached.")

    # Save uploaded file
    save_path = UPLOAD_DIR / filename
    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1. Transcribe
    try:
        transcript = transcribe_with_openai_whisper(str(save_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ASR failed: {e}")

    # 2. Summarize via LLM
    try:
        summary = generate_summary_and_actions(transcript)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {e}")

    response = {
        "filename": filename,
        "transcript": transcript,
        "summary": summary,
        "transcript_path": str((OUTPUT_DIR / (save_path.stem + "_transcript.txt")).absolute()),
    }
    return JSONResponse(response)

@app.get("/health")
def health():
    return {"status": "ok"}
