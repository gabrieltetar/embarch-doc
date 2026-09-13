# 060 — Six dead pointers in `doctor.rs`, and two of them are strings an operator reads

**State:** claimed — leg 111, 2026-09-13, `agent/umbrella/060-doctor-dead-pointers`
**Source:** leg 111's refill sweep — a read-only hunter over `embarch-umbrella`, run because
`--refill-owed` fired on scope spread. Every finding below was verified against both sides before
filing.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

Three groups, all in `src/doctor.rs`. **Two of the six sites are not comments** — they are `detail`
and `fix` strings that `doctor` prints to a human, so a wrong pointer there is a wrong instruction,
not merely a wrong footnote.

### 1. Check 14's `detail` string cites `§3 decision 36` — which resolves to *umbrella's* 36

`src/doctor.rs:3475`, inside the `no-flash-backend-subcommand` verdict: "*this embarch-core has no
`flash-backend` subcommand — it predates §3 decision 36 and will flash every target with probe-rs,
including Nordic RRAM parts*". Under `DOC-CONVENTIONS.md`'s rule ("a decision number addresses a
sub-project"), a bare `decision 36` written inside `embarch-umbrella` is umbrella's decision 36 —
`embarch-umbrella/decisions/schema-skew.md`, "`embarch`'s own constant survives as a fourth number,
and can only warn", which is about version reporting. The one meant is **`embarch-core` decision
36** (`embarch-core/decisions/flash-backend.md`), "a flashing backend per chip family, refusing
probe-rs where the vendor's semantics are not implemented". **The same file already gets it right 85
lines earlier**, at `doctor.rs:3390`.

### 2. Four pointers at "`spec.md`'s check table" — the table moved on 2026-09-10

`embarch-umbrella/spec.md` §doctor now delegates outright to
`embarch-umbrella/interfaces/doctor-chain.md`, which records the verbatim split and carries the
rows. `grep` for `check 6`, `check 9`, `never a pass` in `spec.md` returns nothing. Four sites still
point at `spec.md`:

| site | text |
|---|---|
| `doctor.rs:1483` — **a `fix` string a user reads** | `…so both name the same build output — see spec.md, check 9` |
| `doctor.rs:1031` | `(decision 16, ``spec.md`` check 6's row)` |
| `doctor.rs:1269` | `A warn naming why, never a pass ([``spec.md``'s rule for the whole chain](…/spec.md))` |
| `doctor.rs:4` | `Ordered the same as spec.md's table` |

The docs are already correct; only the pointers are stale.

### 3. `doctor.rs:20` cites `embarch-core decision 57 (decisions/surfaces.md)`; 57 lives in `enrollment.md`

`embarch-core/decisions/surfaces.md` defines 13, 12, 55 and 59 — no 57. Decision 57 is
`embarch-core/decisions/enrollment.md`, "`EnrolledBoardResponse` does not grow a persisted
validation timestamp; the existing field gets an honest label instead", and that file even records
the move ("54 — moved to decision 57"). **The substance of the comment is correct** — only the file
pointer rotted, across exactly the mission split `DOC-CONVENTIONS.md` says to prefer a bare number
because of.

## Notes for whoever runs this

- **Re-derive every replacement yourself** from the decision bodies and from `spec.md` /
  `doctor-chain.md` as they stand in your own worktree. This task file was written from a hunter's
  report; treat its line numbers as approximate and its conclusions as hypotheses.
- **Check whether the count is still six.** If your own grep finds more or fewer, say so explicitly
  in your report — a count that matches is worth as much as one that does not.
- The two user-facing strings (`doctor.rs:3475`, `doctor.rs:1483`) are the ones that matter most.
  Keep them readable as instructions, not as citations with prose attached.
- **`embarch-umbrella/decisions/bind.md` is in reserve** — 11533/12288 B, **755 B left**, parked
  against `tasks/umbrella/009`. Nothing here should need to write it; if your work does, say so
  before spending the headroom.

## Done when

- [ ] Every site above points at something that exists and says what the sentence claims.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green.
- [ ] `changelog.d/` fragment.
