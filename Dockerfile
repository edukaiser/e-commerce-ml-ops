# ==========================================
# Estágio 1: Builder / Treinamento
# ==========================================
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends curl git && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /usr/local/bin/uvx

WORKDIR /app
COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --frozen || uv sync --no-dev

# Copia o código para rodar o pipeline e gerar o modelo
COPY . /app/
# Se o seu pipeline DVC gera o modelo, execute-o aqui:
# RUN uv run dvc repro  (ou execute diretamente o script de treino que gera models/recommender_model.pt)

# ==========================================
# Estágio 2: Runtime (API FastAPI)
# ==========================================
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
# Copia a pasta models gerada/treinada no estágio anterior
COPY --from=builder /app/models /app/models

ENV PATH="/app/.venv/bin:$PATH"
COPY . /app/

EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]