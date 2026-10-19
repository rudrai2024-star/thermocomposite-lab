# Task ledger

| ID | Description | Priority | Status | Evidence |
|---|---|---:|---|---|
| MAT-001 | Material records and physical validation | P0 | verified with provenance limitation | `tests/test_models.py`; uncited estimates remain documented |
| MOD-001 | Scalar thermal and effective-property models | P0 | verified | `tests/test_models.py`; directional CTE fix |
| CLT-001 | Plane-stress Classical Laminate Theory | P0 | verified | `tests/test_clt.py`; independent A-matrix and thermal checks |
| APP-001 | Simulation orchestration and reports | P0 | verified | `tests/test_simulation.py`; units/source/author metadata |
| UI-001 | Streamlit interface | P1 | verified with responsive gap | Live browser workflow on port 8503 |
| APP-002 | User-facing validation and attribution | P0 | verified | Unsupported models are labeled; non-finite laminate inputs are rejected; footer/report name verified |
| QA-001 | Automated numerical verification | P0 | verified | 11 passed with plain `.venv/bin/pytest`; `pytest.ini` makes imports reproducible |
| AUD-001 | Acceptance audit and critical/high fixes | P0 | verified with documented gaps | `ACCEPTANCE_AUDIT.md` |
| API-001 | Typed API integration | P1 | verified for current foundation | FastAPI health, materials, simulation, and persisted simulation-list endpoints; frontend route workflows use the API |
| OPS-001 | Reproducible deployment files and docs | P1 | verified | `requirements.txt`, `README.md` |
| MIG-001 | React/FastAPI migration foundation | P0 | in progress | Distinct React pages, persisted simulation history, and explicit taxonomy/model compatibility metadata; frontend build and 16 backend/scientific tests pass |
| MAT-002 | Extensible material taxonomy and model registry | P0 | in progress | Added family, architecture, model, and compatibility metadata; catalog-only categories remain disabled until data/models exist |
| UI-002 | Responsive adaptive workspace | P1 | verified with viewport scope | Added mobile drawer keyboard dismissal, touch-sized controls, overflow guards, adaptive grids, and responsive form/result layouts |
| SEC-001 | 14-check pre-deployment security audit | P0 | blocked by high findings | `docs/security/SECURITY_AUDIT.md`; auth, authorization, production infrastructure, and database controls remain incomplete |

## Verified acceptance run

- Date: 2026-10-18
- App: `http://localhost:8503/` returned HTTP 200 and rendered the dashboard and
  `Rudrajyoti Paul` footer attribution.
- Tests: `.venv/bin/pytest -q` -> **11 passed**.
- Compilation: `.venv/bin/python -m py_compile app.py thermo_composite/*.py tests/*.py`
  completed successfully.
- Scientific probes: free expansion returns no restrained stress; aluminium/silicon
  carbide rejects CLT; non-finite ply inputs reject; JSON metadata contains the author.

## Remaining incomplete items

- Material records remain traceable only to explicit engineering-estimate statements,
  not publication or supplier citations.
- React pages are now distinct and functional for material browsing, validated builder input,
  thermal simulation, laminate simulation, persisted reports, and comparison. Authentication,
  authorization, true saved material configurations, report-file downloads, and production
  PostgreSQL deployment remain incomplete.
- Material taxonomy metadata now covers eight composite/configuration families and seven
  architectures. Live API verification returned 8 families, 7 architectures, and 5 models;
  ceramic-matrix CLT was explicitly rejected.
- Hypothetical/custom material combinations are intentionally not implemented.
- Responsive/mobile browser coverage remains limited to representative emulated
  viewports, not physical devices.
- Authentication, authorization, simulation ownership/IDOR protection, password
  recovery, request rate limits, calculation resource limits, privacy/retention
  controls, PostgreSQL migrations/RLS/backups, and report-file downloads remain
  incomplete.
- The frontend dependency audit reports two moderate React Router advisories;
  the CI gate currently rejects high and critical advisories but does not upgrade
  across the breaking React Router major-version change.
- `pip-audit` is not installed, so Python dependency vulnerability scanning has
  not been independently completed.
- Netlify configuration is syntactically present and the local build succeeds,
  but no external Netlify, backend, PostgreSQL, TLS, DNS, or GitHub repository
  settings have been verified.

## Latest security regression verification

- `.venv/bin/pytest -q tests backend/tests`: **16 passed**, one existing
  Starlette/httpx deprecation warning.
- `cd frontend && npm run typecheck`: **passed**.
- `cd frontend && npm run build`: **passed**.
- `npm audit --omit=dev --audit-level=high`: reports **2 moderate** React Router
  advisories and no high/critical advisories.
- Fresh isolated FastAPI process: health **200** with
  `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, and
  `Permissions-Policy` headers.
- Production settings reject a short secret before startup.
- CI workflow YAML parses; the local credential-pattern scan passes after
  excluding safe `*.example` templates.
