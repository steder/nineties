# Nineties — cross-platform task runner.
# Recipes prefer `uv run`, `docker compose`, and `gh` over raw shell so they work on Win/Mac/Linux.
# Run `just` (no args) to list available recipes.
#
# All Python-side recipes cd into librarian/ since that's where pyproject.toml lives.

set shell := ["bash", "-cu"]
set dotenv-load := true

# Default recipe: list everything.
default:
    @just --list --unsorted

# --- Dev environment ---

# Bring up the local Compose stack (Postgres + AudioBookShelf).
# Librarian runs on the host — see `just serve`.
dev:
    docker compose up -d
    @echo ""
    @echo "Services up:"
    @echo "  Postgres:       127.0.0.1:5432"
    @echo "  AudioBookShelf: http://localhost:13378"
    @echo ""
    @echo "Start the Librarian on host in another terminal:  just serve"

# Run the Librarian Django dev server on the host (against the dockerized DB).
serve:
    cd librarian && uv run python manage.py runserver 127.0.0.1:8000

# Tear down the local stack.
down:
    docker compose down

# Tail logs from all services.
logs:
    docker compose logs -f

# --- Tests ---

# Unit + property + integration tests; target under 60s.
test:
    cd librarian && uv run pytest -m "not e2e and not bdd and not slow"

# Gherkin user-journey scenarios.
bdd:
    cd librarian && uv run pytest -m bdd

# End-to-end: Alexa request replay + Playwright browser E2E.
e2e:
    cd librarian && uv run pytest -m e2e

# Single happy-path smoke run, ~10s. The agent's "did I break anything obvious" check.
smoke:
    cd librarian && uv run pytest -m smoke

# Hypothesis property tests only (useful when iterating on the policy engine).
property:
    cd librarian && uv run pytest -m property

# Django manage.py passthrough — `just manage migrate`, `just manage createsuperuser`, etc.
manage *args:
    cd librarian && uv run python manage.py {{args}}

# Django system check.
check:
    cd librarian && uv run python manage.py check

# --- Quality gates ---

# Lint (no fixes).
lint:
    cd librarian && uv run ruff check .

# Apply formatting (Python + justfile).
fmt:
    cd librarian && uv run ruff format .
    cd librarian && uv run ruff check --fix-only .
    just --fmt --unstable || true

# Type check.
typecheck:
    cd librarian && uv run pyright

# Everything CI runs.
ci: lint typecheck test

# --- Setup helpers ---

# Sync Python deps (use after editing pyproject.toml).
sync:
    cd librarian && uv sync

# Install pre-commit hooks.
install-hooks:
    cd librarian && uv run pre-commit install

# Install Playwright browser binaries (needed once after `uv sync`).
install-playwright:
    cd librarian && uv run playwright install --with-deps chromium

# Generate silent .m4b fixture audiobooks for AudioBookShelf to scan.
# Uses a small static-linked ffmpeg Docker image so no system ffmpeg needed.
fixtures:
    python3 fixtures/catalog/generate.py
