# 🏗️ Project Samarth - System Architecture

## 📊 Two-Model AI Architecture

### Model 1: QueryRouter (Intelligent API Routing)
- **Purpose**: Routes queries to the correct data sources
- **Model**: Google Gemini 1.5 Flash (Fast & Efficient)
- **API Key**: `API_GUESSING_MODELKEY` from .env
- **Function**: `route_query(question)` → Returns API selection parameters
- **Location**: `src/app.py` (Lines 350-475)

### Model 2: QueryProcessor (Answer Generation)
- **Purpose**: Generates natural language answers from data
- **Model**: Google Gemini 2.5 Flash (More Powerful)
- **API Key**: `SECRET_KEY` from .env
- **Function**: `generate_answer(question, data, sources)` → Returns formatted answer
- **Location**: `src/app.py` (Lines 477+)

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
- **Product Codes**: 
  - Rice: 1011
  - Wheat: 1013
  - Maize: 1009
  - Milk: 1023
  - Mango: 1050
  - Potato: 1083
  - Turmeric: 1099
  - (See `crop_to_code` dictionary in app.py)

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
│   QueryRouter (Model 1)         │
│   - Analyzes question            │
│   - Determines year range        │
│   - Selects appropriate APIs     │
│   - Returns parameters           │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   DataQueryEngine               │
│   - Calls selected APIs          │
│   - Fetches data                 │
│   - Filters & aggregates         │
│   - Returns structured results   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   QueryProcessor (Model 2)      │
│   - Receives data & sources      │
│   - Generates natural answer     │
│   - Formats with citations       │
│   - Returns beautified response  │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────┐
│  User Answer    │
│  (Beautified)   │
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
│   ├── app.py                    # 🔥 Core FastAPI application
│   │                             # - DataGovIntegration class (all API fetching)
│   │                             # - QueryRouter class (API routing)
│   │                             # - QueryProcessor class (answer generation)
│   │                             # - DataQueryEngine class (query execution)
│   │                             # - FastAPI endpoints
│   ├── index.html                # 🎨 Beautified React frontend
│   ├── requirements.txt          # Python dependencies
│   ├── test_gemini.py            # Gemini API test script
│   ├── enhanced_data.py          # Data enhancement utilities
│   └── list_models.py            # List available Gemini models
│
├── test/                         # Test suite
│   ├── test_system.py            # System integration tests
│   ├── test_integrated_system.py # Full API integration tests
│   └── api_tests/                # Individual API test scripts
│       ├── test_apeda_api.py              # APEDA API comprehensive tests
│       ├── test_apeda_categories.py       # APEDA category validation
│       ├── test_rainfall_api.py           # Daily rainfall tests
│       ├── explore_pune_rainfall.py       # Pune rainfall exploration
│       ├── fetch_pune_complete.py         # Pune 2024 complete data
│       ├── test_historical_rainfall.py    # Historical rainfall tests
│       ├── test_punjab_rainfall.py        # Punjab historical data
│       ├── discover_subdivisions.py       # Discover meteorological subdivisions
│       ├── get_subdivisions.py            # Get all subdivision names
│       └── *.csv, *.json                  # Test data outputs
│
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md           # Original architecture notes
│   ├── INDEX.md                  # Documentation index
│   ├── PROJECT_SUMMARY.md        # Project summary
│   ├── QUICKSTART.md             # Quick start guide
│   ├── README (1).md             # Additional README
│   └── SYSTEM_ARCHITECTURE.md    # 📘 This file
│
└── deployment/                   # Deployment configuration
    └── (deployment files)
```

---

## 🔧 Key Components

### DataGovIntegration Class
**Location**: `src/app.py`

**Methods**:
- `__init__(api_key)` - Initialize with data.gov.in API key
- `fetch_crop_production_data()` - Loads district crop data at startup
- `fetch_rainfall_data()` - Loads sample rainfall data
- `fetch_apeda_data(fin_year, category, product_code)` - Fetches APEDA production
- `fetch_daily_rainfall(state, district, year, limit)` - Fetches daily rainfall
- `fetch_historical_rainfall(subdivision, year, limit)` - Fetches historical rainfall
- `_fetch_real_crop_data(limit)` - Internal method for real crop data
- `_get_sample_crop_data()` - Returns sample crop data
- `_get_sample_rainfall_data()` - Returns sample rainfall data

### QueryRouter Class
**Location**: `src/app.py` (Lines 350-475)

**Purpose**: Intelligent API routing using Gemini 1.5 Flash

**Method**:
- `route_query(question)` - Analyzes question and returns API selection parameters

**Returns**:
```python
{
    "states": ["Punjab"],
    "districts": ["Amritsar"],
    "crops": ["rice"],
    "crop_types": ["cereals"],
    "years": ["2023-24"],
    "data_needed": ["apeda_production"],  # The key routing decision
    "comparison_type": "temporal" | "spatial" | "correlation" | None,
    "aggregation": "sum" | "average" | "top" | "trend" | None,
    "apeda_category": "Agri" | "Fruits" | etc. | None,
    "product_code": "1011" | None,
    "rainfall_type": "daily" | "historical" | None
}
```

### DataQueryEngine Class
**Location**: `src/app.py`

**Methods**:
- `__init__(crop_data, rainfall_data, data_gov_integration)`
- `query_crop_production(params)` - Queries district-level crop data (2013-2015)
- `query_apeda(params)` - Queries APEDA state-level data (2019-2024)
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

```properties
# Development Configuration
FASTAPI_ENV=development
DEBUG=True
DATABASE_URL=sqlite:///./test.db

# Gemini AI Keys
SECRET_KEY=your_gemini_api_key_here          # Answer generation
API_GUESSING_MODELKEY=your_gemini_api_key_here  # Query routing

# Data.gov.in API
DATA_GOV_API_KEY=your_data_gov_api_key_here
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
**GET** `/`

Serves the beautified React frontend (`index.html`)

---

## 🎨 Frontend Features

**File**: `src/index.html`

**Features**:
- 💡 Gradient answer boxes with light bulb icon
- 🔢 Large, highlighted numbers (24px bold blue)
- 💚 Green percentages
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

### 1. Activate Virtual Environment:
```bash
cd "C:\Users\Lenovo\Desktop\Project samarth"
.\.venv\Scripts\Activate.ps1
```

### 2. Start Server:
```bash
cd src
python app.py
```

### 3. Access Application:
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

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
- "Show me Punjab rainfall from 1950 to 1960" → Historical Rainfall API
- "Compare rainfall in Punjab and Haryana for last 3 years" → Sample Rainfall

### Complex Queries:
- "Top 3 rice producing districts in Punjab" → District Crop API with aggregation
- "Analyze production trend of wheat in Karnataka" → District Crop API with trend analysis
- "Average annual rainfall in Maharashtra from 1980 to 2000" → Historical Rainfall API

---

## 🔐 Security Notes

- API keys are stored in `.env` file (not committed to git)
- CORS is configured to allow all origins (change in production)
- No authentication required for public endpoints
- Data.gov.in API key has rate limits (10 records per request with sample key)

---

## 📝 Future Enhancements

- [ ] Add more crop-to-product-code mappings
- [ ] Implement caching for frequently asked questions
- [ ] Add authentication for API access
- [ ] Create admin dashboard for monitoring
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
