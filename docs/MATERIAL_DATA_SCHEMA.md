# Material data schema

The current runtime registry contains immutable composite records with explicit
constituent labels, scalar properties in SI units, temperature range, source
statement, family, architecture/form, status, and supported model names.

The backend currently persists simulation records in SQLAlchemy. Normalized
constituent/property/provenance tables and versioned PostgreSQL migrations are
not yet implemented; SQLite remains the local fallback. This is a known
migration blocker, not hidden functionality.
