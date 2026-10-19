# Remediation log

## 2026-10-19

- Added `.gitignore` exclusions for backups, build output, and TypeScript artifacts.
- Corrected the PostgreSQL placeholder in `backend/.env.example`; no real
  credential was present.
- Added production settings validation requiring a long secret, PostgreSQL, and
  explicit CORS origins.
- Added baseline backend security headers.
- Added Netlify build, SPA fallback, and response-header configuration.
- Added least-privilege CI checks for tests, build, dependency audit, and secret
  patterns.
- Added redacted security inventory and evidence reports.

No credentials were revoked because no real credentials were found. No external
repository, Netlify account, database, or deployment settings were changed.
