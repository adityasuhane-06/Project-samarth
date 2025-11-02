# 🌾 Project Samarth - Intelligent Agricultural Data Q&A System

> **An advanced AI-powered system for querying Indian agricultural data with two-model architecture and MongoDB caching**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)](https://www.mongodb.com/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5--flash-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Overview

Project Samarth is a production-ready intelligent Q&A system that makes Indian agricultural data accessible through natural language queries. It features a sophisticated **two-model AI architecture** for optimal query routing and answer generation, combined with **MongoDB caching** for lightning-fast response times (135x faster on cache hits).

### ✨ Key Features

- 🤖 **Two-Model AI Architecture** - Separate models for routing and answer generation
- ⚡ **MongoDB Caching** - 135x performance improvement with intelligent caching
- 📊 **Multi-Source Data Integration** - 5 data sources spanning 1901-2024
- 🏗️ **Modular Architecture** - Clean, maintainable, team-ready codebase
- 🔍 **Source Traceability** - Every answer includes citations
- 🚀 **Production Ready** - FastAPI, async operations, health monitoring

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- MongoDB Atlas account (free tier)
- Google Gemini API keys (2 keys recommended)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/project-samarth.git
cd project-samarth
```

2. **Install Python dependencies**
```bash
pip install -r src/requirements.txt
```

3. **Configure environment**
```bash
# Create .env file in project root
cp .env.example .env
# Edit .env with your credentials
```

4. **Run the backend server**
```bash
cd src
python app_modular.py
```

5. **Verify backend is working**
```bash
# Health check
curl http://localhost:8000/api/health

# Cache statistics
curl http://localhost:8000/api/cache/stats
```

### Frontend Setup

1. **Navigate to frontend folder**
```bash
cd frontend
```

2. **Install Node dependencies**
```bash
npm install
```

3. **Create frontend .env**
```bash
cp .env.example .env
# Default: VITE_API_URL=http://localhost:8000
```

4. **Start development server**
```bash
npm run dev
```

5. **Open in browser**
```
http://localhost:3000
```

---

## 📊 System Architecture

### Two-Model Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Query                            │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────▼──────────────┐
        │   STEP 0: MongoDB Cache   │
        │   (0.1s if cached)        │
        └────────────┬──────────────┘
                     │ Cache Miss
        ┌────────────▼──────────────┐
        │   STEP 1: QueryRouter     │
        │   (Model 1 - Routing)     │
        │   gemini-2.5-flash        │
        └────────────┬──────────────┘
                     │
        ┌────────────▼──────────────┐
        │   STEP 2: Data Fetching   │
        │   (5 Data Sources)        │
        └────────────┬──────────────┘
                     │
        ┌────────────▼──────────────┐
        │   STEP 3: QueryProcessor  │
        │   (Model 2 - Answers)     │
        │   gemini-2.5-flash        │
        └────────────┬──────────────┘
                     │
        ┌────────────▼──────────────┐
        │   STEP 4: Cache Response  │
        │   (MongoDB - 180-365 days)│
        └────────────┬──────────────┘
                     │
                   Result
```

### Modular Structure

```
src/
├── app_modular.py          # Main entry point (105 lines)
├── config/                 # Configuration management
│   └── settings.py         # Environment & API keys
├── models/                 # Pydantic API models
│   └── api_models.py       # Request/Response schemas
├── database/               # MongoDB operations
│   └── mongodb.py          # Caching logic
├── services/               # Business logic
│   ├── ai_models.py        # Two Gemini models
│   ├── data_integration.py # External API integration
│   └── query_engine.py     # Query execution
└── api/                    # API endpoints
    └── routes.py           # FastAPI routes
```

---

## 💾 Data Sources

| Source | Period | Type | Records |
|--------|--------|------|---------|
| **Crop Production** | 2013-2015 | District-level | 100+ |
| **APEDA Production** | 2019-2024 | State-level | Real-time API |
| **Daily Rainfall** | 2019-2024 | District-wise | Real-time API |
| **Historical Rainfall** | 1901-2015 | State-wise | Real-time API |
| **Sample Data** | Current | Fallback | 8 records |

---

## 🎯 Example Queries

### Production Queries
```bash
# Recent data (APEDA)
"What is the rice production in Punjab for 2023?"

# Historical data
"Show wheat production in Karnataka for 2014"

# Comparison
"Compare maize production across states"
```

### Rainfall Queries
```bash
# Recent rainfall
"Show rainfall in Pune for 2024"

# Historical trends
"Punjab rainfall from 1950 to 1960"

# Pattern analysis
"Compare monsoon patterns across regions"
```

### Multi-Source Queries
```bash
# Cross-dataset
"Compare rice in 2014 and 2023"

# Correlation
"How does rainfall affect crop yield?"
```

---

## 🔌 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/query` | Process natural language query |
| GET | `/api/health` | Health check + cache stats |
| GET | `/api/datasets` | Available dataset information |

### Cache Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cache/stats` | Detailed cache statistics |
| POST | `/api/cache/clear?confirm=true` | Clear all cached queries |
| DELETE | `/api/cache/expired` | Delete expired entries |

### Example Request

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the rice production in Punjab for 2023?"
  }'
```

### Example Response

```json
{
  "question": "What is the rice production in Punjab for 2023?",
  "answer": "Based on APEDA data for 2023-24, Punjab produced 14,356 tonnes...",
  "data_sources": [
    {
      "dataset": "APEDA Production Statistics",
      "source": "APEDA - Ministry of Commerce",
      "url": "https://agriexchange.apeda.gov.in/"
    }
  ],
  "query_params": {
    "states": ["Punjab"],
    "crops": ["rice"],
    "years": ["2023-24"],
    "data_needed": ["apeda_production"]
  }
}
```

---

## ⚡ Performance

### Cache Performance
- **First Query (Cache Miss)**: 13-30 seconds
- **Cached Query (Cache Hit)**: 0.1 seconds
- **Improvement**: **135x faster** 🚀

### Cache Statistics Example
```json
{
  "total_queries_cached": 2,
  "active_cached_queries": 2,
  "cache_hits": {
    "total": 3,
    "average_per_query": 1.5
  }
}
```

---

## 🛠️ Configuration

### Environment Variables

Create a `.env` file:

```env
# Gemini API Keys (Get from https://aistudio.google.com/app/apikey)
SECRET_KEY=your_gemini_api_key_for_answers
API_GUESSING_MODELKEY=your_gemini_api_key_for_routing

# MongoDB (Get from https://www.mongodb.com/cloud/atlas)
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/agri_qa_cache

# Data.gov.in API (Get from https://data.gov.in/catalogs)
DATA_GOV_API_KEY=your_data_gov_api_key_here
USE_REAL_API=true

# Server Configuration
PORT=8000
DEBUG=True
```

### Cache TTL Configuration

| Data Type | TTL | Reason |
|-----------|-----|--------|
| APEDA Production | 180 days | Updated annually |
| Crop Production | 365 days | Historical data |
| Historical Rainfall | 365 days | Unchanging data |
| Daily Rainfall | 90 days | Recent data |

---

## 📚 Documentation

Comprehensive documentation available in the `docs/` folder:

- **[INDEX.md](docs/INDEX.md)** - Documentation hub
- **[QUICKSTART.md](docs/QUICKSTART.md)** - 5-minute setup guide
- **[MODULAR_ARCHITECTURE.md](docs/MODULAR_ARCHITECTURE.md)** - Complete module guide
- **[MONGODB_CACHING.md](docs/MONGODB_CACHING.md)** - Caching system details
- **[COMPARISON_REPORT.md](docs/COMPARISON_REPORT.md)** - Feature parity analysis
- **[TWO_MODEL_TEST_REPORT.md](docs/TWO_MODEL_TEST_REPORT.md)** - Testing results

---

## 🧪 Testing

### Run Tests
```bash
python test_system.py
```

### Manual Testing
```bash
# Test imports
cd src
python -c "from config import settings; print('✅ Config OK')"
python -c "from models import QueryRequest; print('✅ Models OK')"
python -c "from database import MongoDBCache; print('✅ Database OK')"
python -c "from services import QueryRouter; print('✅ Services OK')"

# Test health endpoint
curl http://localhost:8000/api/health

# Test query (first time - cache miss)
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is rice production in Punjab for 2023?"}'

# Test query again (cache hit - 135x faster!)
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is rice production in Punjab for 2023?"}'

# Check cache stats
curl http://localhost:8000/api/cache/stats
```

---

## 🔧 Development

### Project Structure
```
project-samarth/
├── src/                    # Backend source code
│   ├── app_modular.py     # Modular version (recommended)
│   ├── app.py             # Monolithic version (backup)
│   ├── config/            # Configuration
│   ├── models/            # API models
│   ├── database/          # MongoDB operations
│   ├── services/          # Business logic
│   ├── api/               # API routes
│   └── requirements.txt   # Python dependencies
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components (9)
│   │   ├── services/      # API client
│   │   ├── utils/         # Helpers & formatters
│   │   ├── App.jsx        # Main app component
│   │   └── main.jsx       # Entry point
│   ├── index.html
│   ├── package.json       # Node dependencies
│   ├── vite.config.js     # Vite configuration
│   └── tailwind.config.js # Tailwind CSS config
├── docs/                  # Documentation
├── test/                  # Test files
├── deployment/            # Deployment configs
├── .env                   # Environment variables
└── README.md             # This file
```

### Adding a New Feature

1. **New Data Source**: Extend `services/data_integration.py`
2. **New API Endpoint**: Add to `api/routes.py`
3. **New Configuration**: Update `config/settings.py`
4. **New Model**: Add to `models/api_models.py`

---

## 🚀 Deployment

### Docker (Recommended)
```bash
docker build -t project-samarth .
docker run -p 8000:8000 --env-file .env project-samarth
```

### Manual Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Run with production settings
cd src
uvicorn app_modular:app --host 0.0.0.0 --port 8000 --workers 4
```

### Health Check for Load Balancer
```
GET /api/health
```

---

## 📈 Roadmap

- [ ] Add more data sources (soil, weather, market prices)
- [ ] Implement user authentication
- [ ] Add GraphQL API
- [ ] Add real-time data streaming
- [ ] Implement ML predictions
- [ ] Add multi-language support

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Ensure all tests pass

---

## 🎨 Frontend Features

The React frontend includes:

- **Modern UI** with Tailwind CSS
- **Modular Components** (9 reusable components)
- **Responsive Design** works on all devices
- **Real-time Stats** from backend
- **Smooth Animations** and transitions
- **Answer Formatting** with syntax highlighting
- **Sample Questions** for quick testing
- **Error Handling** with user-friendly messages

### Frontend Components

```
src/components/
├── Header.jsx           # App header with badges
├── ServerStats.jsx      # Live statistics cards
├── SampleQuestions.jsx  # Quick query buttons
├── QueryForm.jsx        # Input form with validation
├── LoadingSpinner.jsx   # Loading animation
├── ErrorMessage.jsx     # Error display
├── ResultDisplay.jsx    # Result container
├── AnswerBox.jsx        # Formatted answer display
└── DataSources.jsx      # Data sources with links
```

### Frontend Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Lightning-fast build tool (5-10x faster than webpack)
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - Promise-based HTTP client
- **ESLint** - Code quality tool

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Data Sources**: data.gov.in, APEDA
- **AI Models**: Google Gemini AI
- **Database**: MongoDB Atlas
- **Framework**: FastAPI

---

## 📞 Support

- **Documentation**: [docs/INDEX.md](docs/INDEX.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/project-samarth/issues)
- **Email**: your.email@example.com

---

## 📊 Project Statistics

- **Total Lines of Code**: ~1,300 (modular)
- **Documentation**: 20,000+ words
- **API Endpoints**: 8
- **Data Sources**: 5
- **Test Coverage**: Coming soon
- **Performance Improvement**: 135x with caching

---

## 🏆 Features Highlights

✅ **Two-Model AI Architecture**  
✅ **MongoDB Caching (135x faster)**  
✅ **5 Data Sources (1901-2024)**  
✅ **Modular & Maintainable Code**  
✅ **Production Ready**  
✅ **Comprehensive Documentation**  
✅ **RESTful API**  
✅ **Source Traceability**  

---

**Built with ❤️ for Indian Agriculture**

*Making agricultural data accessible through AI*
