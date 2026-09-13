# 059 — Split decision 42 out of `embarch-umbrella/decisions/doctor.md` into its own `locate-api.md`

**State:** done — leg 108, 2026-09-13, `agent/umbrella/059-split-locate-api-doc`. Decision 42 moved
byte-identical (`diff` exit 0) into new `embarch-umbrella/decisions/locate-api.md`; `doctor.md`
6,039 B, out of reserve. Citation sweep found two path-qualified hits on decision 42
(`tasks/umbrella/009-compact-docs.md`, twice) and the index row in `embarch-umbrella/decisions.md`,
all repointed; `interfaces/doctor-chain.md`'s "(decisions 38, 42)" is a bare number with no file, left
alone per this task's own rule. `check-docs.py`: all 11 green. Code branch carries zero commits, as
expected. One residual: `scripts/decision-size-baseline.json`'s pin is keyed
`embarch-umbrella/decisions/doctor.md#42` and could not be re-keyed to `locate-api.md#42` from here
(`scripts/` is off-limits to a worker) — `check-doc-size.py --decisions` now shows it `OVER` rather
than `pin`, which does **not** fail the gate (only a pinned decision growing past its own baseline
does), but the pin itself is stale until someone with `scripts/` access reseeds it. Filed as
`inbox/doc-reseed-locate-api-decision-42-pin.md`.
**Source:** supervisor, leg 108, 2026-09-13 — filed against the size-reserve debt parked in
`tasks/umbrella/048`, which is `blocked` on `In flux: yes` and stays blocked. Its
`Size debt due: 2026-09-20` is the soonest date on the whole ledger that a split can reach. See "Why
this is not that task" below.
**Scope:** umbrella
**Hardware:** none — documentation only. No `doctor` run, no board, no install.
**Owner:** no

## What

`embarch-umbrella/decisions/doctor.md` is **11,082 / 12,288 B (90.2%)** — in reserve, with 1,206 B
left. It holds exactly three decisions:

| decision | bytes | subject |
|---|---|---|
| 18 | 2,754 | Check 5 distinguishes "no probe attached" from "a probe is attached but this user cannot open it" |
| 31 | 2,412 | Check 14: which program Core would flash each chip family with |
| **42** | **5,157** | **`locate_api` reads the agent CLI's own registration and `setup`'s install directory, not just `PATH`** |

Move **decision 42 alone**, verbatim, into a new `embarch-umbrella/decisions/locate-api.md`, and
leave a one-line cross-reference in `doctor.md`.

**Decision 42 is the seam because it is not a check.** This file's mission, stated in its own title,
is *what `doctor` checks*. Decisions 18 and 31 are each one numbered check and its reasoning.
Decision 42 is a **resolution mechanism** — how umbrella finds `embarch-api` at all — which several
checks then consume. It is also 47% of the file on its own, so moving it is both the cleanest
mission cut and the only one that pays the debt. `doctor.md` drops to roughly **5,950 B**, out of
reserve with about 5,100 B of headroom.

**Decision 42 is `pin`ned over the 4 KB per-decision cap and stays pinned.** `check-doc-size.py
--decisions` lists it as `pin`, not `OVER`; that is an accepted state, it is not what this task is
about, and **nothing here may shorten decision 42 to chase it.** Carry the pin across with the text
if the ledger records it per-file; if the gate complains after the move, say so and stop rather than
trimming the decision.

`DOC-BUDGET.md` line 22 already covers the new file: `<sub-project>/decisions/<topic>.md` at 12 KB.
No budget entry needs adding, and no owner-reserved file is touched.

## Why this is not `tasks/umbrella/048`, and why `In flux: yes` does not forbid it

`048` parks a **compaction pass** — a squeeze that rewrites prose. Its flux answer is `yes` and it
stays `yes`; leg 070 corrected that task from `open` to `blocked` for exactly the right reason and
this task does not undo that.

**A verbatim split is a different operation.** It restates nothing: every byte that moves arrives
byte-identical, so there is no way for it to encode a claim that is about to become wrong — which is
the entire hazard the flux field exists to catch. `DOC-COMPACTION.md` §2 names a mission split as
the cheaper move where one fits; `DOC-BUDGET.md` line 47 says outright that a parked compaction task
is a deferral and not a wall, *"it does nothing about the reserve, so the next unit to write there
hits the cap mid-flight anyway"*; and `tasks/ui/043` demonstrated it end to end on 2026-09-13 —
2,295 B paid with not one sentence of live reasoning deleted anywhere in the suite.

So `048` is left exactly as it is, `blocked`, with its date. If this task lands, `doctor.md` leaves
reserve and that debt is discharged rather than paid; say so in the commit, and do **not** edit
`048`'s `In flux:` field to make it dispatchable.

## Must not delete

- Decision 42's full text, including its rationale for reading the agent CLI's own registration and
  `setup`'s install directory rather than trusting `PATH`.
- Line 7's `Current truth:` pointer in `doctor.md` — `tasks/umbrella/047` corrected it from
  `../spec.md` to `../interfaces/doctor-chain.md` to match its five siblings, and that correction is
  what pushed this file into reserve in the first place. The **new** file needs its own
  `Current truth:` line following the same convention.
- Decisions 18 and 31 in full, untouched.

## The citation problem this move creates, which is the real work

`tasks/doc/044` records it as a class: **a verbatim split is the one move `check-decision-refs.py`
cannot see.** The number still resolves, so the gate stays green while a citation now points at a
file that no longer holds the thing cited. Decision 42 is consumed by checks documented elsewhere in
this repo, so expect real hits. So:

- Sweep the **whole suite** — this repo including `history/`, `tasks/` and
  `embarch-decision-reversals.md`, plus the `embarch-umbrella` source tree and any other repo's docs
  — for **path-qualified** references to `decisions/doctor.md`, and repoint every one whose subject
  is decision 42.
- A citation that names only `decision 42` with no file, or that points at decision 18 or 31, must
  be left alone.
- Also check `embarch-umbrella/interfaces/doctor-chain.md` specifically: it is the file `047`
  repointed `doctor.md` *at*, so it is the most likely place to cite back.
- Report the sweep's outcome **either way**, including "I found nothing else". A clean result is the
  only thing that tells the next leg this file's citations are settled, and it is exactly the
  sentence a worker omits when it finds nothing.

## Done when

1. `embarch-umbrella/decisions/locate-api.md` exists and holds decision 42 **byte-identical** to its
   text at this task's parent commit. Prove it: extract the decision from both sides and `diff`
   them, and put the exit status in the report. The only new prose anywhere is the new file's title
   line, its `Current truth:` header line, and one cross-reference line in each file pointing at the
   other.
2. `embarch-umbrella/decisions/doctor.md` is out of reserve — under 11,059 B — and still holds
   decisions 18 and 31 unchanged plus its corrected `Current truth:` line.
3. The suite-wide citation sweep above is done and its outcome reported either way.
4. `python3 scripts/check-docs.py` is green in `embarch-doc`, including `check-doc-size.py` and
   `check-decision-refs.py`.
5. `tasks/umbrella/048` is **untouched**. This task's own file is closed `done`.

## Not in scope

- Shortening decision 42 to bring it under the 4 KB per-decision cap. It is pinned; leave it pinned.
- `embarch-umbrella/decisions/bind.md`, which is 93.9% full and holds a 10,691 B pinned decision 22
  — a much harder problem parked in `tasks/umbrella/009`. Do not touch it.
- Any change to `embarch-umbrella`'s source. The code branch for this unit is expected to carry zero
  commits.
- Anything about check 5's permission-denied probe, check 17's arms, or check 13 — all standing
  hardware debts, none of them a documentation move.
