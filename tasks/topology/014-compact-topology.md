# 014 — `embarch-topology/open.md` is in reserve

**State:** done — agent/topology/014-compact-topology, 2026-09-08
**Source:** `scripts/check-doc-size.py`'s reserve floor, added 2026-09-07
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/open.md
**Size debt due:** 2026-10-08

## What

`open.md` is **4,206 / 5,120 B (82.1%), 914 B left**. It crossed on the rule
change rather than on an edit: reserve was 90% of a limit, which for a 5 KB
`open.md` is 512 B, and 512 B is not one amendment's runway — the 2026-09-06
fold records single additions of 350 B, ~940 B and 1,548 B. Reserve is now
`max(1200 B, 10%)` from the top.

**Prefer a split.** [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: a split
restates nothing, so it costs no argument, and a file warned 1.2 KB out still
has a seam to cut. This one may not have a seam — a 5 KB `open.md` is a role
cap on a single file, and `tasks/umbrella/009` records reaching exactly that
wall — in which case say so and delete an answered question instead.

`topology/008` took this same file from 97.9% to 56.0% on 2026-09-06 by
deleting answered questions, so the recent history of what is answerable is
short and worth reading before cutting.

## Why now

The debt is real once a file is within one amendment of its cap, and recording
it is the whole mechanism: an unfiled file in reserve is what
`check-doc-size.py` fails on, not the reserve itself.

## In flux: no

Nothing here is mid-argument as of 2026-09-07 — `topology/012` and `013` are
open against `decisions.md`, not this file.

## Done when

- [x] `open.md` is out of reserve, or the task says why it cannot be and what
      was deleted instead.
- [x] Whichever it was — split or delete — is stated, with the byte numbers
      before and after.

## Resolution — 2026-09-08, agent/topology/014-compact-topology

**No seam found, as the task itself suspected.** `open.md` has no
mission-based split axis the way `decisions.md`/`interfaces.md` do (§3 gives
this file no sub-split), so this was a delete pass, not a move.

Read every bullet against `decisions.md`'s four files and `spec.md`. Three of
the eleven were not actually unresolved:

- **The `detected_by` over-crediting bullet** — decision 24 already states
  this exact acceptance ("accepted rather than chased … under-sells how much
  was pinned down without asserting something false"). Nothing here would
  ever be "unblocked"; it was decisions.md's own conclusion wearing an
  open-question frame.
- **The Nordic mismatch-exposure bullet** — same shape: decision 21 already
  says a chip on the fallback-register path "would come back *mismatch*
  rather than *undeclared*… accepted on the same terms." Restated, not open.
- **The "no agent can induce a mismatch" bullet** — this one was not even a
  duplicate-in-spirit, it was a literal duplicate: `spec.md`'s own "Where it
  stands" section already asserts "No agent can induce one… there is no
  topology override on the store path… unsettable for an already-running
  service" as *current truth*. `open.md`'s own header says "Unresolved only.
  Current truth: spec.md" — this had drifted across that line.

Deleted all three (`git log -p` holds them). `scripts/collect-open-questions.py`
diff confirms nothing else moved: 106 → 103 questions suite-wide, exactly the
three removed, verbatim, nowhere re-added.

**Byte numbers: 5,016 → 3,669 B (98.0% → 71.7% of the 5,120 cap) — out of
reserve** (`check-doc-size.py --pressure` now reports `PAID … is out of
reserve; close its item`). No new decision authored, per this leg's
burndown constraint — nothing here needed one.

**Answering the pass's own question:** yes, `spec.md` alone still answers
what someone needs to work on this component today — none of the eight
remaining `open.md` bullets are things `spec.md` asserts; they are genuinely
open (an unbuilt alert path, an unread signal byte, a documented resolution
gap in `NotFound`, a real unknown bench fact, two live silicon-coverage
gaps, an unspecified caller contract, and two tracked-elsewhere mirror/
detection gaps). The three cut ones were the only ones that had quietly
become answers.

Gate: `cargo build`/`test`/`clippy --all-targets -D warnings` green in the
code repo (no code change was needed — doc-only task); `check-docs.py` green
except one **pre-existing, out-of-scope** `check-links.py` red
(`tasks/api/051-....md -> ../../embarch-fleet/burndown.md`, an `api`-scope
task file, nothing this task touched); `check-client-names.py` and
`check-ownership.py --scope topology` (both repos) clean.

## Spend recorded against this task

**2026-09-08, leg 054, folding `topology/022` (doc `e420bf5`): `open.md` 4,841 → 5,016 B, +175,
leaving 104 B of headroom against the 5,120 cap.** `topology/022` amended `decisions/crate.md`
decision 4 to say the `embarch-umbrella/src/token.rs` mirror is closed, and its reviewer found that
the mirrors bullet here still counted that mirror among two that "still raise the
extract-or-CI-diff question" — a line the unit's own landing made wrong. I corrected it in the fold
rather than filing it, and the correction costs bytes because the honest version has to say *how*
the mirror closed (a direct call, which is a third answer neither of this bullet's two had) rather
than just dropping it. Recorded here rather than filed as a new task, per `tasks/topology/022`'s own
reserve note. **104 B is the tightest this file has been**; the next edit to it very likely cannot
be paid this way and this pass should run first.
