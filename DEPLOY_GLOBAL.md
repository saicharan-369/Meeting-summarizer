# 🌍 Global Deployment Guide

## 🚀 Quick Deploy Options

Your meeting summarizer is ready to deploy! Choose one of these FREE options:

---

## Option 1: Render.com (Recommended ⭐)

### Why Render?
- ✅ 100% FREE tier (750 hours/month)
- ✅ Easiest setup
- ✅ Auto HTTPS
- ✅ Custom domains

### Steps to Deploy:

#### 1. Push to GitHub
```bash
cd "c:\Users\saich\Downloads\Meeting summarizer\meeting-summarizer"
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### 2. Deploy on Render
1. Go to https://render.com
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name**: meeting-summarizer
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
6. Click **"Create Web Service"**

#### 3. Get Your URL
- You'll get: `https://meeting-summarizer.onrender.com`
- Share this link with anyone!

---

## Option 2: Railway.app

### Why Railway?
- ✅ $5 free credit/month
- ✅ Fastest deployment
- ✅ Auto deploy on git push

### Steps to Deploy:

#### 1. Push to GitHub (if not done)
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### 2. Deploy on Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository
6. Railway auto-detects settings!

#### 3. Get Your URL
- You'll get: `https://meeting-summarizer.railway.app`

---

## Option 3: Split Deployment (Best Performance)

### Frontend on Vercel + Backend on Render

#### Frontend (Vercel)
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click **"Add New Project"**
4. Select your repo
5. Configure:
   - **Framework**: Other
   - **Root Directory**: `frontend/static`
6. Deploy!

#### Backend (Render)
- Follow Option 1 steps above
- Update frontend's `app.js` with backend URL

---

## 📝 Important Notes

### Update Backend URL in Frontend
After deployment, update `frontend/static/app.js`:

```javascript
// Change this line:
const API_BASE_URL = 'http://127.0.0.1:8000';

// To your deployed backend URL:
const API_BASE_URL = 'https://meeting-summarizer.onrender.com';
```

### Environment Variables
Add these on your hosting platform:
- No API keys needed! (Whisper runs locally)
- All config is in `.env` file

---

## 🎯 Recommended: Render.com

**Easiest and most reliable for your project!**

1. Create GitHub account (if needed)
2. Push code to GitHub
3. Deploy on Render
4. Get your URL
5. Share with the world! 🌍

---

## 🔧 Troubleshooting

### If deployment fails:
- Check Python version (3.11)
- Verify `requirements.txt` is complete
- Check logs on hosting platform

### If Whisper takes too long:
- Render free tier has limited resources
- Consider upgrading or using smaller audio files

---

## 📱 After Deployment

Your app will be accessible:
- From any device
- Anywhere in the world
- With HTTPS security
- No login required

**Ready to go global? Let me know which option you prefer!** 🚀
