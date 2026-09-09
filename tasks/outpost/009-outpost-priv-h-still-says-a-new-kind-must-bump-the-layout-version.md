# 009 — `outpost_priv.h`'s header comment still says a new record kind must bump the layout version

**State:** claimed — leg 057, 2026-09-09, `agent/outpost/009-outpost-priv-layout-version-comment`
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

- [x] `src/outpost_priv.h`'s comment states what does and does not bump
      `OUTPOST_RECORD_LAYOUT_VERSION`, agreeing with `interfaces/wire.md` — and
      cites the reason (unknown kinds render, they do not fail), not just the
      rule.
- [x] No other copy of the old price survives: grep the code tree for
      "layout" and "bump" before closing.
- [x] `python3 tests/decoder_unit.py` still green (no `cargo`, no `west` — this
      repo has neither).
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment dropped.

## Result

Fixed the blanket rule in `src/outpost_priv.h`'s top `@file` comment (lines
10-17), which said "Anything changed here ... OUTPOST_RECORD_LAYOUT_VERSION
must be bumped" with no qualification. It now says only a shape change bumps
the version, points at the existing correct block below (line 77 on, "Bump on
ANY change to the record or frame layout above ... Adding an `enum
outpost_kind` value is not one") for the full rule, and states the reason
inline (unknown kinds render as `unknown_N`, they do not fail decoding). That
lower block already had the accurate rule — only the top summary comment was
stale. Grepped the whole tree for "must be bumped" / "must bump" / "new
kind ... bump" / "adding a kind" / "new record kind": no other survivors.
`tests/decoder_unit.py` (20 tests) still green. No decision needed — this was
a comment-only correction bringing code in line with `interfaces/wire.md`,
which already stated the rule; per burndown, none was authored.

No doc-repo content changes were needed beyond the changelog fragment: the two
doc copies (decisions/tracing.md decision 19, open.md) were already corrected
in `outpost/007`'s fold. `decisions/tracing.md` was not touched, so its 784 B
of reserve is untouched.

## Doc-size reserve in `embarch-outpost`, at dispatch (leg 057, 2026-09-09)

`decisions/tracing.md` **7,408 / 8,192 B — 784 B left** (90.4%), the only file in reserve, already
filed under `tasks/outpost/008` (open). `spec.md` and `decisions/transport.md` were both squeezed
out of reserve by `outpost/012` late on 2026-09-08 and are clear. Do not push `tracing.md` further;
if you must add to it, pay it down in the same commit. If this unit leaves any other file in
reserve with nothing filed, file `tasks/outpost/<NNN>-compact-outpost.md` in the same commit — your
own scope's directory, never `tasks/doc/`.

**This leg runs in burndown, which forbids authoring a new numbered decision.** This task is a
comment correction that brings code into line with `interfaces/wire.md`, which already states the
real rule — it should need **no** new decision, and `tasks/outpost/008` exists precisely because the
GPIO family's missing decision is a separate, filed piece of work. If you conclude a decision is
needed, stop and say so in your report instead of writing one.

## Note for whoever dispatches this

`embarch-outpost`'s `decisions/<topic>.md` cap is **tightened to 8 KB**, not the
usual 12 (`scripts/check-doc-size.py`'s `TIGHTENED` table). `decisions/tracing.md`
is the file this touches if it grows a decision, and it is close to that cap —
check it rather than assuming 12 KB. See `tasks/outpost/008`.
