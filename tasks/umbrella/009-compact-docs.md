# 009 — embarch-umbrella's open.md and decisions/bind.md are in reserve

**State:** blocked
**Source:** scripts/check-doc-size.py --pressure
**Scope:** umbrella
**Hardware:** none
**Compacts:** embarch-umbrella/decisions/doctor.md, ~~embarch-umbrella/open.md~~, ~~embarch-umbrella/spec.md~~, embarch-umbrella/decisions/bind.md
**Reserve:** `spec.md`'s item was paid 2026-09-05 (`umbrella/006`, ride-along under `016`); it is out at 87.9%. `open.md`'s was paid the same day, **`umbrella/017` put it straight back in** at 94.5%, and **`umbrella/018` paid it again as a ride-along, 2026-09-06 — 4,840 → 4,591 B (89.7%)**. **`decisions/doctor.md` took its place**: 10,634 → 11,674 B (95.0%) in the same unit, because check 17's `bind-too-narrow` arm needed both its defect and the two rejected repairs argued in decision 22(a). `018` compacted the retired 22(b) and 22(c) entries and a dozen sentences elsewhere in that file and still landed at **11,519 B (93.7%)**, so it is filed here rather than paid. **`umbrella/020` paid it on 2026-09-06 by splitting, not squeezing** — `018`'s judgement that the file could go no further without deleting live reasoning was taken as evidence. Decision 22 moved verbatim into a new [`decisions/bind.md`](../../embarch-umbrella/decisions/bind.md) (check 17, its own mission, the way `012` and `015` split this file before), leaving `doctor.md` at **6,188 B (50.4%)** and `bind.md` at **8,465 B (68.9%)** after the two amendments `020` added there. **A split restates nothing, so `In flux: yes` never applied to it** — [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2's own preference. `020` also spent `open.md` and paid it in the same commit: 4,591 → 4,601 B (89.9%), the new check-17 step in and three sentences of history and duplication out. The pass is owed on all three regardless. **`umbrella/021` put both back, 2026-09-06, and this is the tightest `open.md` has ever been left.** That unit fixed check 17's `bound-narrow` fix line — the class it names now comes from the arguments `setup` itself reads — and both halves had to be written down: `open.md` 4,601 → **5,080 B (99.2%)**, one bullet for the `saved.host` stickiness it found in `doctor` check 2 and deliberately did not fix; `decisions/bind.md` 8,465 → **11,409 B (92.8%)**, one amendment carrying two defects and both losing arguments. **`open.md` has 40 bytes left.** `021` shortened its own bullet twice rather than touch the protected prose below, found no cross-doc duplication (`check-duplication.py` reports none for this sub-project), and judged that the remaining slack is wording rather than content — so the next unit to write this file cannot ride along the way `018` and `020` did, and either splits nothing (5 KB is a role cap on a single file) or genuinely deletes. That is the state this task exists to be handed. **`umbrella/022` paid `open.md` back to 5,080 → 4,661 B (91.0%) on 2026-09-06** by deleting the "Whether `init` should warn on a repo holding more than one recorded build" bullet as answered (decision 41) — still in reserve, but no longer at the wall, and that deletion is the whole of it: `022` added nothing to the file. **The same unit split `decisions/projects.md` rather than spending its reserve.** Decision 41 is 1,548 B against 1,381 B of headroom, so the file could not hold it; decisions 10 and 12 — where the `embarch/` folder lives and what it may touch, which is a different subject from what `init` derives — moved verbatim into a new [`decisions/integration.md`](../../embarch-umbrella/decisions/integration.md), leaving `projects.md` at **10,491 B (85.4%)** with 41 in it and `integration.md` at 2,325 B. **A split restates nothing, so `In flux: yes` did not apply**, the same reasoning `020` used. The seam was checked before it was cut: nothing outside `embarch-umbrella/` links `projects.md` for decisions 10 or 12, while `embarch-api/decisions/build.md` and `embarch-decision-reversals.md` link it for 26 and 17 — which is why **26 was the wrong decision to move**, obvious though it looks, since three of its inbound links are in a repo a worker may not edit.
**And `decisions/doctor.md` is back in, put there by the same unit — 6,188 -> 11,095 B (90.3%).** `023` traded one file's reserve for another's deliberately: [decision 42](../../embarch-umbrella/decisions/doctor.md) is 4.9 KB carrying a defect, a contested ranking with its losing alternative, the measurement that settles it, and a residual left unfixed, and putting it in `topology.md` beside its sibling decision 38 would have taken that file over cap outright. **It is filed here rather than as a new task**, per `check-doc-size.py`'s own note that one item may name several files of one sub-project. **Barely in** — 1,193 B of headroom, and 37 B of wording would have kept it out, which is exactly the shave this file's history says not to take.

**`open.md`'s item is closed, `umbrella/023`, 2026-09-06 — 4,661 -> 4,527 B (88.4%), out of reserve.** Paid the way `022` paid it, by deletion rather than squeezing, and by the task that earned the deletion: `023` answered the `embarch-api`-not-located half of check 11's bullet, so that clause left the file instead of being rewritten shorter, and the check-8 bullet — whose whole content was a *prediction* of a run — became a one-line statement of the one thing still unrun. The new material went to [decision 42](../../embarch-umbrella/decisions/doctor.md) instead, which is where decision 38's own residual already lives. **No protected clause was touched**: check 15's not-a-hash note, check 17's two Fail branches with which half each arm settles, and `saved.host`'s stickiness with the reason it was left unfixed are all verbatim. `decisions/bind.md` is untouched at 11,409 B (92.8%) and its item stays open, and the pass stays parked on `In flux:` below — which `023` did not make any less true: it wrote `decisions/doctor.md` (6,188 -> 10,293 B, 83.7%) and one row of `spec.md`'s table.

**In flux:** yes — the open umbrella tasks still rewrite the doctor table in spec.md, and check 17's entry, now [`decisions/bind.md`](../../embarch-umbrella/decisions/bind.md), is owed a live narrow-bound Core **and an answer to whether `embarch-core install --bind 0.0.0.0` rewrites an existing narrow registration** (`020`), either of which rewrites it again. (`007` closed 2026-09-05; `spec.md`'s reserve item was paid there as a ride-along, under `016`. The *pass* is still this task's and is still parked.)
**Must not delete:** spec.md's eighteen-row `doctor` table, and in particular which rows are **designed and unbuilt** — decisions have described checks that do not exist, the doc asserted four of them as shipped for weeks, and that table is now the only place the distinction lives; open.md's note that check 15 is not a hash comparison and must not be read as one; open.md's note that check 17's two Fail branches have never met a real narrow-bound Core, **and which half of that debt each arm settles** (`018`); in **`decisions/bind.md`** (decision 22 moved there 2026-09-06, `020`), 22(a)'s record that a loopback hit discriminates nothing and that a fix line could green its own check — **now twice over**, `bind-too-narrow`'s and `bound-narrow`'s, which are different arms with different conditions and neither collapses into the other; and, added by `umbrella/021`, **both losing arguments in `bind.md`'s last amendment** — *retract the "cannot disagree" claim instead of fixing the input* (it loses because the **fix line**, not the decision, is what a human reads while deciding what to type, so a doc that accurately describes a lie still ships the lie) and *leave the `remote` arm unguarded because the fixed input makes it unreachable* (it loses because that makes a printed remedy's correctness depend on an invariant held two hundred lines away in a struct field's initialiser). Both read as redundant once shortened and neither is; and `open.md`'s note that `saved.host` is sticky and `doctor` check 2 still reads it, **including why it was left unfixed** — that is a deliberate abstention, and without the reason it reads as an oversight somebody will "fix" on a guess.

**Supervisor note, leg 016, 2026-09-06 — this task's own unpark condition has now fired, and it
disagrees with its `In flux:` field.** "Why blocked" below says *unparks when the umbrella queue
is down to one open task, whichever it is.* With `019`, `020` and `021` all closed this leg,
**the umbrella queue is down to zero open tasks** — so the condition is met twice over, while
`In flux:` still reads `yes` and `supervise.md` forbids dispatching a compaction task whose flux
field says yes. **Do not resolve that by dispatching anyway, and do not resolve it by flipping
the field to make the queue move.** The two facts are both true: nothing else is competing for
this sub-project's docs *and* check 17's entry is still owed a live narrow-bound Core. The next
leg should read the `In flux:` reason on its merits and either park it again with a sharper
condition or run the pass knowing exactly which sentence it may be about to make stale.

**And the reserve is not parked with it — `open.md` has 40 bytes.** `DOC-COMPACTION.md` §2's
ride-along, which `018` and `020` both used, is what has kept this file writable for three
units, and `021` reports it is spent: no cross-doc duplication remains, 5 KB is a role cap on a
single file so nothing can split, and what is left is protected prose. **The next umbrella unit
that writes `open.md` at all meets the cap mid-task** — the first time in this log that a
reserve has actually become a wall rather than a debt notice.

**Counts refreshed by `umbrella/017`, 2026-09-05.** The table is now **eighteen rows**, and **one** decision is designed-and-unbuilt: `umbrella/017` built 22(a) as check 17 and retired 22(b) and 22(c) unbuilt, which deleted two rows outright, leaving only 26's `--prune`. A `Must not delete:` clause that preserves a table *by a count* is worse than useless once the count is stale, so whoever runs this task protects **eighteen rows / one unbuilt decision**, not the earlier nineteen/five, twenty/four, twenty/three or twenty/two.

**`open.md` is back in reserve, and `umbrella/017` is what put it there.** That unit resolved decision 22 — built (a) as check 17, retired (b) and (c) — which closed the "two designed pieces are confirmed unbuilt" bullet but opened a new one: check 17's two Fail branches have never met a real narrow-bound Core, and that debt has to be written down somewhere. `open.md` 4509 → **4840 B (94.5%)**; `spec.md` went the other way, 9014 → **8966 B (87.6%)**, because retiring 22(b-c) deleted two table rows. Filed here rather than as a second task, per `tasks/README.md`.

This task stays `blocked` on `In flux: yes`, which is still true.

## What

`spec.md` is at ~93% of 10 KB and `open.md` at ~94% of 5 KB. Both had a pass on
2026-09-04 whose main find was a duplication rather than cold prose:
`decisions/doctor.md` was re-arguing build status that `spec.md`'s table owns,
worth ~1.2 KB. Run `scripts/check-duplication.py embarch-umbrella` before
anything else — the same class may still be there between `spec.md` and
`decisions/projects.md` or `decisions/release.md`.

## Why blocked

Tasks 003–008 are all open, all in this sub-project, and between them they build
`setup --dry-run`, check 10's handshake, `doctor --prune`, check 5's
not-permitted branch, check 8's shellout and check 11's `embarch-api versions`
read. **Every one of those changes a row of the table this task would be
compacting**, and several close an `open.md` bullet outright. Compacting first
means writing a clean statement of five things about to become false.

**Unparks when the umbrella queue is down to one open task**, whichever it is.
Not on a timer, and not on "enough of them landed".

**And meanwhile the reserve was not parked with it, 2026-09-05 — and is now paid.** Neither
file can be split — 10 KB and 5 KB are role caps on single files — so shortening was the
only move, and `DOC-COMPACTION.md` §2's ride-along rule put it inside the units doing the
rewriting. `open.md` went 5,051 → 4,388 B in the owner's live-`doctor` pass and `spec.md`
10,089 → 9,131 B in `umbrella/006`, which also spent 526 B more of `open.md` and gave it
back. **What `umbrella/006` moved rather than deleted**, since a move restates nothing and
so survives the in-flux objection: `spec.md`'s "Committing a repo integration" section into
[decision 12](../../embarch-umbrella/decisions/integration.md), and `open.md`'s measured v17
reading into [decision 35](../../embarch-umbrella/decisions/schema-skew.md). What it deleted
outright: the runtime-path half of the Shape diagram, and a question `open.md` itself called
closed. **Refresh the counts above before trusting them.**

**This task got further away, not closer, on 2026-09-05.** Its unpark condition is "the
umbrella queue is down to one open task", and that queue went from two to five: the
owner's live `doctor` run filed `010`, `011` and `012`. That is the condition working —
three of sixteen checks were found dark on the primary topology, and every one of them
rewrites a row of the table this task would be compacting.

## Done when

- [x] `open.md` out of reserve, `umbrella/023`, 2026-09-06 (4,527 B, 88.4%); **`decisions/doctor.md` went back in the same unit at 90.3%.** All four files out of reserve. `spec.md` (9006 B, 87.9%) and `decisions/doctor.md` (6188 B, 50.4%) are out and stay out. **`decisions/bind.md` went back in with `umbrella/021`, 2026-09-06 and is untouched at 11,409 B (92.8%); `open.md` was paid out by `umbrella/023` and its item is closed** — see **Reserve** above for what each spent it on and why `open.md`'s 40 remaining bytes make a ride-along impossible next time.
- [ ] The unbuilt/built distinction survives, per row.
- [ ] No question disappears from `collect-open-questions.py` unless you can
      name it as answered.
- [ ] `DOC-COMPACTION.md` §7's question answered in the commit message.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
