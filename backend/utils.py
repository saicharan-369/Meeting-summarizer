# utils.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env before importing Google client
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

# Google Cloud setup (OPTIONAL - only needed if not using Whisper)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("⚠️ GOOGLE_API_KEY not found. Will use Whisper (local, free) instead.")

# Output path setup

# Output directory for transcripts and summaries
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./output"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
