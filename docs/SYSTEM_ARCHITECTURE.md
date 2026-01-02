# 🏗️ Project Samarth - System Architecture

## 📊 AI Architecture

### Primary: LangGraph Agentic Workflow
- **Purpose**: Autonomous multi-step reasoning with tool usage
- **Model**: Google Gemini 2.5 Flash
- **API Key**: `AGENT_API_KEY` (fallback to `SECRET_KEY`)
- **Location**: `src/services/langgraph_agent.py`
- **State Machine**: TypedDict-based state management
- **Tools**: 5 autonomous tools for data fetching and search
- **Routing**: Conditional edges based on LLM decisions

### Fallback: Two-Model Architecture

#### Model 1: QueryRouter (Dataset Selection)
- **Purpose**: Intelligent routing to correct data sources
- **Model**: Google Gemini 2.5 Flash
- **API Key**: `API_GUESSING_MODELKEY`
- **Function**: `route_query(question)` → Returns parameters
- **Location**: `src/services/ai_models.py`

#### Model 2: QueryProcessor (Answer Generation)
- **Purpose**: Natural language answer generation
- **Model**: Google Gemini 2.5 Flash
- **API Key**: `SECRET_KEY`
- **Function**: `generate_answer(question, data, sources)` → Answer
- **Location**: `src/services/ai_models.py`

---

## 🗄️ Data Sources Integration

### 1️⃣ District-Level Crop Production API
- **Source**: data.gov.in - Ministry of Agriculture
- **Coverage**: 2013-2015
- **Granularity**: District-level
- **Resource ID**: `35be999b-0208-4354-b557-f6ca9a5355de`
- **Fetch Function**: `fetch_crop_production_data()`
- **Query Function**: `query_crop_production(params)`
- **Data Fields**: State, District, Crop, Year, Area, Production

### 2️⃣ APEDA Production API
- **Source**: agriexchange.apeda.gov.in - APEDA Ministry of Commerce
- **Coverage**: 2019-2024 (Financial Years)
- **Granularity**: State-level aggregated
- **URL**: `https://agriexchange.apeda.gov.in/Production/IndiaCat/GetIndiaProductionCatObject`
- **Fetch Function**: `fetch_apeda_data(fin_year, category, product_code)`
- **Query Function**: `query_apeda(params)`
- **Categories**: All, Agri, Fruits, Vegetables, Spices, LiveStock, Plantations, Floriculture
- **Product Code Mapping**: Automatic via `find_product_code()` method

### 3️⃣ Daily Rainfall API
- **Source**: data.gov.in - India Meteorological Department (IMD)
- **Coverage**: 2019-2024
- **Granularity**: District-level daily data
- **Resource ID**: `6c05cd1b-ed59-40c2-bc31-e314f39c6971`
- **Fetch Function**: `fetch_daily_rainfall(state, district, year, limit)`
- **Query Function**: `query_daily_rainfall(params)`
- **Data Fields**: State, District, Date, Avg_rainfall

### 4️⃣ Historical Rainfall API
- **Source**: data.gov.in - India Meteorological Department (IMD)
- **Coverage**: 1901-2015
- **Granularity**: State-level (36 meteorological subdivisions)
- **Resource ID**: `440dbca7-86ce-4bf6-b1af-83af2855757e`
- **Fetch Function**: `fetch_historical_rainfall(subdivision, year, limit)`
- **Query Function**: `query_historical_rainfall(params)`
- **Data Fields**: Subdivision, Year, JAN-DEC (monthly), Annual, Seasonal
- **Subdivisions Map**: See `subdivision_map` in `query_historical_rainfall()`

### 5️⃣ Sample Rainfall Data (Fallback)
- **Source**: Hardcoded sample data
- **Coverage**: 2020-2022
- **Granularity**: State-level
- **Fetch Function**: `_get_sample_rainfall_data()`
- **Query Function**: `query_rainfall(params)`
- **Purpose**: Fallback when no specific API matches

---

## 🔄 Query Flow

```
┌─────────────────┐
│  User Question  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│   MongoDB Cache Check           │
│   - Generate MD5 hash            │
│   - Lookup cached response       │
└────────┬────────────────────────┘
         │
         ├─ ✅ Cache Hit → Return (100ms)
         │
         └─ ❌ Cache Miss
                  ↓
         ┌─────────────────────────┐
         │  LangGraph Agent        │
         │  (Primary Path)         │
         │  - Multi-step reasoning  │
         │  - Tool selection        │
         │  - 5 autonomous tools    │
         └────────┬────────────────┘
                  │
                  ├─ ✅ Success → Cache & Return
                  │
                  └─ ❌ Error/Unavailable
                           ↓
                  ┌──────────────────────┐
                  │  Two-Model Fallback  │
                  │  1. QueryRouter      │
                  │  2. DataQueryEngine  │
                  │  3. QueryProcessor   │
                  └────────┬─────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Cache Response  │
                  │  Return Answer   │
                  └─────────────────┘
```

---

## 📁 File Structure

```
Project samarth/
├── .env                          # Environment variables & API keys
├── .venv/                        # Python virtual environment
├── activate_env.bat              # Windows activation script
│
├── src/                          # Main application source
│   ├── app_modular.py            # 🔥 Main FastAPI application
│   ├── requirements.txt          # Python dependencies
│   ├── test_gemini.py            # Gemini API test script
│   │
│   ├── api/                      # API routes
│   │   ├── __init__.py
│   │   └── routes.py             # All API endpoints
│   │
│   ├── config/                   # Configuration
│   │   ├── __init__.py
│   │   └── settings.py           # Settings & environment vars
│   │
│   ├── database/                 # Database layer
│   │   ├── __init__.py
│   │   └── mongodb.py            # MongoDB caching
│   │
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   └── api_models.py         # Pydantic models
│   │
│   └── services/                 # Business logic
│       ├── __init__.py
│       ├── ai_models.py          # Two-model fallback
│       ├── data_integration.py   # External API integration
│       ├── query_engine.py       # Query execution
│       ├── langgraph_agent.py    # LangGraph agentic workflow
│       ├── rag_service.py        # RAG with ChromaDB
│       ├── langchain_ai.py       # LangChain implementations
│       └── apeda_codes.py        # Product code mappings
│
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # 9 modular components
│   │   └── services/             # API client
│   ├── package.json
│   └── vite.config.js
│
├── test/                         # Test suite
│   ├── test_system.py
│   ├── test_integrated_system.py
│   └── api_tests/                # API testing scripts
│
└── docs/                         # Documentation
    LangGraph Agent (Primary)
**Location**: `src/services/langgraph_agent.py`

**Components**:
- **AgentState**: TypedDict-based state management
- **5 Tools**: fetch_apeda_production, fetch_crop_production, fetch_rainfall_data, search_knowledge_base, web_search
- **StateGraph**: Conditional routing based on LLM decisions
- **ToolNode**: Executes selected tools
- **Multi-step reasoning**: Agent can chain multiple tool calls

### RAG Service
**Location**: `src/services/rag_service.py`

**Features**:
- **Knowledge Base**: 100+ agricultural documents
- **Embeddings**: HuggingFace sentence-transformers (local, free)
- **Vector Store**: ChromaDB (cloud & local support)
- **Semantic Search**: Retrieves relevant context for queries

### DataGovIntegration Class
**Location**: `src/services/data_integration.py`

**Key Methods**:
- `fetch_apeda_data(fin_year, category, product_code)` - APEDA production
- `find_product_code(crop_name)` - Automatic product code mapping
- `fetch_daily_rainfall(state, district, year)` - Daily rainfall
- `fetch_historical_rainfall(subdivision, year)` - Historical rainfall

### QueryRouter & QueryProcessor (Fallback)
**Location**: `src/services/ai_models.py`

**QueryRouter**:
- Analyzes question and returns routing parameters
- Selects appropriate datasets based on years and query type

**QueryProcessor**:
- Generates natural language answers with citations
- Formats responses with structured data

### DataQueryEngine Class
**Location**: `src/services/query_engine.py`

**Methods**:
- `query_crop_production(params)` - District data (2013-2015)
- `query_apeda(params)` - State data (2019-2024)
- `query_daily_rainfall(params)` - District rainfall (2019-2024)
- `query_historical_rainfall(params)` - Historical (1901-2015)
- `execute_query(params)` - Orchestrates all queries

### MongoDB Cache
**Location**: `src/database/mongodb.py`

**Features**:
- Async operations with Motor
- MD5 hash-based cache keys
- TTL-based expiration (180-365 days)
- Hit count tracking
- Cache statistics API
- `query_daily_rainfall(params)` - Queries district daily rainfall (2019-2024)
- `query_historical_rainfall(params)` - Queries historical rainfall (1901-2015)
- `query_rainfall(params)` - Queries sample rainfall data (fallback)
- `execute_query(params)` - Orchestrates all query methods based on `data_needed`

### QueryProcessor Class
**Location**: `src/app.py` (Lines 477+)

**Methods**:
- `__init__(api_key)` - Initialize with Gemini API key (for answer generation)
- `generate_answer(question, query_results, data_sources)` - Generates natural language answer with citations

---

## 🔑 Environment Variables

**File**: `.env` (in project root)

``Gemini AI Keys (3 separate keys for optimal rate limiting)
SECRET_KEY=your_gemini_api_key_here           # Answer generation
API_GUESSING_MODELKEY=your_gemini_api_key_here  # Query routing
AGENT_API_KEY=your_gemini_api_key_here        # LangGraph agent (optional)

# MongoDB Atlas
DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net/

# ChromaDB Cloud (optional - can use local)
CHROMA_API_KEY=your_chroma_api_key
CHROMA_TENANT=your_tenant
CHROMA_DATABASE=Project Samarth

# Data.gov.in API
DATA_GOV_API_KEY=your_data_gov_api_key_here
USE_REAL_API=true

# Optional: Google Search API (for web_search tool)
GOOGLE_SEARCH_API_KEY=your_google_api_key
GOOGLE_SEARCH_CX=your_search_engine_idyour_data_gov_api_key_here
USE_REAL_API=true
```

---

## 🚀 API Endpoints

### Health Check
**GET** `/api/health`

**Response**:
```json
{
  "status": "healthy",
  "data_loaded": true,
  "last_updated": "2025-11-01T12:00:00",
  "crop_records": 104,
  "rainfall_records": 8
}
```

### Query Endpoint
**POST** `/api/query`

**Request**:
```json
{
  "question": "What is the rice production in Punjab for 2023?"
}
```

**Response**:
```json
{
  "question": "What is the rice production in Punjab for 2023?",
  "answer": "Based on the provided data, Punjab's rice production for 2023-24 was **14356.0 thousand tonnes** [Source: APEDA Production Statistics]...",
  "data_sources": [
    {
      "dataset": "APEDA Production Statistics",
      "source": "APEDA - Ministry of Commerce",
      "url": "https://agriexchange.apeda.gov.in/"
    }
  ],
  "query_params": { ... },
  "raw_results": { ... }
}
```

### Root Endpoint
**Location**: `frontend/src/`

**Technology Stack**:
- React 18 with hooks
- Vite 5 (fast build tool)
- Tailwind CSS 3 (utility-first styling)
- Axios (API client)

**9 Modular Components**:
- Header, ServerStats, SampleQuestions
- QueryForm, LoadingSpinner, ErrorMessage
- ResultDisplay, AnswerBox, DataSources

**Features**:
- Rich answer formatting with HTML parsing
- Real-time cache statistics display
- Responsive mobile-first design
- Sample question quick-start buttons
- Source citations with links
- Error handling with user-friendly messages
- 🏷️ Financial year badges (blue pills)
- 📊 Source tags with styling
- 💪 Bold state names
- 📚 Enhanced source cards with hover effects
- 🎯 Responsive design
- ⚡ Real-time query processing with loading states

**Beautification Function**: `formatAnswer(answer)` - Parses and styles answer text

---

## 📊 Routing Rules

### Production Queries:
- **Years 2019-2024** → `apeda_production` (State-level, financial years)
- **Years 2013-2015** → `crop_production` (District-level)
- **No year specified** → Both `["crop_production", "apeda_production"]`

### Rainfall Queries:
- **Years 2019-2024** → `daily_rainfall` (District-level daily)
- **Years 1901-2015** → `historical_rainfall` (State-level historical)
- **No year specified** → `rainfall` (Sample data fallback)

### Comparison Queries:
- **Multiple time periods** → Multiple data sources selected automatically

---

## 🧪 Testing

### Run All Tests:
```bash
cd "C:\Users\Lenovo\Desktop\Project samarth\test"
python test_integrated_system.py
```

### Individual API Tests:
```bash
cd "C:\Users\Lenovo\Desktop\Project samarth\test\api_tests"
python test_apeda_categories.py   # APEDA comprehensive test
python test_punjab_rainfall.py    # Historical rainfall test
python fetch_pune_complete.py     # Daily rainfall test
```

### PowerShell Query Test:
```powershell
$body = @{question="What is the rice production in Punjab for 2023?"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/api/query" -Method POST -Body $body -ContentType "application/json" | Select-Object -ExpandProperty Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## 🔧 Running the System

### 1. ActivaBackend:
```bash
cd src
python app_modular.py
```

### 3. Start Frontend (separate terminal):
```bash
cd frontend
npm run dev
```

### 4. Access Application:
- **Frontend**: http://localhost:5173 (Vite dev server)
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### 5. Production URLs:
- **Frontend**: https://project-samarth.vercel.app
- **Backend**: https://project-samarth-gxou.onrender.comfetches
✅ **Web search capability**: Access to real-time information
✅ **RAG integration**: Semantic search over knowledge base
✅ **Flexible**: Adapts to complex, multi-faceted queries

### MongoDB Caching Benefits:
✅ **30-40x faster**: 3-4s → 100ms on cache hits
✅ **Cost savings**: Zero API calls on cached responses
✅ **Hit tracking**: Identifies popular queries
✅ **TTL-based**: Auto-expires old data (180-365 days)

### System Architecture:
✅ **Fault tolerance**: Automatic fallback to two-model
✅ **Modular design**: Easy to maintain and extend
✅ **Scalable**: Async operations, cloud databases
✅ **Production-ready**: Deployed on Render + Vercel
---

## 📈 Performance Characteristics

### Two-Model Architecture Benefits:
✅ **Separation of Concerns**: Routing logic separate from answer generation  
✅ **Cost Optimization**: Lighter model for routing, powerful model for answers  
✅ **Better Accuracy**: Specialized models for specific tasks  
✅ **Easier Maintenance**: Update routing logic without touching answer generation  

### Two-Model Architecture Tradeoffs:
⚠️ **Slower**: 2 API calls instead of 1 (adds ~1-2 seconds)  
⚠️ **Higher API Usage**: Double API calls per query  
⚠️ **More Complex**: More code paths and failure points  

---

## 🎯 Sample Queries

### Production Queries:
- "What is the rice production in Punjab for 2023?" → APEDA API
- "Show wheat production in Karnataka for 2014" → District Crop API
- "Compare rice production in 2014 and 2023" → Both APIs

### Rainfall Queries:
- "What was the rainfall in Pune in 2024?" → Daily Rainfall API
- "S� Support

**Repository**: https://github.com/adityasuhane-06/Project-samarth

For documentation, check:
- `docs/` folder - Complete architecture guides
- `test/` folder - API testing examples
- `/docs` endpoint - FastAPI auto-generated API docs
- `README.md` - Quick start guide

---

**Last Updated**: January 2, 2026  
**Version**: 3.0 (LangGraph Agentic Architecture with RAG)  
**Status**: ✅ Production Ready - Deployed on Render + Vercelor monitoring
- [ ] Expand to more data sources
- [ ] Add export functionality (CSV, PDF)
- [ ] Implement query history tracking
- [ ] Add real-time notifications for data updates

---

## 📞 Support

For issues or questions, check:
- Documentation in `docs/` folder
- Test examples in `test/api_tests/`
- FastAPI auto-generated docs at `/docs`

---

**Last Updated**: November 1, 2025  
**Version**: 2.0 (Two-Model Architecture)  
**Status**: ✅ Production Ready
