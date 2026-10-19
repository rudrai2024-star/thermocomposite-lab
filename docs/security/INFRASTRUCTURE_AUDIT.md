# Infrastructure audit

Status: **INCOMPLETE**

`netlify.toml` defines the frontend build, SPA fallback, and baseline response
headers. Netlify account settings, deploy-preview access, HTTPS enforcement,
environment variables, and the production backend origin were not accessible.

FastAPI remains a separately hosted service. No public backend, container image,
TLS terminator, production network policy, or PostgreSQL deployment was verified.
