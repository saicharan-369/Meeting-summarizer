# app.py
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
# Ensure .env is loaded before importing modules that read env vars
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / ".env")

from .utils import OUTPUT_DIR
# Import transcription and summarization functions
from .asr import transcribe
from .summarizer import generate_summary_and_actions

app = FastAPI(title="Meeting Summarizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use absolute path for uploads directory
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Accept audio file (wav, mp3). Returns transcript & summary.
    """
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="No file attached.")

    # Save uploaded file with absolute path
    save_path = UPLOAD_DIR / filename
    print(f"📁 Saving uploaded file to: {save_path.absolute()}")
    
    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    print(f"✅ File saved successfully: {save_path.exists()}")

    # 1. Transcribe
    try:
        absolute_path = str(save_path.absolute())
        print(f"🎙️ Transcribing: {absolute_path}")
        print(f"📂 File exists: {save_path.exists()}")
        print(f"📏 File size: {save_path.stat().st_size} bytes")
        
        transcript = transcribe(absolute_path)
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        import traceback
        traceback.print_exc()
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
