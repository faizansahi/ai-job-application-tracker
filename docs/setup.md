# Setup

## Local execution

Use Python 3.12+ and a separate virtual environment. Install `python -m pip install -e ".[dev,demo]"`. Copy `.env.example` to `.env` only when customizing defaults; settings are read at process startup.

```bash
uvicorn job_tracker.main:app --reload
```

The default database is local SQLite.

## Reproduce evidence

Use a fresh database and a running API:

```bash
python scripts/demo_workflow.py
```

The script saves actual JSON in `docs/results/` and output visuals in `docs/images/`. Rerunning replaces the saved demo artifacts. Swagger screenshots were captured from running Uvicorn servers with a headless browser.

## PostgreSQL and Docker

Set a unique URL-safe `POSTGRES_PASSWORD` in your ignored `.env`. Compose requires it and supplies the internal connection URL. Start with `docker compose up --build`. Persistent volumes survive ordinary `docker compose down`.

The container applies Alembic migrations before Uvicorn. Outside Docker, set the database URL and run `alembic upgrade head` explicitly to use the versioned schema.

## Validate

```bash
ruff format --check .
ruff check .
pytest --cov=job_tracker --cov-report=term-missing
python -m pip check
```

See [verification status](results/verification.md) for environment limits and CI evidence. No paid API credentials are required.
