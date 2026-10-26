# 113 — Core refuses a submitted study whose Notify or Indicate step has a wait budget of 0

**State:** done — agent/core/113-study-submission-refuses-a-zero-wait-budget, 2026-10-26
**Dispatch note:** three `embarch-core` docs are in reserve, all parked under `tasks/core/112` (blocked, `In flux: yes` because of decision 89): `decisions/probes.md` 11,263/12,288 B, `spec.md` 9,225/10,240 B, `open.md` 4,262/5,120 B. File the new decision in `decisions/studies.md` (6,250 B) or another topic file with room, never `probes.md`. Prefer not to touch `spec.md`/`open.md`; if your change needs a line in either, pay that file out of reserve in this unit (a verbatim split or wording only), carry `core/112`'s `Must not delete:` list, and delete that file from `core/112`'s `Compacts:` line, saying so in its body. `embarch-study-designer` on `main` (`5ea5ac9`) already has `Study::validate_wait_budgets()`.
**Source:** `tasks/study-designer/075` (`embarch-study-designer` decision 83, `5ea5ac9`). Filed from the worker's inbox drop `core-call-validate-wait-budgets.md`, 2026-10-26.
**Scope:** core
**Hardware:** none — a submission-time check, testable with a hand-built `Study` and no probe.
**Owner:** no

## What

`embarch-study-designer` now has `Study::validate_wait_budgets() -> Result<(), WaitBudgetError>`, which refuses a `Notify { timeout_ms: 0 }` or `Indicate { timeout_ms: 0 }` step by index and operation. dev-bench reads that 0 as a deadline already past, so the step reports `TimedOut` at once. The crate does not call it itself: `build_study` can no longer emit a 0, but a hand-written or saved study still can, and nothing refuses it before the run. Core's study submission should call it and return the error's Display text as a 4xx, the way its other pre-run refusals do. `embarch-api` may want the same in its own pre-HTTP validation; that is a separate api task if so, not this one.

## Done when

- [x] Core's study submission calls `validate_wait_budgets` and refuses with the named step and operation, before any hardware is touched.
- [x] A test submits a study with `Notify { timeout_ms: 0 }` and sees the refusal; a nonzero budget passes as before.
- [x] Gate green (`../../embarch-fleet/gate.md`); `decisions.md`/`spec.md` per `DOC-PROTOCOL.md`, `changelog.d/` fragment.
