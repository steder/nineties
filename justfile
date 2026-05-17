# Nineties — cross-platform task runner.
# Recipes prefer `uv run`, `docker compose`, and `gh` over raw shell so they work on Win/Mac/Linux.
# Run `just` (no args) to list available recipes.

set shell := ["bash", "-cu"]
set dotenv-load := true

# Default recipe: list everything.
default:
    @just --list --unsorted

# --- Dev environment ---

# Bring up the local Compose stack (Librarian + Postgres + AudioBookShelf + Caddy).
dev:
    docker compose up -d
    @echo "Librarian: http://localhost:8000"
    @echo "AudioBookShelf: http://localhost:13378"

# Tear down the local stack.
down:
    docker compose down

# Tail logs from all services.
logs:
    docker compose logs -f

# --- Tests ---

# Unit + property + integration tests; target under 60s.
test:
    uv run pytest -m "not e2e and not bdd and not slow"

# Gherkin user-journey scenarios.
bdd:
    uv run pytest -m bdd

# End-to-end: Alexa request replay + Playwright browser E2E.
e2e:
    uv run pytest -m e2e

# Single happy-path smoke run, ~10s. The agent's "did I break anything obvious" check.
smoke:
    uv run pytest -m smoke

# Hypothesis property tests only (useful when iterating on the policy engine).
property:
    uv run pytest -m property

# --- Quality gates ---

# Lint (no fixes).
lint:
    uv run ruff check .

# Apply formatting (Python + justfile).
fmt:
    uv run ruff format .
    uv run ruff check --fix-only .
    just --fmt --unstable

# Type check.
typecheck:
    uv run pyright

# Everything CI runs.
ci: lint typecheck test

# --- Setup helpers ---

# Install pre-commit hooks.
install-hooks:
    uv run pre-commit install

# Install Playwright browser binaries (needed once after `uv sync`).
install-playwright:
    uv run playwright install --with-deps chromium
