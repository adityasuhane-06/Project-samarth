"""Pydantic models for API requests and responses"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class QueryRequest(BaseModel):
    """Request model for query endpoint"""
    question: str
    api_key: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the rice production in Punjab for 2022?"
            }
        }


class QueryResponse(BaseModel):
    """Response model for query endpoint"""
    question: str
    answer: str
    data_sources: List[Dict[str, str]]
    query_params: Dict[str, Any]
    raw_results: Dict[str, Any]


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    data_loaded: bool
    last_updated: Optional[str]
    crop_records: int
    rainfall_records: int
    mongodb_connected: bool = False
    cache_stats: Optional[Dict[str, Any]] = None
