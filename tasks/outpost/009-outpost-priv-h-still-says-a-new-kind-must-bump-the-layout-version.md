# 009 — `outpost_priv.h`'s header comment still says a new record kind must bump the layout version

**State:** open
**Source:** `outpost/007`'s reviewer, 2026-09-06 — it found three copies of a wrong price; the supervisor fixed the two doc copies in that fold and this is the third
**Scope:** outpost
**Hardware:** none
**Owner:** no

## What

`src/outpost_priv.h:12` carries a blanket rule that `OUTPOST_RECORD_LAYOUT_VERSION`
"must be bumped" for a record-layout change, in a comment that a reader adding a
record kind will land on first.

That is **not what the project does**, and the file itself proves it: kinds
`GPIO_DISPATCH = 9` and `GPIO_CALLBACK_DONE = 10` shipped in `706aeb1` at
`OUTPOST_RECORD_LAYOUT_VERSION 3`, unbumped, and the version constant has not
changed since the module's first commit. `interfaces/wire.md` now states the real
rule — **kinds are append-only and appending one does not bump the version**,
because the record shape is fixed so a host can render an unknown kind as
`unknown_N` rather than fail, and what tells a host whether a family is present
is the header's `flags`, not the version byte.

The comment needs to say which changes actually bump it — a change to the record
*shape*, not an addition to the kind enum — and the enum's own append-only note
should be reachable from it.

## Why now

This was one of three places pricing a new kind as costing a layout bump. The
other two — `decisions/tracing.md` decision 19's rejected alternative and the
same sentence in `open.md` — were corrected in `outpost/007`'s fold. **This one
is in the code repo and is the copy a firmware author actually reads**, so
leaving it is leaving the wrong rule in the most-consulted position while the
docs say the right one.

`wire.md` opens by calling `outpost_priv.h` the specification three
implementations must agree on, which makes a stale rule in its header comment
worse than a stale one in prose.

## Done when

- [ ] `src/outpost_priv.h`'s comment states what does and does not bump
      `OUTPOST_RECORD_LAYOUT_VERSION`, agreeing with `interfaces/wire.md` — and
      cites the reason (unknown kinds render, they do not fail), not just the
      rule.
- [ ] No other copy of the old price survives: grep the code tree for
      "layout" and "bump" before closing.
- [ ] `python3 tests/decoder_unit.py` still green (no `cargo`, no `west` — this
      repo has neither).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.

## Note for whoever dispatches this

`embarch-outpost`'s `decisions/<topic>.md` cap is **tightened to 8 KB**, not the
usual 12 (`scripts/check-doc-size.py`'s `TIGHTENED` table). `decisions/tracing.md`
is the file this touches if it grows a decision, and it is close to that cap —
check it rather than assuming 12 KB. See `tasks/outpost/008`.
