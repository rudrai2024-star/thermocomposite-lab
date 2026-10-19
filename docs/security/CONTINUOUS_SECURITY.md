# Continuous security

`.github/workflows/ci.yml` runs on pull requests, protected-branch pushes, and a
weekly schedule. It runs backend/scientific tests, frontend typecheck/build,
high-severity npm audit, and a narrow secret-pattern scan.

It does not replace manual privacy, authorization, infrastructure, backup/recovery,
or deployment-gate review. GitHub branch protection and required checks must be
configured and verified in the actual repository.
