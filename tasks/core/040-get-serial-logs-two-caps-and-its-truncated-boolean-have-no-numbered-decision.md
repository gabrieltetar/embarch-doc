# 040 — `GET /serial-log`'s two caps and its `truncated` boolean have no numbered decision

**State:** done (leg 082)
**Source:** `embarch-core/open.md` — *"`GET /serial-log`'s caps have no numbered decision"*
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`tasks/core/009` shipped three things and numbered none of them:

- `serial::MAX_DURATION_MS` — 10,000 ms
- a byte cap, `EMBARCH_SERIAL_LOG_MAX_BYTES`, defaulting to 1 MiB
- a `truncated: bool` field on the response shape

All three are **reasoned, not measured**, and `embarch-core/open.md` says so. What is owed is a
numbered `embarch-core` decision that records *why those two numbers* and *why a boolean rather
than a byte count* — so that the next person who meets a truncated serial log knows whether the
cap is a considered bound or a placeholder, and knows without re-deriving it that the response
deliberately does not say how much was lost.

**Do not change the numbers.** This task is the record, not a re-tuning. If while writing it you
conclude a number is wrong, say so in the decision as an explicit open question with its own
trigger, and leave the constant alone — changing a wire-visible bound is a separate task and one
that wants the owner's eyes.

**The `truncated: bool` half is the more interesting one** and should get the longer paragraph. A
boolean tells a caller *that* it lost data and refuses to tell it *how much*; a byte count would
let a scripted caller decide whether to re-request with a narrower window. Say which of those the
design chose and on what grounds, and whether a byte count is deferred-with-a-trigger or rejected.

**Doc-size reserve in this scope, and it is tight.** `embarch-core/decisions/surfaces.md` is at
**12019/12288 B — 269 B left** (filed against `tasks/core/038`, parked) and
`embarch-core/decisions/flashing.md` at **11487/12288 B — 801 B left** (`tasks/core/035`, parked).
A new decision will not fit in `surfaces.md` as it stands. Per `DOC-BUDGET.md`'s split-first rule
and `DOC-COMPACTION.md` §2, prefer a **new topic file** over squeezing an existing one, or compact
the file you are writing into as part of this unit and close that file's item on the parked task.
Whichever you do, say which and why in the commit message. `embarch-core/open.md` is **PAID** —
out of reserve at 75.9% — so if you touch it, keep it that way.

## Why now

`embarch-core/open.md` carries this as an explicit owed-decision bullet, and an owed decision that
lives only in an `open.md` bullet is one that gets re-derived rather than read. The bullet comes
out when the decision lands.

## Done when

- [x] A numbered `embarch-core` decision records both numbers' rationale and the boolean-vs-count
      choice, in a topic file that is not pushed into reserve by it.
- [x] `embarch-core/open.md`'s `GET /serial-log` bullet is replaced by a pointer to that decision,
      or deleted if nothing is left open.
- [x] Any residual open question (e.g. a byte count) is stated with its trigger, not left implied.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10): `cargo build` / `cargo test` /
      `cargo clippy --all-targets -- -D warnings` in `embarch-core`, `python3 scripts/check-docs.py`
      in `embarch-doc`.
- [x] `changelog.d/` fragment dropped.

## Outcome — leg 082

**Numbered decision 58, filed in `embarch-core/decisions/logging.md`** — not `surfaces.md`
(no room: it was at 12,019/12,288 B, parked on `tasks/core/038`) and not a new topic file. Logging
is the closer topical fit anyway: `GET /serial-log` is "Meant for dev-bench's link" per
`interfaces/hardware.md`, sibling to decision 37's `dev-bench.log`, and `logging.md` had 3,232 B
of headroom before its own reserve line (9,056/12,288 B). The entry added 1,949 B, landing
`logging.md` at 11,005/12,288 B — 54 B clear of its 11,059 B reserve threshold, checked by hand
against `check-doc-size.py --pressure` (green, `logging.md` not listed) rather than assumed.
No new topic file was needed; the split-first precedent (`probe-vendors.md`/`bind.md`,
`decisions/testing.md`) applies when the natural home is full, not when a better-fitting home with
room exists.

**Both numbers' rationale**, pulled from `serial.rs`'s own doc comments and made checkable: 10,000
ms sits under `embarch-core-client`'s 15,000 ms default timeout rather than matching it; 1 MiB is
"in the spirit of" `stream_store::EMBARCH_STREAM_MAX_BYTES` (decision 30) but two orders smaller
because this is a snapshot, not a bulk tap. Neither number changed.

**The boolean-vs-count half, the longer paragraph:** read `serial::capture()` rather than guessing
— its read loop `break`s the instant the byte cap is hit and never drains further, so the crate
cannot know a true loss total even in principle, only the last chunk's overflow. `stream_store`'s
own `truncated: bool` (decision 30) is the in-crate precedent: both byte-capped surfaces here
answer *whether*, never *how much*. **Rejected, not deferred** — a caller acts on `truncated: true`
with a shorter `duration_ms` or a larger `EMBARCH_SERIAL_LOG_MAX_BYTES`, neither of which needs a
count. **Trigger recorded** (decision 58 and `open.md`, both): a caller that must act differently
on 1 byte lost versus 900 KB.

**`open.md`:** the "Owed decisions" section (one bullet, now closed) is removed entirely; a new
one-line trigger bullet for the residual byte-count question sits under "Designed, not built",
mirroring decision 12's own entry there. Net effect shrank the file from 3,887 B to 3,735 B —
185 B clear of its 3,920 B reserve threshold (was already PAID before this task, per
`--pressure`, from decision 55's unrelated bullet closing on leg 075).

**`tasks/core/036` closed** (`embarch-core/open.md`'s parked reserve debt): the file stays paid
after this edit, so per this task's own instruction the debt is closed rather than left open with
no one paying it. Its `Must not delete:` list was checked — none of its four protected claims live
in the section this task touched.

**`decisions.md` index and `interfaces/constants.md`** updated: Logging's row now lists decision
58 (and 51, missing from the row before this task — a pre-existing gap, corrected in passing) and
its size; the `/serial-log` caps row in `constants.md` now cites decision 58.

**No code changed** — this is a doc-only unit; `serial::MAX_DURATION_MS`, the byte cap, and the
response shape are untouched, per this task's own instruction.

**Gate:** `cargo build`, `cargo test` (191 passed, 2 ignored), `cargo clippy --all-targets -- -D
warnings` all green in `embarch-core` (no diff, so unchanged). `check-docs.py` (all 11 checks),
`check-doc-size.py`, `check-decision-refs.py` all green in `embarch-doc`. `check-ownership.py
--scope core` (doc worktree) and `--code-repo --scope core` (code worktree, 0 paths changed) both
green. `check-client-names.py --repo <code worktree>` clean. Windows-native build not attempted —
not code-touching, no debt.
