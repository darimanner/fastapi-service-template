# fastapi-service-template

[Copier](https://copier.readthedocs.io/) template for FastAPI services on Python 3.14, managed with [uv](https://docs.astral.sh/uv/).

## What you get

- `src/` layout with an app factory, liveness and readiness routes
- async SQLAlchemy 2 on PostgreSQL (asyncpg): declarative `Base` with a constraint naming convention, `TimestampMixin`, a `get_db` session dependency
- typed nested settings (`pydantic-settings`, `SECTION__KEY` env vars) that exit with a readable message on bad config
- structlog logging: JSON by default, console output with `LOGGER__DEBUG=true`, secrets masked, a request id and an access log line per request
- RFC 7807 error responses (`application/problem+json`) for `AppError` subclasses, HTTP errors, request validation and unexpected exceptions
- `pyproject.toml` with project metadata, dev dependencies, pytest and ruff config
- ruff limits on function and class size: complexity, branches, statements, arguments, locals, nesting, public methods
- `uv.lock` for the default dependency set
- `.python-version` pinned to 3.14
- strict mypy over `src`, `tests` and `migrations`
- `.pre-commit-config.yaml` with ruff, mypy, a uv lock check and basic file hygiene hooks
- Alembic migrations configured in `pyproject.toml`, new revisions formatted by ruff
- tests on pytest-asyncio with a real PostgreSQL from testcontainers: the schema is built by the migrations, `alembic check` fails the run on model drift, every test is rolled back
- `compose.yaml` with PostgreSQL 18 for local development
- multi-stage `Dockerfile` on uv: non-root user, healthcheck, no dev dependencies
- a GitHub Actions workflow that runs the pre-commit hooks, the tests and the image build

## Usage

```bash
uvx copier copy gh:darimanner/fastapi-service-template my-service
cd my-service
uv sync
cp .env.example .env
docker compose up -d --wait
uv run alembic upgrade head
uv run fastapi dev src/main.py
```

Copier asks for the project name, description and author. To pull later template changes into a generated project, run `uvx copier update` inside it.

## Generated layout

```
my-service/
  .github/workflows/ci.yml
  migrations/
  src/
    api/health.py
    config/settings.py
    core/db/
    core/exceptions/
    core/observability/
    main.py
  tests/
  .dockerignore
  .env.example
  .pre-commit-config.yaml
  .python-version
  compose.yaml
  Dockerfile
  pyproject.toml
  uv.lock
```

## Why Copier

Unlike Cookiecutter, Copier can update projects generated from an older version of the template, so every service stays on a shared baseline.
