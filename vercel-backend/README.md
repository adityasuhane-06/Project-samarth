Vercel Backend for Project Samarth

This folder contains a wrapper to run the existing FastAPI app (`src/app.py`) on Vercel serverless using Mangum.

How it works:
- `api/index.py` imports `src.app` and wraps it with `Mangum` to run as an AWS Lambda-compatible handler.
- `requirements.txt` includes `-r ../src/requirements.txt` so it installs your app dependencies plus `mangum`.

Local testing:
1. Install Vercel CLI: `npm i -g vercel`
2. From repo root run: `vercel dev --listen 3000` to run both frontend and backend locally (Vercel will detect both projects if configured).

Deployment:
- Create a Vercel project and set the project root to `vercel-backend` for the backend project.
- Add the environment variables (GEMINI keys, MONGODB_URI, DATA_GOV_API_KEY) in Vercel dashboard for the backend project.
- Deploy: Vercel will install dependencies and expose endpoints under the project domain.

Notes:
- Cold starts are possible. Consider keeping warm or using a small warm-up cron if needed.
- If you encounter import issues, ensure `src` is on the Python path (we add it in `api/index.py`).
