"""
Vercel serverless entry point for FastAPI backend
"""
from mangum import Mangum
import sys
from pathlib import Path

# Add src to Python path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Import the FastAPI app from src
from src.app_modular import app

# Wrap with Mangum for AWS Lambda/Vercel compatibility
handler = Mangum(app, lifespan="off")
