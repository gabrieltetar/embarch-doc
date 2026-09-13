# 060 — Six dead pointers in `doctor.rs`, and two of them are strings an operator reads

**State:** done — leg 111, 2026-09-13, `agent/umbrella/060-doctor-dead-pointers`
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

- [x] Every site above points at something that exists and says what the sentence claims.
- [x] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green.
- [x] `changelog.d/` fragment.

## What actually landed

Re-derived every replacement from `interfaces/doctor-chain.md`, `decisions/schema-skew.md`,
and `embarch-core/decisions/{flash-backend,enrollment,surfaces}.md` as they stand, not from
the hunter's report's conclusions taken on faith — but the line numbers themselves checked out
exactly (4, 20, 1031, 1269, 1483, 3475), no drift to report.

**Count re-checked: still six.** `grep -n "decision 36\|decision 57\|spec.md\|check 9" src/doctor.rs`
found no seventh stale site. One near-miss considered and rejected: `doctor.rs:1` ("`embarch
doctor` — spec.md's check chain") also says `spec.md`, but that one is **not** stale —
`spec.md` §"The `doctor` chain" still exists and still describes the chain in prose, it only
delegates the *table itself* to `doctor-chain.md`. The four table/row references (module doc
line 4, decision-16 comment, the `Unanswerable` doc comment, and check 9's `fix` string) all
point at content that moved; line 1's chain-level description did not move, so it was left
alone.

Fixes:
1. `doctor.rs:4` (module doc) — `spec.md's table` → `doctor-chain.md's table`.
2. `doctor.rs:20` — `decisions/surfaces.md` → `decisions/enrollment.md` (decision 57 lives
   there; `moved to decision 57` is recorded in that same file).
3. `doctor.rs:1031` — `spec.md` check 6's row → `doctor-chain.md` check 6's row.
4. `doctor.rs:1269` — retargeted the markdown link from `spec.md` to
   `interfaces/doctor-chain.md`, and corrected the link depth from `../../embarch-doc/...` to
   `../embarch-doc/...` to match the convention already established twice elsewhere in this
   same file (lines 569, 2753).
5. `doctor.rs:1483` (the `fix` string an operator reads) — `see spec.md, check 9` → `see
   doctor-chain.md, check 9`. Left as a bare filename, no markdown link and no added prose —
   an operator reading a `fix` line needs an instruction, not a citation.
6. `doctor.rs:3475` (the `detail` string check 14 prints) — `§3 decision 36` → `embarch-core
   decision 36`. Bare `§3 decision N` addresses *this* sub-project's own decision (umbrella's
   36, `schema-skew.md`'s fourth-number decision — unrelated); the flashing-backend decision
   is `embarch-core`'s own 36 (`decisions/flash-backend.md`), so it needs the cross-project
   prefix per `DOC-CONVENTIONS.md`'s rule. Matches the already-correct citation 85 lines
   earlier at `doctor.rs:3390`.

No `spec.md`/`decisions.md`/`open.md`/`status.d/`/`features.d/` edit needed — this is a
citation-only fix inside `doctor.rs`'s own comments and strings, no behavior, capability, or
suite-level fact changed. `decisions/bind.md` (in reserve) was not touched.
