# 060 — `embarch-api/open.md` is 221 bytes inside its reserve floor

**State:** done — closed by leg 085, 2026-09-11, at `api/067`'s fold. **Not by a further squeeze:
the file left reserve on its own.** `embarch-api/open.md` is **3,469 B against a 5,120 B cap —
67.8%, clear of the 3,920 B reserve floor by 451 B**, and `check-doc-size.py --pressure` now
reports it `PAID ... close its item`. Later units removed bullets this file had recorded as open
questions once they stopped being open; none of them was a compaction pass. **The finding below
stands and is the reason this task is worth reading**: two passes each squeezed this file to
within single digits of the floor and each deleted a fact recorded nowhere else in the suite, and
the argument that the 5 KB cap is the wrong lever (made here and independently in
`tasks/core/036`) was never answered — it is `DOC-BUDGET.md`'s call and `DOC-BUDGET.md` is
owner-reserved. Closing this task closes a byte-count debt, not that argument.

**Previous state:** blocked — leg 074, `agent/api/060-compact-api`. `open.md` cut 4,208 → 4,124 B (84 B of
connective filler); still 204 B inside reserve. Debt dated 2026-09-24, left unpaid — no safe
further cut or split found without risking a repeat of `api/026`'s lost fact; see finding below.
Unparks when either: `DOC-BUDGET.md`'s cap is revisited (the owner's call, argued for below) or a
future pass finds a genuine cut this one did not.

**Supervisor's dispatch note, leg 074, 2026-09-10.** Dispatched as an ordinary unit: `In flux: no`,
nothing overdue on the ledger, and `api/042` landed earlier in this leg without touching `open.md`.
**Three outcomes are acceptable and the third is not a failure**: cut ~221 B of genuine filler;
split the file verbatim if a seam exists; or **conclude there is no safe cut left and say so in
this file**, leaving the debt dated and unpaid. This file has been squeezed once already
(`api/026`) and that pass **deleted a fact recorded nowhere else in the suite** — the reviewer
found it by sweeping nine documents. Read the `Must not delete:` block as binding, in particular
the restored sentence it names.
**Raising the cap is explicitly NOT in scope.** This task's own body argues `open.md`'s 5 KB cap
may be too tight, and `tasks/core/036` makes the same argument independently. That is
`DOC-BUDGET.md`'s call and `DOC-BUDGET.md` is owner-reserved — no worker and no supervisor may
change it. If you conclude the cap is the real problem, **say so in this task file as a finding**
and leave it; do not edit `DOC-BUDGET.md`, and do not treat the cap as negotiable while cutting.
**Reserve in `api` after `api/042` landed** (re-measure before you rely on these): `open.md`
4,141/5,120 B is the subject; `decisions/tool-wrapping.md` has ~66 B left and `decisions/zephyr.md`
and `decisions/core-link.md` are both **over** cap — do not add to any of the three.
`interfaces/tools.md` was split and paid earlier in this leg.
**Source:** `api/026`'s fold, leg 073, 2026-09-10. `api/026` squeezed this file to 3,914 B — six
bytes under a 3,920 B floor — and its reviewer then found that the squeeze had **deleted a fact
recorded nowhere else in the suite** (`inbox/api-026-squeeze-quoting-and-lost-fact.md`, resolved at
the fold rather than filed as its own task). Restoring that fact cost 227 B and put the file back
inside reserve. `DOC-COMPACTION.md` §2 — the commit that spends the reserve is the one that files
the debt, and this is that filing.
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/open.md
**Size debt due:** 2026-09-24
**In flux:** no. `api/026` established this for both its files and its reasoning holds: the
event-stream flux that parked the old `api/026` moved out into `decisions/study-events.md` and was
settled by `api/035` against a real Core.
**Must not delete:** the restored sentence itself — **"`embarch init` never writes `serial_port` at
all"**, with its pointer to `embarch-umbrella` decision 17's minimal discovery schema. The reviewer
swept `embarch-umbrella/spec.md`, `decisions/projects.md`, `decisions/integration.md`,
`embarch-api/interfaces/config.md`, `interfaces/tools.md`, `decisions/core-link.md`,
`history/api.md`, `suite/features.md` and `features.d/*` at merge `04929b8` and found the claim
stated **nowhere else** — umbrella decision 17 describes the minimal schema without ever naming
`serial_port`. It was deleted, not moved, and it is back only because a reviewer caught it. Also
inherited from `api/026`: decision 15's failure signature, decision 36's rejected
`Builder::thread_stack_size` and its 64 MiB/512 MiB pair, decision 26's correction, and decision
55's corrected `default_headers` rejection — all of which live in `decisions/core-link.md` and were
untouched.

## What

`embarch-api/open.md` is **4,141 B against a 5,120 B cap, 979 B left against a 1,200 B floor** —
221 B inside reserve.

## Why this one should probably not be paid by squeezing

**This file has now been squeezed twice in three days and both passes ended with a reviewer putting
a fact back.** `api/031` cut it 4,802 → 3,782 B; `api/026` cut it again to 3,914 B, six bytes under
the floor, and lost the `serial_port` aside doing it. The same thing happened to
`embarch-core/open.md` in the same leg (`tasks/core/036`). Two independent passes tuned to within
single-digit bytes of a floor, each losing one real claim, is evidence about the floor rather than
about the compactors.

So the outcome this task should be willing to reach is **"no safe cut remains, and the cap is wrong
for what this file holds"** — written down as an argument, with what was considered. That is a real
finding, not a failure to complete. `DOC-COMPACTION.md` §2 prefers a split, and this file has six
named sections, so a split has at least not been tried.

**Changing the cap is not this task's to do** — `DOC-BUDGET.md` carries it. If the conclusion is
that the cap is wrong, say so here and file it for the owner.

## Done when

- [x] `embarch-api/open.md` is clear of its reserve floor (≤ 3,920 B), **or** this task closes with
      a written argument that no safe cut or split remains, naming what was considered and whether
      the cap is the thing that should move. — **Neither cleanly.** See finding below: 4,208 → 4,124 B
      (84 B of genuine connective filler cut), still 204 B inside reserve. No further cut was made.
- [x] The restored `serial_port` sentence and every other `Must not delete:` item is still readable
      in full. Verified by re-reading the file after edit: the `serial_port` sentence, decision 15's
      failure signature, decision 36's `Builder::thread_stack_size` rejection, decision 26's
      correction and decision 55's `default_headers` rejection are all untouched (the latter four
      live in `decisions/core-link.md`, which this task did not open).
- [x] The commit message quotes the **first dozen words of every deleted hunk verbatim**
      (`DOC-COMPACTION-PASS.md`). See commit message.
- [x] The commit message answers the human question in the compactor's own words: can
      `embarch-api/spec.md` alone answer what someone needs to work on `embarch-api` today?
- [x] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).

## Finding: 84 B cut, no more available without risking a repeat of `api/026`

Three genuinely connective, fact-free phrases were cut, verbatim:
- `, and it fired` — dropped from the alert/enrolled-board bullet; the sentence still states the
  same failure (`link_port_interface` reached Core's wire body and was silently dropped) without
  the added drama.
- `; revisit otherwise` — dropped from the inbound-trust bullet; it was a bare directive to
  reconsider later, not a recorded fact.
- `Re-read suite-wide; none acquired a new argument.\n\n` — the standalone sentence under
  `## Settled-deferred`, describing the review process rather than any of the five settled items
  it introduces.

That is 84 B, `4,208 → 4,124 B`. The reserve floor is 3,920 B — **204 B still inside reserve.**

No further cut was attempted. Every remaining sentence in this file, checked clause by clause,
either names a fact not recorded elsewhere (task numbers, decision numbers, byte counts, dates,
the specific rejected APIs) or is the rationale a future reader needs to tell "settled" from
"still open" — the same shape of clause that `api/026` cut once already, calling it filler, and
that turned out to be the one sentence recorded nowhere else in the suite. Two independent passes
in three days (`api/031`, `api/026`) each read this file, each concluded a further cut was safe,
and each lost a real fact that a reviewer had to restore by hand. A third pass reaching the same
conclusion under the same time pressure is not more trustworthy than the first two; it is the same
process producing the same failure mode again.

A split was considered and not attempted. The file has four section headers (`## Known wrong /
unfinished`, `## Owed decisions`, `## Structural limits`, `## Settled-deferred`), not six as this
task's dispatch note counted — `## Owed decisions` and `## Structural limits` are each a single
paragraph, too short to be a standalone file without themselves needing a new cross-reference back
into `open.md`, which would cost bytes rather than save them net. `## Settled-deferred` (5 bullets,
~950 B) is the one section large enough that splitting it would matter, but `open.md`'s role per
`DOC-PROTOCOL.md` is to be the single place a reader checks for "is this still true" — splitting
settled-vs-open questions across two files works against that role for every future reader, for a
one-time gain that does not reduce how much text exists, only where it lives. This task did not
attempt it.

**This is the same finding `tasks/core/036` reached about `embarch-core/open.md`, independently,
in the same leg: the floor is being reached by real content, not filler, and the cap
(`DOC-BUDGET.md`) is the thing that should move, not this file.** Changing it is out of this
task's scope. The debt is dated 2026-09-24 and left unpaid at 4,124 B, 204 B inside reserve.

**Human question, answered:** can `embarch-api/spec.md` alone answer what someone needs to work on
`embarch-api` today? No. `spec.md` states what the crate does and its invariants; `open.md` is
where the gaps between that and reality live — the unconfirmed `board` field, the unpinned mirror
that already broke once, `study_watch`'s untested reconnect path, the missing `error_kind`, and
`init`'s silent omission of `serial_port`. Someone working the crate needs both files; `spec.md`
alone would let them re-introduce a bug this file already records as known-broken.
