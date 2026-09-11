# 048 — embarch-umbrella/decisions/doctor.md is in reserve

**State:** blocked — corrected from `open` by the supervisor, leg 070, 2026-09-10. `In flux:` below
says `yes` for the only file on the `Compacts:` line, and `tasks/README.md` is explicit that an
all-yes flux answer means `**State:** blocked` naming what unparks it. Filed `open`, it was
dispatchable, and `.claude/leg.md` forbids dispatching a compaction task whose flux answer is yes —
so the queue was offering a task no leg was allowed to take. The unpark condition is unchanged and
stated below; the `**Size debt due:** 2026-09-20` date is what keeps this park from absorbing.
**Source:** scripts/check-doc-size.py, hit landing `tasks/umbrella/047`
**Scope:** umbrella
**Hardware:** none
**Owner:** no
**Compacts:** embarch-umbrella/decisions/doctor.md
**Size debt due:** 2026-09-20

## What

`decisions/doctor.md` is **11,082 / 12,288 B (90.2%), 1,206 B left** — pushed there by
`047`'s one-line fix (line 7's `Current truth:` pointer, corrected from `../spec.md` to
`../interfaces/doctor-chain.md`, matching the five siblings `046` already repointed). The
net growth was unavoidable within a one-line fix that had to stay one line; the file was
already close to its cap before this edit.

## Why now

`DOC-COMPACTION.md`'s reserve is a debt notice, not a wall — the debt is real once a file
is in the last 10% of its cap, whether or not the unit that tipped it over is itself small.

## In flux: yes

`tasks/umbrella/033` (open) is a check-17 doctor-chain row change, and this same file's
prose narrates all four check groups by number — a landed `033` can rewrite the sentence
this task would otherwise compact. **Unparks when `033` lands**, or when no open umbrella
task names a `doctor`-chain row change.

## Must not delete

- The per-check-group pointers (`schema-skew.md`, `mcp.md`, `bind.md`,
  `dev-bench-firmware.md`) — each names which check numbers it covers.
- The "Current truth" pointer this task's trigger corrected — do not revert it to `spec.md`.

## Done when

- [ ] `decisions/doctor.md` out of reserve (below 90% of its cap), by trimming duplicated
      wording or a split, not by reverting the `047` correction.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/umbrella-*` fragment
      dropped.
