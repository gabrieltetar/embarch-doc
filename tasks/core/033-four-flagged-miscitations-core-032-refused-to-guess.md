# 033 — The four citations `core/032` flagged rather than guessed, and one citation form it invented

**State:** done — leg 065, 2026-09-10

## Dispatch note, leg 065

**Doc reserve in your scope:** `embarch-core/open.md` is 4,813 / 5,120 B — **307 B left**, inside
the reserve floor, and its compaction task `tasks/core/022-compact-core.md` is already filed and
`open` (not blocked), so you do **not** owe a new compaction task for that file. Nothing else in
`embarch-core/` is in reserve. Plan for 307 B if you write to `open.md`; prefer editing an existing
question to appending one.

**The four citations are the expensive half; the citation-form item is the cheap half — do both,
and do the cheap one mechanically.** Leg 064 landed ~50 citations written as `` `decision N` ``
(number inside the code markup) against a convention that puts the number in plain prose. Normalise
them with a script *and read the resulting diff* before committing; that read is the part that
cannot be skipped.

**On the four numbers: a guess here wastes the previous worker's refusal.** For each, open the
target repo's `decisions/` file and read the decision **body**, never its heading or its
parentheticals — two legs running have found a citation that looked wrong because only the body
says what it covers. If a number still cannot be settled from a body, leave it carrying its
original number, say so in this file, and do not substitute your candidate.

**Source:** `tasks/core/032`'s own Result section, leg 064, 2026-09-10 — the worker de-`design.md`'d
170 citations, found five whose *number* looked wrong, resolved exactly one with confidence, and
**deliberately left the other four carrying their original numbers** rather than guessing. That was
the right call and it is the reason this task exists.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Four flagged citations in `embarch-core/src`, each now a live bare `decision N` pointing at a
decision whose body may not be its subject. **Read each decision's body before changing anything —
the whole point of this task is that `core/032` refused to guess, so a guess here would waste the
refusal.** Verify against the target repo's own `decisions/` index, not its headings.

1. **`src/chip_resolve.rs:46` and `src/api.rs:1274`** — both read
   `` `embarch-dev-bench` decision 26, reversing that repo's decision 13 ``. The worker's read:
   dev-bench decision 13 is *"Core can flash dev-bench firmware, reversing a separation-of-concerns
   rule"*, unrelated to the ESP JTAG/board choice these comments describe, and 26 is the actual ESP
   JTAG content. Confirm 26, and **drop the stale "reversing decision 13" clause if it does not hold**
   — a wrong reversal claim is worse than a missing one.
2. **`src/dev_bench_link.rs:115-116`** — *"an outpost frame carries its own CRC"* cites
   `embarch-outpost` decision 5, which is **"Overflow policy: drop, count, and emit an explicit gap
   record"** (`embarch-outpost/decisions/transport.md`) — verified by leg 064's supervisor, not the
   worker. CRC framing appears to live in that repo's `manifest.md`/`clocks.md` with no decision of
   its own. Either find the decision that does cover framing/CRC, or cite `embarch-outpost/spec.md`'s
   section. **This citation predates `core/032`** — the number was carried over unchanged, so this is
   an inherited defect, not one the sweep introduced.
3. **`src/api.rs:971`** — bare `decision 7`, for the `NotEnrolled` / "not configured" 404 behaviour.
   The worker's read is that the text belongs to **`embarch-core` decision 28** (`POST /validate` /
   `GET /alerts`). Check decision 7's body before repointing: if 7 genuinely covers part of it, the
   comment may need both numbers rather than a swap.
4. **`src/study.rs:2475`** — the clock-resync-gap citation resolved to `embarch-study-designer`
   `spec.md` §7 because its original number (that repo's decision 7) is an FFI/C-bridge decision.
   The worker's candidate is **`embarch-study-designer` decision 30** ("Core records its own arrival
   time on every incoming message"). Confirm and repoint, or leave the `spec.md` pointer and say why.

**Second, smaller item — a citation form `core/032` invented, and the task file told it not to.**
The sweep wrote roughly fifty citations as `` `decision 40` `` — the number *inside* the backticks.
Both prior sweeps wrote them bare: `embarch-umbrella/src/deploy.rs` has `(decision 32)` and
`embarch-api/src/config.rs` has `` `embarch-study-designer` decision 35 `` — repo name in code
markup, the word "decision" and its number in plain prose. That is the convention `api/052` settled
and `umbrella/043` reused, and `embarch-core` is now the one repo of the four spelling it a third
way. Normalise it in the same pass: it renders as inline code in rustdoc, so it is visible, not
merely stylistic. **Mechanical enough to script, but check the diff afterwards** — the same
`decision N` string appears inside at least one *shipped* string literal
(`src/study.rs`'s undeclared-signal-tap error message, and `src/deploy.rs`-style generated text
elsewhere in the suite), and a shipped string is data a machine may match on.

## Why now

`core/032` landed 170 citations' worth of repair and left exactly these four unresolved, in a repo
the other three sub-projects cite *into* more than any other. A bare number that resolves to the
wrong decision is worse than the dead `design.md` pointer it replaced, because it now looks correct
— `check-decision-refs.py` resolves a number and falls back to "defined somewhere in this
sub-project", so nothing will catch these.

## Result

Read each target decision's **body** (never heading/parenthetical) before touching anything, per
the dispatch note.

1. **`chip_resolve.rs:46` / `api.rs:1273`** — `embarch-dev-bench` decision 26's body
   (`decisions/boards.md`) is the ESP32-C5 board substitution and matches both comments. Decision
   13's body (`decisions/link.md`) is *"Core can flash dev-bench firmware, reversing a
   separation-of-concerns rule"* — unrelated. **Dropped the stale "reversing that repo's decision
   13" clause at both sites**, kept decision 26.
2. **`dev_bench_link.rs:115`** — confirmed leg 064's supervisor read: `embarch-outpost` decision 5
   is the overflow/gap-record policy, nothing to do with frame CRC, and no outpost decision covers
   per-frame CRC — it lives in `interfaces/wire.md` (`frame := COBS(body || crc32_ieee(body) ...)`,
   "The CRC covers the body only, sealed before COBS"). **Repointed to
   `` `embarch-outpost` interfaces/wire.md `` **, no decision number.
3. **`api.rs:970`** — `embarch-core` decision 7's body (`decisions/platform.md`) is the
   Rust/probe-rs/Axum/`spawn_blocking`/CI platform choice, no overlap with `NotEnrolled`/404 at
   all — not a partial match, a straight wrong number. Decision 28's body (`decisions/surfaces.md`)
   is exactly this: `POST /validate`/`GET /alerts` needed "a typed `NotEnrolled` in the topology
   crate ... enough to tell 'not configured yet' from 'a real I/O error'". **Repointed decision 7 →
   decision 28** (single number, not both — 7 covers none of it).
4. **`study.rs:2471`** (line shifted from the task's 2475 by unrelated prior edits) — already reads
   `` `embarch-study-designer` decision 30 ``, not the `spec.md §7` pointer the task description
   named. Decision 30's body (`decisions/versioning.md`) is exactly "Core records its own arrival
   time on every incoming message" to give post-hoc analysis what a resync-on-handshake-only design
   can't — matches "the clock-resync gap ... closes" verbatim. **No change needed; confirmed
   correct as it stands**, so leg 064 (or an earlier hand) had already landed the worker's own
   candidate here.

Mechanical pass: normalised all ~47 remaining `` `decision N` `` (backtick-enclosed number)
citations across `embarch-core/src` to the suite's plain-prose-number convention with a scripted
`perl -pi` substitution restricted to the backtick-wrapped pattern, then read the full diff by hand.
No shipped string literal was touched — the one shipped string carrying a decision citation
(`api.rs`'s `contract_version` message, `decision 13, amended ...`) was already in prose form, not
backtick form, so the substitution's pattern never matched it.

**Debt, unrelated to this task's scope:** `embarch-core`'s native Windows build was not attempted,
per protocol §5 — path-dep resolution over a worktree's symlinks is a known-broken combination
(see the leg's own dispatch context), unchanged by this citation-only diff.

## Done when

- [x] Each of the four is either repointed to a decision whose **body** matches the comment, or left
      in place with one sentence saying why the original is right after all.
- [x] Any citation that turns out to be cross-repo names the repo as a plain qualifier.
- [x] The `` `decision N` `` form is normalised to the suite's convention across `embarch-core`, and
      the diff is checked for any change to a string literal rather than a comment.
- [x] Gate green ([protocol](../../../embarch-fleet/protocol.md) §10); `changelog.d/core-*` fragment.
