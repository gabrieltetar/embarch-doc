# 087 — Three decision files point at `open.md` items that are gone, and one of those pointers is now false

**State:** done — worker umbrella/087, 2026-09-17, `agent/umbrella/087-open-md-pointers`. All three
coordinates re-derived and confirmed to hold as the sweep described (see `## Verification` below).
**Source:** leg 144's refill sweep, 2026-09-17 — a mechanical check of every `open.md` pointer in
`embarch-umbrella/decisions/` against what `embarch-umbrella/open.md` actually still carries.
**Scope:** umbrella
**Hardware:** none — three markdown files. **Do not run `doctor`, do not touch a board.**
**Owner:** no

## What

Three decision files defer something to `embarch-umbrella/open.md`, and in all three cases the item
they defer to is no longer there. One of them is not merely dangling — it **contradicts another
decision file in the same directory**:

1. **`decisions/locate-api.md` (around line 26) is false, not just stale.** It says:

   > **Neither check 8 nor check 11 has run inside a live `doctor` yet** — that needs a live Core and
   > stays in [`open.md`](../../embarch-umbrella/open.md).

   But `decisions/budgets.md` (around line 40) already records:

   > **Verified on a bench** [2026-09-07, `tasks/umbrella/034`]. `embarch doctor` on the primary
   > `wsl-host` bench now prints check 11 as **PASS** …

   Check 11 running to PASS inside a live `doctor` means check 8 ran too — they are the same chain.
   So `locate-api.md` asserts as an open debt something the suite has a dated bench measurement
   against, and `open.md` no longer carries the bullet either pointer names.

2. **`decisions/budgets.md` (around line 52)** and **3. `decisions/projects.md` (around line 113)**
   each reference an `open.md` item that no longer exists there. These are dangling pointers rather
   than false claims — but a pointer into a file that has moved on is how a reader concludes the
   question is still open.

**Re-derive every coordinate above before editing** — line numbers, both quoted sentences, and above
all **whether `open.md` really no longer carries each item**. The sweep read them; you verify them.
"This does not hold" is a correct outcome to report, and for item 1 it is the one that matters most:
do not correct a sentence to match a measurement you have not confirmed is in `budgets.md` and dated.

## Why now

The false one is the reason. A decision file that says a check has never run, sitting three files
away from a dated bench run of that check, is exactly the kind of self-contradiction that makes a
reader distrust the whole directory — and this suite's measured-vs-stated discipline is the thing
being undermined.

## Done when

- [x] `decisions/locate-api.md`'s sentence reflects what `budgets.md` measured: say what **has** run
      in a live `doctor` and when, citing `budgets.md`'s own dated line rather than restating its
      evidence. If some part of that debt genuinely survives (e.g. a specific field neither run
      read), keep exactly that part and say what it is.
- [x] `decisions/budgets.md` and `decisions/projects.md`'s dangling `open.md` pointers are resolved:
      either re-pointed at where the question now lives, or the sentence is rewritten to stand on its
      own without the pointer. **Do not "fix" one by adding the item back to `open.md`** — that is
      `open.md`'s own question, not this task's, and `open.md` is at 85.4% of its cap.
- [x] **Watch the size caps.** `decisions/bind.md` is at **94.0%**, `decisions/projects.md` at
      **90.8%**, `decisions/install.md` at **98.2%** and `open.md` at **85.4%** — all four are in or
      near the reserve, and all four are already filed against blocked compaction tasks
      (`umbrella/009`, `umbrella/084`, `umbrella/079`, `umbrella/077`). **Write tightly: aim to end
      net-neutral or smaller on `projects.md`.** Prefer cutting a restatement to adding a
      qualification. No new compaction task is needed — these are already filed — but say in your
      report what each file's byte count was before and after.
- [x] **Do not restate `embarch-core`'s `sweep_study_results` mechanism or any other decision's
      content** to justify an edit. `decisions/projects.md` decision 26 already carries mechanisms in
      full; a second copy in a file with 1.1 KB of headroom is the failure `DOC-PROTOCOL.md` exists
      to prevent. Cite, never restate.
- [x] A `changelog.d/` fragment for the `locate-api.md` correction — that one is reader-facing,
      because it changes what the docs say has been verified.
- [x] Gate green per `../../embarch-fleet/protocol.md` §10.

## Verification

Re-derived independently rather than trusted from the sweep's description:

- **Item 1 holds.** `open.md` (read in full) carries no bullet about check 8 or check 11 never
  having run in a live `doctor`. `decisions/budgets.md` decision 44 does record, dated
  2026-09-07 (`tasks/umbrella/034`), `embarch doctor` on the primary `wsl-host` bench printing check
  11 as PASS. Whether that also means check 8 ran turns on `doctor` not short-circuiting: `spec.md`
  line 55 calls `embarch doctor` "the full check chain", and `interfaces/doctor-chain.md` lists 1–18
  as one ordered sequence with no early-exit language; budgets.md's own dated paragraph confirms the
  same run also reached check 13 (later in the order), which only happens if the run did not stop
  at 11. So check 8, earlier still, ran too. `locate-api.md` is corrected to say this, citing
  decision 44 rather than restating its evidence.
- **Item 2 holds.** `decisions/budgets.md`'s closing sentence of decision 45 pointed at "the debt in
  `open.md`" (the ambiguity between a timed-out call and a refused connection). No bullet in
  `open.md` carries that debt. Rewritten to stand alone without the pointer.
- **Item 3 holds.** `decisions/projects.md` decision 41 called picking among several recorded builds
  "`open.md`'s undecided half". No bullet in `open.md` carries that question — decision 41 itself
  settles it (name all, pick none). The parenthetical is removed rather than re-pointed, since the
  decision already stands on its own.

Byte counts (`wc -c`), before → after:

| file | before | after | delta |
|---|---|---|---|
| `decisions/locate-api.md` | 4579 | 4668 | +89 |
| `decisions/budgets.md` | 7845 | 7829 | -16 |
| `decisions/projects.md` | 11163 | 11116 | -47 |

`projects.md` ends smaller, as asked. `locate-api.md` grows by 89 B — it is not one of the four
capped files this task named, and stating a corrected, cited fact plus the one-clause reasoning for
it could not be done in fewer bytes than the false claim it replaces without losing the citation.

Also fixed, found while running the doc gate: the task's own `## What` section quoted
`locate-api.md`'s original sentence verbatim, including its markdown link `[\`open.md\`](../open.md)`
— correct relative to `decisions/locate-api.md`, broken relative to this task file's own location.
`check-links.py` flagged it pre-existing (confirmed red on `git stash` before any of my edits).
Repointed to `../../embarch-umbrella/open.md`, correct from `tasks/umbrella/`.

No new decision. Nothing dropped in `embarch-doc/inbox/` — no decision was needed to resolve any of
the three coordinates.

`embarch-umbrella` (code repo): doc-only task, no source touched. Gate run on baseline for an honest
report — see below.

## Not yours

- **No new numbered decision.** Correcting a stale sentence inside an existing decision is not a new
  decision; if you find yourself wanting to *decide* something, stop and drop it in
  `/home/gabriel/Github/embarch/embarch-doc/inbox/` as a task instead.
- **Do not touch `embarch-umbrella` source, `doctor`'s check chain, or check 13's baseline.** Check
  13's `FAIL` is a live question recorded elsewhere and is not in scope.
- **Do not edit `open.md`'s content** beyond confirming what it does and does not carry.
