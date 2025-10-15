# 🎓 FOR COMPANY REVIEWERS

## ✅ This Project Works WITHOUT API Keys!

### 🎯 Quick Start (No Setup Required):

1. **Clone the repository:**
   ```bash
   git clone https://github.com/saicharan-369/Meeting-summarizer.git
   cd Meeting-summarizer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Run the backend:**
   ```bash
   uvicorn backend.app:app --reload
   ```

4. **Open frontend:**
   ```
   Open frontend/static/index.html in your browser
   ```

5. **Upload audio and test!** ✨

---

## 🆓 Transcription Backends (Automatic Fallback)

The project intelligently falls back through multiple options:

### 1️⃣ **AssemblyAI** (Optional - If API key provided)
- Free tier: 5 hours/month
- Best quality and speed
- Not required for testing!

### 2️⃣ **Whisper AI** (100% FREE - No API Key!)
- ✅ **Recommended for company review**
- ✅ No limits, no API keys
- ✅ Works completely offline
- ✅ Excellent quality (OpenAI model)
- ✅ Automatically downloads model on first use (~150MB)

### 3️⃣ **Google Speech Recognition** (FREE Fallback)
- Free, no API key needed
- Good quality
- Requires internet

### 4️⃣ **PocketSphinx** (Offline Backup)
- Works offline
- Basic quality
- No dependencies

---

## 🚀 For Reviewers: Best Testing Method

**The project will automatically use Whisper AI if no AssemblyAI key is provided!**

Just:
1. Install requirements
2. Run the server
3. Upload a WAV file
4. See instant transcription + AI summary!

**No API keys, no setup, no limits!** 🎉

---

## 📝 Technical Details

- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Backend**: FastAPI (Python)
- **Transcription**: Multi-backend with automatic fallback
- **Summarization**: Local TF-IDF (no external APIs)
- **Storage**: LocalStorage (no database needed)

---

## 🎯 Key Features

✅ Speech-to-text transcription
✅ AI-powered summarization  
✅ Action item extraction
✅ Beautiful purple gradient UI
✅ No login required
✅ 100% free to use
✅ Works offline (with Whisper)

---

## 💡 Notes

- First transcription with Whisper downloads model (~150MB)
- Subsequent transcriptions are fast
- Supports WAV audio files
- All processing happens locally (privacy-friendly)

---

**Built by**: AYITHA VENKATA SAI CHARAN
**Internship**: Unthinkable Solutions — Super Dream Internship
