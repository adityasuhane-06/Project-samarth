# Project Samarth - Modular Architecture

## 📁 Project Structure

```
src/
├── app_modular.py          # Main application entry point
├── app.py                  # Old monolithic version (backup)
├── index.html              # Frontend
│
├── config/                 # Configuration module
│   ├── __init__.py
│   └── settings.py         # Environment variables & settings
│
├── models/                 # Pydantic models
│   ├── __init__.py
│   └── api_models.py       # Request/Response models
│
├── database/               # Database operations
│   ├── __init__.py
│   └── mongodb.py          # MongoDB cache operations
│
├── services/               # Business logic
│   ├── __init__.py
│   ├── data_integration.py # External API integration
│   ├── ai_models.py        # Gemini AI models
│   └── query_engine.py     # Query execution engine
│
└── api/                    # API routes
    ├── __init__.py
    └── routes.py           # FastAPI route handlers
```

## 🎯 Module Responsibilities

### `config/`
- **settings.py**: Centralized configuration
  - Environment variables loading
  - API keys management
  - Cache TTL configuration
  - Server settings

### `models/`
- **api_models.py**: Pydantic models
  - QueryRequest
  - QueryResponse
  - HealthResponse

### `database/`
- **mongodb.py**: MongoDB operations
  - Connection management
  - Cache CRUD operations
  - Cache statistics
  - TTL management

### `services/`
- **data_integration.py**: External APIs
  - Data.gov.in integration
  - APEDA API integration
  - Sample data fallbacks

- **ai_models.py**: Gemini AI
  - QueryRouter: Intelligent query routing
  - QueryProcessor: Answer generation

- **query_engine.py**: Data processing
  - Query execution
  - Data filtering & aggregation
  - Multi-source data integration

### `api/`
- **routes.py**: API endpoints
  - Query processing endpoint
  - Health check
  - Cache management
  - Dataset information

## 🚀 Running the Application

### Using the new modular version:
```bash
python app_modular.py
```

### Or with uvicorn:
```bash
uvicorn app_modular:app --reload
```

## ✅ Benefits of Modular Architecture

1. **Separation of Concerns**: Each module has a single responsibility
2. **Maintainability**: Easy to locate and fix bugs
3. **Testability**: Each module can be tested independently
4. **Scalability**: Easy to add new features
5. **Readability**: Clean, organized code structure
6. **Reusability**: Modules can be imported anywhere
7. **Team Collaboration**: Multiple developers can work on different modules

## 📝 Migration Notes

- Old `app.py` kept as backup
- New `app_modular.py` uses all modules
- All functionality preserved
- MongoDB caching fully integrated
- Two-model architecture maintained

## 🔧 Development

### Adding a new data source:
1. Add integration method in `services/data_integration.py`
2. Add query method in `services/query_engine.py`
3. Update routing logic in `services/ai_models.py`

### Adding a new API endpoint:
1. Add route handler in `api/routes.py`
2. Add Pydantic model (if needed) in `models/api_models.py`

### Modifying configuration:
1. Update `config/settings.py`
2. Add to `.env` file if needed
