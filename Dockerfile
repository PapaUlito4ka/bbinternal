FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock /app/
COPY src /app/

#ENV PATH="/app/.venv/bin:$PATH"

RUN uv sync --no-dev --frozen --no-install-project

RUN uv pip freeze > requirements.txt

RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "manage", "migrate"]

CMD ["python3", "-m", "manage", "runserver", "0.0.0.0:8000"]
