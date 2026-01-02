# Deployment Guide - Project Samarth
**Last Updated**: January 2, 2026  
**Version**: 3.0  
**Architecture**: LangGraph + RAG + Two-Model Fallback

This guide covers deploying the Project Samarth application with a split architecture:
- **Frontend (React 18 + Vite 5 + Tailwind CSS)** → Vercel
- **Backend (FastAPI + LangGraph + MongoDB)** → Render/Railway
- **Vector DB (ChromaDB)** → Cloud or Local
- **Database (MongoDB Atlas)** → Cloud

---

## 🎯 Architecture Overview

```
┌─────────────────┐      HTTPS       ┌──────────────────┐
│                 │  ───────────────► │                  │
│  Vercel         │                   │  Render/Railway  │
│  (Frontend)     │  ◄─────────────── │  (Backend API)   │
│  React 18       │      API Calls    │  FastAPI         │
│  Vite 5         │                   │  LangGraph Agent │
└─────────────────┘                   └──────────────────┘
                                              │
                                    ┌─────────┼─────────┐
                                    ▼         ▼         ▼
                          ┌──────────────┐ ┌──────────┐ ┌──────────┐
                          │  MongoDB     │ │ ChromaDB │ │ Google   │
                          │  Atlas       │ │ (RAG)    │ │ APIs     │
                          │  (Cache)     │ │          │ │          │
                          └──────────────┘ └──────────┘ └──────────┘
```

---

## 📦 Step 1: Deploy Backend to Render

### 1.1 Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub

### 1.2 Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `project-samarth-backend`
   - **Environment**: `Python 3.11`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `src`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app_modular.py`

### 1.3 Add Environment Variables
Add these in Render dashboard:
```
# Gemini AI Keys (3 keys for optimal rate limiting)
SECRET_KEY=your_gemini_key_1
API_GUESSING_MODELKEY=your_gemini_key_2
AGENT_API_KEY=your_gemini_key_3

# MongoDB Atlas
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/

# ChromaDB (optional - local works too)
CHROMA_API_KEY=your_chroma_api_key
CHROMA_TENANT=your_tenant_id
CHROMA_DATABASE=Project Samarth

# Data.gov.in API
DATA_GOV_API_KEY=your_data_gov_key
USE_REAL_API=true

# Google Custom Search (optional for web search tool)
GOOGLE_SEARCH_API_KEY=your_google_api_key
GOOGLE_SEARCH_CX=your_search_engine_id

# Server Config
ENVIRONMENT=production
PORT=8000
```

### 1.4 Get Backend URL
After deployment, Render gives you a URL like:
```
https://project-samarth-backend.onrender.com
```
**Save this URL** - you'll need it for frontend!

---

## 🎨 Step 2: Deploy Frontend to Vercel

### 2.1 Install Vercel CLI (Optional)
```bash
npm install -g vercel
```

### 2.2 Deploy via Vercel Dashboard (Recommended)

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### 2.3 Add Environment Variables
In Vercel project settings → Environment Variables:
```
VITE_API_URL=https://project-samarth-backend.onrender.com
VITE_ENV=production
```

### 2.4 Deploy
Click "Deploy" - Vercel will build and deploy your frontend.

Your frontend will be live at:
```
https://project-samarth.vercel.app
```

---

## 🔧 Step 3: Update CORS Configuration

### 3.1 Update Backend CORS
In `src/app_modular.py`, update the CORS origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",                    # Vite dev server
        "https://project-samarth.vercel.app",       # Production frontend
        "https://*.vercel.app"                      # Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push - Render will auto-redeploy.

---

## ✅ Step 4: Test Production Deployment

1. Visit your Vercel URL: `https://project-samarth.vercel.app`
2. Check server status (should show green)
3. Try a sample question
4. Verify data loads correctly

---

## 🚀 Alternative: Deploy Backend to Railway

### Railway Setup
1. Go to [railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Configure:
   - **Root Directory**: `src`
   - **Start Command**: `python app_modular.py`
5. Add same environment variables as Render (all 3 Gemini keys, MongoDB, ChromaDB, etc.)
6. Railway provides URL like: `https://project-samarth-production.up.railway.app`

---

## 📝 Quick Command Reference

### Push to GitHub (if needed)
```bash
git add .
git commit -m "feat: Deploy v3.0 with LangGraph + RAG"
git push origin main
```

### Deploy Frontend via CLI
```bash
cd frontend
vercel --prod
```

### Check Backend Health
```bash
curl https://project-samarth-gxou.onrender.com/api/health
```

### Test LangGraph Agent
```bash
curl -X POST https://project-samarth-gxou.onrender.com/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are rabi crops?"}'
```

---

## ⚠️ Important Notes

### Free Tier Limitations
- **Render Free**: Backend sleeps after 15 min inactivity (first request takes 30-60s to wake)
- **Vercel Free**: 100GB bandwidth/month, unlimited deployments
- **MongoDB Atlas Free**: 512MB storage (sufficient for caching)
- **ChromaDB**: Can use local (free) or cloud (free tier available)
- **Google Custom Search**: 100 queries/day free

### Environment Variables
- ✅ Already configured in `.env.example`
- ⚠️ Never commit `.env` files to Git
- ✅ Set them in hosting dashboards
- 🔑 Need 3 Gemini API keys for optimal rate limiting

### API Keys Security
- All API keys should be set as environment variables
- Frontend only needs `VITE_API_URL`
- Backend needs:
  - 3 Gemini API keys (agent + fallback)
  - MongoDB connection string
  - ChromaDB credentials (optional)
  - Data.gov.in API key
  - Google Custom Search API + CX (optional)

---

## 🔄 Continuous Deployment

Both Vercel and Render support auto-deployment:
- **Push to master** → Automatic deployment
- **Pull requests** → Preview deployments
- **Rollback** → Easy rollback to previous versions

---

## 🐛 Troubleshooting

### Frontend can't connect to backend
- Check `VITE_API_URL` in Vercel env vars
- Verify CORS settings in backend (app_modular.py)
- Check backend is running (visit `/api/health`)
- Ensure URL doesn't have trailing slash

### Backend deployment fails
- Check `requirements.txt` has all dependencies
- Verify Python version (3.11+ recommended)
- Check build logs in Render dashboard
- Ensure `app_modular.py` is the entry point

### LangGraph agent not working
- Verify AGENT_API_KEY is set
- Check Render logs for error messages
- Ensure Gemini API has sufficient quota
- Test with fallback: agent falls back to two-model automatically

### MongoDB connection fails
- Verify MongoDB Atlas allows connections from anywhere (0.0.0.0/0)
- Check `DATABASE_URL` environment variable format
- Ensure database user has read/write permissions
- Test connection with `mongosh` command

### ChromaDB connection fails
- Check if CHROMA_API_KEY and CHROMA_TENANT are set
- Verify ChromaDB cloud account is active
- System works without ChromaDB (RAG disabled gracefully)
- Can use local ChromaDB instead of cloud

---

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Render Documentation](https://render.com/docs)
- [MongoDB Atlas Setup](https://www.mongodb.com/docs/atlas/)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)

---

**🎉 Deployment Complete!**

Your application is now live with:
- ⚡ Fast global CDN (Vercel)
- 🔒 HTTPS by default
- 🔄 Automatic deployments on push
- 📊 Performance analytics
- 🌍 Production-ready infrastructure
- 🤖 LangGraph agentic workflow
- 📚 RAG knowledge base
- 💾 MongoDB caching (30-40x faster)
- 🔄 Graceful fallback to two-model

**Production URLs:**
- Frontend: https://project-samarth-frontend.vercel.app
- Backend: https://project-samarth-gxou.onrender.com
- API Docs: https://project-samarth-gxou.onrender.com/docs

**Last Updated**: January 2, 2026  
**Version**: 3.0  
**Status**: Production Ready
