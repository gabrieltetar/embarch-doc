# The doc-size budget

**Status:** active, 2026-09-07.

**Split out of [DOC-COMPACTION.md](DOC-COMPACTION.md) §2 on 2026-09-07**, under
that file's own split-first rule: adding the ledger and the per-decision cap
below took it into reserve, and a verbatim move restates nothing, so no argument
had to be shortened to make room for a new one. `DOC-COMPACTION.md` §2 is a
pointer, so every `§2` reference across the suite still resolves — there were
twelve.

`scripts/check-doc-size.py` implements everything here.
[DOC-COMPACTION.md](DOC-COMPACTION.md) is the method that pays a debt;
this is what counts as one.

`scripts/check-doc-size.py` enforces this in CI. A file may shrink freely; it may never grow past `min(cap, its baseline)`.

| Role | Cap | Path |
|---|---|---|
| Spec — what is true now | **10 KB** | `<sub-project>/spec.md` |
| Decisions — why | **25 KB** | `<sub-project>/decisions.md` |
| One decision group, where they outgrow a file | **12 KB** | `<sub-project>/decisions/<topic>.md` |
| Open questions | **5 KB** | `<sub-project>/open.md` |
| Interface reference, only where big | **15 KB** | `<sub-project>/interfaces.md` |
| One interface group, where they outgrow a file | **12 KB** | `<sub-project>/interfaces/<topic>.md` |
| Suite-level doc | **10 KB** | `suite/*.md` |
| A complete inventory table — every row must be there | **15 KB** | `suite/roadmap.md` |
| An assembled inventory — the budget is per row, and there is **no** per-file cap | **none** | `suite/features.md`, from `features.d/` |
| A narrative guide | **25 KB** | `suite/{user,studies}-guide.md` |
| A protocol doc | **12 KB** | `DOC-*.md` |
| Reversals index | **10 KB** | `embarch-decision-reversals.md` |
| Reversal range | **20 KB** | `reversals/rows-<a>-<b>.md` |
| Assembled history | **20 KB** | `history/*.md`, rolled to `history/archive/` |

**This table is `embarch-doc`'s corpus only.** The `embarch-fleet` repo — the fleet's own rules, which a leg never checks out — was covered by nothing until 2026-09-05, and its two design docs drifted to 32 KB while `risks.md` cited this section as the cap that had split it out. It now has its own ratchet, `embarch-fleet/scripts/check-fleet-doc-size.py`, run by that repo's `deploy.py`: same caps-plus-baseline mechanism, no reserve band, because the reserve exists to keep a *worker* from meeting a wall mid-edit and no worker ever writes those files.

**Nothing is over cap and the baseline holds no exceptions.** A file that is somehow pinned reaches its cap, retires its entry, and is capped from then on. `--report` shows the corpus, `--update` records progress and **refuses a regression**, `--pressure` lists what is near its limit **before** a task that must write there is dispatched. Per-sub-project overrides tighten a cap where [the second pass](DOC-COMPACTION-PASS.md) has landed.

**An inventory of a suite still being built has no quiet state**, so the in-flux warning's wait never comes and no pass helps — every row must be there. `suite/features.md` is therefore **assembled**, one fragment per row, and the budget it answers to is the row's ([features.d/](features.d/README.md)).

**So an assembled file has no byte cap at all, as of 2026-09-07: the one it had became the constraint it was written not to be.** The 20 KB was called a backstop, then `features.md` sat at 20,444 of 20,480 B, so **every legitimate fragment breached it** and three units spent their reserve shaving Status-column rows — the third to clear 14 bytes. A cap the file's own assembler breaches on every valid addition is a wall in front of a generator, not a discipline anyone can exercise. The per-row cap (600 B, `build_features.py`) is the real one, and the only one an author can act on.

**The last `max(1.2 KB, 10%)` of a limit is the RESERVE, and it is writable** — a cap a worker meets only when its edit is refused turns unrelated work into a compaction task mid-flight. A file in reserve still passes the gate but must be named on a `**Compacts:**` line of an open task **in the scope directory of the doc being compacted**, not `tasks/doc/`, **filed by whoever spends it, in the same commit**: that actor alone can answer the in-flux question ([DOC-COMPACTION-PASS.md](DOC-COMPACTION-PASS.md)). `--pressure` lists the reserve, filed and unfiled; `tasks/README.md` has the shape.

**The floor exists because a percentage of a small cap is not runway.** 10% of a 5 KB `open.md` is 512 B, while single amendments here have cost 350 B, ~940 B and 1,548 B — so the old line warned some files with a seam still to cut and others 22 bytes from the wall (`core-link.md`, measured 2026-09-07; `features.md` had 36). A worker dispatched at either cannot write the sentence its task exists to add. **The floor files debts earlier, not later, and that is the point**: 1.2 KB out, a file can still be split; 22 bytes out, it can only be squeezed.

**A parked compaction task is a deferral, not a wall.** `In flux: yes` correctly refuses a *separate* compaction pass — but it does nothing about the reserve, so the next unit to write there hits the cap mid-flight anyway, which is what the reserve exists to prevent. On 2026-09-05 it did something worse than that: `embarch-api/decisions/zephyr.md` had 96 bytes left, so a decision that belonged in it was **filed in `decisions/shape.md` instead** — the first time in this suite a byte cap moved a decision rather than shortening one. **A cap that misfiles is worse than a cap that refuses**, because nothing fails and the reader never learns.

So when a file is in reserve and its task is `blocked` on `In flux: yes`, **the compaction rides in the unit that is about to write that file** — same actor, same commit, carrying the parked task's `Must not delete:` list and closing only that file's item. That actor is the one *making* the flux, so it is the only one who can shorten a paragraph without writing a clean statement of something about to be wrong.

**A SPLIT IS THE DEFAULT REMEDY and squeezing is the exception** — reversed 2026-09-07 from "splitting is the other move". A split by mission (§3) moves entries **verbatim**, so it restates nothing, the in-flux objection cannot apply, and no argument is shortened to pay for a new one. Squeezing pays for a new argument out of old reasoning and fails in a way nothing catches: the reader never learns what was cut. So a task filed by the reserve **proposes a split first**, and compacts only where there is no seam — one mission, or a role cap on a single file as a 5 KB `open.md` is — where it says so and **deletes an answered question** rather than tightening a live one. Check a seam's inbound links before cutting (`tasks/umbrella/022` nearly moved the wrong decision), and run `scripts/check-duplication.py <sub-project>` first: two files in reserve side by side are often one re-arguing what the other owns.

**The worked example is how this rule was written.** One new rule pushed `embarch-fleet/ops.md` 1.2 KB past its ratchet; four squeeze passes went into paying for it, the last nearly deleting evidence for a question the fleet has not answered; the split that replaced them took one move and lowered that file's baseline by 2,553 B for good.

**The cap is the design constraint, not a target to approach.** A budget forces the question "is this the most valuable 10 KB I can write about this component", never asked before there was one.

## The ledger: an overrun lands once, on a clock

**A cap no longer refuses a correct edit.** A file may exceed its limit by up
to **2 KB** — one amendment — if and only if the overrun is recorded on an open
item's `**Compacts:**` line *and* that item carries a
`**Size debt due:** <yyyy-mm-dd>`. Past the date, or past the 2 KB, the gate
fails. `check-doc-size.py --due` prints the ledger, soonest first, and exits
non-zero when anything is overdue.

**Because refusing at the wall does not prevent growth, it displaces it
somewhere nothing is watching.** Three measured cases in two days: three units
spent their reserve shaving Status rows to clear fourteen bytes; a supervisor
**filed a decision in the wrong file** because the right one had 96 bytes left,
which is §2's own *a cap that misfiles is worse than a cap that refuses*; and a
task parked on `In flux: yes` sat at 22 bytes with the argument that unparked
it written inside it.

**Two bounds, because a grace with one bound is a licence.** The bytes stop a
file drifting up in "one amendment" steps; the date stops a debt being parked.
**A missing due date fails the same as an unrecorded debt** — `blocked` was an
absorbing state, and on 2026-09-07 **13 of 28 reserve debts were filed only
against a blocked task**, so no leg was ever offered one.

**A date is set once, from the day the debt opens.** Nothing here can tell a
date quietly moved forward; it is a reserved path, so the move shows in the
diff and is an owner act. **A leg spends its first unit on the oldest overdue
entry**, blocked or not (`leg.md`), so docs debt costs a scheduled share of
throughput instead of ambushing whichever unit touched a full file.

**So a `blocked` debt with no date fails the gate, in reserve as well as over
the limit** (2026-09-09, `tasks/doc/030`; the over-limit rule already demanded
one). That is the whole residue of the absorption: an *open* debt in reserve is
offered to a leg on its own, so its clock is a backstop, while a blocked one is
never offered and the clock is its only drain. With one, `blocked` is a resting
state and `In flux: yes` may keep implying it; without one, it is the bucket.
`In flux:` is also answered **per file** — `tasks/README.md` has that rule and
why a per-task field kept outliving the file it was about.

## The ratchet moves in steps

A baseline records where an over-cap file has got to and **never rises**. It
now lands on the next **1 KB** boundary above the new size rather than on the
exact byte: `min(old baseline, next step above size)`, which is still monotone
and cannot raise anything.

**Because pinning to the exact byte means "no correct edit may ever be made
here".** Measured 2026-09-07: `ops.md` at 29,701/29,701 and `protocol.md` at
32,466/32,466, both at **zero** headroom — a hard stop wearing a gradient's
clothes, and why one new rule in `ops.md` cost four squeeze passes before a
split replaced them. With steps, a shrink that crosses a boundary earns real
room; a file already pinned tight stays tight until someone shrinks it. Room is
always earned and never returned.

## The per-decision cap: 4 KB

A file-level cap cannot tell **many decisions** from **one sprawling
decision**, and that difference decides the remedy. `check-doc-size.py
--decisions` reports every `### N` entry against a 4 KB cap, ratcheted the same
way files are and seeded with the entries already over it, so each may only
shrink.

**4 KB is measured, not chosen.** Over all 307 decisions in the corpus on
2026-09-07: median 1,395 B, p75 2,435 B, p90 3,904 B, max 10,605 B. So 4 KB
sits at about p90 and puts 26 entries over — a tractable list, and every one of
them a sprawl rather than a well-argued entry.

**The worked example is why this exists.**
`embarch-umbrella/decisions/bind.md` is 92.8% full, parked in
`tasks/umbrella/009` for days, and its **decision 22 alone is 10,605 of the
file's 11,409 bytes — 92%**. The file-level view says "split it"; the file has
essentially one decision in it, so a split cannot help, and every pass that
tried was working on the wrong object. The per-decision view gives the right
instruction: compact that entry, or make it two numbered decisions if it is
really two arguments.
