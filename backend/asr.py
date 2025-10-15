# asr.py - Speech-to-Text with AssemblyAI API
from pathlib import Path
import speech_recognition as sr
from .utils import OUTPUT_DIR
import os

# Try to import AssemblyAI
try:
    import assemblyai as aai
    ASSEMBLYAI_AVAILABLE = True
except ImportError:
    ASSEMBLYAI_AVAILABLE = False

def transcribe_with_assemblyai(file_path: str):
    """
    Transcribe using AssemblyAI API (FREE tier available with API key).
    
    Sign up for FREE at: https://www.assemblyai.com/
    Free tier includes: 5 hours/month of transcription
    """
    print(f"🎙️ Using AssemblyAI API (FREE tier)...")
    print(f"📁 Processing: {Path(file_path).name}")
    
    # Get API key from environment
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key or api_key == "your-assemblyai-api-key-here":
        raise RuntimeError(
            "AssemblyAI API key not configured!\n"
            "Please:\n"
            "1. Sign up for FREE at https://www.assemblyai.com/\n"
            "2. Get your API key from the dashboard\n"
            "3. Add it to backend/.env: ASSEMBLYAI_API_KEY=your-key-here"
        )
    
    try:
        # Configure AssemblyAI
        aai.settings.api_key = api_key
        
        # Create transcriber
        transcriber = aai.Transcriber()
        
        # Transcribe audio file
        print("⏳ Uploading and transcribing audio...")
        transcript = transcriber.transcribe(file_path)
        
        # Check status
        if transcript.status == aai.TranscriptStatus.error:
            raise RuntimeError(f"AssemblyAI transcription failed: {transcript.error}")
        
        transcript_text = transcript.text
        print(f"✅ AssemblyAI transcription complete! ({len(transcript_text)} characters)")
        
        return transcript_text
        
    except Exception as e:
        raise RuntimeError(f"AssemblyAI transcription failed: {e}")

def transcribe(file_path: str):
    """
    Transcribe audio with multiple backends:
    1. AssemblyAI API (if API key configured) - Best quality
    2. Google Speech Recognition (free, no key) - Good quality
    3. PocketSphinx (offline fallback) - Basic quality
    """
    # Try AssemblyAI first (if available and configured)
    if ASSEMBLYAI_AVAILABLE:
        api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if api_key and api_key != "your-assemblyai-api-key-here":
            try:
                transcript_text = transcribe_with_assemblyai(file_path)
                # Save transcript
                out_file = OUTPUT_DIR / (Path(file_path).stem + "_transcript.txt")
                out_file.write_text(transcript_text or "", encoding="utf-8")
                print(f"📄 Saved to: {out_file}")
                return transcript_text
            except Exception as e:
                print(f"⚠️ AssemblyAI failed: {e}")
                print("🔄 Falling back to Google Speech Recognition...")
    
    # Fallback to Google Speech Recognition + PocketSphinx
    print(f"🎙️ Using SpeechRecognition (FREE, no API key)...")
    print(f"📁 Processing: {Path(file_path).name}")
    
    recognizer = sr.Recognizer()
    
    # Handle MP3 files - convert to WAV first
    file_ext = Path(file_path).suffix.lower()
    if file_ext == '.mp3':
        print("🔄 Converting MP3 to WAV...")
        try:
            from pydub import AudioSegment
            # pydub can read MP3 without ffmpeg if you have it installed
            # But it's more reliable to just tell users to upload WAV files
            raise RuntimeError(
                "MP3 files require ffmpeg. Please upload WAV files instead.\n"
                "You can convert MP3 to WAV using online tools like: https://online-audio-converter.com/"
            )
        except ImportError:
            raise RuntimeError("Please upload WAV files instead of MP3.")
    
    # Transcribe audio file
    print("⏳ Transcribing audio...")
    try:
        with sr.AudioFile(file_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Record the audio
            audio_data = recognizer.record(source)
            
        # Try Google Speech Recognition first (requires internet)
        try:
            print("🌐 Trying Google Speech Recognition API (free tier)...")
            transcript_text = recognizer.recognize_google(audio_data, language='en-US')
            print("✅ Google API successful!")
            
        except sr.RequestError as e:
            # Google API failed (network issue, timeout, etc.)
            print(f"⚠️ Google API failed: {e}")
            print("🔄 Falling back to PocketSphinx (offline)...")
            
            try:
                # Use PocketSphinx (works offline, no internet needed!)
                transcript_text = recognizer.recognize_sphinx(audio_data)
                print("✅ PocketSphinx (offline) successful!")
                
            except sr.UnknownValueError:
                transcript_text = "[Could not understand audio - please ensure the audio has clear speech]"
                print("⚠️ PocketSphinx could not understand audio")
            except Exception as sphinx_error:
                print(f"⚠️ PocketSphinx also failed: {sphinx_error}")
                raise RuntimeError(
                    f"Both online and offline transcription failed.\n"
                    f"Google API: {e}\n"
                    f"PocketSphinx: {sphinx_error}\n"
                    f"Please check your internet connection or audio file quality."
                )
        
    except sr.UnknownValueError:
        transcript_text = "[Could not understand audio - please ensure the audio has clear speech]"
        print("⚠️ Could not understand audio")
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {e}")
    
    # Save transcript
    out_file = OUTPUT_DIR / (Path(file_path).stem + "_transcript.txt")
    out_file.write_text(transcript_text or "", encoding="utf-8")
    
    print(f"✅ Transcription complete! ({len(transcript_text)} characters)")
    print(f"📄 Saved to: {out_file}")
    
    return transcript_text
