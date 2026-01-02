# 🚀 Quick Reference - Project Samarth
**Last Updated**: January 2, 2026  
**Version**: 3.0  
**Architecture**: LangGraph + RAG + Two-Model Fallback

## 📁 Project Structure

```
project-samarth/
├── src/                    # Backend (Python/FastAPI)
│   ├── app_modular.py      # Main backend entry
│   ├── config/             # Settings
│   ├── models/             # API models
│   ├── database/           # MongoDB
│   ├── services/           # AI + Data
│   │   ├── langgraph_agent.py  # LangGraph (PRIMARY)
│   │   ├── rag_service.py      # RAG with ChromaDB
│   │   ├── ai_models.py        # Two-model fallback
│   │   ├── data_integration.py
│   │   └── query_engine.py
│   └── api/                # Endpoints
│
├── frontend/               # Frontend (React/Vite)
│   ├── src/
│   │   ├── components/     # 9 React components
│   │   ├── services/       # API client
│   │   └── utils/          # Helpers
│   ├── package.json
│   └── vite.config.js
│
├── docs/                   # Documentation
├── test/                   # Tests
├── .env                    # Environment vars (SECRET!)
└── README.md               # Main documentation
```

---

## ⚡ Quick Start

### Backend (Port 8000)
```bash
cd src
pip install -r requirements.txt
cp .env.example .env         # Edit with your API keys
python app_modular.py
```

### Frontend (Port 5173)
```bash
cd frontend
npm install
npm run dev                  # Vite dev server
```

### Access
- 🌐 **Frontend**: http://localhost:5173
- 🔌 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs
- 🚀 **Production Backend**: https://project-samarth-gxou.onrender.com
- ✨ **Production Frontend**: https://project-samarth-frontend.vercel.app

---

## 🔑 Required API Keys

### `.env` (Project Root - Backend)
```env
# Gemini AI (https://aistudio.google.com/app/apikey)
SECRET_KEY=your_gemini_key_here
API_GUESSING_MODELKEY=your_second_gemini_key_here
AGENT_API_KEY=your_third_gemini_key_here

# MongoDB Atlas (https://www.mongodb.com/cloud/atlas)
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/agri_qa_cache

# ChromaDB Cloud (optional - local works too)
CHROMA_API_KEY=your_chroma_api_key
CHROMA_TENANT=your_tenant
CHROMA_DATABASE=Project Samarth

# Data.gov.in API (Get from https://data.gov.in/catalogs)
DATA_GOV_API_KEY=your_data_gov_api_key_here
USE_REAL_API=true
```

### `frontend/.env`
```env
VITE_API_URL=http://localhost:8000
```

---

## 🎯 Key Features

### Backend
- ✅ **LangGraph Agent (Primary)** - Autonomous reasoning with 5 tools
- ✅ **RAG with ChromaDB** - 100+ agricultural documents
- ✅ **Two-Model Fallback** - Reliability through redundancy
- ✅ **MongoDB Caching** - 30-40x performance boost
- ✅ **5 Data Sources** - 1901-2024 coverage
- ✅ **8 REST APIs** - Complete CRUD operations
- ✅ **Modular Design** - 10+ clean modules

### Frontend
- ✅ **React 18** - Modern hooks
- ✅ **Vite 5** - Lightning-fast builds
- ✅ **Tailwind CSS 3** - Beautiful UI
- ✅ **9 Components** - Fully modular
- ✅ **Responsive** - Mobile-friendly
- ✅ **Deployed on Vercel** - Global CDN

---

## 🧪 Testing

### Backend Health Check
```bash
curl http://localhost:8000/api/health
```

### Sample Query (Backend)
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is rice production in Punjab for 2023?"}'
```

### Cache Stats
```bash
curl http://localhost:8000/api/cache/stats
```

### Frontend
Open browser to http://localhost:3000 and try sample questions!

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/query` | Submit question |
| GET | `/api/health` | Health check |
| GET | `/api/datasets` | Available datasets |
| GET | `/api/cache/stats` | Cache statistics |
| POST | `/api/cache/clear?confirm=true` | Clear cache |
| DELETE | `/api/cache/expired` | Delete expired |

---

## 🏗️ Architecture

### Backend Flow
```
User Query → Cache Check → LangGraph Agent (5 tools) → Cache Store → Response
   (100ms)      (STEP 0)    (STEP 1 - PRIMARY)            (STEP 2)    (30-40x faster!)
   
   If LangGraph fails → Two-Model Fallback (Router → Fetch → Processor)
```

### LangGraph Tools
1. **fetch_apeda_production** - APEDA data (2019-2024)
2. **fetch_crop_production** - District data (2013-2015)
3. **fetch_rainfall_data** - Rainfall patterns
4. **search_knowledge_base** - RAG with 100+ docs
5. **web_search** - Google Search API

### Frontend Components
```
App.jsx
├── Header.jsx              # Title & badges
├── ServerStats.jsx         # Live statistics
├── SampleQuestions.jsx     # Quick buttons
├── QueryForm.jsx           # Input form
├── LoadingSpinner.jsx      # Loading state
├── ErrorMessage.jsx        # Errors
└── ResultDisplay.jsx       # Results container
    ├── AnswerBox.jsx       # Formatted answer
    └── DataSources.jsx     # Source links
```

---

## 🚀 Git Commands

### Initial Setup (Already Done)
```bash
git init
git add .
git commit -m "Initial commit: v1.0.0"
```

### Add Frontend
```bash
git add frontend/
git commit -m "Add React frontend with Tailwind CSS"
```

### Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/project-samarth.git
git branch -M main
git push -u origin main
```

---

## 🎥 Demo Flow

1. **Show GitHub** - Clean README, good structure
2. **Backend Demo** - Health check, cache stats
3. **Frontend Demo** - Beautiful UI, sample query
4. **Cache Performance** - First query (15s) vs cached (0.1s) = **135x faster!**
5. **Architecture** - Two models, modular design
6. **Code Quality** - Show components, services, clean structure

---

## 🐛 Troubleshooting

### Backend won't start
- Check `.env` file exists in project root
- Verify all API keys are set
- Run: `pip install -r src/requirements.txt`

### Frontend won't start
- Check Node.js installed: `node --version`
- Delete `node_modules`: `rm -rf node_modules`
- Reinstall: `npm install`

### Can't connect to backend
- Ensure backend running on port 8000
- Check `frontend/.env` has `VITE_API_URL=http://localhost:8000`
- Check CORS settings in backend

### MongoDB connection failed
- Verify `DATABASE_URL` in `.env`
- Check MongoDB Atlas IP whitelist
- Test connection string

---

## 📚 Documentation

- **README.md** - Main documentation
- **SETUP_GUIDE.md** - Detailed setup
- **docs/INDEX.md** - Documentation hub
- **docs/QUICKSTART.md** - 5-minute guide
- **docs/MODULAR_ARCHITECTURE.md** - Backend architecture
- **frontend/README.md** - Frontend guide

---

## 💡 Sample Questions

1. "What is the rice production in Punjab for 2023?"
2. "Show me wheat production data for Karnataka"
3. "Compare rainfall in Punjab and Haryana for 2024"
4. "What are the top 3 crops produced in Maharashtra?"
5. "Analyze production trends for maize in India"

---

## 📦 Tech Stack Summary

### Backend
- Python 3.9+
- FastAPI 0.104.1
- Google Gemini AI
- MongoDB (Motor 3.3.2)
- Pandas 2.1.3

### Frontend
- React 18.2.0
- Vite 5.0.8
- Tailwind CSS 3.3.6
- Axios 1.6.0

---

## 🎯 Performance Metrics

- **Cache Hit**: 0.1 seconds
- **Cache Miss**: 13-30 seconds
- **Improvement**: **135x faster**
- **Data Coverage**: 1901-2024 (123 years)
- **Total Records**: 100+ crop + rainfall data
- **API Endpoints**: 8
- **Frontend Components**: 9

---

## ✅ Pre-Demo Checklist

- [ ] Backend running (port 8000)
- [ ] Frontend running (port 5173)
- [ ] MongoDB connected
- [ ] LangGraph agent loaded
- [ ] RAG knowledge base initialized
- [ ] Sample query works
- [ ] Cache hit demonstrated (30-40x faster!)
- [ ] GitHub repo updated
- [ ] Documentation complete
- [ ] .env files configured (NOT committed!)

---

## 🔗 Useful Links

- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs
- Production Backend: https://project-samarth-gxou.onrender.com
- Production Frontend: https://project-samarth-frontend.vercel.app
- GitHub: https://github.com/adityasuhane-06/Project-samarth

---

**Quick Start in 3 Steps:**

1. **Backend**: `cd src && python app_modular.py`
2. **Frontend**: `cd frontend && npm run dev`
3. **Browser**: Open http://localhost:5173

**That's it! 🎉**

---

**Last Updated**: January 2, 2026  
**Version**: 3.0  
**Status**: Production Ready (Render + Vercel)
