# Project Samarth - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (React Frontend - index.html)                │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Question   │  │   Sample     │  │   Results    │        │
│  │   Input      │  │   Questions  │  │   Display    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP POST /api/query
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK API SERVER                           │
│                        (app.py)                                 │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │         Query Processing Pipeline                     │     │
│  │                                                       │     │
│  │  1. Receive Question                                 │     │
│  │  2. Extract Parameters (via Claude AI)              │     │
│  │  3. Execute Query on Data                            │     │
│  │  4. Generate Answer (via Claude AI)                  │     │
│  │  5. Return with Citations                            │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐          │
│  │   Query     │  │    Data      │  │   Answer    │          │
│  │  Processor  │  │   Query      │  │  Generator  │          │
│  │             │  │   Engine     │  │             │          │
│  └─────────────┘  └──────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
┌─────────────────┐  ┌─────────────┐  ┌──────────────────┐
│  Claude AI API  │  │ Data Cache  │  │  data.gov.in     │
│  (Anthropic)    │  │             │  │  Integration     │
│                 │  │ - Crop Data │  │                  │
│ - Parameter     │  │ - Rainfall  │  │ - Fetch Data     │
│   Extraction    │  │             │  │ - Transform      │
│ - Answer        │  │             │  │ - Normalize      │
│   Generation    │  │             │  │                  │
└─────────────────┘  └─────────────┘  └──────────────────┘
                                               │
                                               │
                    ┌──────────────────────────┴────────────────────┐
                    │                                               │
                    ▼                                               ▼
    ┌──────────────────────────────┐        ┌──────────────────────────────┐
    │   Ministry of Agriculture    │        │  India Meteorological Dept   │
    │   Crop Production Data       │        │  Rainfall Data               │
    │   data.gov.in                │        │  data.gov.in                 │
    └──────────────────────────────┘        └──────────────────────────────┘
```

## Component Details

### 1. Frontend (index.html)
**Technology**: React (via CDN)
**Responsibilities**:
- User input collection
- Display of sample questions
- Real-time query submission
- Results rendering with citations
- Error handling

**Key Features**:
- Clean, modern UI with gradient design
- Mobile responsive
- Loading states
- Source citation display
- API key management

### 2. Backend API Server (app.py)
**Technology**: Flask + Python
**Responsibilities**:
- Request handling
- Query orchestration
- Data management
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

#### Stage 1: Parameter Extraction
**Component**: QueryProcessor.extract_query_parameters()
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
- Uses Claude AI with structured prompting
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
**Component**: QueryProcessor.generate_answer()
**Input**: Query results + sources
**Output**: Natural language answer with citations

**How it works**:
- Uses Claude AI for synthesis
- Incorporates all relevant data points
- Generates citations for each claim
- Formats for readability

## Data Flow Example

### Query: "Compare rice production in Punjab and Haryana for 2022-23"

1. **User Input** → Frontend sends POST to `/api/query`

2. **Parameter Extraction** → Claude AI extracts:
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

4. **Answer Generation** → Claude AI synthesizes:
   ```
   Punjab produced 2,277,000 tonnes of rice in 2022-23 across 4 major 
   districts, while Haryana produced 1,468,000 tonnes. [Source: District-wise 
   Crop Production Statistics]
   
   Punjab's rice production is 55% higher than Haryana's...
   ```

5. **Response** → Returns JSON with answer, sources, raw data

## Key Design Decisions

### 1. Two-Stage NLP Processing
**Why**: Separating parameter extraction from answer generation improves accuracy
- First stage: Structured understanding (parameters)
- Second stage: Natural language synthesis (answer)
- Benefits: Debugging, testing, accuracy

### 2. Data Schema Normalization
**Why**: Different ministries use different formats
- Internal unified schema
- Consistent field names
- Easy to add new sources

### 3. Source Traceability
**Why**: Critical for government/policy use
- Every data point has source
- Direct links to data.gov.in
- Full transparency

### 4. Caching Strategy
**Why**: Performance and API rate limits
- Data loaded on startup
- Cached in memory
- Refresh on demand

### 5. Stateless API
**Why**: Scalability and simplicity
- No session management
- Each request independent
- Easy to deploy multiple instances

## Scalability Considerations

### Current Design
- Single-server deployment
- In-memory caching
- Good for: Demo, small deployments

### Production Enhancements
1. **Database Layer**: PostgreSQL for persistent storage
2. **Redis Cache**: Distributed caching
3. **Load Balancing**: Multiple API servers
4. **Background Jobs**: Periodic data refresh
5. **API Gateway**: Rate limiting, authentication

## Security Considerations

### Data Privacy
- No user data stored
- API keys used per-session only
- Can run in air-gapped environment

### Data Integrity
- Direct source citations
- Immutable data references
- Audit trail possible

## Extensibility

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

### Optimization Opportunities
- Parallel Claude API calls (extraction + generation)
- Streaming responses
- Pre-computed aggregations
- Query result caching

## Technology Stack

### Backend
- **Python 3.8+**: Core language
- **Flask 3.0**: Web framework
- **Pandas 2.1**: Data manipulation
- **Anthropic SDK**: Claude AI integration

### Frontend
- **React 18**: UI framework
- **Vanilla CSS**: Styling
- **Fetch API**: HTTP requests

### AI/ML
- **Claude Sonnet 4.5**: Latest Anthropic model
- Used for NLP, parameter extraction, answer synthesis

## Deployment Options

### Option 1: Local Development
```bash
python app.py
open index.html
```

### Option 2: Docker Container
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

### Option 3: Cloud Deployment
- AWS: Elastic Beanstalk or EC2
- Google Cloud: App Engine or Cloud Run
- Azure: App Service
- Frontend: Any static hosting (S3, Netlify, Vercel)

## Future Roadmap

### Phase 1 (Current): MVP
✅ Basic Q&A functionality
✅ Two datasets integrated
✅ Source citations
✅ Demo-ready

### Phase 2: Enhanced Features
- Real-time data.gov.in API integration
- More datasets (soil, market prices, schemes)
- Advanced visualizations
- Query history

### Phase 3: Production Ready
- Authentication system
- Rate limiting
- Monitoring & logging
- Automated testing
- API documentation

### Phase 4: Advanced Analytics
- Predictive modeling
- Trend forecasting
- Policy impact simulation
- Custom report generation

## Conclusion

This architecture provides:
- ✅ End-to-end functionality
- ✅ Source traceability
- ✅ Extensibility
- ✅ Deployability in secure environments
- ✅ Practical for real-world use

The system demonstrates how AI can make government data accessible through natural language while maintaining accuracy and transparency.
