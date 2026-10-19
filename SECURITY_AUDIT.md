# ThermoComposite Lab pre-deployment security audit

Audit date: 2026-10-18  
Guide: `Downloads/Complete_Pre_Deployment_Security_Audit_Guide.pdf`  
Scope: migrated `frontend/`, `backend/`, preserved scientific engine, and deployment
configuration currently present in the workspace.

This is an evidence record, not a security certification. The migration is not yet
production-ready because authentication, authorization, database deployment, and
several operational controls remain incomplete.

| # | Check | Evidence | Status | Risk / required action |
|---|---|---|---|---|
| 01 | Secret leak prevention | Redacted source scan found no private-key, cloud-key, token, or credential-pattern matches. `.env.example` files contain placeholders and `.gitignore` excludes local env files. No Git history exists in this workspace to inspect. | PASS with limitation | Run Gitleaks/history scanning after the project is placed in version control. |
| 02 | Personal data and privacy | Current backend persists simulation request/result JSON only. No user profile deletion, privacy notice, retention policy, or third-party telemetry policy is implemented. | INCOMPLETE | Define retention/deletion and privacy handling before collecting account data. |
| 03 | Authentication security | Password hashing and signed-token primitives exist in `backend/auth.py`, but no registration, login, refresh/revocation, MFA, reset, or session endpoints are wired. Frontend auth buttons are placeholders. | HIGH / BLOCKER | Implement and test complete auth flows, secure cookies or bearer handling, expiry, lockout/rate limits, and reset controls. |
| 04 | Authorization and IDOR | Simulation records are stored without authenticated ownership and there are no user/role/ownership checks or report retrieval endpoints. | HIGH / BLOCKER | Add identities, ownership constraints, role policy, and authorization tests before exposing persisted data. |
| 05 | API security | FastAPI validation and restricted method CORS are present. No rate limits, request correlation, security headers, webhook verification, or authenticated API boundary is implemented. | INCOMPLETE | Add production middleware, rate limiting, request-size limits, and authenticated endpoint policy. |
| 06 | Input, injection, and file security | SQLAlchemy parameterization and Pydantic validation are used. No file upload or URL-fetch feature exists. Non-finite scientific input guards are covered by legacy tests. | PASS for current surface | Add explicit payload size limits and fuzz/property tests before expansion. |
| 07 | Production and infrastructure | Local HTTP works. No production Dockerfiles, TLS termination, hardened headers, non-root container, or deployment manifest exists. | HIGH / BLOCKER | Add and verify production deployment configuration and HTTPS boundary. |
| 08 | Dependency and supply chain | `npm audit --audit-level=high --omit=dev` initially reported three high findings. React Router was updated to exact `6.30.6`; the repeat audit now reports two moderate advisories that require a future major-version decision. Python dependencies are version-bounded but no lockfile or pip-audit report exists. | INCOMPLETE | Resolve the remaining moderate advisory without an unreviewed breaking upgrade, add lock/update policy, and scan container/CI dependencies. |
| 09 | Database security | SQLAlchemy supports PostgreSQL and local SQLite fallback. No production PostgreSQL instance, least-privilege role, TLS requirement, encryption, RLS, backup/restore test, or migration tool is configured. | HIGH / BLOCKER | Add Alembic migrations, restricted roles, TLS, backups, restore evidence, and ownership/RLS policy. |
| 10 | AI/LLM security | No AI/LLM integration exists. | N/A | Re-audit if AI features are introduced. |
| 11 | Abuse and business logic | Scientific fraction/temperature/model validation exists. No account abuse controls, quotas, replay protection, or workflow authorization exists. | INCOMPLETE | Add authenticated quotas, rate limits, and abuse tests with the product policy. |
| 12 | Monitoring, backup, and incident readiness | A verified pre-migration backup exists at `.backups/thermocomposite-pre-react-20261018-222816.tar.gz`. No structured audit logging, alerts, rotation, recovery runbook, or restore drill exists. | INCOMPLETE | Configure redacted structured logs, alerting, rotation, and tested recovery. |
| 13 | AI-generated code verification | Combined legacy and backend tests pass: **14 passed**. Frontend typecheck/build pass. Browser smoke checks covered the existing Streamlit app, not full migrated workflows. | PASS with scope limitation | Add frontend component/E2E tests and backend auth/database integration tests. |
| 14 | Final deployment gate | Frontend production build passes and backend tests pass, but checks 03, 04, 07, and 09 are unresolved high blockers. | FAIL / do not deploy | Complete blockers and repeat the full audit in a production-like environment. |

## Current verification evidence

- Legacy scientific and backend tests: `14 passed, 1 warning`.
- Frontend `npm run typecheck`: passed.
- Frontend `npm run build`: passed.
- Production dependency audit: the initial high React Router findings were removed by
  pinning `react-router`/`react-router-dom` to `6.30.6`; the repeat audit reports two
  moderate advisories and no high findings.
- Verified source backup: `.backups/thermocomposite-pre-react-20261018-222816.tar.gz`.

## Migration status

The React/FastAPI work is a validated foundation, not a complete replacement yet.
The old Streamlit implementation and scientific package remain intentionally present
until the high blockers and full end-to-end workflows are implemented and verified.
