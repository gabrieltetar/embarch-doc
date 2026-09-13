# 050 — `study.rs`'s test fixture bare-cites "Decision 44" and "Decision 62" for `embarch-study-designer` fields, and 44 collides with a real, unrelated `embarch-core` decision

**State:** done
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

- [x] Both citations carry the repo name, in the form the comment three lines above already uses.
      **Do not renumber anything** — the numbers are right for the repo that owns the fields; only
      the attribution is missing. Done — `study.rs:4168` and `study.rs:4171` (now `4168`/`4171`
      shifted by the added line) each now open with `` `embarch-study-designer` decision NN's ``,
      matching the `decisions 31/32` comment two lines above them. Numbers untouched.
- [x] Each target is **re-derived against the decision's actual text**, not accepted from this
      file. Confirmed against `embarch-doc/embarch-study-designer/decisions/ble.md:17` — heading
      `### 44 — `Action::BleSecurity { level }` — elevating the link is a step an engineer
      authors`, whose implementation section states "The result gains a level field, populated on
      *every* step" — that is `security_level`. And against
      `embarch-doc/embarch-study-designer/decisions/protocol-exec.md:27` — heading `### 62 — A
      protocol run reports the state it stopped in, and nothing it could lie about`, which states
      "Where the outcome lands... this field reaches the file automatically" — that is `protocol`.
      Both also cross-checked against `embarch-study-designer/src/result.rs:211`/`224`, whose doc
      comments cite the same two decision numbers for the same two fields. The scout's mapping was
      right on both.
- [x] `embarch-core`'s own decision 44 is confirmed to be the retired `/logs/stream` one — read at
      `embarch-doc/embarch-core/decisions/logging.md:22`, `### 44 — *(retired)* `/logs/stream`
      advances its offset only past a `\n`, and pays a tick for it`. Confirmed unrelated to
      `security_level`; the collision is two repos each legitimately holding a 44, not a defect in
      either's numbering.
- [x] **Sweep run.** `grep -rnE 'decision[s]? [0-9]+' -i src/ bin/` returned 244 hits (`bin/` has
      none — only `src/` did). 97 already carry an explicit `embarch-<repo>` attribution somewhere
      in the same doc-comment block (some split across lines, which a naive per-line check would
      have flagged as false positives). Of the remaining bare ones, every citation's number was
      checked against `embarch-core/decisions.md`'s own index and, where it touched a
      shared-crate type (`StepResult`, `ProbeInfo`, `embarch_topology::hardware::{NotEnrolled,
      TopologyMismatch, Alert}`, etc.), against the target heading's actual topic — e.g. `decision
      40` (dev_bench_link.rs, `StepResult`'s diagnosis field) resolves to `studies.md`'s own
      "An undecodable frame costs the frame..." and is topically about Core's frame handling, not
      about the field's origin, so bare is correct there; `decision 28` (api.rs, `NotEnrolled`)
      resolves to `enrollment.md`'s own "`POST /validate` and `GET /alerts`, reachable without
      touching hardware," likewise correct. **Result: the two citations named in this task
      (`study.rs`'s old lines 4168 and 4171, `security_level`/`protocol`) were the only wrong-body
      case found.** Every other bare citation in `src/` resolves to a real, topically-matching
      `embarch-core` decision. This class is closed in this repo as of this unit; nothing else
      needs a repo-name added.
- [x] Gate green, including `cargo test` — see below.
- [x] No `changelog.d/` fragment. Comment-only fix inside a test helper; nothing reader-visible
      changed (no behavior, no wire, no doc surface).

## Gate results (this unit)

- `cargo build`: green.
- `cargo test`: 197 passed, 0 failed, 2 ignored.
- `cargo clippy --all-targets -- -D warnings`: green.
- `python3 scripts/check-docs.py` (doc worktree): all 11 checks green.
- `scripts/check-client-names.py --repo <code worktree>`: clean against 7 denylist entries.
- `scripts/check-ownership.py --scope core` (doc worktree): OK, 0 changed paths.
- `scripts/check-ownership.py --scope core --code-repo --repo <code worktree>`: OK, worker owns
  the whole tree, 1 path changed.

Branches pushed: `agent/core/050-fixture-decision-citations` (code),
`agent/core/050-fixture-decision-citations-doc` (doc).

## Do not

**Do not "fix" the collision by renumbering `embarch-core`'s decision 44.** A decision number is
permanent (`DOC-CONVENTIONS.md`), the retirement does not free the number, and two legs this week
had to correct renumbering damage. The collision is not a defect in either repo's numbering — two
repos are allowed to both have a 44. It is a defect in one comment omitting which repo it meant.

## In flux: no

Nothing queued against `embarch-core` targets `study.rs`'s test module. `tasks/core/046` is a
blocked compaction task against `decisions/auth.md`, which this does not touch.
