# 011 — Answer protocol questions: what a role must support, and what a state does

**State:** done
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — about 605 spec lookups outside the atlas were state-machine questions, 105 distinct Policy Engine and Protocol Layer state names were grepped 327 times, 44 lookups named the applicability tables (USB PD R3.2 Tables 7.4-7.7), and a review round corrected two responders a commit called Required that Table 7.4 lists as Recommended
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Two question types the atlas cannot answer today, both from a standard's tables and per-state text, both as records with cites and a lookup. **Applicability:** a record kind `applicability`, one per table cell: `item` (sequence or message name as printed), `item_kind` (sequence, message), `role` (the column as printed: Source, Sink, DRP, Cable Plug), `cond` (the condition the table attaches, such as PPS, EPR, or "sends Alerts"), `as` (initiator, responder), `level` (as printed: Normative, Recommended, Optional, Shall Not, N/A), `p`, `q`. Lookup `applies <doc> role=<role> [cond=<c>]` lists every item for that role grouped by level; `applies <doc> item=<name>` lists the levels across roles. **State machines:** record kinds `state` (machine, name as printed, entry actions as printed: messages sent, timers started or stopped, counters reset) and `transition` (machine, from, to, the event or condition as printed, the message or timer that triggers it). They come from the per-state subsections (R3.2 writes one per state, for example 9.2.4.1 `PE_SNK_Startup` State) and are checked for completeness against the state diagram figure. Lookup `transitions <doc> state=<name>` gives a state's entry actions, its exits and the states that lead to it; `transitions <doc> on=<event>` lists every state that reacts to a message or timer (`Get_Status`, `SenderResponseTimer`). The same kinds fit a datasheet's or reference manual's state machine (a charger's or a peripheral's). Applicability is smaller (Tables 7.4-7.7 are about six pages) and can land first. This builds on the standard kind (atlas-standard-sections); with atlas-code-lookup-over-the-build, which covers the firmware's own state machines, a reviewer can put the spec's transitions for a state next to the code's.

## Why now

R3.2 chapter 9 (State Machine Diagrams, pp 255-393, a third of the spec) has no distillation, and `doc_section` answered "not found" for 9.2.4, 9.2.8 and 9.1.2.2 (`embarch-atlas/src/embarch_atlas/query.py:305`). The applicability answer lived in a session memory file written by hand, and a wrong reading of it reached a commit message.

## Done when

- [x] Schema (`schemas/record.schema.json`): `applicability`, `state` and `transition` kinds with the fields above; DESIGN.md "Kinds" table updated.
- [x] `doc check`: the `level` word and the `item` name are in the quoted row; a transition's `from` and `to` are `state` records of the same machine; every state named by the machine's `figure` record has a `state` record.
- [x] `standard-procedure.md` gains steps for applicability tables (one record per cell) and for state sections, each with an invented example.
- [x] `applies` and `transitions` lookups (MCP and CLI), with a nearest-names miss and machine disambiguation when two machines share a state name.
- [x] Synthetic fixture tests: a two-table applicability spec, and an invented four-state machine with one timer and one message trigger.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Blocked (history)

Parked by the supervisor on 2026-10-29, not by a worker: the task says it builds on the `standard` kind `tasks/atlas/016` lands, and that task waits on the owner's review. Back to `open` when 016 is done.

## Result

Shipped on `agent/atlas/011-protocol-records` (embarch-atlas fdd346b, cut from `agent/atlas/016-standard-sections` 31e1857, so it lands after 016). The atlas has no `spec.md`/`decisions.md`/`open.md`: that box is met by the repo's DESIGN.md (the "Records" kinds table, "Standards and specifications", "Query surface" and every place the lookup count is stated, now fifteen), a short "Protocol records" paragraph in `embarch-atlas/design.md` and `changelog.d/atlas-protocol-records.added.md`. No `features.d/` row, no decision number.

- **Schema and facts.txt**: `applicability` (`item`, `item_kind` sequence|message, `role`, `cond`, `as` initiator|responder, `level` as printed, `table`), `state` (`machine`, `name`, `entry` as a list of actions as printed), `transition` (`machine`, `from`, `to`, `event`, `trigger`); a state diagram's `figure` record takes `machine` and `states`. Render tables for the three kinds (`kind=applicability|state|transition` blocks).
- **Check L**: `item` and `level` both in the quoted row as whole names (a line break inside allowed, a longer name around them not). **Check E**: a transition's `from`/`to` are state records of its machine (a state of another machine is named in the finding); every state a figure lists has a state record of that machine; a figure listing states with no machine fails; a state the diagram does not list is a warning. Both fail the record and print one summary line in `doc check`.
- **`applies <doc> role=|item=|cond=`**: a role's items grouped by level, strongest first (normative, recommended, optional, shall not, N/A); `cond` keeps that condition's cells plus the unconditional ones; `item` gives the level per role; neither gives roles, conditions, tables, item counts; a miss lists the nearest names. **`transitions <doc> state=|on=|machine=`**: entry actions, exits (trigger shown when the event does not name it) and predecessors; `on` lists per machine the transitions it triggers or names and the entry actions naming it, and narrows a `state` answer; a state two machines share asks for `machine`; neither lists each machine, its states and its diagram. MCP tools and `q` verbs, paged with `offset`.
- **`standard-procedure.md`**: "Applicability tables" and "State sections", steps and an invented example each; `atlas-use` gains two quick-lookup rows.
- **Tests**: `tests/test_protocol.py`, 31: an invented demo link spec with two applicability tables (one with conditional footnotes, one split by initiator/responder) and a four-state machine with one timer and one message trigger, plus a second machine sharing a state name; L, E, both lookups' exact answers, misses, paging, CLI, MCP, render plus check M, and the procedure's examples validated and anchored. `tests/test_records.py` covers the new kinds. Gate: pytest 793 passed, 3 skipped (baseline 762/3; `test_public_guard` ran); client-names, ownership (code and doc), check-docs green.
- **Choices made here**: the check letters L and E; `table` added as an optional field; `as` as an enum; machine and state names compared as printed (blanks aside) by E, case- and punctuation-free by the lookups; `cond` keeps the unconditional cells; `standard-procedure/1` kept rather than bumped (the new steps only add kinds, and no standard section is frozen anywhere before this lands); the lookups do not write the usage log (second-look's `--used` reads only find_fact, register and part_card).
- **Unverified**: no real specification was distilled with these steps; L cannot tell which column of a row a level sits in, so a level read from the wrong column of the right row still passes (an x-position check like K's would close that); a transition the spec draws from every state has no shorthand and needs one record per state.
