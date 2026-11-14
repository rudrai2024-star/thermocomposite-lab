# 13 — Testing and Quality Assurance

Tests cover scientific core (CLT, models, simulation), backend routes/testing/quantity/research/ingestion, and frontend API URL/request behavior.

Backend command used an isolated SQLite database:

```sh
DATABASE_URL=sqlite:////private/tmp/thermocomposite-documentation-audit-20261114.db .venv/bin/pytest -q -p no:cacheprovider tests backend/tests -k 'not test_thermal_analysis_comparison_and_export_artifacts'
```

**Result: 83 passed, 1 deselected.** The excluded thermal export test writes files in `Graphs/generated`, so it was not run under the documentation-only constraint. One Starlette deprecation warning concerns TestClient/httpx integration.

Frontend `npm test`: **5 passed, 0 failed**. No package installation or build was run. These results are software checks, not experiment validation, accuracy measurements, or standards conformance. No browser end-to-end, populated-research, live PostgreSQL, or production deployment test was performed; no coverage percentage was collected.
