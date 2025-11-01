"""API route handlers"""
from fastapi import HTTPException, APIRouter
from typing import Dict, Any, Callable
from datetime import datetime

from models import QueryRequest, QueryResponse, HealthResponse
from services import QueryRouter, QueryProcessor, DataQueryEngine
from database import MongoDBCache
from config.settings import settings


def create_routes(app, data_cache: dict, mongodb_cache: MongoDBCache, get_query_engine: Callable):
    """Create and configure all API routes"""
    
    router = APIRouter()
    
    @router.post("/api/query", response_model=QueryResponse)
    async def process_query(request: QueryRequest):
        """
        Main endpoint for processing natural language queries about agricultural data.
        Uses two-model architecture with MongoDB caching.
        """
        try:
            print(f"\n{'='*60}")
            print(f"DEBUG: NEW QUERY RECEIVED")
            print(f"DEBUG: Question: {request.question}")
            print(f"{'='*60}\n")
            
            if not request.question:
                raise HTTPException(status_code=400, detail="No question provided")
            
            # STEP 0: Check MongoDB cache
            query_hash = mongodb_cache.generate_cache_key(request.question)
            print(f"💾 STEP 0: CHECKING CACHE (key: {query_hash[:12]}...)")
            
            cached = await mongodb_cache.get_cached_response(query_hash)
            if cached:
                print(f"⚡ RETURNING CACHED RESPONSE (saved ~3-4 seconds!)")
                return {
                    'question': request.question,
                    'answer': cached['answer'],
                    'data_sources': cached['data_sources'],
                    'query_params': cached['query_params'],
                    'raw_results': cached.get('raw_results', {})
                }
            
            print(f"❌ Cache miss. Processing query from scratch...")
            
            # Get API keys
            routing_api_key = settings.GEMINI_ROUTING_KEY
            answer_api_key = request.api_key or settings.GEMINI_API_KEY
            
            if not routing_api_key or not answer_api_key:
                raise HTTPException(
                    status_code=400, 
                    detail="Gemini API keys required. Set SECRET_KEY and API_GUESSING_MODELKEY in .env file."
                )
            
            # STEP 1: Route the query
            print("\n🔀 STEP 1: ROUTING QUERY TO CORRECT APIs...")
            router_model = QueryRouter(routing_api_key)
            params = router_model.route_query(request.question)
            print(f"✅ Routing complete. APIs to use: {params.get('data_needed', [])}")
            
            # STEP 2: Execute query on data
            print("\n📊 STEP 2: FETCHING DATA FROM APIs...")
            query_engine = get_query_engine()  # Get query engine with loaded data
            results, sources = query_engine.execute_query(params)
            print(f"✅ Data fetched. Results size: {len(str(results))} chars, Sources: {len(sources)}")
            
            # STEP 3: Generate natural language answer
            print("\n💡 STEP 3: GENERATING NATURAL LANGUAGE ANSWER...")
            processor = QueryProcessor(answer_api_key)
            answer = processor.generate_answer(request.question, results, sources)
            print(f"✅ Answer generated: {answer[:100]}...")
            
            # STEP 4: Cache the response
            print("\n💾 STEP 4: CACHING RESPONSE FOR FUTURE USE...")
            await mongodb_cache.cache_response(query_hash, request.question, params, answer, sources, results)
            
            return {
                'question': request.question,
                'answer': answer,
                'data_sources': sources,
                'query_params': params,
                'raw_results': results
            }
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"\nDEBUG: ERROR in process_query: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/api/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint with cache statistics"""
        cache_stats = None
        mongodb_connected = mongodb_cache.is_connected()
        
        if mongodb_connected:
            try:
                cache_stats = await mongodb_cache.get_simple_stats()
            except Exception as e:
                print(f"Error getting cache stats: {e}")
                cache_stats = {"error": str(e)}
        
        return {
            'status': 'healthy',
            'data_loaded': data_cache['crop_production'] is not None,
            'last_updated': data_cache['last_updated'].isoformat() if data_cache['last_updated'] else None,
            'crop_records': len(data_cache['crop_production']) if data_cache['crop_production'] is not None else 0,
            'rainfall_records': len(data_cache['rainfall']) if data_cache['rainfall'] is not None else 0,
            'mongodb_connected': mongodb_connected,
            'cache_stats': cache_stats
        }
    
    @router.get("/api/datasets")
    async def get_datasets():
        """Get information about available datasets"""
        return {
            'datasets': [
                {
                    'name': 'District-wise Crop Production Statistics',
                    'source': 'Ministry of Agriculture & Farmers Welfare',
                    'url': 'https://www.data.gov.in/catalog/district-wise-season-wise-crop-production-statistics',
                    'description': 'District, crop, season and year wise data on crop area and production',
                    'fields': ['State_Name', 'District_Name', 'Crop_Year', 'Season', 'Crop', 'Area', 'Production']
                },
                {
                    'name': 'Rainfall in India',
                    'source': 'India Meteorological Department (IMD)',
                    'url': 'https://www.data.gov.in/catalog/rainfall-india',
                    'description': 'State-wise and sub-division wise rainfall data',
                    'fields': ['State', 'Year', 'Annual_Rainfall', 'Monsoon_Rainfall']
                }
            ]
        }
    
    @router.get("/api/cache/stats")
    async def get_cache_stats():
        """Get detailed cache statistics"""
        if not mongodb_cache.is_connected():
            raise HTTPException(status_code=503, detail="MongoDB not connected")
        
        try:
            return await mongodb_cache.get_cache_stats()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting cache stats: {str(e)}")
    
    @router.post("/api/cache/clear")
    async def clear_cache(confirm: bool = False):
        """Clear all cached queries (requires confirmation)"""
        if not mongodb_cache.is_connected():
            raise HTTPException(status_code=503, detail="MongoDB not connected")
        
        if not confirm:
            return {
                "message": "Are you sure? This will delete all cached queries.",
                "hint": "Add ?confirm=true to the URL to confirm deletion"
            }
        
        try:
            deleted_count = await mongodb_cache.clear_cache()
            return {
                "message": "Cache cleared successfully",
                "deleted_count": deleted_count
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")
    
    @router.delete("/api/cache/expired")
    async def delete_expired_cache():
        """Delete expired cache entries"""
        if not mongodb_cache.is_connected():
            raise HTTPException(status_code=503, detail="MongoDB not connected")
        
        try:
            deleted_count = await mongodb_cache.delete_expired()
            return {
                "message": "Expired cache entries deleted successfully",
                "deleted_count": deleted_count
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting expired cache: {str(e)}")
    
    @router.get("/api/")
    async def api_root():
        """API root endpoint"""
        return {
            "message": "Project Samarth API - FREE VERSION (Gemini) with MongoDB Caching",
            "version": "1.0.0",
            "ai_model": "Google Gemini 2.5 Flash (FREE)",
            "cache": "MongoDB Atlas" if mongodb_cache.is_connected() else "Disabled",
            "docs": "/docs",
            "health": "/api/health"
        }
    
    # Include all routes in the app
    app.include_router(router)
    
    return app
