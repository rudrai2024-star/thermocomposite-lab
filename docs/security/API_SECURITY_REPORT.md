# API security report

| Surface | Status | Evidence / remaining risk |
|---|---|---|
| Health and catalog GET endpoints | PARTIAL | Pydantic response models and explicit CORS; no authentication or rate limit |
| Compatibility metadata | PARTIAL | Explicit model/family rejection; catalog metadata is not user-owned |
| Simulation POST | PARTIAL | Server-side validation and bounded laminate count; no auth, quota, timeout, or ownership |
| Simulation history GET | FAIL | Returns persisted records without authentication or ownership checks |

Security headers and explicit methods/origins are configured. Production
request-size limits, rate limiting, authentication, authorization, and structured
redacted audit logging remain incomplete.
