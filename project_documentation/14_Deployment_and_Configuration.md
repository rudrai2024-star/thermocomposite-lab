# 14 — Deployment and Configuration

Local backend startup:

```sh
.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8011
```

Vite development is configured on `127.0.0.1:5175` with `/api/v1` proxy to that backend. Frontend runs via `npm run dev -- --host 127.0.0.1 --port 5175`. `netlify.toml` builds and publishes the React frontend with SPA fallback; it does not host FastAPI. Root `app.py` is a separate legacy Streamlit app.

API origin handling supports same-origin and validated explicit origin. Backend deployment must be configured separately with matching CORS and durable storage. Environment setting names include database URL, CORS origins, environment mode, and session/secret settings; no values are reproduced here. SQLite is suitable for local use, not by itself a production backup/multi-user plan. Export artifact persistence requires an explicit deployment strategy.
