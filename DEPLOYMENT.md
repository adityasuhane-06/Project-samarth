# Deployment Guide - Project Samarth

This guide covers deploying the Project Samarth application with a split architecture:
- **Frontend (React + Vite)** → Vercel
- **Backend (FastAPI + MongoDB)** → Render/Railway

---

## 🎯 Architecture Overview

```
┌─────────────────┐      HTTPS       ┌──────────────────┐
│                 │  ───────────────► │                  │
│  Vercel         │                   │  Render/Railway  │
│  (Frontend)     │  ◄─────────────── │  (Backend API)   │
│                 │      API Calls    │                  │
└─────────────────┘                   └──────────────────┘
                                              │
                                              │ Connection
                                              ▼
                                      ┌──────────────────┐
                                      │  MongoDB Atlas   │
                                      │  (Database)      │
                                      └──────────────────┘
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
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `master`
   - **Root Directory**: `src`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

### 1.3 Add Environment Variables
Add these in Render dashboard:
```
GEMINI_API_KEY=your_gemini_key
GEMINI_API_KEY_2=your_gemini_key_2
MONGODB_URI=your_mongodb_connection_string
DATA_GOV_API_KEY=your_data_gov_key
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
In `src/app.py`, update the CORS origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://project-samarth.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app"  # Allow all Vercel preview deployments
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
   - **Start Command**: `python app.py`
5. Add same environment variables as Render
6. Railway provides URL like: `https://project-samarth-production.up.railway.app`

---

## 📝 Quick Command Reference

### Push to GitHub (if needed)
```bash
git add .
git commit -m "feat: Add deployment configurations for Vercel and Render"
git push origin master
```

### Deploy Frontend via CLI
```bash
cd frontend
vercel --prod
```

### Check Backend Health
```bash
curl https://project-samarth-backend.onrender.com/api/health
```

---

## ⚠️ Important Notes

### Free Tier Limitations
- **Render Free**: Backend sleeps after 15 min inactivity (first request takes 30-60s to wake)
- **Vercel Free**: 100GB bandwidth/month, unlimited deployments
- **MongoDB Atlas Free**: 512MB storage

### Environment Variables
- ✅ Already configured in `.env.example`
- ⚠️ Never commit `.env` files to Git
- ✅ Set them in hosting dashboards

### API Keys Security
- All API keys should be set as environment variables
- Frontend only needs `VITE_API_URL`
- Backend needs all API keys (Gemini, MongoDB, Data.gov)

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
- Verify CORS settings in backend
- Check backend is running (visit `/api/health`)

### Backend deployment fails
- Check `requirements.txt` has all dependencies
- Verify Python version (3.10+)
- Check build logs in Render dashboard

### MongoDB connection fails
- Verify MongoDB Atlas allows connections from anywhere (0.0.0.0/0)
- Check `MONGODB_URI` environment variable
- Ensure database user has read/write permissions

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
