# AGENTS.md

Copier template for FastAPI services. Everything under `template/` is rendered into the generated project. Files at the repository root belong to the template itself and are never copied.

## Layout

- `copier.yml`: questions and Copier settings (`_subdirectory: template`)
- `template/`: project payload. Files ending in `.jinja` are rendered, the rest are copied as is
- `template/uv.lock.jinja`: lock file with the project name templated, generated (see below)
- `template/{{ _copier_conf.answers_file }}.jinja`: answers file that makes `copier update` work

## Rules

- Python 3.14, uv, ruff, pytest, pre-commit. Keep `requires-python`, `.python-version` and the lock file in step.
- Generated code stays minimal and comment free: no example business logic.
- Templates use only the answers defined in `copier.yml`. Every new question needs a default so `--defaults` keeps working.
- Never edit `template/uv.lock.jinja` by hand. Regenerate it after any dependency change in `template/pyproject.toml.jinja`.
- Bump the pre-commit hook revisions together with the matching dev dependencies.

## Verify a change

Render the template into a temporary directory and run the generated project's checks:

```bash
uvx copier copy --defaults --vcs-ref HEAD . /tmp/render
cd /tmp/render
uv sync --locked
uv run ruff check . && uv run ruff format --check .
uv run pytest
git init -q && git add -A && uv run pre-commit run --all-files
```

`--vcs-ref HEAD` includes uncommitted changes of the template.

## Regenerate the lock file

```bash
uvx copier copy --defaults --vcs-ref HEAD --data project_name=lock-placeholder . /tmp/lock
(cd /tmp/lock && uv lock --upgrade)
sed 's/^name = "lock-placeholder"$/name = "{{ project_name }}"/' /tmp/lock/uv.lock > template/uv.lock.jinja
```

Then run the verification above.

## Commits

Imperative mood, subject line under 72 characters, everything in English.
