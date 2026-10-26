# 119 — Decide how a host study handles the CY4500 analyzer's capture

**State:** open
**Source:** `core/101` (console capture during a host study, decision 98), its CY4500 box. The worker could not confirm the analyzer's capture format and decided nothing by inference, per that task's dispatch note. Filed from `inbox/core-cy4500-capture-decision.md` by the 2026-10-26 09:03 leg, in core/101's fold.
**Scope:** core
**Hardware:** required — the format has to be read off the analyzer itself, which needs a person at the analyzer; no fleet actor can start it.
**Owner:** no

## What

The CY4500 USB PD analyzer is a Windows GUI that nothing reads. Someone at the analyzer confirms what it can save: the file format, whether it exports without the GUI, and whether a capture can be started or stopped from outside. Then record one decision in `embarch-core/decisions/host-study.md`: either a `Prompt` step asks the operator to save the analyzer's capture and Core attaches that file to the study result, or the analyzer is declared out of scope for host studies. `Prompt` is not executed by Core yet (`suite/048`), so the first option also waits on that.

## Why now

`core/101` put both PD stacks' consoles on Core's one receive clock; the analyzer is the only evidence source still outside Core's record. In the field its timing came from the stacks' INF logs instead.

## Done when

- [ ] The analyzer's capture format and export options are written down, read from the analyzer.
- [ ] `decisions/host-study.md` records which option is chosen, and why.
- [ ] If attached: a task is filed for the attach path, alongside `suite/048`'s `Prompt` step.
