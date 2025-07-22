FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock /app/
COPY src /app/

RUN uv sync --no-dev --frozen --no-install-project

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "manage.py", "migrate"]

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
