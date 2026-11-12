# fastapi-service-template

[Copier](https://copier.readthedocs.io/) template for FastAPI services on Python 3.14, managed with [uv](https://docs.astral.sh/uv/).

## What you get

- `src/` layout with typed settings (`pydantic-settings`) and a health route
- `pyproject.toml` with project metadata, dev dependencies, pytest and ruff config
- ruff limits on function and class size: complexity, branches, statements, arguments, locals, nesting, public methods
- `uv.lock` for the default dependency set
- `.python-version` pinned to 3.14
- strict mypy over `src` and `tests`
- `.pre-commit-config.yaml` with ruff, mypy, a uv lock check and basic file hygiene hooks
- a smoke test for the health route

## Usage

```bash
uvx copier copy gh:darimanner/fastapi-service-template my-service
cd my-service
uv sync
uv run fastapi dev src/main.py
```

Copier asks for the project name, description and author. To pull later template changes into a generated project, run `uvx copier update` inside it.

## Generated layout

```
my-service/
  src/
    api/health.py
    config/settings.py
    main.py
  tests/test_health.py
  .env.example
  .pre-commit-config.yaml
  .python-version
  pyproject.toml
  uv.lock
```

## Why Copier

Unlike Cookiecutter, Copier can update projects generated from an older version of the template, so every service stays on a shared baseline.
