# 043 — `embarch-api/decisions/surface.md` is in reserve after decision 57

**State:** blocked
**Source:** `api/040` added decision 57 (tool-description citation format) and crossed the
11,059 B reserve line; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/surface.md
**Size debt due:** 2026-09-20
**In flux:** yes — this file is the tool and CLI surface, the part of the crate that
changes every time a tool gains a param or a description gets corrected (most
recently decision 57 itself, this same unit). A shortening pass now would be
compacting a file that is still actively taking new entries; better to let it
settle and compact once, per `DOC-COMPACTION.md` §2's own preference for
splitting/shortening over letting a live-flux file get squeezed mid-motion.
**Must not delete:** decision 41's distinction between a routine knob and `erase`
being the one tool argument that can leave a board unrecoverable — that is the
whole reason its description is worded the way it is, not a detail. Decision 52's
three rejected alternatives (`status --json` field, clap `--version` string) and
the `host_type_schema_version` vs `schema_version` name collision they're
rejected to avoid. Decision 57's four-bare/one-wrong-number split, which is the
finding that justified the fix rather than the fix alone.

## What

`decisions/surface.md` is now **11,785 B against a 12,288 B cap** — inside the
last 10% (the 11,059 B reserve line) with 503 B of headroom left. The next `api`
unit that writes into this file may find none.

This file already carries the whole tool/CLI surface as one mission — shapes,
failure text, `erase`'s description rationale, live-study watching, the schema
version diagnostic, and now the citation-format decision. It is a reasonable
single-file scope by topic, unlike `core-link.md`'s six-mission sprawl (`api/026`);
the fix here is more likely a shortening pass over several entries than a split,
once the file is confirmed not to still be moving.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it, and the
commit that spends the reserve is the one that files it (`DOC-COMPACTION.md` §2).
This task is that filing.

## Note from `api/036`, 2026-09-07

`api/036` needed to write into this file (adding a tool, exactly the flux this
park names) and found `DOC-COMPACTION.md` §2's split-first rule applies: a
verbatim split restates nothing, so `In flux: yes` does not forbid one. It split
`surface.md` along a topic seam — general JSON/error shape and the
tool-description citation convention (16, 24, 50, 57) stayed in `surface.md`;
every per-tool wrapping decision (23, 29, 34, 35, 41, 47, 52) moved verbatim to
the new `decisions/tool-wrapping.md`, where its own new decision 59
(`dev_bench_hello`) landed. Every entry moved byte-for-byte; only the two
files' headers are new prose. `decisions.md`'s index table now names both
files, their decision numbers and sizes; `check-decision-refs.py` resolves
every reference (some prose elsewhere pointed at `surface.md` by path for a
decision that moved — fixed where in `api`'s own scope, filed to `inbox/` where
not).

**This does not resolve the park.** `tool-wrapping.md` is the file that will now
take every future per-tool addition — the exact flux this task's `In flux: yes`
describes — so the underlying question (is this subsystem still moving) is
unchanged; only ticking the mechanical index-table item below reflects what
this unit actually did. Left `blocked` for a future unit to say `In flux: no`
against `tool-wrapping.md`, if that day ever comes.

## Done when

- [x] `decisions/surface.md` is clear of the 11,059 B reserve line, or a
      successor confirms `In flux: no` and re-blocks/re-files with a concrete
      compaction plan. — done by `api/036`'s split: `surface.md` is now 5.5 KB,
      well clear of the line. `tool-wrapping.md` (the new file the per-tool
      decisions moved into) is its own reserve item now — see `tasks/api/<NNN>`
      filed in the same commit.
- [ ] Every `Must not delete:` item above is still readable, wherever it ends up.
- [x] If split rather than shortened, `decisions.md`'s index table names the new
      file, its decision numbers and both files' sizes, and
      `check-decision-refs.py` resolves every number. — done by `api/036`:
      `decisions/tool-wrapping.md` added, `decisions.md` updated, refs resolve.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
