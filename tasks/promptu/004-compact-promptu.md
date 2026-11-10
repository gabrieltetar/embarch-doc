# 004 — `embarch-promptu` spec.md is in reserve after decision 41's build

**State:** open — unparked by the supervisor 2026-11-10 as a verbatim split; see the update below
**Source:** `promptu/002` added the context-planning bullet to `spec.md` and crossed the reserve line; `DOC-COMPACTION.md` §2
**Scope:** promptu
**Hardware:** none
**Owner:** no

**Compacts:** embarch-promptu/spec.md
**Size debt due:** 2026-11-23
**In flux:** no, for the verbatim split this task now asks for. Build step 4 (the weekly sheet, decision 30) still changes what `spec.md` says it builds, so a squeeze would restate what is about to change. A split by mission moves sections whole and restates nothing (`DOC-BUDGET.md`, "a split is the default remedy"), so that objection does not apply to it.
**Must not delete:** the invariants in §3 and the "deliberately does not do" list in §5.

## Update (supervisor, 2026-11-10)

Unparked as a split, not a squeeze. The park waited on build step 4, which has no date. `DOC-BUDGET.md` makes a split the default remedy because it restates nothing, and `check-doc-size.py --pressure` asks each park to be re-read against that rule. **Reword nothing** in what moves.

The seam worth checking first (your call): §2b and §2c, the build steps that are committed or built but not installed, are one mission apart from §2's installed step 1. `spec/constants.md` is the precedent for a `spec/<topic>.md` file. Keep §3 and §5 in `spec.md`, leave a one-line pointer where the sections left, and check inbound links (`grep -rn 'promptu/spec.md'`) before cutting. If no seam leaves `spec.md` able to say what promptu is and what is installed, say so and re-file with the plan instead.

## What

`spec.md` 9,563/10,240 B; out of reserve at <= 9,039 B.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it; this is that filing.

## Done when

- [ ] `spec.md` is clear of its reserve line, or a successor re-files with a concrete plan.
- [ ] Moved text matches the original apart from headers and pointer lines.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Can `spec.md` alone answer what someone needs to work on this component today? Answered in the commit message.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
