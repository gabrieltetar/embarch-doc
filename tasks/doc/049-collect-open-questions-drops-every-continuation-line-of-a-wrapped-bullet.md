# 049 — `collect-open-questions.py` drops every continuation line of a wrapped bullet, and says it collected "in full"

**State:** open
**Source:** leg 104, 2026-09-13, refill sweep. Found by reading the collector's output beside the
file it had just read.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/collect-open-questions.py`, a reserved path, or in
`DOC-PROTOCOL.md`, also reserved. Either way it is not an agent's to make.

## What

`scripts/collect-open-questions.py` prints its own header as:

> Collected from every sub-project's open.md **in full**, plus the "Open questions" section of any
> design.md that still carries one

It is not in full. A bullet whose source wraps onto continuation lines is emitted as its **first
physical line only**, with no marker that anything was cut. From this leg's sweep:

```
- **Espressif-family dev-bench port selection has no current story.** Decision
```

The source (`embarch-core/open.md:27-31`) continues `23's four removed env overrides had no stated
replacement: ...` and names `link_port_interface`, the ESP32-C5-WROOM-1 DK, and an explicit
`**[assumed]**` marker. The output ends mid-sentence on the word "Decision" — which reads as a
sentence that trails off in the *source*, not as a truncation by the tool.

## How much is affected today

**One bullet out of 79**, measured across all eight `embarch-*/open.md` files on `main` at
`3cd6770`: every other bullet in the suite happens to be written on a single long line.

That is the reason this is worth writing down rather than shrugging at. The collector works today
by a **convention nobody has stated** — one physical line per bullet in an `open.md` — and the
single file that breaks it is silently misread. Nothing in `DOC-PROTOCOL.md` says an `open.md`
bullet may not wrap, nothing checks it, and a wrapped bullet is ordinary Markdown that renders
correctly everywhere else.

## Why it matters more than one bullet

This script is the **refill step's input**. `.claude/leg.md` sends a supervisor to
`collect-open-questions.py` to sweep every sub-project's open questions "in one pass" when the
queue is below its low-water mark, and the supervisor then decides from that output what to file
as a task. A truncated bullet is an open question a leg reads as smaller than it is — and the
truncation removes exactly the part that carries the detail a task would be written from. A
supervisor is not going to re-read eight `open.md` files to check the index it ran to avoid
reading them.

## Suggested fix

Two shapes, and they are not equivalent:

1. **Make the collector honest** — accumulate continuation lines (a following line that is indented
   and non-empty belongs to the bullet above it) until the next `- ` at column zero or a blank line.
   Costs a few lines, keeps `open.md` authorable as ordinary Markdown, and makes the header's "in
   full" true.
2. **State the convention and check it** — write "one physical line per bullet" into
   `DOC-PROTOCOL.md`'s `open.md` rules and fail on a wrapped one. Cheaper in the script, but it
   makes a real Markdown file illegal for a reason that exists only inside one tool, and it would
   fail `embarch-core/open.md` as it stands today.

**(1) is the recommendation.** The convention in (2) is invisible to every other consumer of these
files, including a human reading them in an editor, and a rule that exists to protect a parser is
the kind that gets broken again the next time someone wraps a long line.

## Done when

- [ ] `collect-open-questions.py`'s output carries the whole of `embarch-core/open.md`'s Espressif
      bullet, and the header's "in full" is true or the word is removed.
- [ ] Gate green.
