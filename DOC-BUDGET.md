# The doc-size budget

**Status:** active, 2026-09-07.

What a doc may weigh and what counts as a debt. `scripts/check-doc-size.py` implements and enforces all of it; [DOC-COMPACTION-PASS.md](DOC-COMPACTION-PASS.md) is how a debt is paid. A file may shrink freely; it may never grow past `min(cap, its baseline)`.

| Role | Cap | Path |
|---|---|---|
| Spec — what is true now | **10 KB** | `<sub-project>/spec.md` |
| One spec group, where it outgrows a file | **10 KB** | `<sub-project>/spec/<topic>.md` |
| Decisions — why | **25 KB** | `<sub-project>/decisions.md` |
| One decision group, where they outgrow a file | **12 KB** | `<sub-project>/decisions/<topic>.md` |
| Open questions | **5 KB** | `<sub-project>/open.md` |
| One open-questions group, where they outgrow a file | **5 KB** | `<sub-project>/open/<topic>.md` |
| Interface reference, only where big | **15 KB** | `<sub-project>/interfaces.md` |
| One interface group, where they outgrow a file | **12 KB** | `<sub-project>/interfaces/<topic>.md` |
| Suite-level doc | **10 KB** | `suite/*.md` |
| A complete inventory table — every row must be there | **15 KB** | `suite/roadmap.md` |
| An assembled inventory — the budget is per row, and there is **no** per-file cap | **none** | `suite/features.md`, from `features.d/` |
| A narrative guide | **25 KB** | `suite/{user,studies}-guide.md` |
| A protocol doc | **12 KB** | `DOC-*.md` |
| Reversals index | **10 KB** | `embarch-decision-reversals.md` |
| Reversal range | **20 KB** | `reversals/rows-<a>-<b>.md` |
| Assembled history — **no reserve**, it rolls itself | **20 KB** | `history/*.md`, rolled to `history/archive/` |

**This table is `embarch-doc`'s corpus only.** `embarch-fleet` has its own ratchet, `scripts/check-fleet-doc-size.py`, run by its `deploy.py`: the same caps-plus-baseline mechanism and no reserve band, because the reserve keeps a *worker* from meeting a wall mid-edit and no worker writes those files.

A file pinned over its cap retires its baseline on reaching the cap and is capped from then on. `--report` shows the corpus, `--update` records progress and **refuses a regression**, `--pressure` lists what is near its limit **before** a task that must write there is dispatched. Per-sub-project overrides tighten a cap where [the second pass](DOC-COMPACTION-PASS.md) has landed.

**An assembled file has no byte cap.** An inventory of a suite still being built has no quiet state, so every row must be there and the budget is the row's (600 B, `build_features.py`; [features.d/](features.d/README.md)). Its 20 KB was called a backstop until `features.md` sat at 20,444 of 20,480 B and **every legitimate fragment breached it** — a wall in front of a generator, not a discipline anyone can exercise.

**The last `max(1.2 KB, 10%)` of a limit is the RESERVE, and it is writable** — a cap a worker meets only when its edit is refused turns unrelated work into a compaction task mid-flight. A file in reserve still passes the gate but must be named on a `**Compacts:**` line of an open task **in the scope directory of the doc being compacted**, not `tasks/doc/`, **filed by whoever spends it, in the same commit**: that actor alone can answer the in-flux question ([DOC-COMPACTION-PASS.md](DOC-COMPACTION-PASS.md)). `tasks/README.md` has the shape.

**The floor exists because a percentage of a small cap is not runway.** 10% of a 5 KB `open.md` is 512 B, while single amendments here have cost 350 B, ~940 B and 1,548 B — so the old line warned some files with a seam still to cut and others 22 bytes from the wall (`core-link.md`; `features.md` had 36). **The floor files debts earlier, not later, and that is the point**: 1.2 KB out, a file can still be split; 22 bytes out, it can only be squeezed.

**A parked compaction task parks the pass, not the reserve.** `In flux: yes` correctly refuses a separate pass, but the next unit to write the file still meets the cap mid-flight. So **the compaction rides in the unit about to write that file** — same actor, same commit, carrying the parked task's `Must not delete:` list and closing only that file's item. That actor is the one *making* the flux, so it alone can shorten a paragraph without writing a clean statement of something about to be wrong.

**A SPLIT IS THE DEFAULT REMEDY and squeezing is the exception.** A split by mission moves entries **verbatim**, so it restates nothing, the in-flux objection cannot apply, and no argument is shortened to pay for a new one. Squeezing pays for a new argument out of old reasoning, and the reader never learns what was cut. So a task filed by the reserve **proposes a split first**, and compacts only where there is no seam — one mission — where it says so and **deletes an answered question** rather than tightening a live one. **A full `open.md` of live questions is no squeeze**: its debt is paid by a split into `open/<topic>.md`. Check a seam's inbound links before cutting (`tasks/umbrella/022` nearly moved the wrong decision), and run `scripts/check-duplication.py <sub-project>` first: two files in reserve side by side are often one re-arguing what the other owns.

**The worked example is how this rule was written.** One new rule pushed `embarch-fleet/ops.md` 1.2 KB past its ratchet; four squeeze passes went into paying for it, the last nearly deleting evidence for a question the fleet has not answered; the split that replaced them took one move and lowered that file's baseline by 2,553 B for good.

**The cap is the design constraint, not a target to approach.** It forces the question "is this the most valuable 10 KB I can write about this component".

## The ledger: an overrun lands once, on a clock

**A cap does not refuse a correct edit.** A file may exceed its limit by up to **2 KB** — one amendment — if and only if the overrun is on an open item's `**Compacts:**` line *and* that item carries `**Size debt due:** <yyyy-mm-dd>`. Past the date, or past the 2 KB, the gate fails. `--due` prints the ledger, soonest first, and exits non-zero when anything is overdue.

**Because refusing at the wall does not prevent growth, it displaces it somewhere nothing is watching.** Three measured cases in two days: three units spent their reserve shaving Status rows to clear fourteen bytes; a task parked on `In flux: yes` sat at 22 bytes with the argument that unparked it written inside it; and a supervisor **filed a decision in the wrong file** because the right one, `embarch-api/decisions/zephyr.md`, had 96 bytes left. **A cap that misfiles is worse than a cap that refuses**, because nothing fails and the reader never learns — so **a decision goes in the file of its subject, never the one with room**, and a full file's overrun lands here.

**Two bounds, because a grace with one bound is a licence.** The bytes stop a file drifting up in "one amendment" steps; the date stops a debt being parked. **A missing due date fails the same as an unrecorded debt**: on 2026-09-07 **13 of 28 reserve debts were filed only against a blocked task**, so no leg was ever offered one.

**A date is set once, from the day the debt opens.** Nothing here can tell a date quietly moved forward; it is a reserved path, so the move shows in the diff and is an owner act. **A leg spends its first unit on the oldest overdue entry**, blocked or not (`leg.md`), so docs debt costs a scheduled share of throughput instead of ambushing whichever unit touched a full file.

**So a `blocked` debt with no date fails the gate, in reserve as well as over the limit.** An *open* debt in reserve is offered to a leg on its own, so its clock is a backstop; a blocked one is never offered, so the clock is its only drain. `In flux:` is answered **per file** — `tasks/README.md` has why.

## The ratchet moves in steps

A baseline records where an over-cap file has got to and **never rises**. It lands on the next **1 KB** boundary above the new size, not the exact byte: `min(old baseline, next step above size)`, still monotone. **Pinning to the exact byte means "no correct edit may ever be made here"** — `ops.md` at 29,701/29,701 and `protocol.md` at 32,466/32,466 had **zero** headroom, a hard stop wearing a gradient's clothes. With steps, a shrink that crosses a boundary earns real room. Room is always earned and never returned.

## The per-decision cap: 4 KB

A file-level cap cannot tell **many decisions** from **one sprawling decision**, and that difference decides the remedy. `--decisions` reports every `### N` entry against a 4 KB cap. Entries already over it when it was introduced are pinned and may not grow past the pin; **an unpinned breach fails nothing**, and `--decisions` lists every one.

**4 KB is measured, not chosen.** Over all 307 decisions on 2026-09-07: median 1,395 B, p75 2,435 B, p90 3,904 B, max 10,605 B. So 4 KB sits at about p90 and put 26 entries over, every one a sprawl rather than a well-argued entry.

**The worked example is why this exists.** `embarch-umbrella/decisions/bind.md`'s **decision 22 alone was 10,605 of the file's 11,409 bytes**. The file-level view says "split it"; a file of one decision cannot split, and every pass that tried was working on the wrong object. The right instruction is per decision: compact that entry, or make it two numbered decisions if it is really two arguments.

**A decision gets a printed margin, not a reserve** (`tasks/doc/067`): `--pressure` lists each one over or within 256 B of its limit, for the dispatch note. A debt per thin decision would be 35 tasks today; failing would make a 3,840 B cap.
