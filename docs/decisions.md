# Engineering decisions

## Accepted baseline

A deterministic taxonomy makes scoring explainable. SQLAlchemy dependencies allow isolated API tests. Database uniqueness protects against duplicate applications, and Alembic migrations read the same environment configuration as the app.

## Testing strategy

Keep deterministic domain tests separate from HTTP/database integration and real model demos. Unit-test stubs are never presented as model evidence. Capture actual responses and preserve the commands needed to reproduce them.

## Tradeoffs

The taxonomy does not infer synonyms, assess experience quality, or predict hiring outcomes. There is no authentication, multi-user isolation, PDF CV parser, or LLM integration. Create an application before analyzing a CV to persist its score. Keep this local when using personal information.

## Next steps

Add authenticated user ownership, German-language skill normalization, pagination, and an evaluated optional semantic matcher.
