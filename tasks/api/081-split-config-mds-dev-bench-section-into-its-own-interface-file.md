# 081 — Split `embarch-api/interfaces/config.md`'s `[dev_bench]` section into its own interface file

**State:** done — worker, 2026-09-13, `agent/api/081-split-dev-bench-config` (code) /
`agent/api/081-split-dev-bench-config-doc` (doc)
**Source:** supervisor, leg 108, 2026-09-13 — filed against the size-reserve debt parked in
`tasks/api/071`, which is `blocked` on `In flux: yes` and stays blocked. See "Why this is not that
task" below.
**Scope:** api
**Hardware:** none — documentation only. No board, no build, no running Core.
**Owner:** no

## What

`embarch-api/interfaces/config.md` is **11,198 / 12,288 B (91.1%)** — inside the last 10% of its cap
and therefore in reserve. It has four top-level sections:

| section | line | bytes |
|---|---|---|
| Where the config comes from | 7 | — |
| `[core]` — one instance | 16 | — |
| `[[projects]]` — zero or more | 30 | 6,962 |
| `[dev_bench]` — zero or one | 64 | 2,349 |

Move the whole `[dev_bench]` section, **verbatim**, into a new
`embarch-api/interfaces/dev-bench-config.md`, and leave a one-line cross-reference where it was.

`DOC-BUDGET.md` line 25 already covers the new file: `<sub-project>/interfaces/<topic>.md` at 12 KB.
No budget entry needs adding, and no owner-reserved file is touched. The move takes `config.md` to
roughly **8,850 B**, out of reserve with about 2,200 B of headroom.

## Why this is not `tasks/api/071`, and why `In flux: yes` does not forbid it

`071` parks a **compaction pass** — a squeeze that rewrites prose — on the grounds that `api/070`
just touched two of this file's rows and the text should be re-checked against `src/config.rs`,
`src/tools.rs` and `src/dev_bench.rs` before anyone shortens it. That reasoning is correct and it
stays correct.

**It does not apply to a verbatim split**, because a split restates nothing: every byte that moves
arrives byte-identical, so there is no way for it to encode a claim that is about to become wrong.
`DOC-COMPACTION.md` §2 names a mission split as the cheaper move where one fits, `DOC-BUDGET.md`
line 47 says outright that a parked compaction task is a deferral and not a wall — *"it does nothing
about the reserve, so the next unit to write there hits the cap mid-flight anyway"* — and
`tasks/ui/043` demonstrated the whole argument on 2026-09-13: `decisions/trace-view.md` paid 2,295 B
by splitting and **not one sentence of live reasoning was deleted anywhere in the suite.**

So `071` is left exactly as it is, `blocked`, with its `Size debt due: 2026-09-25`. If this task
lands, `config.md` leaves reserve and that debt is discharged rather than paid; say so in the
commit, and do **not** edit `071`'s `In flux:` field to make it dispatchable.

## Must not delete — carried verbatim from `tasks/api/071`

Nothing in this list may be shortened, reworded, merged or re-ordered. It applies to the text in
**both** files after the split:

- Every field's Type/Req/Default/Notes row for `[core]`, `[[projects]]` and `[dev_bench]` — the
  schema reference is this file's whole purpose.
- The `env` additive-semantics note on **both** the `[[projects]]` and `[dev_bench]` rows. `api/070`
  just corrected these two into agreement; a split that separates them is exactly the shape that
  lets them silently re-diverge, so after the split each file must still carry its own copy of the
  note and the two must still say the same thing.
- Every numbered `../decisions/*.md` citation.
- The retirement notices for `soc_chip_overrides` and `[[projects.targets]]` — both are
  config-load-time failures a reader needs to recognize.

## The citation problem this move creates, which is the real work

`tasks/doc/044` records it as a class: **a verbatim split is the one move `check-decision-refs.py`
cannot see.** The numbers still resolve, so the gate stays green while a citation now points at a
file that no longer holds the thing cited. So:

- Sweep the **whole suite** — this repo including `history/`, `tasks/` and
  `embarch-decision-reversals.md`, plus the `embarch-api` source tree and any other repo's docs —
  for references to `interfaces/config.md`, and repoint every one whose subject moved.
- A **path-qualified** citation (`interfaces/config.md`'s `[dev_bench]` row) must be repointed. A
  citation that names only the section, or points at content that did not move, must be left alone.
- Report the sweep's outcome **either way**, including "I found nothing else". A clean result is the
  only thing that tells the next leg this file's citations are settled, and it is exactly the
  sentence a worker omits when it finds nothing.

## Done when

1. [x] `embarch-api/interfaces/dev-bench-config.md` exists and holds the `[dev_bench]` section
   **byte-identical** to its text at this task's parent commit. Prove it: extract the section from
   both sides and `diff` them, and put the exit status in the report. The only new prose anywhere is
   the new file's title line, a `Current truth:` header line matching its siblings' convention, and
   one cross-reference line in each file pointing at the other.
2. [x] `embarch-api/interfaces/config.md` is out of reserve — under 11,059 B — and still carries every
   item on the Must-not-delete list that belongs to it.
3. [x] The suite-wide citation sweep above is done and its outcome reported either way.
4. [x] `python3 scripts/check-docs.py` is green in `embarch-doc`, including `check-doc-size.py` and
   `check-decision-refs.py`.
5. [x] `tasks/api/071` is **untouched**. This task's own file is closed `done`.

## What shipped

`config.md`'s `[dev_bench]` section (lines 64–81 at the parent commit, 2,349 B) moved verbatim to
new `embarch-api/interfaces/dev-bench-config.md`. `diff` of the section extracted from both sides:
**exit status 0** — byte-identical. New prose is exactly the new file's title line, its
`**Status:**` line, a `Current truth:` line matching siblings' convention, and one cross-reference
line in each direction — nothing else. `config.md` is now **8,978 B** (was 11,198 B), out of
reserve with ~2,220 B headroom; `dev-bench-config.md` is well under its 12 KB
`interfaces/<topic>.md` cap.

**Citation sweep:** searched this repo (including `history/`, `tasks/`, `embarch-decision-reversals.md`),
`embarch-api`'s whole source tree, and every other sub-project repo
(`embarch-core`, `embarch-umbrella`, `embarch-study-designer`, `embarch-topology`, `embarch-dev-bench`,
`embarch-outpost`, `embarch-ui`, `embarch-fleet`) for `interfaces/config.md` and for `dev_bench`
co-mentions. **Found nothing to repoint.** Every existing citation of `interfaces/config.md` is
either generic (points at the file as the config doc overall — `embarch.md`, `spec.md`,
`decisions.md`'s index lines) or names a different, un-moved section (`[[projects]]`'s
`build_cwd`/`soc_chip_overrides`/snippet semantics, or the top-of-file "where the config comes
from" convention, cited from `embarch-umbrella/src/init.rs` and `embarch-study-designer/src/registry.rs`).
None named `[dev_bench]` or content that moved. This file's citations are settled; no repoint
needed anywhere.

Code branch (`agent/api/081-split-dev-bench-config`) carries zero commits, as expected — pure doc
split, `check-ownership.py --code-repo` confirms 0 changed paths.

Gate: `python3 scripts/check-docs.py` — all 11 checks green (including `check-doc-size.py`,
`check-decision-refs.py`). `check-client-names.py --repo <code worktree>` — clean. `check-ownership.py
--scope api` (doc worktree) and `--code-repo` (code worktree) — both green.

`tasks/api/071` untouched — its `In flux: yes` and `blocked` state stand; this task's landing
discharges its size-reserve debt rather than paying it, per this file's own reasoning above.

## Not in scope

- Any change to `config.md`'s prose beyond moving the section and adding the cross-reference.
- Any change to `embarch-api`'s source. The code branch for this unit is expected to carry zero
  commits.
- Retiring `artifact_path_for_core`'s toleration (`embarch-api` decision 64) — that is cross-repo
  work this task must not start.
