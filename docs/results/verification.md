# Verification status

Local Windows execution on 7 September 2026 passed 5 tests with 96% statement coverage. Ruff lint, formatting, and source compilation passed. Raw reports are in this directory.

The live demo created one fictional application, moved it to Interview, and returned an **80% skill overlap**: four of five listed skills matched, with PostgreSQL missing. The analytics endpoint returned the same saved score. This is a skill-overlap result, not an ATS acceptance prediction.

Docker and PostgreSQL execution were unavailable locally. GitHub Actions container verification is pending publication; this record will be updated after an actual run.

The test output retains upstream Starlette/httpx deprecation warnings; no tests were skipped because of them.
