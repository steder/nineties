# Code review rubric

This file is the checklist a reviewer (human or AI) applies to any change in this repository. CI enforces what it can; the rest is on the reviewer. Keep this list short — if it grows past one screen, something is wrong with the codebase, not the rubric.

A change is ready to merge when every relevant item below has a clear ✅ or "N/A".

## Always

- [ ] Commit message references the relevant plan (`refs plan/NNNN`)
- [ ] No `.env` files, secrets, keys, or tokens committed
- [ ] No telemetry or unsolicited external HTTP calls added
- [ ] No child PII in logs (names, exact ages, device IDs); pseudonymous IDs only
- [ ] `just lint` clean
- [ ] `just typecheck` clean (or new ignores justified in PR description)
- [ ] `just test` passes locally
- [ ] If the change is user-visible, `just smoke` passes

## When the change touches policy (`librarian/policy/`)

- [ ] At least one new property test added covering the eligibility invariant being changed or preserved
- [ ] Existing property tests still pass without weakening any invariants
- [ ] PR description explains the invariant in plain English

## When the change touches voice adapters (`librarian/voice/`)

- [ ] Core modules (`policy`, `loans`, `catalog`) still do not import from any concrete `voice/<adapter>/` package
- [ ] If touching `voice/alexa/`: snapshot tests against recorded Alexa request fixtures updated; diffs reviewed
- [ ] If adding a new adapter: lives in its own subpackage; abstract `VoiceAdapter` not modified without a plan doc

## When the change touches media backends (`librarian/media/`)

- [ ] Core modules still do not import from any concrete `media/<backend>/` module
- [ ] Streaming URL signing/expiry logic unchanged or explicitly reviewed for security
- [ ] If adding a new backend: lives behind the `MediaBackend` interface; integration tested with `testcontainers`

## When the change adds or alters migrations

- [ ] PR description includes a migration plan: lock impact, backfill strategy if applicable, rollout order
- [ ] Migration is reversible, or non-reversibility is justified in the PR
- [ ] No data loss; destructive changes (drop column / table) ship behind a feature flag with a separate migration

## When the change adds a dependency

- [ ] License is AGPL-compatible (MIT, BSD, Apache 2.0, MPL 2.0, LGPL, GPL/AGPL all OK; SSPL and "source-available" not OK)
- [ ] Justified in `pyproject.toml` comment or PR description
- [ ] Pinned via `uv` lockfile

## When the change touches the parent UI

- [ ] Playwright tests pass; new flows have new tests
- [ ] axe-core a11y assertions pass on new pages
- [ ] No client-side JS that calls third-party endpoints

## When the change touches the kid-facing UI or voice flow

- [ ] At least one Gherkin feature scenario added or updated in `tests/features/`
- [ ] No path lets a kid bypass their policy without an `OverrideLog` entry being written
- [ ] Voice/UI text uses age-appropriate language; no jargon

## "Done" definition

A task is done when:
1. All applicable checklist items above are ✅
2. The commit (or PR) clearly references the plan it implements
3. The relevant `plans/NNNN-*.md` has its status updated if the work shipped a milestone
4. CHANGELOG.md has an entry under `## [Unreleased]` for user-visible changes
