# Matching and application state

The skill taxonomy uses word-boundary regular expressions. The score is recognized job skills also found in CV text, divided by recognized job skills. This is reproducible but ignores unrecognized skills and context.

An application belongs to one job, enforced by database uniqueness. Stages are enum values, not a transition graph; users can correct an earlier stage freely. Missing scores are excluded from analytics averages.

SQLAlchemy dependencies let API tests use isolated SQLite stores. The container applies Alembic migrations and CI checks the workflow against PostgreSQL. Add user ownership before supporting multiple users.
