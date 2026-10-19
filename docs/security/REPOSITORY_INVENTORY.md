# Repository inventory

Audit date: 2026-10-19.

## Inspected areas

- `frontend/`: React, TypeScript, Vite client and lockfile.
- `backend/`: FastAPI, SQLAlchemy, settings, API schemas, and local SQLite fallback.
- `thermo_composite/`: scientific models, material registry, CLT, reporting, and taxonomy.
- `tests/` and `backend/tests/`: scientific and API regression tests.
- Root documentation, environment templates, generated artifacts, and deployment files.

## Architecture

The local architecture is React/Vite on port 5173, FastAPI/Uvicorn on port 8010,
and SQLite for local persistence. PostgreSQL is supported by configuration but no
production instance or migration system is present. Netlify configuration is
provided for the static frontend; the backend must be hosted separately.

## Sensitive-data locations

No real credentials were found in the scanned source tree. Local `.env` files,
SQLite data, backups, caches, build output, and dependency directories are excluded
from publication. No Git metadata or history exists in this workspace, so history
scanning remains unavailable.

## Existing controls

Pydantic request validation, SQLAlchemy query construction, explicit CORS origins,
password-hashing/token primitives, scientific input validation, source templates,
security headers, and CI checks are present.

## Missing controls

Authentication routes, authorization/ownership, rate limits, production PostgreSQL
migrations and TLS verification, backup restore evidence, Netlify account settings,
GitHub branch protection, and a full production deployment remain unverified.
