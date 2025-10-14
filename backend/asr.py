# asr.py
from openai import OpenAI
from pathlib import Path
from .utils import OPENAI_API_KEY, OUTPUT_DIR

# Create a client using the modern OpenAI SDK
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else OpenAI()


def transcribe_with_openai_whisper(file_path: str, model: str = "whisper-1"):
    """
    Sends audio file to OpenAI Whisper for transcription using the modern OpenAI client.
    Returns the transcript text.
    """
    with open(file_path, "rb") as audio_file:
        # New client surface: client.audio.transcriptions.create(...)
        resp = client.audio.transcriptions.create(model=model, file=audio_file)

    # response exposes the text as attribute
    transcript_text = getattr(resp, "text", None)
    if transcript_text is None:
        # Try dict-like access as a fallback
        transcript_text = resp.get("text") if isinstance(resp, dict) else ""

    # Save transcript
    out_file = OUTPUT_DIR / (Path(file_path).stem + "_transcript.txt")
    out_file.write_text(transcript_text or "", encoding="utf-8")
    return transcript_text or ""
