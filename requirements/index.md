# Requirements index

Evergreen "what must be true" documents. Unlike plans (which are time-bounded designs), these describe properties the system must always exhibit, regardless of version or phase.

If a plan would violate something here, either the plan changes or the requirement changes — explicitly, with discussion in commit history.

| Document | Topic |
|----------|-------|
| [privacy.md](./privacy.md) | What kid data exists, where it lives, what never leaves the house |
| [accessibility.md](./accessibility.md) | WCAG targets for the parent UI, voice UX considerations for kids |
| [safety.md](./safety.md) | Invariants the policy engine must guarantee |
| [license-posture.md](./license-posture.md) | AGPL boundaries, dependency license rules |

## Conventions

- One document per stable concern. Don't fragment.
- If a section grows controversial (e.g., "should we ever log child names?"), record the decision and the date so it's traceable later.
- These docs change rarely. When they do, the commit message and PR description must include a "why now."
