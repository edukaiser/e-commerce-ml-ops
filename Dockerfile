# ==========================================
# Estágio 1: Builder (Instalação de dependências com uv)
# ==========================================
FROM python:3.12-slim AS builder

# Instala o utilitário curl e o uv oficial
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /usr/local/bin/uvx

WORKDIR /app

# Copia os arquivos de configuração de dependências
COPY pyproject.toml ./

# Instala as dependências de produção no virtualenv do projeto (.venv)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --frozen || uv sync --no-dev

# ==========================================
# Estágio 2: Runtime (Imagem final limpa)
# ==========================================
FROM python:3.12-slim

WORKDIR /app

# Copia o ambiente virtual gerado no builder
COPY --from=builder /app/.venv /app/.venv

# Configura o PATH para usar o ambiente virtual do uv por padrão
ENV PATH="/app/.venv/bin:$PATH"

# Copia o restante do código fonte e configurações para dentro do container
COPY . /app/

# Define o comando padrão para rodar o pipeline completo via DVC
CMD ["uv", "run", "dvc", "repro"]