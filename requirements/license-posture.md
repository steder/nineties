# License posture

The legal framing of this project and what we accept (and refuse) as dependencies.

## This project

**Licensed under AGPL-3.0** (see [`../LICENSE`](../LICENSE)). The AGPL was chosen deliberately over MIT/Apache/BSD because:

- This is a **networked service**. If someone runs a modified version on the network for others to use, AGPL's §13 ensures users of that modified service can get the source. GPL alone would not.
- "Libre" was a stated goal of the project. AGPL is the strongest copyleft option for our shape.
- We accept the downside (some businesses won't use AGPL software) because our audience is families and self-hosters, not SaaS vendors.

## What contributors agree to

By contributing code (PR, patch, commit) to this repository, the contributor agrees their contribution is licensed under AGPL-3.0. No CLA. No DCO required yet — may add `Signed-off-by` later if the project grows.

## Dependency license rules

A dependency may be added if its license is on the **allowed** list. If it's on the **forbidden** list, it cannot be added. Anything else requires a plan-doc justification.

### Allowed licenses

- MIT
- BSD (2-clause, 3-clause)
- Apache 2.0
- MPL 2.0
- LGPL (any 2.x or 3.x version)
- GPL (any 2.x or 3.x version, with the linking clause appropriate to AGPL)
- AGPL-3.0
- ISC
- Public domain / CC0 / Unlicense

### Forbidden licenses

- Server Side Public License (SSPL) — explicitly incompatible with AGPL distribution
- BUSL (Business Source License) — not OSI-approved, time-bombed
- "Source-available" licenses (Elastic License v2, Confluent Community License, etc.)
- Commons Clause additions to otherwise-OSS licenses
- No-license-at-all code from public sources

### Requires justification

- Anything I haven't seen before — research it, document in PR
- Anything dual-licensed where one option is forbidden and we'd need to use the allowed one

## Calling vs. linking

We can *call* services with any license over a network (HTTP, etc.) without AGPL contamination — they're separate programs. So:

- AudioBookShelf is AGPL-3.0 (same license as us, fine either way) — we call it via HTTP, no linking
- Amazon Alexa is a proprietary service — we call it via HTTP, no contamination
- AWS Lambda (future) is proprietary infrastructure — we'd run our AGPL code on it, that's fine

## Patent grants

We accept patent grants in dependencies (Apache 2.0 §3 is fine). We do not currently grant or claim any patent rights of our own.

## Trademark

"Nineties" is the working project name. No trademark filing yet. If the project gets popular enough that name confusion is a concern, we'll address it then.

## What we will never do

- Relicense to a non-libre license to enable commercial offerings. If anyone wants a commercial fork, they can do it; we won't.
- Add a CLA that transfers copyright. Contributors retain their copyright; their AGPL grant is sufficient.
- Add usage telemetry, even "anonymous". (See [`privacy.md`](./privacy.md).)
