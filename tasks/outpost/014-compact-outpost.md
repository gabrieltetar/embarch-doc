# 014 — Compact embarch-outpost/spec.md

**State:** done — 2026-09-10
**Source:** `scripts/check-doc-size.py`, run from `agent/outpost/005-verify-the-arrival-join`
**Scope:** outpost
**Hardware:** none
**Owner:** no
**Compacts:** embarch-outpost/spec.md
**In flux:** no
**Must not delete:** the `--allow-unverified-join` / `--allow-build-id-mismatch`
posture pairing in the invariant-61 paragraph — it is the reader's only pointer
from the invariant to the escape hatch and the decision it mirrors; and the
missing/short `frame_bytes` column's degrade-not-refuse behaviour, which is the
one case a reader could otherwise assume is a third refusal alongside the
manifest and build-ID ones.

## What

`agent/outpost/005-verify-the-arrival-join` implemented `spec.md:61`'s
invariant in the reference decoder and added one paragraph recording it,
which put `embarch-outpost/spec.md` at 9,515/10,240 B — inside the last 10%
of its cap (`RESERVE_PCT`), 725 B left. The file is still writable and the
gate still passes; this task exists only to name the debt per
`DOC-COMPACTION.md` §2, since the commit that spent the reserve owes the task
that files it.

## Why now

`check-doc-size.py` failed the doc gate for `embarch-outpost` with this file
named and no open task covering it (`embarch-outpost/decisions/tracing.md`'s
reserve is already covered by `tasks/outpost/008`, which is a different file).

## Dispatch note from the supervisor, leg 063

**Try a split before you try a squeeze, and `core/030` is the worked example from yesterday.**
`DOC-BUDGET.md`'s split-first rule exists because a verbatim move restates nothing and therefore
costs no accuracy, whereas a squeeze trades provenance for bytes. On 2026-09-09 `embarch-core/spec.md`
was 108 B into its reserve and the task file suggested squeezing a 12-row constants table; the worker
instead lifted the whole table out verbatim into a new `embarch-core/interfaces/constants.md`, left a
pointer paragraph in `spec.md` naming what moved and that nothing was cut, and added a row to
`interfaces.md`'s table. 9,148 B → 7,977 B, and not one fact left the corpus. **Look for that seam
here first**; only squeeze the prose if there genuinely is none.

**The numbers have moved since this task was filed.** It says 9,515 B / 725 B left; today
`check-doc-size.py` reports `embarch-outpost/spec.md` at **9,775/10,240 B, 465 B left**. Re-measure
before and after rather than trusting either figure, and note that reserve is
`max(1200 B, 10%)` from the top — so getting under 10,240 B is not enough, you need to clear the
reserve band and have `check-doc-size.py` stop naming the file.

**One caution on the `Must not delete:` list above.** Both items are there because a reader would
otherwise draw a *wrong* conclusion, not merely an incomplete one — the `frame_bytes` degrade
behaviour in particular reads as a third refusal alongside the manifest and build-ID refusals if it
goes missing. If a split moves either one, it must land verbatim on the other side.

**Docs-only is expected.** The `embarch-outpost` code branch will almost certainly have a zero diff,
which is fine and has precedent (`core/030`, `topology/023`). Do **not** invent a code change to
justify the branch. And you cannot run `embarch-outpost`'s Zephyr `tests/unit` ztest suite from this
environment — no `west`, no `ZEPHYR_BASE` — which is a standing, already-recorded debt; since this
unit touches no C, it does not deepen it. Say so rather than claiming the suite green.

## Done when

- [x] `embarch-outpost/spec.md` reduced below its reserve threshold without
      losing any fact the `Must not delete:` list names — a paragraph
      tightened or a repeated fact folded into a cross-reference, not a
      judgement removed.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), `check-doc-size.py`
      no longer names this file.
- [x] `changelog.d/` fragment dropped for the compaction itself.

## Resolution

Split, not squeeze. §5 "Host-side outputs" (the three `streams/` files, their
columns, and the `us`/`cycles` formatting and wrap rules) was a verbatim move
out of `spec.md` into `interfaces/integration.md` — a new `## Host-side
outputs` section there, with `spec.md` left holding a pointer paragraph naming
what moved and a one-line summary of the three files. The two internal
cross-references that pointed at `spec.md §5` (`interfaces/wire.md`'s
`cycles_per_sec` note and `interfaces/integration.md`'s own "Reading the
trace" line) were repointed at the new location. Nothing was reworded or cut.

First attempt moved the section into `interfaces/wire.md` instead, which
cleared `spec.md`'s reserve but pushed `wire.md` itself to 94.8%/12,288 B —
into its own reserve, so the gate still failed (just relocated the debt).
Retargeted the move to `interfaces/integration.md` (6,096 B before, 7,953 B
after, cap 12,288 B) instead, which has headroom. Re-measured:
`embarch-outpost/spec.md` 9,775 B → **8,316 B** (reserve threshold is
10,240 − 1,024 = 9,216 B), `check-doc-size.py` no longer names it.

Both `Must not delete:` items were re-read after the edit and neither moved:
the `--allow-unverified-join`/`--allow-build-id-mismatch` pairing is still in
§3's invariant-61 paragraph verbatim, and the missing/short `frame_bytes`
degrade-not-refuse sentence is still there too, byte-for-byte, in
`spec.md` §3 (not the section that moved).

**Can `spec.md` alone still answer what someone needs to work on this
component today?** Mostly yes, with one narrower exception than before: the
architecture, invariants, the measured-cost table, and the manifest/join
refusal rules are all still in `spec.md` untouched. What it no longer answers
standalone is the *exact byte layout* of the three `streams/` output files —
for that it now points to `interfaces/integration.md` § Host-side outputs,
one hop away, right next to the Kconfig table that already governs the same
integration surface. That's a legitimate split, not a loss: the outputs
section was reference material (column names, formatting contracts) that
belongs beside the other "how this DUT-facing surface behaves in detail"
material, not narrative "what is true now" prose — spec.md keeps the latter
and points at the former.

Gate run from the doc worktree: `python3 scripts/check-docs.py` — all 11
checks green. `python3 scripts/check-doc-size.py` — clean, `spec.md` no
longer named (21 files in reserve suite-wide, all filed elsewhere).
`check-ownership.py --scope outpost` — OK, all 3 changed paths owned by
`outpost`. Code worktree (`embarch-outpost`) has a zero diff, as the
dispatch note predicted — no C touched, so this does not deepen the
already-recorded debt that this environment cannot run `tests/unit`'s Zephyr
ztest suite (no `west`, no `ZEPHYR_BASE`); that suite was not run and is not
claimed green.
