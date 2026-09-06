# 005 — `suite/features.md` is 632 B from stalling every gate in the suite, and the one lever the fleet may pull is the fragments

**State:** open — **announced and parked** under `../../embarch-fleet/ops.md` §4.
**Announced:** `#embarch-fleet` **`ts 1788675832.554579`** (2026-09-06 00:23 MDT) — the full
announcement, naming what, which repos, and the guardrails. The leg-start message at
`ts 1788675547.326739` (00:19) named the intent first. **Window closes 00:55 MDT.** Do not
start before then. **If a leg ends before the window closes, leave this `open` with the `ts`
in this file** — the next leg reads it and *completes* the window rather than restarting the
clock (`../../embarch-fleet/ops.md` §4; three legs have restarted it wrongly, two have
completed it correctly). A reply saying go runs it immediately; cancel drops it back to
`open` with the reply quoted here.
**Source:** `tasks/suite/004-compact-suite.md`'s second half, plus the last two legs' log
entries. Leg 013 filed it, leg 014 reported it twice and acted zero times and said in its own
"least sure about" that the next leg should treat it as a task to dispatch rather than a line
to repeat. This is that task.
**Scope:** suite — **the supervisor executes it, never a worker** (`protocol.md` §8). The
fragments are per-scope files owned by nine different sub-projects; no single worker may
touch more than its own.
**Hardware:** none
**Owner:** no — this is the one of `suite/004`'s three moves that is *not* in `scripts/`.

## What

`suite/features.md` stands at **19,848 / 20,480 B — 96.9%, 632 B left**, and grew **+1,311 B
in leg 014 alone** against the ~200 B per leg its own script header models. It is assembled by
`scripts/build_features.py` from `features.d/` on **every fold**, and it is `never` for every
worker scope. When it crosses the cap, `check-doc-size.py` goes red inside `check-docs.py` —
**every unit's merge gate, in every sub-project, fleet-wide** — and no agent is permitted to
clear it. `suite/004`'s other two moves (raise the cap, split the inventory) are both
`scripts/` and therefore the owner's.

**The lever that is available is also the correct one, and that is the finding.**
`features.d/HEADER.md` states the file's own contract:

> Deliberately a *pointer*: the reasoning is in the owning decision, never restated here.

Fourteen of the 122 rows are over 300 chars and the worst four run 416–481 B — all of them
`doctor` rows restating in the Status column what the owning decision already says
(`umbrella-105`, `umbrella-065`, `umbrella-107`, `ui-100`). **They are not over the cap
because the inventory grew; they are over it because rows stopped being pointers.** Trimming
them is not compaction against the file's intent, it is enforcement of it.

## What I will do

1. **Trim the Status prose of the longest `features.d/` fragments** until the assembled
   `suite/features.md` is back under its **18,432 B reserve line** — ≥1,416 B, roughly the
   fourteen rows already over 300 chars. **Only the Status column.** Never a row's
   capability text, never its `Verified` value, and never its decision numbers — those are
   how the row is found and how it resolves.
2. **Each trimmed row must still carry its caveat.** `HEADER.md` says a `Shipped` with a
   caveat spells the caveat out; deleting a caveat to save bytes converts a qualified claim
   into an unqualified one, which is the exact failure `DOC-COMPACTION.md` exists to prevent.
   A caveat that survives only in the owning decision must still be *named* in the row, in
   fewer words — "unverified on `wsl-host`", not the paragraph explaining why.
3. **Record it as a decision**, because `suite/004` says recording it is the point: the
   fragments are the fleet's only lever, the trim is enforcement of `HEADER.md` rather than
   an exception to it, and **it buys time rather than fixing anything** — at 122 monotonically
   growing rows the file re-enters reserve on some future feature row whatever is done today.
4. **Tick `suite/004`'s `suite/features.md` item and leave its
   `embarch-decision-reversals.md` half open**, with `004` still naming the cap-and-split
   question as the owner's.

## What I will not do

- **Not edit `suite/features.md` itself.** The next fold overwrites it; the bytes live in the
  fragments.
- **Not touch `scripts/`.** Raising the cap and splitting the inventory are both there and
  both reserved — reported to the owner, not done.
- **Not dispatch this.** Nine scopes' fragments in one pass is nine ownership violations.
- **Not run it while a worker holds a scope whose fragments I am trimming.** `umbrella/018`
  is live and may rewrite `features.d/umbrella-107`. This runs after both workers land.

## Done when

- [ ] `python3 scripts/check-doc-size.py --pressure` no longer lists `suite/features.md`.
- [ ] Every trimmed row still names its caveat and still carries its decision numbers; the
      diff of `suite/features.md` shows no row lost from the inventory.
- [ ] A decision records the trim, its rationale, and that it buys time rather than fixing
      the ceiling — with the two owner-side moves still named as the real answers.
- [ ] `suite/004`'s features half is ticked and its reversals half left open.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
