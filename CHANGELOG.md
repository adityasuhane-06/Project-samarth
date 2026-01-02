# Changelog

All notable changes to Project Samarth will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2026-01-02

### 🎉 Major Release - LangGraph Agentic Architecture

#### Added - LangGraph Agent System

- **LangGraph Agentic Workflow** (`services/langgraph_agent.py`)
  - Autonomous multi-step reasoning with state machine
  - 5 autonomous tools with conditional routing
  - AgentState TypedDict for state management
  - Multi-tool orchestration in single query
  - Intelligent tool selection based on query analysis

- **5 Agent Tools**
  - `fetch_apeda_production` - APEDA data (2019-2024)
  - `fetch_crop_production` - District data (2013-2015)
  - `fetch_rainfall_data` - Rainfall patterns
  - `search_knowledge_base` - RAG semantic search
  - `web_search` - Google Custom Search integration

#### Added - RAG System

- **RAG Service** (`services/rag_service.py`)
  - ChromaDB vector database integration (cloud & local)
  - HuggingFace sentence-transformers embeddings (local, free)
  - 100+ agricultural knowledge documents
  - Semantic search with similarity scoring
  - Answers agricultural concept questions

- **Knowledge Base Documents**
  - Crop types (Rabi, Kharif, Zaid)
  - Agricultural practices
  - Crop grading standards
  - Government schemes
  - Regional crop information

#### Added - Enhanced Features

- **Three API Keys System**
  - AGENT_API_KEY - LangGraph agent (primary)
  - API_GUESSING_MODELKEY - QueryRouter (fallback)
  - SECRET_KEY - QueryProcessor (fallback)
  - Optimal rate limiting distribution

- **Web Search Integration**
  - Google Custom Search API
  - Real-time information retrieval
  - Handles current/future queries (2025+)

- **Force-Routing Logic**
  - 2025+/current → force web search
  - 2019-2024 → force APEDA database
  - General knowledge → force RAG search
  - Eliminates hallucinations

#### Changed - Architecture Updates

- **Two-Model System → Fallback**
  - QueryRouter now fallback only
  - QueryProcessor now fallback only
  - Activates when LangGraph unavailable
  - Maintains reliability

- **Performance Improvements**
  - Cache hit: 100ms (unchanged)
  - Cache miss with LangGraph: 3-5 seconds (vs 13-30s)
  - 6-10x faster query processing
  - Still 30-40x with cache

- **Frontend Updates**
  - React 18 + Vite 5 + Tailwind CSS 3
  - 9 modular components
  - Live server statistics
  - Rich answer formatting
  - Deployed on Vercel

#### Added - Deployment

- **Production Deployment**
  - Backend: Render (https://project-samarth-gxou.onrender.com)
  - Frontend: Vercel (https://project-samarth-frontend.vercel.app)
  - Auto-deploy from GitHub main branch
  - Global CDN with HTTPS

#### Fixed

- MongoDB boolean evaluation errors (carried from v1.0)
- Agent initialization race conditions
- RAG embeddings loading on cold start
- CORS configuration for Vercel deployments

#### Documentation

- Updated all docs to reflect LangGraph primary
- Added LangGraph tool development guide
- Updated architecture diagrams
- Revised performance benchmarks
- Complete deployment guide for v3.0

#### Dependencies Added

```
langchain==0.1.0
langchain-google-genai==0.0.5
langgraph==0.0.20
chromadb==0.4.22
sentence-transformers==2.2.2
```

#### Migration from v2.0 to v3.0

- Same `.env` file works (add 3rd API key + ChromaDB vars)
- Same API endpoints (100% backward compatible)
- LangGraph automatically used when available
- Falls back to two-model if LangGraph fails
- No client code changes required

---

## [2.0.0] - 2025-11-15

### 🏗️ Modular Architecture Release

#### Changed - Code Organization

- **Modularized Codebase**
  - Split monolithic app.py (~2000 lines) into 8 modules (~1300 lines)
  - Clean separation of concerns
  - Easier maintenance and testing
  - Team-ready development

- **Module Structure**
  - `config/` - Configuration management
  - `models/` - Pydantic API models
  - `database/` - MongoDB operations
  - `services/` - Business logic (AI, data, queries)
  - `api/` - API route handlers

#### Added

- Development documentation in MODULE_README.md
- Module-specific import paths
- Comprehensive comparison report

#### Maintained

- 100% feature parity with v1.0
- All API endpoints unchanged
- Same performance characteristics
- Identical functionality

---

## [1.0.0] - 2025-11-01

### 🎉 Initial Release

#### Added - Core Features

- **Two-Model AI Architecture**
  - QueryRouter (gemini-2.5-flash) for intelligent query routing
  - QueryProcessor (gemini-2.5-flash) for natural language answer generation
  - Separate API keys for better rate limiting
  - Smart routing logic for 5 different data sources

- **MongoDB Caching System**
  - Async caching with Motor
  - 135x performance improvement on cache hits
  - Intelligent TTL management (90-365 days based on data type)
  - Cache hit tracking and statistics
  - Automatic expired query cleanup
  - SHA-256 based cache key generation

- **Data Integration**
  - APEDA Production Statistics API (2019-2024)
  - Crop Production Data (2013-2015)
  - Daily Rainfall Data API (2019-2024)
  - Historical Rainfall API (1901-2015)
  - Sample Data Fallback (8 records)

- **API Endpoints**
  - POST `/api/query` - Natural language query processing
  - GET `/api/health` - Health check with MongoDB status
  - GET `/api/datasets` - Available dataset information
  - GET `/api/cache/stats` - Detailed cache statistics
  - POST `/api/cache/clear` - Clear all cached queries
  - DELETE `/api/cache/expired` - Remove expired entries
  - GET `/api/` - API information
  - GET `/` - Welcome page

#### Added - Modular Architecture

- **Configuration Module** (`config/`)
  - Centralized settings management
  - Environment variable handling
  - Cache TTL configuration

- **Models Module** (`models/`)
  - Pydantic request/response models
  - Type-safe API contracts

- **Database Module** (`database/`)
  - MongoDBCache class with async operations
  - Connection lifecycle management
  - Cache statistics tracking

- **Services Module** (`services/`)
  - AI Models service (QueryRouter + QueryProcessor)
  - Data Integration service (5 data sources)
  - Query Engine service (unified query interface)

- **API Module** (`api/`)
  - RESTful endpoint handlers
  - 5-step query processing flow
  - Error handling and validation

#### Added - Documentation

- `README.md` - Comprehensive project overview
- `docs/INDEX.md` - Documentation hub
- `docs/QUICKSTART.md` - 5-minute setup guide
- `docs/PROJECT_SUMMARY.md` - Project overview
- `docs/ARCHITECTURE.md` - System architecture
- `docs/SYSTEM_ARCHITECTURE.md` - Technical details
- `docs/MODULAR_ARCHITECTURE.md` - Module guide
- `docs/MONGODB_CACHING.md` - Caching implementation
- `docs/TWO_MODEL_TEST_REPORT.md` - Testing results
- `docs/COMPARISON_REPORT.md` - Feature parity analysis
- `src/MODULE_README.md` - Developer guide

#### Added - Testing

- `test/test_system.py` - Basic system tests
- `test/test_integrated_system.py` - Integration tests
- `test/test_two_models.py` - Two-model architecture tests
- `test/list_routing_models.py` - Model verification

#### Added - Configuration Files

- `.env.example` - Environment template
- `.gitignore` - Git ignore rules
- `requirements.txt` - Python dependencies
- `LICENSE` - MIT License
- `CONTRIBUTING.md` - Contribution guidelines

### 🐛 Bug Fixes

- Fixed MongoDB database object boolean evaluation errors
  - Changed `if mongodb_client:` to `if mongodb_client is not None:`
  - Changed `if db:` to `if db is None:` in disconnect logic
  - Applied to 6 locations across codebase
- Fixed query engine initialization timing issues
- Fixed cache key generation for consistent hashing

### 🚀 Performance

- **135x faster** queries with MongoDB caching
- Cache hit time: ~0.1 seconds
- Cache miss time: 13-30 seconds (depending on data source)
- Async database operations for non-blocking I/O

### 📊 Data Coverage

- **Time Range**: 1901-2024 (123 years)
- **Geographic**: State and District level data
- **Crops**: 20+ crop varieties
- **Data Points**: 100+ records + real-time API access

### 🔒 Security

- Environment variable based configuration
- API key separation for rate limiting
- MongoDB connection string security
- CORS configuration for web access

### 📦 Dependencies

```
fastapi==0.104.1
uvicorn==0.24.0
pandas==2.1.3
requests==2.31.0
google-generativeai==0.3.1
motor==3.3.2
pymongo==4.6.0
python-dotenv==1.0.0
pydantic==2.5.0
```

### 🎯 Achievements

- ✅ 100% feature parity between monolithic and modular versions
- ✅ Production-ready codebase
- ✅ Comprehensive documentation (20,000+ words)
- ✅ Clean modular architecture (~1,300 lines)
- ✅ Type-safe API with Pydantic
- ✅ Source traceability for all answers

---

## [Unreleased]

### Planned Features (v4.0)

- [ ] More LangGraph tools (market prices, weather forecasts, soil data)
- [ ] Expand RAG knowledge base to 500+ documents
- [ ] Multi-language support (Hindi, regional languages)
- [ ] Streaming responses for real-time agent reasoning
- [ ] User authentication and query history
- [ ] Advanced visualizations and charts
- [ ] Export data in multiple formats (CSV, Excel, PDF)
- [ ] Email notifications and subscriptions
- [ ] Mobile app (React Native)

### Under Consideration

- [ ] PostgreSQL support as alternative to MongoDB
- [ ] Redis caching layer for hot queries
- [ ] Elasticsearch integration for full-text search
- [ ] Kubernetes deployment configurations
- [ ] GraphQL API alongside REST
- [ ] WebSocket support for real-time updates
- [ ] Admin dashboard for monitoring
- [ ] A/B testing framework
- [ ] API versioning (v2)
- [ ] Custom LangGraph workflows per user

---

## Version History

### Version Numbering

- **Major** (X.0.0): Breaking changes, major feature additions (v1.0 → v2.0 → v3.0)
- **Minor** (3.X.0): New features, backward compatible
- **Patch** (3.0.X): Bug fixes, minor improvements

### Release Schedule

- **Major releases**: Quarterly (Q4 2025: v1.0, Q4 2025: v2.0, Q1 2026: v3.0)
- **Minor releases**: Monthly
- **Patch releases**: As needed

---

## Migration Guides

### From v2.0 to v3.0 (LangGraph)

If you're upgrading from modular two-model (v2.0) to LangGraph (v3.0):

1. **Update dependencies**:
   ```bash
   pip install -r src/requirements.txt
   ```

2. **Add new environment variables**:
   ```env
   # Add 3rd Gemini key
   AGENT_API_KEY=your_third_gemini_key
   
   # Add ChromaDB (optional - local works)
   CHROMA_API_KEY=your_chroma_key
   CHROMA_TENANT=your_tenant
   CHROMA_DATABASE=Project Samarth
   
   # Add Google Search (optional)
   GOOGLE_SEARCH_API_KEY=your_google_key
   GOOGLE_SEARCH_CX=your_search_engine_id
   ```

3. **No code changes required** - 100% API compatibility
4. **Same run command**: `python app_modular.py`
5. **LangGraph automatically used** - falls back to two-model if unavailable

### From v1.0 to v2.0 (Modular)

If you're upgrading from the monolithic `app.py` to the modular `app_modular.py`:

1. **No code changes required** - 100% API compatibility
2. **Update run command**:
   ```bash
   # Old
   python app.py
   
   # New
   python app_modular.py
   ```
3. **Same .env file works** - No configuration changes needed
4. **All endpoints identical** - Client code works without changes

---

## Support

For questions or issues:
- Check [documentation](docs/INDEX.md)
- Open [GitHub Issue](https://github.com/adityasuhane-06/Project-samarth/issues)
- Review [FAQ](docs/QUICKSTART.md#troubleshooting)
- Read [Architecture Guide](docs/ARCHITECTURE.md)

---

**Current Version**: 3.0.0  
**Release Date**: January 2, 2026  
**Status**: Production Ready  
**Architecture**: LangGraph + RAG + Two-Model Fallback

**Note**: This project is actively maintained. We welcome your feedback and contributions!
