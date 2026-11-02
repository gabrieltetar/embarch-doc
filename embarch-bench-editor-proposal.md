# Proposal: a bench editor that replaces the Topology diagram

**Status:** proposal, 2026-11-01.

Spans `embarch-ui` (almost all of it), `embarch-study-designer` and `embarch-core` (one field each), which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). A USB PD bench is a DUT, a PD partner with a shield, an analyzer in line, a load and a supply, re-cabled by hand between tests. The owner tried a clickable mockup on 2026-11-01; what it settled is below.

**Phases 1–4 are built and documented in `embarch-ui`, not here**: the part templates, the bench files, the routes and the rule checks ([embarch-ui/spec/bench.md](embarch-ui/spec/bench.md), `embarch-ui` decisions 71–75), the canvas the Topology tab now is (76–78), editing it, the part editor included ([embarch-ui/spec/bench-editing.md](embarch-ui/spec/bench-editing.md), 80–89), and making a bench live, the old diagram deleted ([embarch-ui/spec/bench-live.md](embarch-ui/spec/bench-live.md), 90–95). This proposal is phase 5.

## What is still missing

**A config is made only by a bench's first part-to-part cable** (`embarch-ui` decision 82), **and the operator-prompt modal (69) draws no cables to change.** `embarch-core` decision 105 counts 25 typed confirmations in one PD session.

## Config slots, and a study that names one

**Adding, renaming and deleting a config on the canvas is phase 5's** (owner, 2026-11-01); phase 3's only config is the `A` a first part-to-part cable makes (`embarch-ui` decision 82).

**A host study names a config by name** (owner, 2026-11-01), through a new optional field, `Prompt { text, bench_config }`. The modal (`embarch-ui` decision 69) draws the change from the current config, cables to unplug and to plug, and **Confirm marks that config current.** A name the live bench lacks renders as unresolved, with the text alone.

**This is the one piece that is not UI-only.** `embarch-study-designer` decision 80 puts `deny_unknown_fields` on every host type, so the field is a type change and a `HOST_TYPE_SCHEMA_VERSION` bump; Core forwards it on `PromptPending` and resolves nothing. *Rejected: a name convention inside `text`*, which a typo breaks silently.

**It is decision 10's indirection, not a breach of it.** A study names what the bench must look like, never which cables do it. **Renaming or deleting a config is never refused; a name is resolved when a study needs it** (owner, 2026-11-01, replacing a `409` that would have had to scan for every study naming the config, when host studies are not saved in a repo at all). A `Prompt` step whose config the live bench lacks says so and offers the bench's configs to pick, or the step's text alone; a prompt waits for a person anyway. A saved study that names a missing config asks for a new one when it is opened, and keeps the answer; an inline study keeps it for that run.

## Decisions it touches

- **`embarch-ui` 10**: the carrier rule is kept and extended to configs.

## Build order

1. ~~Model and files~~ — built.
2. ~~A read-only canvas~~ — built, as the whole Topology tab rather than beside the old diagram (`embarch-ui` decision 78).
3. ~~Editing~~ — built, writing files only (`embarch-ui` decisions 80–89).
4. ~~Making a bench live~~ — built, the old diagram deleted (`embarch-ui` decisions 90–95).
5. **Config slots**, then `bench_config`, the modal's drawing and its pick when the named config is missing.
