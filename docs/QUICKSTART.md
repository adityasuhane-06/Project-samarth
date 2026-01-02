# Quick Start Guide - Project Samarth
**Last Updated**: January 2, 2026

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r src/requirements.txt
```

Key packages:
```bash
pip install fastapi uvicorn pandas requests google-generativeai python-dotenv motor pymongo langchain langchain-google-genai langgraph chromadb sentence-transformers
```

### Step 2: Configure Environment
Create `.env` file in project root:
```env
# Gemini AI Keys (3 keys for optimal rate limiting)
SECRET_KEY=your_gemini_api_key_here
API_GUESSING_MODELKEY=your_second_gemini_key_here
AGENT_API_KEY=your_third_gemini_key_here

# MongoDB Atlas
DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net/

# ChromaDB Cloud (optional - can use local)
CHROMA_API_KEY=your_chroma_api_key
CHROMA_TENANT=your_tenant
CHROMA_DATABASE=Project Samarth

# Data.gov.in API
DATA_GOV_API_KEY=your_data_gov_api_key_here
USE_REAL_API=true
```

**Get API Keys:**
- Gemini API: https://aistudio.google.com/app/apikey (get 3 keys)
- MongoDB: https://www.mongodb.com/cloud/atlas (free tier)
- ChromaDB: https://www.trychroma.com (optional, local works too)

### Step 3: Start the Backend

```bash
cd src
python app_modular.py
```

You should see:
```
============================================================
APPLICATION STARTUP
============================================================
✅ Connected to MongoDB Atlas successfully!
✅ LangGraph Agent loaded successfully
✅ LangGraph Agent initialized
Loading data from data.gov.in...
Data loaded successfully. Crop records: 10, Rainfall records: 8
============================================================

INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Start the Frontend (separate terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: http://localhost:5173

### Step 5: Test the System

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

**Cache Statistics:**
```bash
curl http://localhost:8000/api/cache/stats
```

### Step 6: Try Sample Queries

**Basic Query (Cache Miss - ~3-4s with LangGraph):**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the rice production in Punjab for 2023?"}'
```

**Same Query Again (Cache Hit - ~100ms):**
```bash
# Run the same command again - 30-40x faster!
```

**More Sample Queries:**
```
"What are rabi crops?"
"Show wheat production in Karnataka for 2014"
"Compare maize production across states"
"Tell me about agricultural practices in Punjab"
"What is crop rotation?"
```

## 📊 Verify LangGraph Agent

Check the console output - you'll see:
```
🤖 USING LANGGRAPH AGENTIC WORKFLOW...
DEBUG: Agent reasoning step 1
DEBUG: Tool call: fetch_apeda_production
✅ Agent completed in 2 steps
✅ Sources used: ['fetch_apeda_production', 'search_knowledge_base']
```

LangGraph agent autonomously decides which tools to use! ✅

**If LangGraph fails, automatic fallback:**
```
⚠️ LangGraph Agent failed
⚠️ Falling back to two-model architecture...
🔀 USING TWO-MODEL ARCHITECTURE (fallback)...
```

## 💾 Verify MongoDB Caching

**First Query (Cache Miss):**
```
💾 STEP 0: CHECKING CACHE (key: abc123...)
❌ Cache miss. Processing query...
🤖 USING LANGGRAPH AGENTIC WORKFLOW...
[3-4 seconds later]
💾 CACHING RESPONSE...
```

**Second Query (Cache Hit):**
```
💾 STEP 0: CHECKING CACHE (key: abc123...)
💾 CACHE HIT! Query has been answered 0 times before
⚡ RETURNING CACHED RESPONSE (saved ~3-4 seconds!)
[100ms - 30-40x faster!]
```

## � System Architecture Overview

### Key Components:

**1. LangGraph Agentic Workflow (Primary)**
- Autonomous tool selection and execution
- 5 tools: APEDA data, crop data, rainfall, RAG search, web search
- Multi-step reasoning with state management

**2. RAG Knowledge Base**
- 100+ agricultural documents embedded
- ChromaDB vector storage (local or cloud)
- HuggingFace sentence-transformers for embeddings
- Semantic search for contextual information

**3. MongoDB Caching**
- 30-40x performance improvement
- TTL-based expiration (180-365 days)
- Hit count tracking
- Detailed analytics

**4. Two-Model Fallback**
- QueryRouter: Dataset selection
- QueryProcessor: Answer generation
- Activates if LangGraph fails

**5. Modular Architecture**
- 8 separate modules (config, models, database, services, api)
- Clean separation of concerns
- Easy to maintain and extend

## 🔍 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use (Windows)
netstat -ano | findstr :8000

# Check if port 8000 is in use (Mac/Linux)
lsof -i :8000

# Try a different port
uvicorn app_modular:app --host 0.0.0.0 --port 8001
```

### Frontend won't connect
- Update `frontend/.env` or `frontend/src/services/api.js`
- Make sure `API_URL` points to correct backend
- Check CORS settings in backend

### API Key Error
- Make sure you're using Google Gemini API keys
- Check that you have credits/quota available
- Verify keys are entered correctly (no spaces)
- Get keys from: https://aistudio.google.com/app/apikey

### MongoDB Connection Error
- Verify DATABASE_URL in .env
- Check network access in MongoDB Atlas (allow 0.0.0.0/0)
- Ensure database user has read/write permissions
- System will continue without cache if MongoDB unavailable

### ChromaDB Error
- Local ChromaDB works without API key
- For cloud, verify CHROMA_API_KEY and CHROMA_TENANT
- System continues without RAG if ChromaDB unavailable

### LangGraph Agent Fails
- System automatically falls back to two-model architecture
- Check logs for specific error
- Verify AGENT_API_KEY is set correctly

## 📊 Understanding the Output

### Answer Format
The answer includes:
- Natural language response to your question
- Specific numbers and statistics from data sources
- Context from RAG knowledge base (if applicable)
- Source citations in [Source: ...] format

### Data Sources Section
Shows:
- Dataset name (APEDA, Crop Production, Rainfall, RAG)
- Source organization
- Link to original data or knowledge base

### Raw Results (in API response)
Contains the actual data queried, useful for debugging and further analysis

## 🎯 Best Practices

### Query Tips:
✅ Start with specific questions (state, crop, year)
✅ Try agricultural knowledge questions ("What are rabi crops?")
✅ Use natural language - system understands context
✅ Check cache stats to see popular queries
✅ Monitor LangGraph agent reasoning in console logs

### Performance Tips:
✅ Let MongoDB handle caching automatically
✅ Popular queries become instant (30-40x faster)
✅ Use RAG for agricultural knowledge
✅ LangGraph adapts to query complexity

### Don't:
❌ Don't manually clear cache frequently (TTL handles it)
❌ Don't worry if LangGraph fails (fallback is automatic)
❌ Don't forget to check both frontend and backend logs

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **LangGraph Agent** | Autonomous multi-tool agentic workflow |
| **RAG Knowledge Base** | 100+ agricultural documents, semantic search |
| **MongoDB Caching** | 30-40x performance improvement |
| **Two-Model Fallback** | Automatic fallback if agent fails |
| **Multi-Dataset** | APEDA, crop production, rainfall, historical data |
| **Source Citations** | Every answer includes traceable sources |
| **Modular Architecture** | Clean, maintainable, production-ready code |

## 📦 Quick Reference

### Start System
```bash
# Backend (Terminal 1)
cd src
python app_modular.py

# Frontend (Terminal 2)
cd frontend
npm run dev
```

### Check Status
```bash
# Health check
curl http://localhost:8000/api/health

# Cache statistics
curl http://localhost:8000/api/cache/stats

# Frontend
http://localhost:5173
```

### Environment Setup
- 3 Gemini API keys (SECRET_KEY, API_GUESSING_MODELKEY, AGENT_API_KEY)
- MongoDB Atlas connection string
- ChromaDB (optional - local works)
- Data.gov.in API key

### Production URLs
- Backend: https://project-samarth-gxou.onrender.com
- Frontend: https://project-samarth-frontend.vercel.app

---

**System Status**: ✅ **PRODUCTION READY**  
**Performance**: ⚡ **30-40x FASTER with caching**  
**Architecture**: 🤖 **LangGraph + RAG + Two-Model Fallback**

**Last Updated**: January 2, 2026  
**Version**: 3.0
