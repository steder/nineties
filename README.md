# Nineties

A curated, low-tech media experience for kids — finite, scheduled, deliberate, with friction. Free as in libre.

This project recreates a pre-streaming relationship to media for children: a library card instead of Audible's catalog, a CD shelf instead of Spotify's "for you" mix, a TV with a schedule instead of an endless Bluey feed. It is built for one family first, and shared in the open for anyone else who wants this for their kids.

## What this is (and isn't)

**It is** a curation / scarcity / scheduling layer on top of existing open-source media servers. AudioBookShelf, Navidrome, Jellyfin, and ErsatzTV do the heavy lifting; this project wraps them with multi-axis content tagging, per-kid policy, library-style check-out semantics, and a kid-facing voice/web front door.

**It is not** another media server. It is not a content store. It is not a parental control product that sells your kid's attention.

## The irony, stated up front

We are using Docker, Postgres, Django, an Alexa cloud skill, and several modern OSS servers to *simulate* the experience of a library card and a CD shelf. The 90s ideal here is the shape of the experience for the child, not the substrate. We chose to be honest about that rather than hide it.

There is also an explicit parent escape hatch: when a parent wants to just stream a thing, they enter a PIN (or go directly to the underlying servers on the LAN). Friction is a feature, but a wall isn't.

## Status

Pre-release. Active design. See [`plans/`](./plans/) for the roadmap and [`plans/index.md`](./plans/index.md) for current status.

The first target release is **v0.1.0 "Card Catalog"** — audiobook library + Alexa front door, working end-to-end for one family.

## Stack

Python 3.14 · Django 5.x · PostgreSQL 18 (+ pgvector + tsvector) · uv · `just` · Docker Compose · AudioBookShelf (media backend) · Alexa custom skill (first voice adapter). See [`plans/0001-v0.1.0-audiobook-library.md`](./plans/0001-v0.1.0-audiobook-library.md) for the architecture in detail.

## License

[AGPL-3.0](./LICENSE). Strong copyleft suits the libre intent of a self-hosted networked service. If you run a modified version of this software and let others interact with it over a network, you must publish your modifications under the same license.

## Contributing

Not actively soliciting contributions until v0.1.0 ships, but the repo is public from day one — feel free to read along, file issues, or open discussions.

## Documentation

- [`plans/`](./plans/) — design plans, ADR-numbered, with status frontmatter
- [`requirements/`](./requirements/) — evergreen "what must be true" docs (privacy, accessibility, safety, license posture)
- [`CLAUDE.md`](./CLAUDE.md) — instructions for Claude Code / future AI sessions on this codebase
- [`REVIEW.md`](./REVIEW.md) — code review rubric
- [`CHANGELOG.md`](./CHANGELOG.md) — release notes
