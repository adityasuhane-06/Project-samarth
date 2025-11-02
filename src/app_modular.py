
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime

# Import modules
from config.settings import settings
from database import MongoDBCache
from services import DataGovIntegration, DataQueryEngine
from api import create_routes


# Data cache
data_cache = {
    'crop_production': None,
    'rainfall': None,
    'last_updated': None
}

# Initialize MongoDB cache
mongodb_cache = MongoDBCache()

# Initialize data integration
data_integration = DataGovIntegration()


def load_data():
    """Load and cache data from data.gov.in"""
    global data_cache
    
    print("Loading data from data.gov.in...")
    data_cache['crop_production'] = data_integration.fetch_crop_production_data()
    data_cache['rainfall'] = data_integration.fetch_rainfall_data()
    data_cache['last_updated'] = datetime.now()
    print(f"Data loaded successfully. Crop records: {len(data_cache['crop_production'])}, "
          f"Rainfall records: {len(data_cache['rainfall'])}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load data and connect to MongoDB on startup"""
    print("\n" + "="*60)
    print("APPLICATION STARTUP")
    print("="*60)
    
    # Connect to MongoDB
    await mongodb_cache.connect()
    
    # Load data
    load_data()
    print("="*60 + "\n")
    
    yield
    
    # Cleanup
    await mongodb_cache.disconnect()


# Create FastAPI application
app = FastAPI(
    title="Project Samarth API", 
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Note: Query engine will be created after data is loaded
# Create and register all API routes (query_engine is passed but created on-demand)
def get_query_engine():
    """Get query engine with loaded data"""
    return DataQueryEngine(
        data_cache['crop_production'],
        data_cache['rainfall'],
        data_integration
    )

create_routes(app, data_cache, mongodb_cache, get_query_engine)


@app.get("/")
async def root():
    """Serve the index.html file"""
    return FileResponse("index.html")


if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT', 8000))
    uvicorn.run(
        "app_modular:app", 
        host="0.0.0.0", 
        port=port,
        reload=False
    )
