# 019 — the EAP trio cites an `embarch-study-designer/design.md §3` that does not exist

**State:** claimed
**Source:** leg 099's refill sweep, 2026-09-12. Verified by reading both sides.
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## What

Eleven comments across three files cite `design.md §3` for `embarch-study-designer` decisions:

- `embarch-dev-bench/app/src/eap_interp.h:2, :93, :160` — e.g. ``one, deliberately (design.md §3
  decision 60)`` and ``` `ProtocolOutcome` -- design.md §3 decision 62 kept decoded values out of a ```
- `embarch-dev-bench/app/src/eap.h:2, :44, :212, :230, :321` — e.g. ``/* `WriteField`/`WriteAction`
  (design.md §3 decision 61)``, ``(design.md §3 decision 60). This selects the ATT operation``,
  ``Session variables are integers only (design.md §3 decision 60)``
- `embarch-dev-bench/app/src/eap_interp.c:2, :22` — ``§3 decisions 58-62, §4.9``

There is **no `design.md`** under `embarch-doc/embarch-study-designer/` — only `decisions/`,
`decisions.md`, `open.md` and `spec.md`. **Only the filename is dead; every decision number
resolves**, which is what makes this a mechanical repoint rather than a research job:
`decisions.md` puts 58, 59, 61 and 71 in `decisions/protocols.md`, 60 and 62 in
`decisions/protocol-exec.md`, and 52 in `decisions/payload-meaning.md`.

**This task is exactly these three files and no others, and that bound is the point.**
`embarch-dev-bench` has **247** such citations in total. The rest — `serial_protocol.h` (48),
`ble_bridge_real.c` (39), `serial_protocol.c` (37), `main.c` (36), `ble_bridge.h` (21),
`tests/serial_protocol/src/main.c` (28) — are **separate units, one file each**, and this unit's
report must file them as follow-up tasks rather than widening into them. The per-hit decision
numbers in those 236 have **not** been checked against `embarch-study-designer`'s index; only the
dead filename and the counts are confirmed. Say so in each follow-up you file.

## Why now

Same defect class cleared out of `embarch-ui` by `ui/033`/`ui/039` and out of `embarch-core` by
`core/008`. No gate can see it: `check-decision-refs.py` resolves decision numbers in `*.md` under a
repo root only, and these are C comments.

## Done when

- [ ] `grep -n "design\.md\|milestone-" app/src/eap.h app/src/eap_interp.h app/src/eap_interp.c`
      returns zero.
- [ ] Each becomes `` `embarch-study-designer` decision N `` — the cross-repo form settled in
      `api/052` — with N **unchanged** and confirmed resolvable in that repo's `decisions.md`.
- [ ] The remaining six files' counts are filed as `tasks/dev-bench/NNN-*` follow-ups, each marked
      as carrying unverified decision numbers.
- [ ] Host-side checks green. **This repo's Zephyr `tests/unit` ztest suite cannot be built from a
      worker's worktree** (no `west`, no `ZEPHYR_BASE`) — that is a standing, known debt, not
      something this unit introduces or is expected to clear. Comment-only changes cannot alter
      firmware behaviour; say plainly in your report what you could and could not run.

**Doc-size note:** `embarch-dev-bench/open.md` (93.4%) and `spec.md` (92.4%) are both in reserve and
filed against blocked `tasks/dev-bench/012` — stay out of both.
