
import os
import pathlib
from dotenv import load_dotenv


class Settings:
    
    def __init__(self):
        # Load environment variables from .env file in parent directory
        env_path = pathlib.Path(__file__).parent.parent.parent / '.env'
        print(f"DEBUG: Looking for .env file at: {env_path}")
        print(f"DEBUG: .env file exists: {env_path.exists()}")
        load_dotenv(dotenv_path=env_path)
        
        # API Keys
        self.GEMINI_API_KEY = os.getenv('SECRET_KEY')
        self.GEMINI_ROUTING_KEY = os.getenv('API_GUESSING_MODELKEY')
        self.DATA_GOV_API_KEY = os.getenv('DATA_GOV_API_KEY')
        
        # MongoDB Configuration
        self.MONGODB_URL = os.getenv('DATABASE_URL')
        self.MONGODB_DB_NAME = 'project_samarth'
        
        # API Configuration
        self.USE_REAL_API = os.getenv('USE_REAL_API', 'false').lower() == 'true'
        
        # Server Configuration
        self.HOST = "0.0.0.0"
        self.PORT = int(os.getenv('PORT', 8000))
        self.DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
        
        # Cache TTL Configuration (in days)
        self.CACHE_TTL = {
            'apeda_production': 180,  # 6 months
            'crop_production': 365,   # 1 year
            'historical_rainfall': 365,  # 1 year
            'daily_rainfall': 90,     # 3 months
            'default': 90             # Default 3 months
        }
        
        self._validate()
    
    def _validate(self):
        """Validate required settings"""
        if self.GEMINI_API_KEY:
            print(f"DEBUG: Main API Key loaded: {self.GEMINI_API_KEY[:20]}...")
        else:
            print("DEBUG: WARNING - No main API key found in environment!")
        
        if self.GEMINI_ROUTING_KEY:
            print(f"DEBUG: Routing API Key loaded: {self.GEMINI_ROUTING_KEY[:20]}...")
        else:
            print("DEBUG: WARNING - No routing API key found in environment!")
        
        if self.MONGODB_URL:
            print(f"DEBUG: MongoDB URL configured")
        else:
            print("DEBUG: WARNING - No MongoDB URL found in environment!")


# Singleton instance
settings = Settings()
