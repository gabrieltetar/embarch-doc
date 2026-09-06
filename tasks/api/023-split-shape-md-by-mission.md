# 023 — Split `embarch-api/decisions/shape.md` by mission: the test-reach decisions come out

**State:** claimed by agent/api/023-split-shape-by-mission, 2026-09-06 03:15
**Source:** `api/020`'s reviewer, 2026-09-06, which measured `shape.md` at **12,281 / 12,288 B**
and named the tension: `tasks/api/021-compact-api.md` concedes the file carries two missions and
names the split as the likely move, then parks on `In flux: yes` anyway.
**Scope:** api
**Hardware:** none. Moving prose between two files in `embarch-doc`.
**Owner:** no

## What

**`embarch-api/decisions/shape.md` is 7 bytes under a hard 12,288 B cap.** Not in reserve —
*past* it, at the wall. Every other `embarch-api` decisions file is one paragraph from its own
reserve line (`zephyr.md` 11,056 against 11,059; `interfaces/config.md` 11,008; `build.md`
10,934; `surface.md` 10,928; `core-link.md` 10,879). **The next `embarch-api` unit that writes a
decision anywhere has nowhere to put it**, which is exactly how an api decision landed in the
wrong topic file on 2026-09-05 with 96 bytes left.

**Split it. Do not compact it.** `decisions.md`'s own index row for `shape.md` describes two
missions in one sentence — *"what this is, what it is not, the one-way relationships, **how far
the tests reach**, and the one target a `static` project has"*. The second clause is the seam:

- **Stays in `shape.md`** (scope and boundaries): decisions **1, 2, 3, 4, 6, 7, 8, 9, 10, 25, 53**.
- **Moves to a new `embarch-api/decisions/tests.md`** (how far the tests reach): decisions
  **30** (the named smoke-harness tier), **46** (the one-module `lib` target), **54** (the bearer
  sweep derives its own route set).

**Move them verbatim.** A split restates nothing, which is precisely why
`DOC-COMPACTION.md` §2 says the in-flux objection does not apply to it — and why this is a
different act from `tasks/api/021`, which is a compaction *pass* and stays `blocked` and
untouched. **Do not shorten, reword or "tidy" a moved entry.** If you find yourself editing one,
stop: that is the compaction pass, and it is parked for a reason.

**No renumbering, ever.** Numbers are permanent identifiers here
(`DOC-CONVENTIONS.md`), and `decisions.md` carries the standing note about 31/33 being one
decision under two numbers because a past commit renumbered. Do not add to that.

## Before you cut, check the seam

`umbrella/022` did this correctly last night and the lesson transfers: **the obvious entry to
move can be the wrong one, because of who links it.** Before moving each of 30, 46 and 54, grep
the whole `embarch-doc` tree and every code repo for inbound references. `check-decision-refs.py`
resolves by number and `check-links.py` resolves paths, so a reference written as
a markdown link whose target is `decisions/shape.md` and whose number is `30`
**breaks silently in the sense that matters** — the link
still resolves to a file that no longer contains 30. Repoint every one you find. Any that lives
outside `embarch-api/` is not yours to edit: **name it in your report and drop it in `inbox/`**,
and say so rather than moving the decision anyway.

`embarch-api/open.md` is one place that cites `decisions/shape.md` 30 and 46 by name. That one
*is* yours.

## Why now

This is the only thing standing between the `embarch-api` sub-project and being undispatchable.
`tasks/api/022` is already `blocked` on exactly this, and `021`'s own text names the split.
The queue found **zero** worker-dispatchable tasks at the top of this leg; a walled doc corpus in
the repo with the most open questions is a large part of why.

## Reserve, at dispatch

`shape.md` **12,281 / 12,288 B — 7 bytes.** Nothing else in `embarch-api` is in reserve, and the
five files listed above are each one paragraph from theirs, so **do not relieve `shape.md` by
moving anything into an existing file.** The new `tests.md` is the only destination.

After the split both files should be comfortably clear. If `shape.md` is still in reserve when
you are done, say so and file it — do not shave prose to get under the line.

## Done when

- [x] `embarch-api/decisions/tests.md` exists and holds decisions 30, 46 and 54, **byte-identical
      to their text in `shape.md` before the move** — demonstrate this in your report by
      extracting each from both and diffing.
- [x] `shape.md` holds 1, 2, 3, 4, 6, 7, 8, 9, 10, 25, 53 and nothing else; its `# ` title and
      `decisions.md`'s index row for it no longer claim the test-reach mission.
- [x] `decisions.md` gains an index row for `tests.md`, with its decision list and size.
- [x] No decision renumbered. `check-decision-refs.py` and `check-links.py` both green.
- [x] Every inbound reference to 30, 46 or 54 inside `embarch-api/` repointed; every one outside
      it named in the report and dropped in `inbox/`.
- [x] Both files' sizes reported, and neither in reserve — or the debt filed.
- [x] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).

## Leave these alone

`tasks/api/021-compact-api.md` and `tasks/api/022-nine-hand-written-bearer-auth-sites.md` are
both `blocked` and both are affected by what you do here. **Do not edit either.** The supervisor
reconciles them in the fold — `021` may be wholly paid by this split, and `022` unparks — and
that judgement needs the sizes you end up with.

## Done, 2026-09-06 — agent/api/023-split-shape-by-mission

`decisions/shape.md` **7,654 B** and the new `decisions/tests.md` **5,434 B**, both against the
12,288 B cap; neither in reserve (line 11,059), so no compaction debt filed. Decisions 30, 46 and
54 verified byte-identical between `shape.md` at 57ab4dc and `tests.md` — SHA-256 prefixes
`d87f95f438dc303e` / `e65783b641a35e6d` / `7a064f7688aa7738` on both sides, per-entry `diff`
empty. Nothing renumbered; the only text in `shape.md` that changed is its `# ` preamble.

Repointed inside `embarch-api/`: `open.md` (30, 46, 54), `interfaces/modules.md` (46, twice),
`decisions/core-link.md` (46), and `decisions.md`'s index, which gains a `tests.md` row. Every
surviving `shape.md` reference elsewhere in `embarch-api/` cites 25 or 53, which stay.

**Outside `embarch-api/`, two, neither repointed.** `history/api.md` line 28 records that
"decision 30 moved to `decisions/shape.md`" and line 91 says "See embarch-api decision 46" —
both dated history entries, true when written, and `history/` is not this scope's to rewrite.
No inbound reference in the `embarch-api` code repo: its "decision 30/46/54" hits all name
`embarch-study-designer` or `embarch-core` decisions, not this sub-project's.

**One pre-existing gate red, fixed here, and a script gap dropped in `inbox/`.** This task file
failed `check-links.py` at its own claim commit 57ab4dc: the seam-check paragraph above used to
demonstrate the dangerous reference shape by writing a literal markdown link inside a code span,
and `check-links.py` extracts every bracket-then-parenthesis link from raw file text with **no inline-code or
fenced-block stripping**, so any doc that documents link syntax by example is flagged. The
paragraph is reworded above so no example link remains. The script itself is owner-only; see
`inbox/doc-check-links-ignores-code-spans.md` and
`inbox/doc-history-api-line-28-points-at-the-wrong-file.md`.
