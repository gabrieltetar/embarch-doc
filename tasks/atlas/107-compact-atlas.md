# 107 — `embarch-atlas/design.md` is in reserve

**State:** done — moved two sections (4.6 KB) verbatim to embarch-atlas/design/library-and-cad.md; design.md 23474 -> 19214 B
**Source:** atlas 106 (EMB-268) added the read-back of measured facts to `design.md`, leaving it at 23,474 of 25,600 B (2,126 B left).
**Scope:** atlas
**Hardware:** none
**Owner:** no

**Compacts:** embarch-atlas/design.md
**Size debt due:** 2026-12-07
**In flux:** no — for the move this task makes. Unparked at claim, 2026-11-25: this task's own remedy is a verbatim move into a topic file, and `DOC-BUDGET.md`'s split-first rule is that a verbatim move restates nothing, so flux cannot forbid one (the `core/093` precedent, 2026-09-28). The old answer, kept as history: *yes — the measured plane is still moving: `via: study` / `via: test` records and where the plane lives once planes are shared are not built, and the live write-back and its read-back landed within two units of each other.* That still governs any **squeeze** of the measured-plane paragraphs; it does not govern moving text.
**Must not delete:** the dated decisions and their issue keys (EMB-267, EMB-268, EMB-109); move reference detail to a topic file verbatim and leave a link.

## What

Bring `design.md` out of reserve by moving the longest sections into a topic file beside it, verbatim, leaving links.

## Dispatch note (supervisor, 2026-11-25)

**Move only; squeeze nothing.** Move whole sections byte-identical into a topic file beside `design.md` (a new `design/<topic>.md`, or the seam you find better, said why) and leave a one-line link where each stood; rewrite no sentence, since the unpark above covers a move and nothing else. Prefer settled sections (the tool and reader sections) over the measured-plane ones. Grep `embarch-doc` and `embarch-atlas` for links into the sections you move and repoint any that name the file and anchor. This is a burndown leg: author no new numbered decision. Doc-only unit, no code worktree. `embarch-atlas/design.md` is the only file in reserve for `atlas` (2,126 B left).

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [x] `scripts/check-doc-size.py --pressure` does not list `embarch-atlas/design.md`.
- [x] Moved text is byte-identical in its new file; `check-links.py` green.
- [x] Gate green (`../../embarch-fleet/gate.md`).
