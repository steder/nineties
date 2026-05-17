# Plans index

Forward-looking design documents for Nineties. Each plan has YAML frontmatter with `status`, `target_version`, and `phase`. Edit the table below when status changes.

## Status legend

- **planned** — written but not actively being built
- **in-progress** — currently being implemented
- **shipped** — implementation merged and released
- **abandoned** — explicitly decided not to do; kept for the historical record

## Plans

| # | Title | Target version | Phase | Status | Codename |
|---|-------|----------------|-------|--------|----------|
| [0001](./0001-v0.1.0-audiobook-library.md) | Audiobook library + Alexa front door | v0.1.0 | 1 | in-progress | Card Catalog |

## Future plans (sketches, not yet numbered)

These will become numbered plan docs when they move from sketch to design:

- **Phase 2 — Music**: Navidrome as second `MediaBackend`; daily-rotated kid mix; kid web client.
- **Phase 3 — Bedside Pi / tablet client**: Kiosk web app served by Librarian; buttons over feeds.
- **Phase 4 — Local voice stack**: Wyoming-protocol-based `VoiceAdapter` replacing Alexa; openWakeWord + whisper.cpp + local LLM intent + Piper TTS.
- **Phase 5 — Scheduled TV**: ErsatzTV channels gated by per-kid policy; Jellyfin as kid client.
- **Phase 6 — Federated community tags**: Opt-in sharing of tagging work between families.

## Conventions

- Plans are numbered sequentially. Reserve a number by creating the file before someone else does.
- Plan filenames follow `NNNN-short-slug.md`.
- Status transitions:
  - `planned` → `in-progress` when implementation starts
  - `in-progress` → `shipped` when the corresponding version tag is created
  - Any → `abandoned` when we explicitly decide not to do it (keep the file)
- Commit messages reference plans: `refs plan/0001` or `closes plan/0001`.
