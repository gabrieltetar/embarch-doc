# 011 — Answer protocol questions: what a role must support, and what a state does

**State:** blocked
**Unparks when:** `tasks/atlas/016` lands the `standard` kind this task builds on
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — about 605 spec lookups outside the atlas were state-machine questions, 105 distinct Policy Engine and Protocol Layer state names were grepped 327 times, 44 lookups named the applicability tables (USB PD R3.2 Tables 7.4-7.7), and a review round corrected two responders a commit called Required that Table 7.4 lists as Recommended
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Two question types the atlas cannot answer today, both from a standard's tables and per-state text, both as records with cites and a lookup. **Applicability:** a record kind `applicability`, one per table cell: `item` (sequence or message name as printed), `item_kind` (sequence, message), `role` (the column as printed: Source, Sink, DRP, Cable Plug), `cond` (the condition the table attaches, such as PPS, EPR, or "sends Alerts"), `as` (initiator, responder), `level` (as printed: Normative, Recommended, Optional, Shall Not, N/A), `p`, `q`. Lookup `applies <doc> role=<role> [cond=<c>]` lists every item for that role grouped by level; `applies <doc> item=<name>` lists the levels across roles. **State machines:** record kinds `state` (machine, name as printed, entry actions as printed: messages sent, timers started or stopped, counters reset) and `transition` (machine, from, to, the event or condition as printed, the message or timer that triggers it). They come from the per-state subsections (R3.2 writes one per state, for example 9.2.4.1 `PE_SNK_Startup` State) and are checked for completeness against the state diagram figure. Lookup `transitions <doc> state=<name>` gives a state's entry actions, its exits and the states that lead to it; `transitions <doc> on=<event>` lists every state that reacts to a message or timer (`Get_Status`, `SenderResponseTimer`). The same kinds fit a datasheet's or reference manual's state machine (a charger's or a peripheral's). Applicability is smaller (Tables 7.4-7.7 are about six pages) and can land first. This builds on the standard kind (atlas-standard-sections); with atlas-code-lookup-over-the-build, which covers the firmware's own state machines, a reviewer can put the spec's transitions for a state next to the code's.

## Why now

R3.2 chapter 9 (State Machine Diagrams, pp 255-393, a third of the spec) has no distillation, and `doc_section` answered "not found" for 9.2.4, 9.2.8 and 9.1.2.2 (`embarch-atlas/src/embarch_atlas/query.py:305`). The applicability answer lived in a session memory file written by hand, and a wrong reading of it reached a commit message.

## Done when

- [ ] Schema (`schemas/record.schema.json`): `applicability`, `state` and `transition` kinds with the fields above; DESIGN.md "Kinds" table updated.
- [ ] `doc check`: the `level` word and the `item` name are in the quoted row; a transition's `from` and `to` are `state` records of the same machine; every state named by the machine's `figure` record has a `state` record.
- [ ] `standard-procedure.md` gains steps for applicability tables (one record per cell) and for state sections, each with an invented example.
- [ ] `applies` and `transitions` lookups (MCP and CLI), with a nearest-names miss and machine disambiguation when two machines share a state name.
- [ ] Synthetic fixture tests: a two-table applicability spec, and an invented four-state machine with one timer and one message trigger.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Blocked

Parked by the supervisor on 2026-10-29, not by a worker: the task says it builds on the `standard` kind `tasks/atlas/016` lands, and that task waits on the owner's review. Back to `open` when 016 is done.
