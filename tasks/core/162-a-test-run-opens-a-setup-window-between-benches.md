# 162 — A Test run opens a setup window between benches

**State:** claimed by agent/core/162-a-test-run-opens-a-setup-window-between-benches, 2026-11-25 10:12
**Source:** EMB-367 — Core does not know a prompt's kind and lets the agent answer any prompt (second half; the kinds are `core/161`)
**Issue:** EMB-367
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Core's Test run executor (`src/test_executor.rs`, decisions 136 and 137) walks
a run bench by bench and leaves "a setup prompt and a smoke check between
benches" open (137). While a run holds the run lock, every gated call is
refused except the `RUN_ADMITTED` list (decision 135), so the person cannot
enrol, assign roles or declare signals for the next bench. The design: between
benches an operator prompt says "which saved bench to set up, with what is
missing"; while it waits, "Core admits the person's setup calls ... with the
person's token, or on an unattested Core the agent's, labelled as the agent's"
(`notes/hil/12-prevention.md`). When this is done:

- **Before each bench after the first**, the executor raises a `setup` prompt
  naming the next saved bench (its name and config from `run.json`) and a
  `missing` list. Until the smoke check exists (EMB-368) that list is empty;
  say so in the decision rather than inventing a check.
- **While that prompt waits, `lease_middleware` admits the setup calls**:
  enrolment, roles, signals, instruments, bootload ports and `dev_bench_link`,
  with the person's token, or with the agent's, labelled in the run record as
  the agent's. Every other gated call stays refused `409` as today. The window
  closes when the prompt is answered, times out or the run is cancelled.
- **A setup prompt answered with the agent's token is recorded as relayed**
  (the scope `core/161` records), not refused: a setup claim is the one kind
  the agent may relay.

## Where to look

- `src/test_executor.rs` — `drive`, the bench loop, `Env`
- `src/api.rs` — `lease_middleware`, `RUN_ADMITTED`, `AppState::run_lock`
- `src/host_study.rs` — the prompt slot `core/161` gave a kind; its
  `RunContext` and `answered_scope` (decision 138, `decisions/host-prompt.md`)
- `embarch-doc/embarch-core/decisions/test-run-go.md` (135),
  `test-run-executor.md` (136, 137)

## Where the doc goes

A new decision, in `decisions/test-run-executor.md` (5,661 B at filing) or
beside it, amending 137's open line for the setup prompt. **Do not grow 135**
(95 B left under its per-decision limit) **or 93** (`lease.md`, 144 B over);
point to your decision from your own text. `interfaces/test-runs.md` for the
setup prompt and the window. If your work pushes any file into reserve, file
`tasks/core/<NNN>-compact-core.md` in the same commit per `tasks/README.md`.

## Done when

- [ ] A two-bench fixture run raises a `setup` prompt before the second bench,
      naming it.
- [ ] During that prompt an enrolment with either token is admitted, and the
      agent's is labelled as the agent's; outside it, the same call is refused
      `409`.
- [ ] A setup prompt answered with the agent's token is recorded as relayed.
- [ ] Gate green.
