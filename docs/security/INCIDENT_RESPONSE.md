# Incident response

Before production, define owners and contact paths for credential compromise,
unauthorized simulation access, abusive calculation traffic, and deployment
compromise.

Minimum response sequence:

1. Preserve redacted logs and identify the affected release.
2. Revoke or rotate exposed credentials and invalidate sessions.
3. Restrict backend/database access and preserve an approved backup.
4. Assess affected records without copying sensitive data into tickets.
5. Patch, test, and redeploy only after the deployment gate is re-evaluated.

No production alerting, session revocation, restore drill, or rollback runbook is
currently configured; those remain pre-launch actions.
