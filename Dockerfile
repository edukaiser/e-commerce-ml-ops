# ==========================================
# Estágio 1: Builder
# ==========================================
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends curl git && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /usr/local/bin/uvx

WORKDIR /app
COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --frozen || uv sync --no-dev

COPY . /app/

# Garante que a pasta models exista no builder (mesmo que vazia) para evitar erro no COPY
RUN mkdir -p /app/models


# ==========================================
# Estágio 2: Runtime (API FastAPI)
# ==========================================
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

# Cria o diretório de destino
RUN mkdir -p /app/models

# Agora a cópia não vai falhar porque a pasta foi criada no builder
COPY --from=builder /app/models/ /app/models/

ENV PATH="/app/.venv/bin:$PATH"
COPY . /app/

EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]