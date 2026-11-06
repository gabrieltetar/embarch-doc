# 040 — `spec.md` is in reserve after the PD bench decisions, and nothing filed the debt

**State:** claimed by agent/dev-bench/040-compact-dev-bench, 2026-11-06 12:29 — reopened as the
size ledger's first unit: overdue since 2026-11-01, and the remedy is a verbatim split, which this
file always said needs no unpark.
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
**In flux:** no, for the remedy this task now takes. `tasks/dev-bench/036`–`039` all change what
`spec.md` says about the PD bench: its own west workspace and patch set (036, which retires
decision 48's "it builds outside `workspaces/`"), a build gate (037), its shell contract (038) and
the DRP1M1 sink path (039). That text is two places only — §1's "A second app, `pd-bench/`"
paragraph and §2's `pd-bench/` layout row — and this task leaves both word for word. What it moves
is a settled section, verbatim, so it restates nothing (`DOC-BUDGET.md`'s split-first rule; the
same reading reopened `chat/004` on 2026-10-28).
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

**A verbatim split first** (`DOC-BUDGET.md`). The filer expected a PD bench section to move, but
`spec.md` holds only one paragraph and one layout row about it, which is too little to pay 593 B
and is the in-flux text besides. So move a **settled** section instead, verbatim (no rewording, no
trimming), into `embarch-dev-bench/spec/<topic>.md` — the shape `embarch-ui/spec/` and
`embarch-api/spec/` already use — and leave a one-line pointer in `spec.md` where it was. §5
"Constants and budgets" (the table and the SRAM paragraph under it) is the obvious candidate: it is
a reference table with its own provenance column, and §4 cites it only by number. §4 "Link and
threading contracts" is the alternative. Pick by inbound links: find every link into the moved
section across the suite and repoint it, including `#5-constants-and-budgets`-style anchors and
cross-repo citations of `spec.md §5`. **Leave §1's `pd-bench/` paragraph and §2's `pd-bench/` row
exactly as they are.**

## Done when

- [ ] `spec.md` out of reserve (`scripts/check-doc-size.py --pressure`), or this task says why not.
- [ ] Every link into a moved section resolves.
- [ ] `DOC-COMPACTION-PASS.md`'s human question answered in the compactor's own words.
- [ ] Gate green (`../../../embarch-fleet/gate.md`).
