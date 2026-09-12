# 020 — `serial_protocol.h` cites an `embarch-study-designer/design.md §3` that does not exist

**State:** claimed — leg 102, 2026-09-12, branch `agent/dev-bench/020-serial-protocol-h-citations`.

**Doc-size reserve for `embarch-dev-bench`:** `open.md` 4782/5120 B (338 B left), `spec.md`
9460/10240 B (780 B left) and `decisions/link.md` 11241/12288 B (1047 B left) are all in
reserve, filed against blocked compaction tasks (`dev-bench/012`, `dev-bench/014`). This unit
is a C-comment sweep and should need none of them; if it does spend reserve, file
`tasks/dev-bench/<NNN>-compact-dev-bench.md` in the same commit.

**Source:** split out of `dev-bench/019`, 2026-09-12.
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## What

`embarch-dev-bench/app/src/serial_protocol.h` has **48** citations of the dead
`embarch-study-designer/design.md §3` filename (same defect class as `dev-bench/019`,
which fixed `eap.h`/`eap_interp.h`/`eap_interp.c`). `019` confirmed only the filename is
dead and the counts, by mechanical grep — **the per-hit decision numbers in this file have
not been checked** against `embarch-study-designer`'s `decisions.md` index. Say so again in
whatever unit picks this up if any number turns out not to resolve.

## Why now

Same defect class cleared out of `embarch-ui` by `ui/033`/`ui/039`, out of `embarch-core` by
`core/008`, and out of the `.eap` trio by `dev-bench/019`. No gate can see it:
`check-decision-refs.py` resolves decision numbers in `*.md` under a repo root only, and
these are C comments.

## Done when

- [x] `grep -n "design\.md\|milestone-" app/src/serial_protocol.h` returns zero.
- [x] Each becomes `` `embarch-study-designer` decision N `` — the cross-repo form settled in
      `api/052` — with N **unchanged** and confirmed resolvable in that repo's `decisions.md`.
- [x] Host-side checks green; say plainly what could and could not be run (the Zephyr
      `tests/unit` ztest suite cannot be built from a worker's worktree — standing debt, not
      introduced here).

## Closed

Of the 48 citations, 45 were embarch-study-designer's (some written bare, without the repo
prefix, once an earlier sentence in the same comment block had already named it — each such
bare cite was matched to that paragraph's subject before rewriting, not decoded by number
alone, since embarch-study-designer's and embarch-dev-bench's own decision ranges overlap).
2 were this repo's own (decisions 7/10/12/20/21 — boards/link/dispatch topics) and now read
as plain `` decision N ``, no repo prefix, matching how this repo's own `decisions.md`
already addresses itself. 1 was embarch-core's (decision 35, the handshake), now
`` `embarch-core` decision 35 ``.

All 48 numbers were checked against their cited repo's `decisions.md` index before rewriting.
**None were unresolvable** — every one still resolves, several across a repo's index having
moved file since the original `design.md` citation was written (e.g. into `removed.md`
tombstones), which the index's own numbering-is-permanent guarantee covers.

Comment-only change; no firmware behaviour altered. `gcc -fsyntax-only` on the header is
clean. Host-side checks that could run: none needed beyond that syntax check, since no code
changed, only comments. What could not run, as flagged going in: the Zephyr `tests/unit`
ztest suite (`app/tests/serial_protocol`) cannot be built from a worker's worktree — standing
debt, not introduced or touched by this unit.

Code: `embarch-dev-bench` branch `agent/dev-bench/020-serial-protocol-h-citations`, pushed.
