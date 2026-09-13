# 047 — `study.rs`'s test fixture bare-cites "Decision 44" and "Decision 62" for `embarch-study-designer` fields, and 44 collides with a real, unrelated `embarch-core` decision

**State:** claimed
**Source:** leg 107 refill sweep, 2026-09-13, scout-verified against `embarch-core/src/study.rs`,
`embarch-study-designer/src/result.rs` and both repos' decisions files. **The scout did not
execute anything and "scout-verified" is one reader**, which has been wrong before in this queue
(`umbrella/058`, and `outpost/020`'s own source note). Re-derive every claim below; they are
offered as a starting point, not as findings.
**Scope:** core
**Hardware:** none — comment text in a test helper. No wire change, no behaviour, no board.
**Owner:** no

## What

`embarch-core/src/study.rs:4159-4172`, inside the `test_step_result` test helper:

```
// `embarch-study-designer` decisions 31/32 — new
// fields this test fixture doesn't need to populate.
gatt_services: None,
// Decision 44's `security_level`, likewise: this fixture has no
// link, and `None` is what a step with no connection reports.
security_level: None,
// Decision 62's `protocol`: `None` for every action kind that
// is not `RunProtocol`, which is every one this fixture uses.
protocol: None,
```

**The first comment gets the form right and the next two do not.** This file's convention —
visible one comment above and again at `study.rs:1060` ("Decision 31's gate", which really is
`embarch-core`'s own decision 31, `decisions/handshake.md:12`) — is that a cross-repo citation
carries the repo name and a **bare** `Decision N` means *this* repo's numbering.

Both `security_level` and `protocol` are fields on `StepResult`, which is defined in
`embarch-study-designer`, not here:

- `embarch-study-designer/src/result.rs:212` — `pub security_level: Option<BleSecurityLevel>`,
  introduced by that repo's decision **44** (`decisions/ble.md:17`, *"### 44 — `Action::BleSecurity
  { level }`"*).
- `embarch-study-designer/src/result.rs:225` — `pub protocol: Option<ProtocolOutcome>`, introduced
  by that repo's decision **62** (`decisions/protocol-exec.md:27`).

Read under this file's own convention, they resolve wrong in two different ways:

- **`Decision 44` lands on a real, unrelated `embarch-core` decision.** `decisions/logging.md:22`
  — *"### 44 — *(retired)* `/logs/stream` advances its offset only past a `\n`, and pays a tick
  for it"*. Nothing to do with `security_level`. The scout dates the comment to 2026-08-26 and
  `embarch-core`'s own 44 to 2026-09-06 (`9e02825`), so **the comment was unambiguous when it was
  written and was made ambiguous later by a number being assigned in this repo** — nothing
  connected the two, and nothing could have.
- **`Decision 62` lands on nothing** — `embarch-core` has no decision 62 at all.

## Why now

This is the wrong-body variety of dead citation, and it is the one no script can see. A number
that resolves to **no** heading is mechanically detectable and is what `check-decision-refs.py`
finds; a number that resolves to the **wrong** heading reads as correct, so a reader stops there
and concludes something false. `topology/036` landed the same class today in a different repo and
its entry called this out as the reason those defects survive.

It also sits in the helper a fixture author reads first when extending `test_step_result`, which
is the worst place for a citation that sends you to a retired logging decision when you are asking
what `security_level` means.

## Done when

- [ ] Both citations carry the repo name, in the form the comment three lines above already uses.
      **Do not renumber anything** — the numbers are right for the repo that owns the fields; only
      the attribution is missing.
- [ ] Each target is **re-derived against the decision's actual text**, not accepted from this
      file. Confirm `embarch-study-designer` 44 owns `security_level` and 62 owns `protocol`, and
      say what you read.
- [ ] `embarch-core`'s own decision 44 is confirmed to be the retired `/logs/stream` one, so the
      collision is stated accurately if the fix mentions it.
- [ ] **A sweep, and its result reported either way.** Run `grep -rnE 'decision[s]? [0-9]+'` (case
      insensitive) over `embarch-core/src/` and `bin/`, and for each **bare** citation touching a
      type that lives in a shared crate (`embarch-study-designer`, `embarch-topology`), check
      whether it resolves to `embarch-core`'s own decision of that number and whether that decision
      is topically right. The scout ran the "no matching heading anywhere" check across the crate
      and this was the only hit; it did **not** do the wrong-body pass beyond this one function,
      and says so. **A clean sweep finding nothing else is a useful result and must be recorded,
      not left silent** — it is the only thing that would tell the next leg this class is closed in
      this repo.
- [ ] Gate green, including a `cargo test` — this is a test helper, so a comment edit that
      accidentally lands inside the struct literal breaks the build rather than reading oddly.
- [ ] `changelog.d/` fragment only if something reader-visible changed; a comment-only fix may
      warrant none, and saying so is fine.

## Do not

**Do not "fix" the collision by renumbering `embarch-core`'s decision 44.** A decision number is
permanent (`DOC-CONVENTIONS.md`), the retirement does not free the number, and two legs this week
had to correct renumbering damage. The collision is not a defect in either repo's numbering — two
repos are allowed to both have a 44. It is a defect in one comment omitting which repo it meant.

## In flux: no

Nothing queued against `embarch-core` targets `study.rs`'s test module. `tasks/core/046` is a
blocked compaction task against `decisions/auth.md`, which this does not touch.
