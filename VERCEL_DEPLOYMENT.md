# Vercel Deployment Guide - Two Projects Setup

## 📦 Project Structure

You have TWO separate Vercel projects to deploy:

1. **Backend Project** (Current repo root) - FastAPI with Mangum
2. **Frontend Project** (frontend/ folder) - React + Vite

---

## 🚀 Backend Deployment (API)

### Step 1: Create Backend Project on Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repo: `adityasuhane-06/Project-samarth`
3. Configure:
   - **Project Name**: `project-samarth-backend` (or any name)
   - **Framework Preset**: Other
   - **Root Directory**: `.` (leave as root)
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
   - **Install Command**: `pip install -r requirements.txt`

### Step 2: Add Environment Variables (Backend)

In Vercel dashboard → Settings → Environment Variables, add:

```bash
SECRET_KEY=your_gemini_api_key_here
API_GUESSING_MODELKEY=your_gemini_routing_key_here
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/agri_qa_cache
DATA_GOV_API_KEY=your_data_gov_api_key_here
USE_REAL_API=true
PORT=8000
```

### Step 3: Deploy Backend

Click "Deploy" → Vercel will:
- Install dependencies from `requirements.txt`
- Run `api/index.py` as serverless function
- Give you a URL like: `https://project-samarth-backend.vercel.app`

**Save this URL!** You'll need it for the frontend.

---

## 🎨 Frontend Deployment

### Step 1: Create Frontend Project on Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import **the same GitHub repo** again
3. Configure:
   - **Project Name**: `project-samarth-frontend` (or any name)
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend` ⚠️ **IMPORTANT!**
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### Step 2: Add Environment Variables (Frontend)

In Vercel dashboard → Settings → Environment Variables, add:

```bash
VITE_API_URL=https://project-samarth-backend.vercel.app
VITE_ENV=production
```

⚠️ **Replace** `https://project-samarth-backend.vercel.app` with your actual backend URL from Step 1!

### Step 3: Deploy Frontend

Click "Deploy" → Vercel will:
- Install npm packages
- Build React app with Vite
- Deploy static files
- Give you a URL like: `https://project-samarth.vercel.app`

---

## 🔧 Final Steps

### 1. Update CORS in Backend

After deploying, update `src/app_modular.py` CORS settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://project-samarth.vercel.app",  # Your frontend URL
        "https://*.vercel.app"  # All Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push → Backend will auto-redeploy.

### 2. Test Production

1. Visit your frontend URL: `https://project-samarth.vercel.app`
2. Check server status indicator (should be green)
3. Try a sample question
4. Check browser console for any errors

---

## 📝 Local Testing (Optional)

Test the Mangum wrapper locally:

```powershell
# Install vercel CLI
npm install -g vercel

# Test backend locally
vercel dev

# Or test with Python directly
cd api
python -c "from index import handler; print('Import successful')"
```

---

## 🔄 Continuous Deployment

Both projects will auto-deploy on every push to `main`:
- Push to GitHub → Both Vercel projects deploy automatically
- Pull requests → Get preview deployments

---

## ⚙️ Environment Variables Summary

### Backend Project
```
SECRET_KEY=<gemini-key-1>
API_GUESSING_MODELKEY=<gemini-key-2>
DATABASE_URL=<mongodb-connection-string>
DATA_GOV_API_KEY=<data-gov-key>
USE_REAL_API=true
PORT=8000
```

### Frontend Project
```
VITE_API_URL=<backend-vercel-url>
VITE_ENV=production
```

---

## 🐛 Troubleshooting

### Backend Issues

**"Module not found" errors:**
- Check `requirements.txt` has all dependencies
- Verify `api/index.py` imports are correct
- Check Vercel build logs

**"Cold start" slow response:**
- First request after inactivity takes 5-10 seconds
- Consider using a cron job to keep it warm
- Or upgrade to Vercel Pro for better performance

**Database connection errors:**
- Verify MongoDB Atlas allows connections from `0.0.0.0/0`
- Check `DATABASE_URL` environment variable is correct
- Ensure MongoDB user has read/write permissions

### Frontend Issues

**"Network Error" or "Cannot connect to backend":**
- Verify `VITE_API_URL` is set correctly
- Check CORS settings in backend
- Verify backend is deployed and running

**Build fails:**
- Check `frontend/package.json` has all dependencies
- Verify Node version (Vercel uses Node 18 by default)
- Check Vercel build logs for specific errors

---

## 📊 Expected URLs

After deployment, you'll have:

- **Frontend**: `https://project-samarth.vercel.app`
- **Backend**: `https://project-samarth-backend.vercel.app`
- **API Health**: `https://project-samarth-backend.vercel.app/api/health`
- **API Query**: `https://project-samarth-backend.vercel.app/api/query`

---

## 🎯 Next Steps

1. ✅ Commit all changes: `git push origin main`
2. ✅ Create backend Vercel project (root directory)
3. ✅ Add backend environment variables
4. ✅ Deploy backend and save URL
5. ✅ Create frontend Vercel project (frontend/ directory)
6. ✅ Add frontend environment variables (with backend URL)
7. ✅ Deploy frontend
8. ✅ Update CORS in backend
9. ✅ Test production deployment

---

**Ready to deploy!** 🚀
