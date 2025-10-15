# audio_converter.py - Convert MP3/MP4 to WAV
from pathlib import Path
from pydub import AudioSegment
import os

def convert_to_wav(input_path: str) -> str:
    """
    Convert MP3, MP4, or other audio formats to WAV.
    Returns the path to the converted WAV file.
    If already WAV, returns the original path.
    """
    input_file = Path(input_path)
    file_extension = input_file.suffix.lower()
    
    # If already WAV, no conversion needed
    if file_extension == '.wav':
        print(f"✅ File is already WAV format: {input_file.name}")
        return input_path
    
    # Supported formats for conversion
    supported_formats = ['.mp3', '.mp4', '.m4a', '.ogg', '.flac', '.aac']
    
    if file_extension not in supported_formats:
        raise ValueError(f"Unsupported audio format: {file_extension}. Supported: {', '.join(supported_formats)}")
    
    # Create output WAV path
    output_path = input_file.with_suffix('.wav')
    
    print(f"🔄 Converting {file_extension.upper()} to WAV...")
    print(f"📁 Input: {input_file.name}")
    print(f"📁 Output: {output_path.name}")
    
    try:
        # Load audio file
        if file_extension == '.mp3':
            audio = AudioSegment.from_mp3(input_path)
        elif file_extension == '.mp4' or file_extension == '.m4a':
            audio = AudioSegment.from_file(input_path, format="mp4")
        elif file_extension == '.ogg':
            audio = AudioSegment.from_ogg(input_path)
        elif file_extension == '.flac':
            audio = AudioSegment.from_file(input_path, format="flac")
        elif file_extension == '.aac':
            audio = AudioSegment.from_file(input_path, format="aac")
        else:
            # Generic fallback
            audio = AudioSegment.from_file(input_path)
        
        # Export as WAV
        audio.export(output_path, format="wav")
        
        print(f"✅ Conversion successful!")
        print(f"📏 Original size: {input_file.stat().st_size / 1024:.2f} KB")
        print(f"📏 WAV size: {output_path.stat().st_size / 1024:.2f} KB")
        
        # Optionally delete original file to save space
        # os.remove(input_path)
        
        return str(output_path)
        
    except Exception as e:
        raise RuntimeError(f"Audio conversion failed: {e}")
