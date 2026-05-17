# Instructions for Claude Code (and future AI sessions)

This file is the operating manual for any AI agent working on this codebase. Keep it short, current, and honest. Update it when stack choices change.

## What this project is

A libre / OSS curation layer over existing media servers, giving parents fine-grained content curation and library-style scarcity, and giving kids agency within those bounds. See [`README.md`](./README.md) for the elevator pitch and [`plans/0001-v0.1.0-audiobook-library.md`](./plans/0001-v0.1.0-audiobook-library.md) for the architecture.

## Stack (current)

- **Python** 3.14 (managed by `uv`)
- **Web framework**: Django 5.x — the parent UI leans heavily on Django admin
- **DB**: PostgreSQL 18.x with `pgvector` and native `tsvector` full-text search (GIN indexes)
- **API surface** (later, if needed): `django-ninja`
- **Background jobs**: `django-q2`
- **Lint / format**: `ruff` + `ruff-format`
- **Types**: `pyright` with `django-stubs`
- **Tests**: `pytest`, `pytest-django`, `Hypothesis`, `factory-boy`, `syrupy`, `pytest-bdd`, `pytest-playwright`, `testcontainers`
- **Task runner**: `just` (cross-platform — recipe bodies prefer `uv run` / `docker compose` / `gh` over raw shell)
- **Container orchestration**: Docker Compose
- **Media backend (v1)**: AudioBookShelf (Docker)
- **Voice adapter (v1)**: Alexa custom skill, developer mode, hosted via Cloudflare Tunnel

## Repository conventions

- **Plans live in `plans/`**, ADR-numbered (`0001-...`, `0002-...`). Each has YAML frontmatter (`status`, `target_version`, `phase`). `plans/index.md` is the living roadmap.
- **Requirements live in `requirements/`** — evergreen "what must be true" docs (privacy, accessibility, safety, license posture). Not time-bounded.
- **Commit messages reference plan numbers**: `refs plan/0001`, `closes plan/0001`.
- **No `.env` files committed.** `.env.example` is the source of truth for required vars.
- **Migrations**: every PR that adds a migration must explain the migration plan in the PR description (zero-downtime considerations, backfill strategy if applicable).
- **AGPL-3.0 license.** Dependency licenses must be AGPL-compatible. Document any GPL-incompatible service we *call* (vs. link) in `requirements/license-posture.md`.

## Pluggable boundaries — do not violate

Two abstractions exist specifically to enable future swaps. Do not leak concrete implementation details into core code.

- **`librarian/voice/adapter.py`** defines the abstract `VoiceAdapter`. The Alexa implementation lives in `librarian/voice/alexa/`. Core code (`policy`, `loans`, `catalog`) must not import anything from `voice/alexa/`.
- **`librarian/media/backend.py`** defines the abstract `MediaBackend`. The AudioBookShelf implementation lives in `librarian/media/abs.py`. Core code must not import anything from `media/abs.py`.

If you find yourself wanting to add an Alexa-specific field to a core model, stop and add it to the voice adapter's per-adapter state table instead.

## Just recipes (the agent's hands)

| Recipe              | What it does                                              |
|---------------------|-----------------------------------------------------------|
| `just dev`          | Bring up the local Compose stack                          |
| `just test`         | Unit + property + integration tests; under 60s target     |
| `just bdd`          | Gherkin user-journey scenarios only                       |
| `just e2e`          | Alexa replay + Playwright browser E2E against a live stack|
| `just smoke`        | Single happy-path run, ~10s; use before claiming "done"   |
| `just lint`         | `ruff` check                                              |
| `just fmt`          | `ruff format` + `just --fmt`                              |
| `just typecheck`    | `pyright`                                                 |
| `just ci`           | Everything CI runs (lint + typecheck + test)              |
| `just install-hooks`| Install pre-commit hooks                                  |

**Before claiming a task is done**, an agent should run at minimum `just lint` and `just smoke`. For changes that touch policy, loans, voice, or media, also run `just test`.

## Test layering

| Layer          | When to add a test                                                                 |
|----------------|------------------------------------------------------------------------------------|
| Unit           | New pure function                                                                  |
| Property       | **Required** for any change to `librarian/policy/`                                 |
| Snapshot       | **Required** for any change to `librarian/voice/alexa/` (response JSON shape)      |
| BDD (Gherkin)  | New user-facing journey (kid checks out a book, parent overrides, etc.)            |
| Browser E2E    | New parent UI flow                                                                 |
| Smoke          | Stays a single fast happy-path; do not grow it                                     |

## Agent team configuration

This project is built primarily by Claude with the user steering. The "team" has roles:

| Role                | Model                                                              | Cost-route to OpenRouter? |
|---------------------|--------------------------------------------------------------------|---------------------------|
| Architect / Lead    | Claude Opus 4.x (main session)                                     | Never                     |
| Explorer            | Claude Sonnet / Opus (subagent)                                    | Never                     |
| Implementer         | Claude Sonnet (subagent)                                           | Only for trivial scaffolds|
| Test-runner         | Cheap model (Haiku / OpenRouter open-weights)                      | Yes                       |
| Lint-cleanup        | Cheap model                                                        | Yes                       |
| Reviewer            | Claude Opus (fresh-context session, runs `REVIEW.md` rubric)       | Never                     |

OpenRouter key (when configured) goes in `.env` as `OPENROUTER_API_KEY`. Test-runner and lint-cleanup agents may route there; **architect and reviewer must not**.

## What NOT to do

- Don't refactor the `voice` or `media` interfaces without a plan doc in `plans/`. They're load-bearing.
- Don't add a new top-level service to `docker-compose.yml` without justifying it in a plan (we want the operational footprint to stay small).
- Don't generate fictional metadata in tests. Use `factory-boy` factories that look like real books from `fixtures/catalog/`.
- Don't add telemetry or external HTTP calls from core code. Network egress is permitted only from explicit adapters (voice, media) and only to documented destinations.
- Don't log child PII (names, exact ages, device IDs). Logs may reference kids by their pseudonymous internal ID.

## Pointers

- Original session plan (Claude plan-mode archive): `/Users/steder/.claude/plans/git-init-lexical-horizon.md`
- Memory for this project: `/Users/steder/.claude/projects/-Users-steder-Github-Nineties/memory/`
- Code review rubric: [`REVIEW.md`](./REVIEW.md)
