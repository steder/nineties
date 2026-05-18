# Setup

First-run setup for a fresh Nineties checkout. Once these steps are done,
the dev loop is `just dev && just serve` (in two terminals) and `just ci`.

## Prerequisites

| Tool             | Why                                  | Install                                                  |
|------------------|--------------------------------------|----------------------------------------------------------|
| Docker runtime   | Postgres + AudioBookShelf containers | macOS: OrbStack (recommended) or Docker Desktop. Linux: native. Windows: Docker Desktop or Rancher Desktop, with WSL2. |
| `uv`             | Python toolchain + dep management    | https://docs.astral.sh/uv/getting-started/installation/  |
| `just`           | Cross-platform task runner           | macOS: `brew install just`. Other: https://just.systems  |
| `gh`             | GitHub CLI (for PR / issue tooling)  | https://cli.github.com                                    |

## Initial bootstrap

```bash
# Clone
git clone https://github.com/steder/nineties.git
cd nineties

# Configure environment (rotate secrets locally)
cp .env.example .env
# Edit .env: set DJANGO_SECRET_KEY to a fresh random value, set POSTGRES_PASSWORD

# Install Python deps + venv
cd librarian && uv sync && cd ..

# Bring up Postgres + AudioBookShelf
just dev

# In another terminal, generate the fixture catalog
just fixtures

# Apply database migrations
just manage migrate
```

## AudioBookShelf one-time setup

AudioBookShelf has no headless bootstrap — the first user is created
through the web UI. After that, our Librarian reads the catalog via the
ABS API using a token you'll paste into `.env`.

1. **Open AudioBookShelf** in a browser: http://localhost:13378
2. **Create the root user**. The first account you make is automatically
   the admin.
3. **Add a library**:
   - *Settings → Libraries → Add Library*
   - **Name**: anything (e.g. "Audiobooks")
   - **Media type**: Books
   - **Folders**: add `/audiobooks`
     - This is the mount point inside the container. On the host it
       corresponds to `fixtures/catalog/` in this repo.
   - Save. ABS will scan automatically; the six fixture audiobooks should
     appear within a few seconds.
4. **Generate an API token** for the Librarian:
   - Click your avatar (top right) → *Account*
   - Scroll to **API Token** → Copy
5. **Paste the token** into `.env`:
   ```
   AUDIOBOOKSHELF_TOKEN=<paste here>
   ```
6. **Restart `just serve`** so Django picks up the new env var.

You're done with ABS until you add real audiobooks later.

## Create a Django superuser

So you can sign in at http://localhost:8000/admin/ as a parent:

```bash
just manage createsuperuser
```

## Smoke test

```bash
just ci
```

Should print `0 errors, 0 warnings` for pyright and a green pytest line.

## Day-to-day commands

| Command           | Purpose                                              |
|-------------------|------------------------------------------------------|
| `just dev`        | Bring up Postgres + AudioBookShelf in Docker         |
| `just serve`      | Run the Librarian Django dev server on the host      |
| `just down`       | Tear down the Compose stack                          |
| `just test`       | Unit + property + integration tests                  |
| `just smoke`      | Single happy-path run (~10s, agent-friendly)         |
| `just lint`       | Ruff lint                                            |
| `just typecheck`  | Pyright                                              |
| `just ci`         | Everything CI runs (lint + typecheck + test)         |
| `just fixtures`   | Regenerate the silent-audiobook fixture catalog      |
| `just manage <cmd>` | Passthrough to `manage.py` (migrate, createsuperuser, etc.) |

## What's next (not yet set up)

- **Alexa skill** (`docs/voice-adapter.md`, to be written): registers the
  custom skill in your Amazon developer account, sets up the interaction
  model, points the skill's endpoint at Librarian via Cloudflare Tunnel.
  Lands with plan/0001 task #16.
- **Cloudflare Tunnel**: only needed once we're testing on a real Echo
  device. Tunnel exposes `localhost:8000` over HTTPS to Alexa.
