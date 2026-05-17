# Accessibility

What we promise the parent UI and the kid voice/UX will support.

## Parent UI (browser)

Target: **WCAG 2.2 AA** for all production parent-facing pages. Verified by:

- `pytest-playwright` tests run `axe-core` (via `pytest-axe`) on every page touched by browser E2E tests
- Manual keyboard-only navigation check on each new flow (no mouse)
- Color contrast verified by axe; no hard-coded text colors that fail AA contrast against their backgrounds

Specific requirements:

- All interactive controls reachable by keyboard
- Visible focus states on every control
- Form fields have associated `<label>` elements
- Images have meaningful `alt` text (book covers: book title + author)
- No information conveyed by color alone (e.g., a "needs review" state must also be expressed in text)
- Page titles are unique and meaningful

## Kid voice UX (Alexa, and future local voice)

The kid's experience is voice-first in v1. There is no visual UI on the bedside Echo, so accessibility here means:

- **Patient prompts.** No hard time limits on the kid's response that would cut off a slow speaker
- **Forgiving slot matching.** Book titles can be mis-pronounced, partial, or fuzzy — the system should ask for confirmation rather than fail
- **Explicit confirmations** for state-changing actions (checkout, return). The kid should hear "Got it, checking out *The Wild Robot*" before the loan is recorded
- **Gentle error messages.** Never blame the kid. "I didn't catch that, can you try again?" — not "Invalid input."
- **No reading of irrelevant metadata** during browse. Title and "by Author" only; skip ISBNs, narrators, durations unless asked

## Kid web/tablet UX (Phase 3)

When the kid-facing web client ships, it inherits the WCAG 2.2 AA target plus:

- **Large touch targets** — minimum 48×48px (WCAG 2.5.5)
- **Pre-reading kid mode** — covers + spoken titles (TTS) for kids who can't yet read
- **No interstitials, no marketing, no upsells** — there is nothing to sell

## What we don't promise (yet)

- Multilingual support — English only in v0.1.0. Tag the architecture to make i18n possible later (use `gettext` from day one in any new strings).
- Screen reader support beyond standard semantic HTML — we don't have a tested-with-NVDA promise yet.
- Color-blindness specific affordances beyond WCAG-mandated contrast — covered transitively by "no info by color alone."
