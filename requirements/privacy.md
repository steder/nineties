# Privacy

What kid data exists, where it lives, and what never leaves the house.

## Principles

- **Self-hosted by design.** All data lives on hardware the family controls.
- **No telemetry.** This project never phones home. No usage metrics, no crash reporting, no analytics. If we need that, it goes through a local self-hosted observability stack (later) and stays local.
- **Minimum necessary.** We collect only what the system needs to function. Listening progress, yes. Detailed behavioral profiles, no.
- **Pseudonymous internal IDs.** Code paths that don't need a kid's real name use an internal opaque ID. Logs use the ID, not the name.

## What kid data exists

| Data | Purpose | Where it lives | Leaves the house? |
|------|---------|----------------|-------------------|
| Kid name | UI display only | Postgres, in `Kid` table | No |
| Kid birthdate | Per-kid policy thresholds (age_floor) | Postgres | No |
| Alexa `deviceId` → Kid mapping | Voice adapter device→identity resolution | Postgres | Yes (transit only, never persisted by Amazon) |
| Listening progress (position, item) | Resume across sessions | Postgres `ListenEvent` | No |
| Loan history | Library mechanics | Postgres `Loan` | No |
| Override log | Accountability for escape hatch use | Postgres `OverrideLog` | No |

## What leaves the house

- **Alexa requests** (during v1, until Phase 4 removes Alexa). Amazon sees: the invocation, the intent name, the slot values (e.g., spoken book titles), and the device ID. Amazon does *not* see: the catalog itself, listening progress, tags, or policy state. Documented in `docs/voice-adapter.md` for parent transparency.
- **AudioBookShelf metadata fetches** to providers like Open Library (parent-initiated, configurable). The metadata provider sees ISBNs and titles, not kid data.

## What never leaves the house

- Listening events
- Tag decisions
- Policy configuration
- Override events
- Loan history

## Logging rules

- Never log a kid's real name. Log their internal ID.
- Never log Alexa `deviceId` raw. Hash it before logging.
- Never log full streaming URLs (they contain signed tokens). Log item ID + status code.
- Application logs are local-only by default; no remote log shipping without an explicit opt-in.
