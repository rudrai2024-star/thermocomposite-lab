# Dependency audit

`npm audit --omit=dev` found 2 moderate advisories, 0 high, and 0 critical.
Both affect React Router 6.x ranges below 7.18.0. No unreviewed major upgrade
was applied.

Python `pip-audit` was unavailable locally, so no Python audit pass is claimed.
Dependencies are bounded in the existing requirement files, but a Python lockfile
and CI Python audit remain needed.
