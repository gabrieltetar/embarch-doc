# 040 — `GET /serial-log`'s two caps and its `truncated` boolean have no numbered decision

**State:** claimed (leg 082)
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

- [ ] A numbered `embarch-core` decision records both numbers' rationale and the boolean-vs-count
      choice, in a topic file that is not pushed into reserve by it.
- [ ] `embarch-core/open.md`'s `GET /serial-log` bullet is replaced by a pointer to that decision,
      or deleted if nothing is left open.
- [ ] Any residual open question (e.g. a byte count) is stated with its trigger, not left implied.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10): `cargo build` / `cargo test` /
      `cargo clippy --all-targets -- -D warnings` in `embarch-core`, `python3 scripts/check-docs.py`
      in `embarch-doc`.
- [ ] `changelog.d/` fragment dropped.
