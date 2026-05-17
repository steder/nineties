# Safety

Invariants the policy engine must guarantee. These are the *whole point* of the project — if any of these fails, the system has failed at its job.

Every invariant below must be exercised by a property test in `librarian/policy/tests/test_invariants.py`.

## Eligibility invariants

For any `Kid` and any `Item`:

- **I-1: Age floor is binding.** If `Item` has tag `age_floor=N` and `Kid.age < N`, the item is NEVER eligible for that kid under default policy. (Parent override is the only way past, and it must write an `OverrideLog` row.)
- **I-2: Deny tags are binding.** If `Kid` has a `Policy` with `mode=deny` on axis A, and `Item` has any tag on axis A matching the policy's threshold or stronger, the item is NEVER eligible. (Same override caveat.)
- **I-3: Require-review tags hide the item.** If `Kid` has a `Policy` with `mode=require_review` on axis A, and `Item` has any matching tag, the item is hidden from browse until a parent grants per-item access. The item is NOT auto-eligible after the kid ages up.
- **I-4: Untagged items are not eligible.** An `Item` with no tags is in `needs_review` state and is hidden from every kid until a parent tags it.

## Loan invariants

- **L-1: No exceeding loan cap.** A kid never has more than `family.max_active_loans` `Loan` rows with `returned_at IS NULL`. The check happens at checkout time and is transactional.
- **L-2: No double-borrow.** A kid cannot have two open `Loan` rows for the same `Item`.
- **L-3: Returns preserve progress.** When a `Loan` is returned (explicit or expired), `progress_seconds` is preserved and used as the starting point on the next checkout of the same `Item`.
- **L-4: Cooldown is enforced.** A returned item cannot be re-borrowed before `cooldown_days` has elapsed since the return. (Parent override exists and logs.)

## Override invariants

- **O-1: Every override produces a log.** A parent override that grants access to a `needs_review` or `denied` item MUST write an `OverrideLog` row with `parent_id`, `kid_id`, `item_id`, `granted_at`, and a `reason` (can be empty string but the field must be present).
- **O-2: Overrides are time-bounded.** A voice override session (after spoken PIN) opens a window of `override_window_seconds` (default 300). After the window, the parent must re-authenticate.
- **O-3: No silent escalation.** No code path may grant access to a normally-ineligible item without writing an `OverrideLog` row. Including admin actions. Including "system" actions.

## Identity invariants

- **ID-1: Voice device → kid is explicit.** Mapping a new Alexa `deviceId` to a `Kid` requires a parent action. There is no auto-onboarding.
- **ID-2: No cross-kid bleed.** A request from `deviceId` mapped to `Kid A` may never return items eligible only for `Kid B`. (Property tested with paired kid policies that differ.)

## What is NOT an invariant (and why)

- **Recommendation quality.** The browse list is not guaranteed to be "good" — that's a design concern, not a safety one.
- **Streaming uptime.** Network blips, transcoding errors, ABS being down — these degrade the experience but don't violate safety.
- **Schedule fidelity** (relevant in Phase 5 for TV). The schedule is a content suggestion; missing a window is not a safety failure.

## How invariants change

Adding an invariant: write the property test first, mark it `xfail` until the code lands, then flip to `pass`. Add the row above.

Removing or weakening an invariant: requires a plan doc in `plans/` justifying the change. The corresponding property test is updated in the same commit, not deleted silently.
