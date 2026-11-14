# 02 — Complete Technology Stack

## Frontend

React 18, TypeScript, Vite, React Router 6, `lucide-react`, and project-owned CSS. API communication is centralized in `frontend/src/api/client.ts`, with origin logic in `api-url.mjs`. State is handled in React components/context; no separate Redux-like store was identified. Charts and diagrams are custom SVG/HTML, not a chart package. No dedicated form-validation, upload, or report-export package is evident. Thermal UI includes browser SVG-to-PNG handling.

## Backend and scientific code

Python, FastAPI, Pydantic/Pydantic Settings, SQLAlchemy, Alembic, and Uvicorn. NumPy supports calculations; the legacy Streamlit interface also uses Pandas and Plotly. Pytest/HTTPX support tests; `pypdf` is declared for parsing. PostgreSQL driver support is declared, but the audited live local data path is SQLite. `pwdlib`/Argon2 and `itsdangerous` helper code exists without connected HTTP authentication.

## Build and deployment

Frontend scripts cover Vite development, TypeScript/Vite build, and Node's built-in test runner. `netlify.toml` builds/publishes the frontend and provides SPA fallback. Root `app.py` is a distinct Streamlit application. No backend hosting manifest, Docker deployment, or CI workflow was identified. Exact dependency ranges are in frontend manifests/lockfile and requirements files; declared ranges are not claims about all installed versions.
