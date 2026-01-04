"""MongoDB cache operations"""
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorClient

from config.settings import settings


class MongoDBCache:
    """Handles MongoDB cache operations"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None # type: ignore
        self.db = None
        self.collection_name = 'query_cache'
    
    async def connect(self) -> bool:
        """Connect to MongoDB Atlas"""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            self.db = self.client[settings.MONGODB_DB_NAME]
            
            # Create indexes for fast lookups
            await self.db[self.collection_name].create_index("query_hash", unique=True)
            await self.db[self.collection_name].create_index("expires_at")
            await self.db[self.collection_name].create_index([("created_at", -1)])
            
            # Test connection
            await self.client.admin.command('ping')
            print(" Connected to MongoDB Atlas successfully!")
            return True
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            print("Continuing without cache (will still work)")
            return False
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client is not None:
            self.client.close()
            print(" Disconnected from MongoDB")
    
    def is_connected(self) -> bool:
        """Check if MongoDB is connected"""
        return self.db is not None
    
    @staticmethod
    def generate_cache_key(query: str) -> str:
        """Generate consistent cache key from query"""
        # Normalize query: lowercase, strip, remove extra spaces
        normalized = ' '.join(query.lower().strip().split())
        return hashlib.md5(normalized.encode()).hexdigest()
    
    async def get_cached_response(self, query_hash: str) -> Optional[Dict[str, Any]]:
        """Check if response exists in cache"""
        if self.db is None:
            return None
        
        try:
            cached = await self.db[self.collection_name].find_one({
                "query_hash": query_hash,
                "expires_at": {"$gt": datetime.now()}  # Not expired
            })
            
            if cached:
                # Update hit count and last accessed
                await self.db[self.collection_name].update_one(
                    {"_id": cached["_id"]},
                    {
                        "$inc": {"hit_count": 1},
                        "$set": {"last_accessed": datetime.now()}
                    }
                )
                print(f" CACHE HIT! Query has been answered {cached.get('hit_count', 0)} times before")
                return cached
            return None
        except Exception as e:
            print(f" Cache lookup error: {e}")
            return None
    
    async def cache_response(self, query_hash: str, query: str, params: dict,
                            answer: str, sources: list, results: dict) -> bool:
        """Store response in cache with TTL"""
        if self.db is None:
            return False
        
        try:
            # Determine expiration based on data type
            ttl_days = self._get_ttl_days(params)
            expires_at = datetime.now() + timedelta(days=ttl_days)
            
            # Upsert to avoid duplicates
            await self.db[self.collection_name].update_one(
                {"query_hash": query_hash},
                {
                    "$set": {
                        "query_hash": query_hash,
                        "original_query": query,
                        "normalized_query": ' '.join(query.lower().strip().split()),
                        "query_params": params,
                        "answer": answer,
                        "data_sources": sources,
                        "raw_results": results,
                        "created_at": datetime.now(),
                        "expires_at": expires_at,
                        "last_accessed": datetime.now()
                    },
                    "$setOnInsert": {
                        "hit_count": 0
                    }
                },
                upsert=True
            )
            
            print(f" Response cached (TTL: {ttl_days} days, expires: {expires_at.strftime('%Y-%m-%d')})")
            return True
        except Exception as e:
            print(f" Cache storage error: {e}")
            return False
    
    def _get_ttl_days(self, params: dict) -> int:
        """ TTL based on data type"""
        data_needed = params.get('data_needed', [])
        
        if 'apeda_production' in data_needed:
            return settings.CACHE_TTL['apeda_production']
        elif 'crop_production' in data_needed:
            return settings.CACHE_TTL['crop_production']
        elif 'historical_rainfall' in data_needed:
            return settings.CACHE_TTL['historical_rainfall']
        elif 'daily_rainfall' in data_needed:
            return settings.CACHE_TTL['daily_rainfall']
        else:
            return settings.CACHE_TTL['default']
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """cache statistics"""
        if self.db is None:
            raise Exception("MongoDB not connected")
        
        total_cached = await self.db[self.collection_name].count_documents({})
        active_cached = await self.db[self.collection_name].count_documents({
            "expires_at": {"$gt": datetime.now()}
        })
        
        # Get cache hits breakdown
        pipeline = [
            {"$match": {"expires_at": {"$gt": datetime.now()}}},
            {"$group": {
                "_id": None,
                "total_hits": {"$sum": "$hit_count"},
                "avg_hits": {"$avg": "$hit_count"},
                "max_hits": {"$max": "$hit_count"}
            }}
        ]
        hit_stats = await self.db[self.collection_name].aggregate(pipeline).to_list(1)
        hits = hit_stats[0] if hit_stats else {"total_hits": 0, "avg_hits": 0, "max_hits": 0}
        
        # Get most popular queries
        popular = await self.db[self.collection_name].find(
            {"expires_at": {"$gt": datetime.now()}},
            {"original_query": 1, "hit_count": 1, "created_at": 1, "_id": 0}
        ).sort("hit_count", -1).limit(10).to_list(10)
        
        # Get recent queries
        recent = await self.db[self.collection_name].find(
            {},
            {"original_query": 1, "hit_count": 1, "created_at": 1, "_id": 0}
        ).sort("created_at", -1).limit(10).to_list(10)
        
        return {
            "total_queries_cached": total_cached,
            "active_cached_queries": active_cached,
            "expired_queries": total_cached - active_cached,
            "cache_hits": {
                "total": hits.get('total_hits', 0),
                "average_per_query": round(hits.get('avg_hits', 0), 2),
                "max_hits_single_query": hits.get('max_hits', 0)
            },
            "top_10_popular_queries": popular,
            "recent_10_queries": recent
        }
    
    async def clear_cache(self) -> int:
        """Clear all cached queries"""
        if self.db is None:
            raise Exception("MongoDB not connected")
        
        result = await self.db[self.collection_name].delete_many({})
        return result.deleted_count
    
    async def delete_expired(self) -> int:
        """Delete expired cache entries"""
        if self.db is None:
            raise Exception("MongoDB not connected")
        
        result = await self.db[self.collection_name].delete_many({
            "expires_at": {"$lt": datetime.now()}
        })
        return result.deleted_count
    
    async def get_simple_stats(self) -> Optional[Dict[str, Any]]:
        """Get simple cache stats for health check"""
        if self.db is None:
            return None
        
        try:
            total_cached = await self.db[self.collection_name].count_documents({})
            active_cached = await self.db[self.collection_name].count_documents({
                "expires_at": {"$gt": datetime.now()}
            })
            
            # Get most popular queries
            popular = await self.db[self.collection_name].find(
                {"expires_at": {"$gt": datetime.now()}},
                {"original_query": 1, "hit_count": 1, "_id": 0}
            ).sort("hit_count", -1).limit(5).to_list(5)
            
            # Calculate total cache hits
            pipeline = [
                {"$match": {"expires_at": {"$gt": datetime.now()}}},
                {"$group": {"_id": None, "total_hits": {"$sum": "$hit_count"}}}
            ]
            hit_stats = await self.db[self.collection_name].aggregate(pipeline).to_list(1)
            total_hits = hit_stats[0]['total_hits'] if hit_stats else 0
            
            return {
                "total_queries_cached": total_cached,
                "active_cached_queries": active_cached,
                "expired_queries": total_cached - active_cached,
                "total_cache_hits": total_hits,
                "top_5_queries": popular
            }
        except Exception as e:
            print(f"Error getting cache stats: {e}")
            return {"error": str(e)}
