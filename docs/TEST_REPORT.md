# Test report

Last verified locally on 2026-10-19:

- `.venv/bin/pytest -q tests backend/tests`: 16 passed, one existing Starlette/httpx deprecation warning.
- `cd frontend && npm run typecheck`: passed.
- `cd frontend && npm run build`: passed.
- `npm audit --omit=dev --audit-level=high`: no high/critical advisories; two
  moderate React Router advisories remain and are documented as a release
  limitation.
- A fresh isolated FastAPI process returned HTTP 200 for `/api/v1/health` and
  emitted `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, and
  `Permissions-Policy`.
- Production configuration rejected a short `SECRET_KEY` before startup.
- GitHub Actions YAML parsed successfully and the local credential-pattern scan
  passed.

Responsive browser checks used representative viewports 320×568, 375×667,
768×1024, 1024×768, and 1440×900. The thermal route rendered at each size
without horizontal document overflow. At 375×667, the mobile navigation opened
as a 320px drawer and closed through Escape; navigation locking was released
after dismissal. These are emulated viewport checks, not coverage of every
physical device.

The endpoint tests cover taxonomy metadata and an explicitly blocked
ceramic-matrix/CLT combination. External deployment, PostgreSQL, GitHub history,
and physical-device verification remain outside this local test run.
