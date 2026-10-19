# Database audit

Status: **HIGH / BLOCKER**

Local persistence uses SQLite and SQLAlchemy. PostgreSQL URL configuration exists,
but there are no migrations, production roles, TLS settings, row-level ownership
controls, backup/restore drill, retention policy, or authorization boundary.

`GET /api/v1/simulations` currently exposes records without a user identity. This
must be fixed before production or multi-user deployment.
