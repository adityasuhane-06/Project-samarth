# Render Deployment Guide - Project Samarth Backend

## 🚀 Deploy Backend to Render

Render is a cloud platform that makes it easy to deploy full FastAPI applications without the size limitations of serverless platforms.

---

## 📦 Prerequisites

- GitHub account with your project pushed
- Render account (free tier available at [render.com](https://render.com))
- Your API keys ready (Gemini, MongoDB, Data.gov.in)

---

## 🔧 Step-by-Step Deployment

### Step 1: Push Your Code to GitHub

```powershell
git add .
git commit -m "feat: configure for Render deployment"
git push origin main
```

### Step 2: Create New Web Service on Render

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account (if not already connected)
4. Select your repository: **`adityasuhane-06/Project-samarth`**

### Step 3: Configure the Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `project-samarth-backend` |
| **Region** | Choose closest to you (e.g., Oregon, Frankfurt) |
| **Branch** | `main` |
| **Root Directory** | `src` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python app_modular.py` |
| **Plan** | `Free` (or choose paid for better performance) |

### Step 4: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

```bash
SECRET_KEY=<your_gemini_api_key_1>
API_GUESSING_MODELKEY=<your_gemini_api_key_2>
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/agri_qa_cache
DATA_GOV_API_KEY=<your_data_gov_api_key>
USE_REAL_API=true
PORT=8000
```

**Replace** the placeholder values with your actual API keys!

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will:
   - Clone your repository
   - Install dependencies from `src/requirements.txt`
   - Start your FastAPI app with `python app_modular.py`
3. Wait 3-5 minutes for the build to complete

Your backend will be live at: `https://project-samarth-backend.onrender.com`

---

## 🎨 Update Frontend to Use Render Backend

### Option 1: Deploy Frontend on Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repo
3. Configure:
   - **Root Directory**: `frontend`
   - **Framework**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Add environment variable:
   ```bash
   VITE_API_URL=https://project-samarth-backend.onrender.com
   ```
5. Deploy

### Option 2: Update Local Frontend

Edit `frontend/.env`:
```bash
VITE_API_URL=https://project-samarth-backend.onrender.com
```

Then rebuild:
```powershell
cd frontend
npm run build
```

---

## 🔧 Update CORS for Render

Your backend needs to allow requests from your frontend domain.

Edit `src/app_modular.py` (around line 60):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://project-samarth.vercel.app",  # Your Vercel frontend
        "https://*.vercel.app",  # All Vercel previews
        "https://project-samarth-backend.onrender.com"  # Allow self
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push → Render will auto-redeploy.

---

## ✅ Verify Deployment

### Test Backend Health
```powershell
curl https://project-samarth-backend.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "mongodb": "connected",
  "data_loaded": true,
  "crop_records": 52,
  "rainfall_records": 8
}
```

### Test Frontend
Visit your frontend URL and try a sample question like:
- "What are the top 3 crops in Maharashtra?"
- "What is the rainfall in Punjab?"

---

## 🔄 Continuous Deployment

Render automatically deploys when you push to `main`:

```powershell
git add .
git commit -m "your changes"
git push origin main
```

Render will:
1. Detect the push
2. Build automatically
3. Deploy the new version
4. Zero-downtime deployment

---

## 📊 Monitor Your Service

In Render Dashboard:
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory usage
- **Events**: Deployment history
- **Settings**: Update env vars, scale up/down

---

## ⚠️ Important Notes

### Free Tier Limitations
- Service **spins down after 15 minutes** of inactivity
- First request after spin-down takes **30-60 seconds** (cold start)
- **750 hours/month** of runtime (enough for one service)

### Performance Tips
1. **Keep service warm**: Use a cron job to ping every 10 minutes
2. **Upgrade to Starter plan** ($7/month): No spin-down
3. **Optimize startup**: Move data loading to first request instead of startup

---

## 🐛 Troubleshooting

### Build Fails
- Check `src/requirements.txt` has all dependencies
- Verify Python version compatibility
- Check Render build logs for specific errors

### Service Won't Start
- Verify `PORT` environment variable is set to `8000`
- Check that `app_modular.py` uses `host="0.0.0.0"`
- Review Render logs for startup errors

### Database Connection Fails
- Verify MongoDB Atlas allows connections from anywhere (`0.0.0.0/0`)
- Check `DATABASE_URL` format is correct
- Ensure database user has proper permissions

### Frontend Can't Connect
- Verify CORS settings include frontend domain
- Check `VITE_API_URL` is set correctly in frontend
- Test backend health endpoint directly

---

## 🚀 URLs Summary

After deployment:
- **Backend**: `https://project-samarth-backend.onrender.com`
- **Health Check**: `https://project-samarth-backend.onrender.com/api/health`
- **API Docs**: `https://project-samarth-backend.onrender.com/docs`
- **Frontend**: `https://project-samarth.vercel.app`

---

## 📝 Files Created for Render

- ✅ `build.sh` - Build script (optional)
- ✅ `Procfile` - Start command
- ✅ `runtime.txt` - Python version
- ✅ `render.yaml` - Service configuration (optional)

---

**Your backend is now ready to deploy on Render!** 🎉

No size limits, full FastAPI support, and automatic deployments!
