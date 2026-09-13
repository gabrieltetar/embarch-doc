# 086 — `embarch-api/decisions/shape.md` is in reserve after decision 64's "Ends when" fired

**State:** done
**Source:** suite task 038 amended decision 64 in place (`embarch-umbrella` stopped scaffolding
`artifact_path_for_core`, so the first clause of that decision's "Ends when" has fired), which put
this file into its reserve band; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/shape.md
**Size debt due:** 2026-09-27
**In flux:** no — this is a decisions file, not a "what is true now" doc. Its entries are settled
records, and the one entry currently moving (64) has just been amended and is now parked on a
condition only the owner can check. The right first move is **the split**, not a rewrite: a
verbatim split restates nothing, and `DOC-BUDGET.md`'s split-first rule applies cleanly to a file
that is many independent decisions rather than one sprawling one. Run
`python3 scripts/check-doc-size.py --decisions` before choosing.

**Must not delete:**
- Decision 64's **two-clause** "Ends when" and its 2026-09-13 amendment. The whole value of that
  entry now is that the first clause has fired and the second has not, and that the second is a
  fact about real machines rather than about this suite. Collapsing it to "tolerated" loses the
  unpark condition, which is one grep.
- The **"Default for the next retired key: refuse by name"** sentence. That is the general rule the
  entry exists to establish; `artifact_path_for_core` is the exception to it, not the subject.
- The `[verified 2026-09-10]` tag and what it was verified against. A verification date on a claim
  about another repo's source is the thing that tells a later reader whether to re-check it.

## Why now

`python3 scripts/check-doc-size.py` names `embarch-api/decisions/shape.md` at 11731/12288 B
(95.5%, 557 B left) — inside the last 10% reserve band (`RESERVE_FLOOR` = 1200 B). It was already
well inside before this amendment; the amendment is what made it worth filing rather than what
caused it.

## Done when

- [x] `embarch-api/decisions/shape.md` is back under its reserve band with every "must not delete"
      fact intact — a verbatim split along decision boundaries is the first thing to try.
- [x] If it is split, every decision number that moves keeps its own size pin (`tasks/doc/052`
      records that a verbatim split drops those silently).
- [x] Gate green (`../../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment.

## Shipped

`check-doc-size.py --decisions` first: none of `shape.md`'s 9 decisions appear on the per-decision
over-4096-B list (the largest, 53, is 3,586 B) — this is many independent decisions over-cap at the
file level, not one sprawling one, so **split**, not rewrite, per the task's own framing.

Split along the existing precedent (`tests.md`, `api/023`): decisions **53** and **64** — the
`[[projects.targets]]` retirement and the general "retired keys refused by name" rule, the two that
are actually about config-schema retirement — moved verbatim into a new
`embarch-api/decisions/config-retirement.md`. Decision **61** (the `dev_bench_hello` CLI twin)
stayed in `shape.md`: it is a case of decision 3/10's "identical capabilities" rule, which also
stays there, and moving it would have forced an extra cross-reference update
(`interfaces/tools-dev-bench.md`) for no size benefit. `shape.md`: 11,731 B → 6,093 B (49.6% full,
well clear of reserve). `config-retirement.md`: 6,488 B, also well clear of its 12,288 B cap.

Neither decision 53, 61 nor 64 carries an entry in `scripts/decision-size-baseline.json` (none ever
exceeded the 4,096 B per-decision cap), so there was no per-decision pin to carry across — checked,
not assumed.

Every "must not delete" fact carried over verbatim into `config-retirement.md`: decision 64's
two-clause "Ends when" and its 2026-09-13 amendment, the "Default for the next retired key: refuse
by name" sentence, and the `[verified 2026-09-10]` tag with what it was verified against.

Updated `embarch-api/decisions.md`'s routing table (two rows now, sizes and decision lists both
corrected) and every live cross-reference that pointed at `decisions/shape.md` for 53 or 64:
`spec.md`, `open.md`, `interfaces/config.md` (×2), `interfaces/tools-discovery.md`, and
`decisions/zephyr.md`. `check-decision-refs.py` passes clean (0 stale topic-file links, 0 unresolved
references) and `check-doc-size.py` shows `shape.md` PAID and out of reserve.

`embarch-umbrella/decisions/mirrors.md` still names `embarch-api/decisions/shape.md` in a backtick
mention of decision 64 (not a markdown link, so no gate sees it, and `embarch-umbrella` is out of
this worker's scope) — harmless: the number still resolves to the `api` sub-project, just not to
the exact file any more, same as every legacy bare-number reference this suite already tolerates.

Code worktree (`embarch-api/086-compact-api`): no changes needed, nothing pushed — this was
doc-only, as expected. Doc worktree pushed on `agent/api/086-compact-api`.
