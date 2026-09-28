# 090 — `embarch-umbrella/open.md` is in reserve

**State:** blocked — see `**In flux:**` below.
**Source:** scripts/check-doc-size.py --pressure, run by `umbrella/089`
**Scope:** umbrella
**Hardware:** none
**Compacts:** embarch-umbrella/open.md
**In flux:** yes — see the "In flux" section.
**Unparks when:** the hardware-verification debt `umbrella/089` left in this same file (check 15's
`binary_sha256` comparison, decision 56) is paid — a real `doctor` run against the installed Core.
Closing it rewrites that bullet down to a settled line the way check 13's `umbrella/034` bullet
(line 7 of this file) already shows for a comparable debt. Landing that is reason to re-read this
field rather than to unpark on sight.

**Size debt due:** 2026-10-19

**Reserve:** `open.md` was at 3,905 B (76.3%, out of reserve) after `umbrella/088` retired a stale
bullet. `umbrella/089` rewrote the check-15 bullet — retiring the "not a hash comparison, must not
be read as one" line now that it consumes `binary_sha256` — but the replacement, naming the two
`doctor` runs the hardware debt still needs, is longer than what it replaced. That landed the file at
**4,048 B (79.1% of the 5,120 B role cap), 1,072 B left** — inside reserve, since `RESERVE_FLOOR`
(1,200 B) dominates `RESERVE_PCT` for a file this small (`scripts/check-doc-size.py`'s own comment on
why a flat percentage of a 5 KB file isn't real runway).

Not filed against `009` or `079`, which carry unrelated reserve episodes in `decisions/bind.md` and
`decisions/install.md` — a third file's debt belongs in its own task.

## What

Bring `open.md` back under 90% of cap (4,608 B) without deleting a live unresolved item or a
hardware debt still owed. Read for duplication against `spec.md`/`decisions.md` first
(`scripts/check-duplication.py embarch-umbrella`), then look for a bullet whose gap has since closed
enough to shorten or retire before considering anything more invasive — this file is a flat list of
independent items, not one sprawling entry, so a split is unlikely to be the right move here the way
it sometimes is for a decisions group.

## Why now

Not yet blocking anything — 1,072 B of headroom remains. Filed now per this repo's own reserve
convention (`DOC-COMPACTION.md`, `check-doc-size.py`'s "RESERVE"/"UNFILED" band) so the debt survives
past this leg rather than living only in a supervisor's report.

## In flux

**Yes.** The bullet that pushed this file into reserve names its own open hardware debt (check 15's
`binary_sha256` comparison, decision 56, never run against a live Core). Whenever that debt is paid,
the honest record of it lands in this exact file, the way check 13's `umbrella/034` bullet and
decision 51's sticky-host bullet both already show a fixed-but-unverified item settling in place.
That is new prose in this file, not a different one, so compacting around it now would be squeezing
live reasoning to make room the task's own guidance says not to do.

## Done when

- [ ] `open.md` back under 90% of its 5,120 B cap, by shortening or retiring a settled item, not by
      deleting a live unresolved one or an owed hardware debt.
- [ ] `scripts/check-duplication.py embarch-umbrella` checked before any content is moved elsewhere.
- [ ] No unresolved item disappears without its gap actually having closed.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
