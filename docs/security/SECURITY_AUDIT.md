# Security audit summary

Audit date: 2026-10-19. Statuses reflect local evidence and unavailable external access.

| Check | Status | Primary finding |
|---|---|---|
| 01 Secret Leak Prevention | PASS with limitation | No local secret found; no Git history available |
| 02 Personal Data & Privacy Audit | INCOMPLETE | No ownership, retention, deletion, or privacy workflow |
| 03 Authentication Security | HIGH / BLOCKER | Auth primitives exist; routes and enforcement do not |
| 04 Authorization & IDOR Audit | HIGH / BLOCKER | Simulation records are not user-owned |
| 05 API Security Audit | PARTIAL | Validation/CORS/headers verified locally; auth/rate limits absent |
| 06 Input, Injection & File Security | PASS for current surface | No uploads; SQLAlchemy and scientific validation used |
| 07 Production & Infrastructure Security | INCOMPLETE | Netlify config/build verified locally; actual accounts/backend/TLS unverified |
| 08 Dependency & Supply-Chain Security | INCOMPLETE | 2 moderate npm advisories; pip-audit unavailable |
| 09 Database Security Audit | HIGH / BLOCKER | Local SQLite fallback; no migrations/roles/RLS/restore evidence |
| 10 AI / LLM Security Audit | NOT APPLICABLE | No AI/LLM functionality exists |
| 11 Abuse & Business Logic Audit | INCOMPLETE | Input bounds exist; rate/quotas/timeouts absent |
| 12 Monitoring, Backup & Incident Readiness | INCOMPLETE | Local backup exists; restore/alerts/rotation unverified |
| 13 AI-Generated Code Verification | PARTIAL | 16 backend tests, frontend typecheck/build, config guards, headers, and CI YAML pass; manual production controls remain |
| 14 Final Deployment Gate | NO-GO | High blockers and missing external evidence |
