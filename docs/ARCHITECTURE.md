# Project Samarth - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                              │
│          (React 18 + Vite 5 + Tailwind CSS 3)                   │
│              Deployed on Vercel                                  │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   QueryForm  │  │    Server    │  │   Result     │         │
│  │   Component  │  │    Stats     │  │   Display    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  9 Modular React Components + Rich Formatting                   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP POST /api/query
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND SERVER                         │
│            Deployed on Render (project-samarth-gxou)            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐      │
│  │         Query Processing Pipeline                      │      │
│  │                                                       │      │
│  │  STEP 0: MongoDB Cache Check (100ms if hit)         │      │
│  │  STEP 1: LangGraph Agent (Primary Path)             │      │
│  │    └─ 5 Tools: APEDA, Crop, Rainfall, RAG, Web      │      │
│  │  STEP 2: Two-Model Fallback (if needed)             │      │
│  │    ├─ QueryRouter (dataset selection)                │      │
│  │    └─ QueryProcessor (answer generation)             │      │
│  │  STEP 3: Cache Response (MongoDB)                   │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┬──────────────────┐
            │               │               │                  │
            ▼               ▼               ▼                  ▼
┌────────────────┐  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│  Google Gemini │  │  MongoDB    │  │  ChromaDB    │  │  data.gov.in │
│  2.5 Flash API │  │   Atlas     │  │  (RAG)       │  │  APIs        │
│                │  │             │  │              │  │              │
│ 3 API Keys:    │  │ Caching     │  │ 100+ docs    │  │ Crop Data    │
│ - Routing      │  │ 30-40x      │  │ HF Embed     │  │ Rainfall     │
│ - Answer       │  │ Faster      │  │ Semantic     │  │ APEDA        │
│ - Agent        │  │             │  │ Search       │  │              │
└────────────────┘  └─────────────┘  └──────────────┘  └──────────────┘
```

## Component Details

### 1. Frontend (React + Vite + Tailwind CSS)
**Technology**: React 18, Vite 5, Tailwind CSS 3, Axios

**Key Components** (9 modular):
- **Header.jsx**: App title and branding
- **ServerStats.jsx**: Live cache statistics
- **SampleQuestions.jsx**: Quick-start buttons
- **QueryForm.jsx**: Input form with validation
- **LoadingSpinner.jsx**: Animated loading state
- **ErrorMessage.jsx**: Error display
- **ResultDisplay.jsx**: Result container
- **AnswerBox.jsx**: Rich formatted answers
- **DataSources.jsx**: Source citations

**Key Features**:
- **Component-based** architecture for reusability
- **Tailwind CSS** utility-first styling with custom theme
- **Vite** for lightning-fast builds (5-10x faster than webpack)
- **Axios** for HTTP client with interceptors
- **Environment variables** for API URL configuration
- **Production deployment** on Vercel with auto-deploy from GitHub

### 2. Backend API Server (FastAPI)
**Technology**: FastAPI 0.104.1, Python 3.11.9, Uvicorn

**Responsibilities**:
- Request handling with CORS middleware
- AI Agent orchestration (two-model system)
- Data management and caching
- Response formatting

**Endpoints**:
- `POST /api/query` - Process natural language queries
- `GET /api/health` - Health check and data status
- `GET /api/datasets` - Available dataset information

### 3. Data Integration Layer

#### DataGovIntegration Class
**Purpose**: Interface with data.gov.in portal

**Methods**:
- `fetch_crop_production_data()` - Retrieve crop production statistics
- `fetch_rainfall_data()` - Retrieve IMD rainfall data
- `_get_sample_crop_data()` - Sample data matching real structure
- `_get_sample_rainfall_data()` - Sample rainfall data

**Data Sources**:
1. **Crop Production**: District-wise, season-wise crop area and production
   - Source: Ministry of Agriculture & Farmers Welfare
   - URL: https://www.data.gov.in/catalog/district-wise-season-wise-crop-production-statistics

2. **Rainfall Data**: State-wise annual and seasonal rainfall
   - Source: India Meteorological Department (IMD)
   - URL: https://www.data.gov.in/catalog/rainfall-india

### 4. Query Processing Pipeline

**Primary Path: LangGraph Agentic Workflow**

#### Stage 1: Agent Initialization
**Component**: LangGraphAgent (services/langgraph_agent.py)
**Process**:
1. Query analysis using Gemini 2.5 Flash
2. Autonomous tool selection from 5 available tools
3. Multi-step reasoning with state management
4. Context accumulation across steps

#### Stage 2: Tool Execution (Autonomous)
**Available Tools**:
1. **fetch_apeda_production** - APEDA export data (2019-2024)
2. **fetch_crop_production** - District-level crop data (2013-2015)
3. **fetch_rainfall_data** - Historical and daily rainfall
4. **search_knowledge_base** - RAG with 100+ documents (ChromaDB)
5. **web_search** - Real-time web search (Google Search API)

**How it works**:
- Agent decides which tools to use based on query
- Can call multiple tools in sequence
- Accumulates context from each tool
- Uses RAG for agricultural knowledge questions
- Falls back to web search for current information

#### Stage 3: Answer Synthesis
**Component**: LangGraphAgent.process_query()
**Process**:
1. Combines results from all executed tools
2. Generates natural language answer
3. Includes citations for all sources used
4. Tracks reasoning steps for transparency

**Fallback Path: Two-Model Architecture**

#### Stage 1: Parameter Extraction (If LangGraph fails)
**Component**: QueryRouter (services/ai_models.py)
**Input**: Natural language question
**Output**: Structured JSON parameters

```json
{
  "states": ["Punjab", "Haryana"],
  "districts": [],
  "crops": ["Rice"],
  "crop_types": ["cereals"],
  "years": [2022, 2021],
  "data_needed": ["crop_production", "rainfall"],
  "comparison_type": "spatial",
  "aggregation": "average"
}
```

**How it works**:
- Uses Gemini 2.5 Flash with structured prompting
- Extracts entities (states, crops, years)
- Identifies query intent (comparison, trend, top-N)
- Determines required datasets

#### Stage 2: Data Querying
**Component**: DataQueryEngine.execute_query()
**Input**: Extracted parameters
**Output**: Filtered and aggregated data + sources

**Operations**:
- Filter by state, district, crop, year
- Aggregate (sum, average, top-N)
- Join multiple datasets when needed
- Track source for each data point

#### Stage 3: Answer Generation
**Component**: QueryProcessor (services/ai_models.py)
**Input**: Query results + sources
**Output**: Natural language answer with citations

**How it works**:
- Uses Claude AI for synthesis
- Incorporates all relevant data points
- Generates citations for each claim
- Formats for readability

## Data Flow Example

### Query: "Compare rice production in Punjab and Haryana for 2022-23"

**Using LangGraph Agent (Primary):**

1. **User Input** → Frontend sends POST to `/api/query`

2. **Agent Analysis** → LangGraph agent reasons:
   ```
   Thought: User wants to compare rice production across states
   Action: Will use fetch_crop_production tool with state and crop filters
   ```

3. **Tool Execution** → Agent calls fetch_crop_production:
   - Punjab rice records for 2022-23: 4 districts
   - Haryana rice records for 2022-23: 4 districts
   - Agent accumulates production totals

4. **Answer Synthesis** → Agent generates:
   ```
   Based on district-level crop production data, Punjab produced 2,277,000 tonnes 
   of rice in 2022-23 across 4 major districts, while Haryana produced 1,468,000 
   tonnes. Punjab's rice production is 55% higher than Haryana's.
   
   [Sources: fetch_crop_production, District-wise Crop Production Statistics]
   ```

5. **Response** → Returns JSON with answer, sources, reasoning steps

**Using Two-Model Fallback (if LangGraph fails):**

1. **User Input** → Frontend sends POST to `/api/query`

2. **Parameter Extraction** → QueryRouter extracts:
   ```json
   {
     "states": ["Punjab", "Haryana"],
     "crops": ["Rice"],
     "years": [2022],
     "data_needed": ["crop_production"],
     "comparison_type": "spatial"
   }
   ```

3. **Data Query** → System filters crop data:
   - Punjab rice records for 2022-23: 4 districts
   - Haryana rice records for 2022-23: 4 districts
   - Aggregates total production for each state

4. **Answer Generation** → QueryProcessor synthesizes:
   ```
   Punjab produced 2,277,000 tonnes of rice in 2022-23 across 4 major 
   districts, while Haryana produced 1,468,000 tonnes. [Source: District-wise 
   Crop Production Statistics]
   
   Punjab's rice production is 55% higher than Haryana's...
   ```

5. **Response** → Returns JSON with answer, sources, raw data

## Key Design Decisions

### 1. LangGraph Agentic Workflow (Primary)
**Why**: Autonomous reasoning provides better query handling
- Agent decides which tools to use dynamically
- Multi-step reasoning with state management
- Can combine multiple data sources intelligently
- RAG integration for agricultural knowledge
- Benefits: Flexibility, adaptability, intelligence

### 2. Two-Model Fallback Architecture
**Why**: Reliability through redundancy
- Separating routing from generation improves accuracy (when LangGraph unavailable)
- First stage: Structured understanding (parameters)
- Second stage: Natural language synthesis (answer)
- Benefits: System always available, debugging easier

### 3. RAG with ChromaDB
**Why**: Agricultural knowledge base integration
- 100+ documents about crops, farming, practices
- Semantic search with HuggingFace embeddings
- Answers "What is..." and concept questions
- Benefits: Contextual knowledge, educational value

### 4. Data Schema Normalization
**Why**: Different ministries use different formats
- Internal unified schema
- Consistent field names
- Easy to add new sources

### 5. Source Traceability
**Why**: Critical for government/policy use
- Every data point has source
- Direct links to data.gov.in
- Full transparency

### 6. MongoDB Caching Strategy
**Why**: Performance and cost efficiency
- Query responses cached in MongoDB Atlas
- 30-40x performance improvement on cache hits
- TTL-based expiration (180-365 days)
- Hit tracking for analytics
- Benefits: Speed, cost savings, user experience

### 7. Stateless API
**Why**: Scalability and simplicity
- No session management
- Each request independent
- Easy to deploy multiple instances

## Scalability Considerations

### Current Design
- Deployed on Render (backend) + Vercel (frontend)
- MongoDB Atlas for caching
- ChromaDB for vector storage
- Good for: Production use, scalable to thousands of users

### Production Enhancements (Future)
1. **Redis Layer**: Additional caching tier for hot queries
2. **Load Balancing**: Multiple API servers
3. **Background Jobs**: Periodic data refresh
4. **API Gateway**: Advanced rate limiting, authentication
5. **CDN**: Global content delivery for frontend

## Security Considerations

### Data Privacy
- No user data stored (queries cached, not user info)
- API keys managed through environment variables
- Can run in air-gapped environment with local ChromaDB
- MongoDB Atlas with encrypted connections

### Data Integrity
- Direct source citations for all answers
- Immutable data references
- Audit trail through MongoDB hit tracking
- Version control for RAG knowledge base

## Extensibility

### Adding New Tools to LangGraph
1. Create tool function in `services/langgraph_agent.py`
2. Add tool to agent's workflow graph
3. Update AgentState if needed
4. Test with relevant queries

### Adding New RAG Documents
1. Add documents to `AGRICULTURAL_KNOWLEDGE` list
2. Vector store auto-updates on startup
3. Test semantic search queries

### Adding New Datasets
1. Add fetch method in DataGovIntegration
2. Add query method in DataQueryEngine
3. Update parameter extraction prompt
4. No frontend changes needed

### Adding New Features
- Visualizations: Add chart generation
- Exports: Add PDF/Excel generation
- History: Add query logging
- Multi-language: Add translation layer

## Performance Metrics

### Query Processing Time
- Parameter extraction: ~2-3 seconds (Claude API)
- Data querying: <100ms (in-memory)
- Answer generation: ~3-5 seconds (Claude API)
- **Total**: ~6-8 seconds per query

## Performance Metrics

### Query Processing Time (with LangGraph)
- Cache check: ~50ms
- **Cache hit**: ~100ms total (30-40x faster)
- **Cache miss (LangGraph)**:
  - Agent reasoning: ~1-2 seconds
  - Tool execution: ~500-1000ms per tool
  - Answer synthesis: ~1-2 seconds
  - **Total**: ~3-5 seconds per query
- **Cache miss (Two-model fallback)**:
  - Parameter extraction: ~800ms
  - Data querying: <100ms (in-memory)
  - Answer generation: ~1200ms
  - **Total**: ~2-3 seconds per query

### Optimization Opportunities
- Parallel tool execution in LangGraph
- Streaming responses for real-time updates
- Pre-computed aggregations for common queries
- Hot query caching in Redis

## Technology Stack

### Backend
- **Python 3.11.9**: Core language
- **FastAPI 0.104.1**: Modern async web framework
- **Uvicorn**: ASGI server
- **Pandas 2.1**: Data manipulation
- **Google Generative AI**: Gemini 2.5 Flash (3 API keys)
- **LangChain**: LLM orchestration framework
- **LangGraph**: Agentic workflow with state machine
- **ChromaDB**: Vector database for RAG
- **Motor**: Async MongoDB driver
- **Sentence Transformers**: HuggingFace embeddings

### Frontend
- **React 18**: Modern UI framework
- **Vite 5**: Lightning-fast build tool
- **Tailwind CSS 3**: Utility-first CSS
- **Axios**: HTTP client

### Databases
- **MongoDB Atlas**: Query response caching
- **ChromaDB**: Vector storage for RAG (100+ docs)

### AI/ML
- **Google Gemini 2.5 Flash**: Fast, capable model
- **LangChain + LangGraph**: Agentic AI framework
- **HuggingFace Embeddings**: Semantic search
- Used for: Agent reasoning, RAG search, query routing, answer synthesis

## Deployment

### Production Deployment (Current)
**Backend**: Render.com
- URL: https://project-samarth-gxou.onrender.com
- Auto-deploy from GitHub main branch
- Environment variables configured
- Free tier (can upgrade for better performance)

**Frontend**: Vercel
- URL: https://project-samarth-frontend.vercel.app
- Auto-deploy from GitHub
- Global CDN
- Instant page loads

**Databases**:
- MongoDB Atlas (free tier, 512MB)
- ChromaDB (local on Render server)

### Local Development
```bash
# Backend
cd src
python app_modular.py

# Frontend
cd frontend
npm install
npm run dev
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD ["uvicorn", "app_modular:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Future Roadmap

### Phase 1 (Current): Production Ready ✅
✅ LangGraph agentic workflow
✅ RAG with 100+ documents
✅ MongoDB caching (30-40x faster)
✅ Two-model fallback architecture
✅ Multi-dataset integration
✅ Source citations
✅ Deployed on Render + Vercel

### Phase 2: Enhanced Features
- More LangGraph tools (market prices, schemes)
- Expanded RAG knowledge base (500+ docs)
- Advanced visualizations
- Query history and analytics
- Multi-language support (Hindi)

### Phase 3: Advanced Analytics
- Predictive modeling with AI
- Trend forecasting
- Policy impact simulation
- Custom report generation
- Export to PDF/Excel

### Phase 4: Enterprise Features
- Advanced authentication system
- Role-based access control
- API rate limiting per user
- Custom deployment options
- White-label solutions

## Conclusion

This architecture provides:
- ✅ **Autonomous AI** - LangGraph agent with 5 tools
- ✅ **Knowledge Integration** - RAG with 100+ documents
- ✅ **High Performance** - 30-40x faster with caching
- ✅ **Reliability** - Automatic fallback to two-model system
- ✅ **Source Traceability** - Every answer cited
- ✅ **Production Ready** - Deployed and accessible
- ✅ **Scalable** - Modular architecture, easy to extend
- ✅ **Professional** - Industry-standard design

**Last Updated**: January 2, 2026  
**Version**: 3.0  
**Status**: Production Deployment on Render + Vercel

---

*For detailed module documentation, see [MODULAR_ARCHITECTURE.md](MODULAR_ARCHITECTURE.md)*  
*For caching details, see [MONGODB_CACHING.md](MONGODB_CACHING.md)*  
*For system architecture, see [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)*
