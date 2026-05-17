# Librarian — dev container.
# Built from ./librarian and run via docker-compose.yml. Source is volume-mounted
# in dev, so this image is essentially "Python 3.14 + uv + all our deps". A
# production-shaped image (multi-stage, no dev deps, no source mount) is a
# separate concern, taken on when v0.1 ships.

FROM python:3.14-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:${PATH}"

# uv: fast, modern Python package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# System deps needed at runtime (libpq for psycopg; ffmpeg later if we transcode)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install deps first (cached) using only pyproject + lockfile.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Source is volume-mounted in dev; in CI/production the COPY below seeds the
# image with the current tree.
COPY . .

EXPOSE 8000

# In dev, docker-compose overrides this with `manage.py runserver`. In CI/prod
# we use uvicorn against ASGI.
CMD ["uv", "run", "uvicorn", "librarian.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
