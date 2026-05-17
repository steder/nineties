# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) until v1.0, after which it will switch to [CalVer](https://calver.org/) (`YYYY.MM` or `YYYY.MM.PATCH`).

Release codenames live here for personality; they are not used as version identifiers.

## [Unreleased]

### Added
- Initial repository scaffolding: `README.md`, `CLAUDE.md`, `REVIEW.md`, `LICENSE` (AGPL-3.0), `.gitignore`, `justfile` skeleton
- `plans/` and `requirements/` directories with index files
- v0.1.0 plan checked in as `plans/0001-v0.1.0-audiobook-library.md`

## [0.1.0] — "Card Catalog" — *unreleased*

First targeted release. **Audiobook library + Alexa front door**, working end-to-end on the user's home network for one family (kids ages 9 and 5). See [`plans/0001-v0.1.0-audiobook-library.md`](./plans/0001-v0.1.0-audiobook-library.md).

Planned scope:
- Librarian service (Django 5.x) wrapping AudioBookShelf
- Multi-axis content tagging + per-kid policy
- Library check-out / return / expiry with progress preservation
- Alexa custom skill (developer mode) for browse, check out, resume, return
- Parent web UI (Django admin + custom views) for ingest, tagging, policy, override

[Unreleased]: https://github.com/steder/nineties/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/steder/nineties/releases/tag/v0.1.0
