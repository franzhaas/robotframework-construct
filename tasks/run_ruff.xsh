uv lock
uv sync --extra test

assert "All checks passed!" in $(uv run ruff check src)
