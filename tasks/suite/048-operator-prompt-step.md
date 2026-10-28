# 048 — Operator prompt step: a visible request to a person, answered from the UI or an MCP tool, with a deadline

**State:** claimed by agent/suite/048-operator-prompt-step, 2026-10-28 17:00 — announced 16:29 (`ts` `1793226580.382079`); the window closed 16:59:40 with no reply (polled 17:00:13). Run by the supervisor (protocol §8).
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — the operator typed 25 confirmations into chat during one PD bench session (2026-10-09 to 10-14), 13 of them between 20:00 and 20:57 on 10-14 ("out", "in", "on", "done", "eload is OFF"). A latched e-load protection that only the front-panel ENT key clears aborted one run (2026-10-13 17:39)
**Scope:** suite
**Hardware:** verify-only
**Owner:** no

## What

A host study can stop at a `Prompt { text }` step until a person answers, as `embarch-host-study-proposal.md` (owner's choice 4) describes. Core emits `PromptPending { step_index, text, deadline }` and shows the pending prompt on `GET /study/{id}`, since SSE has no replay. It accepts `POST /study/{id}/prompt` and emits `PromptResolved { answer, answered_by }`. `confirmed` continues the study. `cancelled` fails the step and runs teardown. No answer by the deadline times the step out. In `embarch-api`: `run_host_study` and `answer_prompt` tools with their CLI subcommands, and `study_watch` returns early on a pending prompt. In `embarch-ui`: a modal on the Live Study tab with the text, a countdown, Confirm and Cancel. It must be visible from across the bench. The field operator had asked for a visual alert, not a chat line.

## Why now

The field prompts were plug or unplug the pack, wire the load to a connector, switch the supply on, swap the expansion board, reseat a cable and press ENT. Each one was relayed through chat, so the run stopped until the operator read the chat. Nothing recorded who confirmed what, or when.

## Done when

- [ ] Core: the two events, the route, the pending prompt on `GET /study/{id}`, and timeout and cancel outcomes that run teardown.
- [ ] `answered_by` records the surface (`ui`, `mcp`, `cli`) and the deadline. **The `answer_prompt` tool description says it relays a person's answer and never answers on the agent's own judgement.**
- [ ] `study_watch` returns early on `PromptPending`, and its output includes the prompt text.
- [ ] UI: a modal with Confirm, Cancel and a countdown, plus a sound or desktop notification when it opens. It is tested headless against a stub Core.
- [ ] `open.md` answers the proposal's two open points: who may answer, and the default timeout.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
