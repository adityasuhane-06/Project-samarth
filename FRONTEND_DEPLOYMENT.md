# Frontend Deployment Guide - Vercel

This guide covers deploying the React frontend to Vercel from the same GitHub repository.

## 🎯 Overview

- **Frontend Framework**: React 18 + Vite 5 + Tailwind CSS
- **Deployment Platform**: Vercel (Static Site)
- **Backend URL**: https://project-samarth-gxou.onrender.com
- **Source Repository**: Same GitHub repo (monorepo structure)

## 📁 Project Structure

```
Project-samarth/
├── frontend/          # Frontend application (deploy this to Vercel)
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vercel.json   # Vercel configuration
│   └── .vercelignore
├── src/               # Backend application (deployed to Render)
└── ...
```

## 🚀 Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/
   - Sign in with GitHub account

2. **Import Project**
   - Click "Add New..." → "Project"
   - Select your GitHub repository: `adityasuhane-06/Project-samarth`
   - Click "Import"

3. **Configure Project Settings**
   
   **Root Directory**: `frontend`
   - ⚠️ **IMPORTANT**: Set the root directory to `frontend/`
   - This tells Vercel to only deploy the frontend folder
   
   **Framework Preset**: Vite
   - Should auto-detect, or select "Vite" from dropdown
   
   **Build Command**: `npm run build`
   - Default is correct
   
   **Output Directory**: `dist`
   - Default is correct
   
   **Install Command**: `npm install`
   - Default is correct

4. **Environment Variables**
   
   Add these environment variables in Vercel dashboard:
   
   ```
   VITE_API_URL = https://project-samarth-gxou.onrender.com
   VITE_ENV = production
   ```
   
   - Click "Environment Variables"
   - Add each variable for all environments (Production, Preview, Development)

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for build to complete
   - You'll get a URL like: `https://project-samarth-frontend.vercel.app`

### Option 2: Deploy via Vercel CLI

```powershell
# Install Vercel CLI globally
npm install -g vercel

# Navigate to frontend folder
cd frontend

# Login to Vercel
vercel login

# Deploy to production
vercel --prod

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Select your account
# - Link to existing project? No
# - Project name? project-samarth-frontend
# - Directory? ./ (current directory is already frontend/)
# - Override settings? No
```

## 🔧 Configuration Details

### vercel.json Configuration

```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "framework": "vite",
  "env": {
    "VITE_API_URL": "https://project-samarth-gxou.onrender.com",
    "VITE_ENV": "production"
  }
}
```

**Key Features:**
- **Rewrites**: All routes redirect to `index.html` (SPA routing support)
- **Build Settings**: Optimized for Vite builds
- **Environment Variables**: Pre-configured backend URL

### Why This Works?

- **Monorepo Support**: Vercel supports deploying a subdirectory from a GitHub repo
- **Root Directory Setting**: Tells Vercel to treat `frontend/` as the project root
- **Automatic Builds**: Every push to `main` branch triggers auto-deployment
- **Preview Deployments**: Every PR creates a preview deployment

## 🔄 Continuous Deployment

Once set up, Vercel will automatically:

1. **Auto-deploy on push to `main`**
   ```bash
   git add .
   git commit -m "Update frontend"
   git push origin main
   ```
   → Vercel detects changes in `frontend/` folder
   → Triggers new deployment automatically

2. **Preview deployments for PRs**
   - Create a PR → Vercel creates preview URL
   - Test changes before merging

3. **Rollback capability**
   - View deployment history in Vercel dashboard
   - Rollback to previous version with one click

## 🌐 Custom Domain (Optional)

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain (e.g., `app.yourdomain.com`)
3. Follow DNS configuration instructions
4. SSL certificate is automatically provisioned

## 🔒 Update Backend CORS

After deploying frontend, update CORS in `src/app_modular.py`:

```python
origins = [
    "http://localhost:3000",  # Local development
    "https://project-samarth-frontend.vercel.app",  # Production
    "https://*.vercel.app"  # Preview deployments
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Change from ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Deploy backend changes:**
```bash
git add src/app_modular.py
git commit -m "Update CORS for production frontend"
git push origin main
```

Render will auto-deploy the backend update.

## 📊 Monitoring

### Vercel Dashboard
- **Deployments**: View build logs and status
- **Analytics**: Track page views and performance (upgrade needed)
- **Functions**: Serverless function logs (not used in this project)

### Check Deployment Status
```powershell
# List all deployments
vercel ls

# Check specific deployment logs
vercel logs [deployment-url]
```

## 🐛 Troubleshooting

### Build Fails

**Issue**: `npm install` fails
```
Solution: Check package.json is valid
cd frontend
npm install  # Test locally first
```

**Issue**: `npm run build` fails
```
Solution: Check Vite config and imports
npm run build  # Test locally first
```

### Environment Variables Not Working

**Issue**: Frontend still uses `localhost:8000`
```
Solution: 
1. Verify env vars in Vercel dashboard
2. Redeploy after adding env vars
3. Check browser DevTools → Network tab for actual API calls
```

### CORS Errors

**Issue**: "CORS policy: No 'Access-Control-Allow-Origin' header"
```
Solution:
1. Check backend CORS settings include Vercel URL
2. Backend must be running: https://project-samarth-gxou.onrender.com/api/health
3. Wait 15 minutes if backend was idle (Render free tier spins down)
```

### 404 on Refresh

**Issue**: Page refreshes show 404 error
```
Solution: vercel.json rewrites should handle this
Verify rewrites configuration is present
```

## 📈 Performance Tips

1. **Enable Vercel Speed Insights** (Optional, paid)
   ```bash
   npm install @vercel/speed-insights
   ```
   
   Add to `src/main.jsx`:
   ```javascript
   import { SpeedInsights } from '@vercel/speed-insights/react';
   
   // Add <SpeedInsights /> to your app
   ```

2. **Enable Vercel Analytics** (Optional, paid)
   ```bash
   npm install @vercel/analytics
   ```

3. **Image Optimization**
   - Use Vercel Image Optimization API
   - Automatic WebP conversion
   - Responsive image loading

## 🎉 Success Checklist

After deployment, verify:

- [ ] Frontend URL is live (e.g., https://project-samarth-frontend.vercel.app)
- [ ] Homepage loads correctly
- [ ] Can submit a query (e.g., "Top crops in Maharashtra")
- [ ] Backend connection works (check Network tab)
- [ ] No CORS errors in console
- [ ] All components render properly
- [ ] Tailwind CSS styles apply correctly
- [ ] Auto-deployment works (push a change and verify)

## 🔗 Useful Links

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Vercel Docs**: https://vercel.com/docs
- **Backend (Render)**: https://project-samarth-gxou.onrender.com/
- **GitHub Repo**: https://github.com/adityasuhane-06/Project-samarth

## 📝 Quick Reference

```powershell
# Deploy from CLI
cd frontend
vercel --prod

# Check deployment status
vercel ls

# View logs
vercel logs

# Rollback to previous deployment
vercel rollback

# Remove project
vercel remove project-samarth-frontend
```

## 🎯 Summary

Your setup:
- **Frontend**: Vercel (Static Site) → `https://*.vercel.app`
- **Backend**: Render (FastAPI) → `https://project-samarth-gxou.onrender.com`
- **Database**: MongoDB Atlas
- **Source**: GitHub → Auto-deploys both platforms

Both services auto-deploy from the same GitHub repository but deploy different folders:
- Vercel deploys `frontend/` folder only
- Render deploys `src/` folder (backend)

This is a standard **monorepo** deployment pattern! 🚀
