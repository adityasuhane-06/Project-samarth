from mangum import Mangum

# Try importing the app from the existing src.app
try:
    import sys
    from pathlib import Path
    # Add project root so we can import src
    ROOT = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(ROOT))
    from src.app import app
except Exception as e:
    # Fallback: create a minimal FastAPI app for health-check
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/api/health")
    def health():
        return {"status": "ok", "detail": f"Fallback app (import error: {e})"}

# Create Mangum handler to run FastAPI under Lambda (Vercel serverless)
handler = Mangum(app)
