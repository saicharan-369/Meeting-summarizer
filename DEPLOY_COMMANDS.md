# 🚀 Quick Deploy Commands

## After creating GitHub repo, run these:

```bash
cd "c:\Users\saich\Downloads\Meeting summarizer\meeting-summarizer"

# Add remote (if not already added)
git remote add origin https://github.com/saicharan-369/meeting-summarizer.git

# Push to GitHub
git push -u origin main
```

## Then deploy on Render.com:

1. Go to: https://render.com/register
2. Sign up with GitHub
3. New Web Service → Connect repo
4. Configure:
   - Build: `pip install -r backend/requirements.txt`
   - Start: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
5. Deploy!

## Your URLs will be:
- Backend: `https://meeting-summarizer.onrender.com`
- Frontend: Deploy separately on Vercel or Render

---

## After backend deploys:

Update `frontend/static/app.js` line 2:
```javascript
const API_BASE_URL = 'https://meeting-summarizer.onrender.com';
```

Then push again and deploy frontend!

---

**Need help? Ask me at any step!** 🎯
