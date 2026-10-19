# Deployment gate

Decision: **NO-GO**

Unresolved blockers:

- Authentication routes and enforced sessions are absent.
- Simulation history has no ownership or authorization boundary.
- Production PostgreSQL migrations, roles, TLS, backups, and restore evidence are absent.
- Backend hosting and Netlify account configuration are unverified.
- Two moderate React Router advisories remain.
- Python dependency audit and Git-history scan were unavailable.

The Netlify configuration and local build are not evidence of a secure production
deployment.
