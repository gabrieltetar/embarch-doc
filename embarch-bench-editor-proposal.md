# Proposal: a bench editor that replaces the Topology diagram

**Status:** proposal, 2026-11-01.

Spans `embarch-ui` (almost all of it), `embarch-study-designer` and `embarch-core` (one field each), which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). A USB PD bench is a DUT, a PD partner with a shield, an analyzer in line, a load and a supply, re-cabled by hand between tests. The owner tried a clickable mockup on 2026-11-01; what it settled is below.

**Phases 1–3 are built and documented in `embarch-ui`, not here**: the part templates, the bench files, the routes and the rule checks ([embarch-ui/spec/bench.md](embarch-ui/spec/bench.md), `embarch-ui` decisions 71–75), the canvas the Topology tab now is (76–78), and editing it, the part editor included ([embarch-ui/spec/bench-editing.md](embarch-ui/spec/bench-editing.md), 80–89). This proposal is phases 4–5.

## What is still missing

**The canvas edits a bench's file and declares nothing.** A probe is still enrolled on the old diagram, in its panel; and loading a bench is still the old apply, which declares signals and the dev-bench link and proposes the two roles' enrolments, nothing more. **Core already holds what a PD bench needs and the canvas declares none of it**: a role-less bench board ([`embarch-topology` decision 41](embarch-topology/decisions.md)), a signal leaving one (48), an instrument (49), a DUT's bootload ports (36). `embarch-core` decision 105 counts 25 typed confirmations in one PD session.

## The model, as phases 4–5 extend it

- **The drawing declares** (owner, 2026-11-01). A cable that ends at this machine is bench-level, shared by every config, and declares what its bound functions declare, which may be nothing (the CY4500's own link). Every other cable belongs to a config and is physical only.
- **Switching configs never calls Core** (owner).
- **Several benches per repo, one live** (owner). **Which bench and config are live is this UI's record, not the repo's**: a shared checkout would otherwise claim another machine's bench.

## What a cable declares

| On the canvas | Core route | When the bench goes live |
|---|---|---|
| A board type on a part holding a role | `PUT /probes/enrolled/{role}/board` | Applied: no identity claim (decision 45) |
| A probe bound on a role's part | `POST /probes/enroll {role}` | **Proposed**, confirmed through the ordinary enroll |
| A probe bound on a role-less part | `POST /probes/enroll`, no role, `name` = its label (`embarch-core` decision 83) | Proposed |
| `vcom` on the dev-bench part's cable | `POST /dev-bench/link` | Applied; deferred while the role is empty |
| A signal on a `vcom` or a bridge | `POST /signals`, `direct` | Applied |
| `scpi` on an instrument's cable | `PUT /instruments`, template line facts as defaults | Applied |
| The bootload pair on the DUT's cable | `PUT /bootload/ports` | Applied |

**Editing the live bench writes through** (owner, 2026-11-01: moved out of phase 3, which writes only files); **editing any other bench writes only its file.** Every route exists, and `embarch-core-client` wraps each.

**Making a bench live extends today's apply.** Declarations apply and report one outcome each; enrolments come back as proposals (a file is not evidence about what is plugged in). **Then the report lists what Core holds that this bench does not name**, each with its own Retract; **nothing is retracted silently** (owner, 2026-11-01), because Core's store is machine-wide, not this repo's.

## Config slots, and a study that names one

**Adding, renaming and deleting a config on the canvas is phase 5's** (owner, 2026-11-01); phase 3's only config is the `A` a first part-to-part cable makes (`embarch-ui` decision 82).

**A host study names a config by name** (owner, 2026-11-01), through a new optional field, `Prompt { text, bench_config }`. The modal (`embarch-ui` decision 69) draws the change from the current config, cables to unplug and to plug, and **Confirm marks that config current.** A name the live bench lacks renders as unresolved, with the text alone.

**This is the one piece that is not UI-only.** `embarch-study-designer` decision 80 puts `deny_unknown_fields` on every host type, so the field is a type change and a `HOST_TYPE_SCHEMA_VERSION` bump; Core forwards it on `PromptPending` and resolves nothing. *Rejected: a name convention inside `text`*, which a typo breaks silently.

**It is decision 10's indirection, not a breach of it.** A study names what the bench must look like, never which cables do it. **Renaming or deleting a config is never refused; a name is resolved when a study needs it** (owner, 2026-11-01, replacing a `409` that would have had to scan for every study naming the config, when host studies are not saved in a repo at all). A `Prompt` step whose config the live bench lacks says so and offers the bench's configs to pick, or the step's text alone; a prompt waits for a person anyway. A saved study that names a missing config asks for a new one when it is opened, and keeps the answer; an inline study keeps it for that run.

## Decisions it touches

- **`embarch-ui` 5**: every enumeration the editor shows comes from Core over HTTP. **10**: the lane geometry goes with the old diagram; the carrier rule is kept and extended to configs. **44, 45, 47**: the saved-bench rule stands; a role keeps two bindings; a DUT's board type is still one real scanned combination. **57**: a desk still names one saved bench.
- **`embarch-topology` 41, 48, 49**: a role-less part stays a bench board; a signal leaving it uses `origin_board`; template line facts are defaults only. **No `embarch-topology` change.**

## What is deleted

In phase 4: `renderTopologyDiagram`, `roleNode`, `signalEdges`, the lane and centre constants, the role-box targets in `initEnrollOnDiagram`, the Old diagram panel, and `drive_topology.py`'s diagram checks, rewritten against the canvas.

## Build order

1. ~~Model and files~~ — built.
2. ~~A read-only canvas~~ — built, as the whole Topology tab rather than beside the old diagram (`embarch-ui` decision 78).
3. ~~Editing~~ — built, writing files only (`embarch-ui` decisions 80–89).
4. **Making a bench live**: the live bench writing through, the extended apply, proposals, the retract report. The old diagram is deleted.
5. **Config slots**, then `bench_config`, the modal's drawing and its pick when the named config is missing.
