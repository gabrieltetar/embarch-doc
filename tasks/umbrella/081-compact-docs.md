# 081 — `embarch-umbrella/decisions/projects.md` is at cap, not just in reserve

**State:** done — leg 140, 2026-09-17, `agent/umbrella/081-compact-projects`.

**Dispatch note (supervisor, leg 140).** This is the leg's first unit because the ledger says so:
`--due` puts this entry at **1 day left** and the file at **12,286/12,288 B — 2 bytes**, the only
`filed`-not-`PARKED` entry in the whole pressure list. Treat the cap as a wall you are standing on,
not a line you are near: **make your first edit a removal or a move, not an addition**, or your very
first write fails the gate.

**What else is in reserve in `umbrella`, so you plan instead of discover:**
`decisions/install.md` 12,071/12,288 (217 B left, filed → `tasks/umbrella/079`, blocked);
`decisions/bind.md` 11,533/12,288 (755 B, filed → `tasks/umbrella/009`, blocked);
`open.md` 3,954/5,120 (1,166 B, filed → `tasks/umbrella/077`, blocked). All three are already filed
against, so you owe no new compaction task for them — but **do not solve `projects.md` by moving
prose into `install.md`**, which has 217 bytes and would simply relocate the wall.

**One ordering fact the body cannot know:** `tasks/umbrella/082` is `open` in this same queue and is
specifically about **decision 26** — the very decision this task's "candidate seam" suggests moving.
If you move 26, say in your report exactly which file it landed in and what its new anchor is; the
supervisor re-points `082` at the fold. Do not edit `tasks/umbrella/082` yourself.

**Source:** `scripts/check-doc-size.py --pressure`, run by `tasks/umbrella/080` (leg 139,
2026-09-17), whose own edit is what pushed this file here.
**Scope:** umbrella
**Hardware:** none
**Compacts:** embarch-umbrella/decisions/projects.md
**Size debt due:** 2026-09-18 — **pulled in from the 2026-10-17 the filing worker wrote, by leg 139
at this unit's fold.** Thirty days is the right default for a file that has *entered reserve*; this
one is at **2 bytes**, and the task's own body says the next unit that writes here at all "meets the
cap immediately, with no slack to word around." A ledger date is supposed to say when the debt
becomes blocking, and this one is blocking now — a month out would let an unrelated `umbrella` unit
hit a hard wall mid-flight, which is the exact ambush the dated ledger replaced. Overdue tomorrow
means the next leg spends its first unit here, which is the intended behaviour and not a penalty.
**In flux:** no — decision 55 (below) closes the one open question this file carried
(`embarch-api/open.md`'s `serial_port` referral). Nothing else in the umbrella queue currently
touches `projects.md`; the historical note under `tasks/umbrella/009` about `umbrella/022`
splitting decisions 10/12 out of this file (into `integration.md`) is settled, not ongoing.

## What

`080` added decision 55 (`init` never writes `serial_port`, deliberately) to
`decisions/projects.md`, landing the file at **12,286/12,288 B — 2 B left, 100.0%.** That is not a
normal reserve entry: the file is functionally full, and the next unit that needs to write here
at all — an amendment to 13, 17, 26, 41 or 55, or a new decision that genuinely belongs in this
group — meets the cap immediately, with no slack to word around.

`projects.md` groups four decisions each with real amendment history (17's cross-repo interop
verification and its target-count-check migration; 26's `--prune` deferral and the `build_dir_name`
gap; 41's board-placeholder mechanism and rejected alternatives) plus decision 55. This group has
been split before — twice (`umbrella/022` moved decisions 10/12 out to `integration.md`;
`umbrella/037` moved decision 19 out to `dev-bench-firmware.md`, both times because the pass
restates nothing and a verbatim move is not blocked by `In flux: yes`). The same move — pull one
self-contained decision out to its own file — is the likely fix here, not prose-shortening, since
none of the four remaining topics is stale enough to cut without losing an argument.

**Candidate seam, not a mandate:** decision 26 (`study_results/` retention and build-directory
pruning) is the largest single entry and the most topically distinct from 13/17/41/55, which are
all about what `init` writes into `[[projects]]` at scaffold time; 26 is about `doctor --prune`,
a different verb entirely. Check inbound links before cutting — `tasks/umbrella/009`'s history
notes `embarch-api/decisions/build.md` and `embarch-decision-reversals.md` link this file for
decisions 26 and 17, so a move must keep both anchors resolvable (redirect or duplicate the
anchor, per `DOC-PROTOCOL.md`'s cross-repo-link rule) — that same check is what made `009` reject
moving 26 previously, so re-verify it rather than assume it still holds.

## Why now

`check-doc-size.py` fails a file over its 90%-of-cap reserve line with no debt filed against it;
`080`'s edit put `projects.md` at 100% in the same commit that must file this.

## Done when

- [x] `decisions/projects.md` back under the 90% reserve line (11,059 B), by split or by genuine
      shortening — never by deleting a rejected-alternative or a verification note that is still
      load-bearing.
- [x] Every decision number (13, 17, 26, 41, 55) still resolves from `decisions.md`'s index, in
      whichever file each ends up in.
- [x] Any cross-repo anchor into a moved decision (see `embarch-api/decisions/build.md`,
      `embarch-decision-reversals.md` for 26 and 17) still resolves.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/umbrella-*` fragment dropped.

## Closed (leg 140)

**Decision 26 was re-checked and rejected again, for the same reason `umbrella/009` gave.**
`embarch-api/decisions/target-json.md` links `embarch-umbrella/decisions/projects.md` twice by
file path for decision 26, and `embarch-decision-reversals.md` links the same file by path for
decision 17 — both are anchors this worker cannot edit (one is a different sub-project's doc, the
other is suite-level). `suite/user-guide.md` does the same for decision 41. Moving any of 17, 26 or
41 out of `projects.md` would leave those three anchors pointing at a file that no longer holds the
decision they name, with no way for this unit to fix the far end. **26 stays in `projects.md`,
unmoved** — `tasks/umbrella/082` needs no re-pointing.

**What actually moved: decision 55 only**, to new `embarch-umbrella/decisions/serial-port.md`.
It has no inbound cross-repo (or suite-level) anchor anywhere in the doc corpus — confirmed by
grep across the whole `embarch-doc` tree before the cut — so no redirect was needed. New anchor:
`embarch-umbrella/decisions/serial-port.md#55` (decision numbers are permanent per
`DOC-CONVENTIONS.md`; the file is new, the number is unchanged). `decisions.md`'s index row for
`projects.md` now reads `13, 17, 26, 41`, with a new row for `serial-port.md` reading `55`.

**Byte counts (measured, this worktree):**
- `embarch-umbrella/decisions/projects.md`: 12,286 B → 10,950 B (89.1%, out of reserve)
- `embarch-umbrella/decisions/serial-port.md`: new file, 2,277 B
- `embarch-umbrella/decisions.md`: 3,175 B → 3,296 B (index row split into two)

Gate: `python3 scripts/check-docs.py` — all 11 checks green. `scripts/check-doc-size.py --pressure`
now lists `projects.md` as `PAID`. `scripts/check-ownership.py --scope umbrella` clean in the doc
worktree; `--code-repo` clean in the code worktree (this task touched no code — the umbrella code
repo has zero diff on this branch).
