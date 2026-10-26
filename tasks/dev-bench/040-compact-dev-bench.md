# 040 — `spec.md` is in reserve after the PD bench decisions, and nothing filed the debt

**State:** blocked — the PD bench section is about to be rewritten by four queued tasks (see `In
flux`). Unparks when `tasks/dev-bench/036` (pd-bench's own west workspace) lands; the clock below
runs regardless, and a verbatim split needs no unpark at all.
**Source:** `scripts/check-doc-size.py`, 2026-10-25. The owner's commits `a94e2c97` (decision 48,
the PD bench, 2026-10-09) and `852d8855` (decision 49, the X-NUCLEO-DRP1M1, 2026-10-13) pushed
`spec.md` into its reserve without a `Compacts:` line. The gate reported it only on 2026-10-25,
once `embarch-study-designer/open.md`'s over-cap failure stopped masking it. Filed by the
supervisor, which did not write these bytes.
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

**Compacts:** embarch-dev-bench/spec.md
**Size debt due:** 2026-11-01
**In flux:** yes — `tasks/dev-bench/036`–`039` all change what `spec.md` says about the PD bench:
its own west workspace and patch set (036, which retires decision 48's "it builds outside
`workspaces/`"), a build gate (037), its shell contract (038) and the DRP1M1 sink path (039).
**Must not delete:** nothing specific is known to the filer, which did not write these bytes. The
DRP1M1 sink-path observation in `tasks/dev-bench/039` (CN2 near 2.3 V under a 9 V contract) is
an open measurement; if `spec.md` states the README's "load on CN2" advice, it is the claim that
task found false, and it is corrected there, not cut here.

## What

`embarch-dev-bench/spec.md` is **9,632 / 10,240 B (608 B left)**, inside the reserve band of
`DOC-BUDGET.md`. When done, it is out of reserve, or this task says why it cannot be.

## Why now

The gate fails on a file in reserve that no task names, so `check-docs.py` was red on `main` for
every unit in the suite until this was filed.

## The move

**A verbatim split first** (`DOC-BUDGET.md`). The PD bench is a second app with its own shell,
shields and (after 036) its own workspace, which is a mission seam: moving its section to a file of
its own under `embarch-dev-bench/` pays the debt without shortening the main app's spec. Whoever
next writes `spec.md` in a unit does this in the same commit and closes this task.

## Done when

- [ ] `spec.md` out of reserve (`scripts/check-doc-size.py --pressure`), or this task says why not.
- [ ] Every link into a moved section resolves.
- [ ] `DOC-COMPACTION-PASS.md`'s human question answered in the compactor's own words.
- [ ] Gate green (`../../../embarch-fleet/gate.md`).
