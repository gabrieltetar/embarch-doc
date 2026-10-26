# 064 — `decisions/link-declares.md` is in reserve after decision 42

**State:** claimed by agent/topology/064-compact-topology, 2026-10-26 05:37
**Source:** `scripts/check-doc-size.py`, 2026-10-26, after `tasks/topology/063` added decision 42 (11,155 / 12,288 B, 1,133 B left).
**Scope:** topology
**Hardware:** none
**Owner:** no

**Compacts:** embarch-topology/decisions/link-declares.md
**Size debt due:** 2026-11-09
**In flux:** no — decisions 20, 27, 36 and 42 are settled; `topology/059`, `061` and `062` touch validation, parity and the signal route, not a role's declared link facts.
**Must not delete:** decision 20's interface finding (the DK's lower VCOM accepts bytes and never answers; the guess was invisible) and its rejected handshake alternative; decision 42's note that the vacated-row choice is reasoned, not measured.

## Dispatch note, 2026-10-26 05:37 leg

**This is a doc-only unit** (`embarch-doc/embarch-topology/` only; the code worktree is yours in case a `src/` comment cites a decision by file and the split moves it, and should otherwise stay untouched). **Doc reserve in your scope:** `decisions/link-declares.md` 11,155 / 12,288 B, the file this task pays. `decisions/enrollment.md` 12,122 / 12,288 B (166 B left) is filed under `tasks/topology/060`, blocked: do not write it, not even an index line; a split's pointer goes in `decisions.md`'s index and in the new file's header. Check every inbound link to a moved decision (`grep -rn 'link-declares' embarch-doc/ embarch-topology/`) and repoint it, or `check-links.py` goes red. Answer `DOC-COMPACTION-PASS.md`'s question in your report as well as the commit message.

**Isolation, not optional.** No live Core, no desk on `:4891`, no real ports or probes, no owner data dirs, no `mcp__embarch-api__*` or desk tools, no `pkill` by name.

## What

Bring `link-declares.md` out of the reserve band. A verbatim split of decision 42 or 36 into a file named for what it settles is the cheapest move (`DOC-BUDGET.md`).

## Done when

- [ ] `scripts/check-doc-size.py --pressure` no longer lists the file in reserve.
- [ ] Answer in the commit message: can `spec.md` alone answer what someone needs to work on this component today?
