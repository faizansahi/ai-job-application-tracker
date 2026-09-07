# Verification status

Local Windows execution on 7 September 2026 passed 5 tests with 96% statement coverage. Ruff lint, formatting, and source compilation passed. Raw reports are in this directory.

The live demo created one fictional application, moved it to Interview, and returned an **80% skill overlap**: four of five listed skills matched, with PostgreSQL missing. The analytics endpoint returned the same saved score. This is a skill-overlap result, not an ATS acceptance prediction.

Docker was unavailable on the local Windows machine. Docker Compose and PostgreSQL 16 were verified successfully on a GitHub-hosted Ubuntu runner.

[Successful CI run 34070945054](https://github.com/faizansahi/ai-job-application-tracker/actions/runs/34070945054) passed both the quality and containers jobs. The run includes dependency resolution, lint, formatting, tests, Compose validation, image build, container execution, and PostgreSQL checks.

The container created a fictional job and application, calculated and persisted its matching score, changed its stage, and queried analytics using PostgreSQL.

[Downloaded container execution artifact](docker-demo.json) preserves the actual results from that run. These artifacts are separate from the local SQLite demo.

The test output retains upstream Starlette/httpx deprecation warnings; no tests were skipped because of them.
