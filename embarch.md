# EmbArch

**Status:** active, 2026-07-17.

## 1. What EmbArch is

EmbArch is a suite of tools for firmware engineers that spans from software to the physical hardware bench: a layer that interfaces PC-side tooling to a debug probe and serial console, a dev-bench sub-project for hardware-in-the-loop testing, a curated prompt/skills library for firmware-specific agent workflows, and — pulling all of it together — the ability to give an agent like Claude Code real hardware testing capabilities on a firmware project.

## 2. Lineage

EmbArch was originally [gabrieltetar/embarch](https://github.com/gabrieltetar/embarch), a C#/WPF desktop application for static analysis and graph visualization of embedded C/C++ codebases — a "firmware-first architecture analysis and exploration platform" that turned a codebase into an interactive structural graph.

Static analysis and graph visualization of a firmware codebase was always part of EmbArch's scope, alongside the hardware-facing tooling — it's just not prioritized right now, so it's paused rather than dropped. It will resurface as `embarch-atlas`: an analysis capability meant to be used by Claude Code and other coding agents (and by engineers directly) to reason about a firmware codebase's structure, not tied to any one protocol — MCP is a plausible transport `embarch-api` could expose it over, not the defining shape of the capability itself. The original C#/WPF GUI's role narrows accordingly: it becomes a debug/dev-facing feature of `embarch-atlas` — useful for visually inspecting the graph while working on the analysis engine — rather than the product itself. See [embarch-roadmap.md](embarch-roadmap.md)'s Later bucket.

## 3. Sub-projects

| Sub-project | Purpose | Status | Doc |
|---|---|---|---|
| `embarch-core` | Owns the debug probe and serial connection (and, since 2026-08-27, chooses the *flashing backend* per chip family rather than always probe-rs — the board's own declared runner wins where probe-rs does not model the part); exposes `/status`, `/flash`, `/reset`, `/serial-log`, `/dev-bench/port`, the `/study*` surface (including per-tap stream captures) and `/signals` over bearer-token-authed HTTP | Shipped | [embarch-core/decisions.md](embarch-core/decisions.md) |
| `embarch-api` | MCP server and CLI for Claude Code and humans alike; runs a project's build and drives Core over HTTP | Shipped | [embarch-api/decisions.md](embarch-api/decisions.md) |
| `embarch-dev-bench` | Physical rig that plays the DUT's BLE counterpart (advertise/connect/GATT exchange) and samples power during a `Study`, per `embarch-study-designer`'s types — Zephyr-based C firmware, one shared application spanning multiple vendor-specific west workspaces | Shipped (real per-`Study` dispatch on physical hardware, Milestone 2; real `BleConnect`/`GattDiscover`/`GattMonitorAll` against a real independent DUT, Milestone 3), [repo](https://github.com/gabrieltetar/embarch-dev-bench) | [embarch-dev-bench/decisions.md](embarch-dev-bench/decisions.md) |
| `embarch-study-designer` | Shared, `no_std` Rust library defining the data types for hardware-in-the-loop studies (BLE interaction + power profiling) that `embarch-core`, `embarch-dev-bench` firmware, and `embarch-api` all compile in — plus a `std`-only registry/merged-action-list library (`study-ui` feature) `embarch-ui` calls in-process to build/run a `Study` by hand | Shipped, [repo](https://github.com/gabrieltetar/embarch-study-designer) | [embarch-study-designer/decisions.md](embarch-study-designer/decisions.md) |
| `embarch-umbrella` | The one binary (`embarch`) a new engineer downloads: sets up the suite on whatever topology their machine is, integrates a firmware repo, verifies the whole chain (`doctor`), and starts Core when it isn't already a running service. Deliberately not a supervisor and not in the runtime path | Shipped, [repo](https://github.com/gabrieltetar/embarch-umbrella) | [embarch-umbrella/design.md](embarch-umbrella/design.md) |
| `embarch-promptu` | Curated library of firmware-specific Claude Code skills, subagents, and prompt patterns | Planned | [embarch-promptu/design.md](embarch-promptu/design.md) |
| `embarch-atlas` | Static analysis and graph visualization of a firmware codebase, for use by agents and engineers; the original C#/WPF GUI survives as its debug/dev feature | Paused, no repo yet | [embarch-atlas/design.md](embarch-atlas/design.md) |
| `embarch-topology` | The suite's single abstraction for software topology (where processes run relative to each other) and hardware topology (what's physically wired to what) — a shared crate `embarch-core`/`embarch-api`/`embarch-umbrella` all link and call live, in-process, replacing detection logic that used to be duplicated across them, plus a thin CLI binary over the same functions (its own local web UI half retired 2026-08-24, superseded by `embarch-ui`) | Implemented, merged, deployed, and live-validated end-to-end (real `build_and_flash` + `run_study` against both real boards) | [embarch-topology/design.md](embarch-topology/design.md) |
| `embarch-ui` | One consolidated human-facing UI for the whole suite — replaced `embarch-topology`'s `ui` subcommand, `embarch-study-designer`'s `study-designer-ui` binary, and `embarch-core`'s `/enroll` page outright, plus a thin VS Code launcher | **Six tabs, all live against the real deployed Core**; VS Code launcher built, packaged, installed for real (internal `.vsix`) and live-confirmed by the repo owner; the three surfaces it replaces are retired ([repo](https://github.com/gabrieltetar/embarch-ui)). Signal-route declaration lives in the Topology tab — the only human surface for it — with the diagram drawing a `direct` signal around the dev-bench node; the post-hoc **Trace** view renders an outpost capture with gaps drawn as gaps, an unnamed trace never presented as a named one, a zoomable chart whose element count is bounded by pixels rather than by the dataset, a per-subject load repartition, and a study-step row projected onto whichever clock the capture carries. Decision 11's reflash selector is deliberately not built — it is `embarch-api` orchestration — and stays open | [embarch-ui/decisions.md](embarch-ui/decisions.md) |
| `embarch-outpost` | The suite's only component that ships **inside** the DUT: a Zephyr module an engineer compiles into their own debug firmware, emitting a thread/ISR/marker timeline out a TX-only UART so a study can answer "what was the CPU actually doing while that ran". **It keeps two clocks** — the DUT stamps each record from its own counter (read lock-free out of the GRTC SYSCOUNTER's low word, layout 3) and `embarch-core` stamps each *frame* on arrival; the first orders and measures events within a frame, the second places the trace against every other stream in a study ([decisions.md](embarch-outpost/decisions.md) decisions 4, 17) | **Working end to end on real hardware as of 2026-08-27: a study captures a real nRF54L15's thread/ISR/GPIO timeline and the UI renders it named and timed. Milestone 7 Phase E closed** ([repo](https://github.com/gabrieltetar/embarch-outpost)). Milestone 7 Phases A and B closed 2026-08-25; **Phase C closed 2026-08-26** — the module, its manifest generator and its tests, building for `native_sim` and for the real nRF54L15 reference-dut target, with the generator resolving 13 real ISRs and 5 real threads out of a real ELF. Closing it fired the shared trigger that had parked the manifest halves in `embarch-core` and `embarch-api`, so **both shipped in the same pass**. **Phase D closed 2026-08-26** across five repos ([embarch-ui](embarch-ui/decisions.md) decisions 10/11 — signal routes and the post-hoc Trace view, minus a reflash selector that is `embarch-api`'s to own), validated against a dev Core from `main` in an isolated namespace rather than anything deployed. **Phase E is started and blocked, 2026-08-27, on a DUT-side emission stall rather than on wiring.** Record layout 2 was withdrawn for **layout 3** (the DUT keeps a per-record clock, read without `sys_clock_cycle_get_32()`'s two nested `irq_lock`s — [embarch-decision-reversals.md](embarch-decision-reversals.md) row 80), the reference-dut builds and flashes an outpost image whose manifest Core accepts, the `outpost` signal resolves over a `Route::Direct` and its `StreamSource::Signal` tap opens and is served — and the DUT emits a burst at boot and then nothing, while its 1 Hz header frame never repeats (row 83). Every wire constant is still an unmeasured default; that simply was not what the first real wire had to say. | [embarch-outpost/decisions.md](embarch-outpost/decisions.md) |
| `embarch-doc` | This repo — design docs, feature inventory, roadmap, user guide | Ongoing | [DOC-PROTOCOL.md](DOC-PROTOCOL.md) |

## 4. Architecture sketch

```
Claude Code (using embarch-promptu skills)          human, direct: `embarch-api <subcommand> ...`
      |                                                              |
      | MCP (stdio)                                                  |
      v                                                              v
                            embarch-api --HTTP+Bearer--> embarch-core --probe-rs/serialport--> hardware
                                                                            |
                                                                            | serial (UART/USB CDC,
                                                                            | COBS-framed postcard)
                                                                            v
                                                                   embarch-dev-bench firmware
                                                                (BLE central/peripheral + power sampling)

                                                            the one signal that skips the bench:
   DUT firmware (embarch-outpost compiled in) --UART, TX-only--> USB bridge --> embarch-core
                                             "dev-bench bypass" — a declared route, not a workaround

setup / verification, off to the side and out of the runtime path entirely:

`embarch setup|init|doctor|status|up`  ->  writes embarch-api's config, installs Core's OS service,
   (embarch-umbrella)                      registers the MCP server, diagnoses the whole chain
```

`embarch-umbrella` isn't a runtime hop either, and that's a deliberate design constraint rather than an accident of scope: it sets the stack up and diagnoses it, then gets out of the way — a working machine keeps working if the `embarch` binary is deleted. It is specifically *not* the process an MCP client spawns ([embarch-umbrella/design.md](embarch-umbrella/design.md) §3 decision 5), and it is not a supervisor: `embarch-core`'s own OS-service install is what keeps Core running (§3.3 there), which is what leaves nothing for a human to start on any same-machine topology.

`embarch-promptu` isn't a separate runtime hop — it's skills and prompt patterns Claude Code loads directly. Everything hardware-facing still funnels through `embarch-api` → `embarch-core` → the probe/serial connection, with `embarch-dev-bench` as the physical fixture sitting at that hardware boundary once it exists — reached over a new serial hop off `embarch-core` (planned, not yet implemented; see [embarch-study-designer/decisions.md](embarch-study-designer/decisions.md) §2, §5). `embarch-core`, `embarch-api`, and `embarch-dev-bench` firmware are all expected to compile in `embarch-study-designer`'s shared data types once that work starts, so the study data crossing this new hop doesn't drift into three independently-maintained definitions. embarch-api itself is reachable two ways — over MCP by Claude Code, or directly via its own CLI subcommands by a human with no agent in front of them (`embarch-api/decisions.md` §2, §3.10) — mirroring the same MCP-vs-CLI convergence embarch-core already established for its own two front-ends (`embarch-core/decisions.md` §2, §9).

## 5. Design principles carried across the suite

- **Single-engineer scope.** No multi-tenancy, no user/permission model, anywhere in the suite — each engineer runs their own full stack. See `embarch-api/decisions.md` §3.1 and `embarch-core/decisions.md` §1.
- **Every hardware-facing capability is reachable both by an agent (MCP/HTTP) and directly by a human (CLI), converging on the same underlying modules — never a privileged or special code path for either.** See `embarch-core/decisions.md` §2/§9 and `embarch-api/decisions.md` §2/§3.10.
- **Design doc as source of truth.** Each sub-project that exists gets its own `design.md` under a subfolder in `embarch-doc`, treated as the durable record superseding whatever chat produced it — not a conversation transcript.
- **Docs are proactively maintained, not requested.** Claude Code updates the relevant design doc as a normal part of doing the work, per [DOC-PROTOCOL.md](DOC-PROTOCOL.md) — not only when asked to.
- **Rust**, for the two services that exist today (`embarch-core`, `embarch-api`), for one toolchain across the stack.

## 6. Index

- [DOC-PROTOCOL.md](DOC-PROTOCOL.md) — how docs in this repo are organized and kept up to date
- [DOC-COMPACTION.md](DOC-COMPACTION.md) — how a doc gets compacted once its work has landed: what must survive, what gets discarded, and the verification gate
- **Shipped milestone docs and implementation guides are deleted, not indexed** (2026-09-02, [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3): 22 of them, 334 KB, folded into their sub-project's own docs. A `milestone-N.md` named in prose elsewhere is one of these — recoverable with `git show <rev>:<path>`. The one live execution plan is [embarch-umbrella/milestone-6.md](embarch-umbrella/milestone-6.md).
- [embarch-core/spec.md](embarch-core/spec.md) — embarch-core: what is true now (purpose, invariants, deployment, modules, constants)
- [embarch-core/decisions.md](embarch-core/decisions.md) — embarch-core: why — an index over `decisions/` (platform, probes, flashing, studies, streams, logging, surfaces), 40 numbered decisions across seven missions
- [embarch-core/interfaces.md](embarch-core/interfaces.md) — embarch-core: the HTTP surface
- [embarch-core/open.md](embarch-core/open.md) — embarch-core: unresolved questions and structural limits
- [embarch-api/spec.md](embarch-api/spec.md) — embarch-api: what is true now (three responsibilities, invariants, build orchestration, topology, modules)
- [embarch-api/decisions.md](embarch-api/decisions.md) — embarch-api: why — an index over `decisions/` (shape, surface, zephyr, core-link, studies, dev-bench), 45 numbered decisions
- [embarch-api/interfaces/config.md](embarch-api/interfaces/config.md) — embarch-api: the TOML config schema
- [embarch-api/interfaces/tools.md](embarch-api/interfaces/tools.md) — embarch-api: MCP tools and CLI subcommands, one table for both front-ends
- [embarch-api/open.md](embarch-api/open.md) — embarch-api: unresolved, including a config field that has been deriving a hardware fact from build artifacts
- [embarch-study-designer/spec.md](embarch-study-designer/spec.md) — embarch-study-designer: what is true now (the crate, its invariants, the feature split, what a study carries)
- [embarch-study-designer/decisions.md](embarch-study-designer/decisions.md) — embarch-study-designer: why — an index over `decisions/`, 62 numbered decisions across sixteen missions
- [embarch-study-designer/interfaces/types.md](embarch-study-designer/interfaces/types.md) — the study and result types (plus `gatt-types.md`, `taps.md`, `decoders.md`, `eap.md`)
- [embarch-study-designer/open.md](embarch-study-designer/open.md) — embarch-study-designer: unresolved, mostly deferred with power profiling
- [embarch-outpost/spec.md](embarch-outpost/spec.md) — embarch-outpost: what is true now (the module, both clocks, and the instrument's measured cost)
- [embarch-outpost/decisions.md](embarch-outpost/decisions.md) — embarch-outpost: why — an index over `decisions/`, 21 numbered decisions across nine missions
- [embarch-outpost/interfaces/wire.md](embarch-outpost/interfaces/wire.md) — the record and frame format (plus `integration.md`, the DUT-repo path)
- [embarch-outpost/open.md](embarch-outpost/open.md) — embarch-outpost: unresolved, led by the one binding number
- [embarch-dev-bench/spec.md](embarch-dev-bench/spec.md) — embarch-dev-bench: what is true now (the board, the layout, invariants, threading contracts, SRAM budget)
- [embarch-dev-bench/decisions.md](embarch-dev-bench/decisions.md) — embarch-dev-bench: why — an index over `decisions/` (platform, boards, link, ble, dispatch, capture, protocols, logging), 43 numbered decisions
- [embarch-dev-bench/open.md](embarch-dev-bench/open.md) — embarch-dev-bench: unresolved questions, including the mid-transmission reset that is root-caused and unfixed
- [embarch-umbrella/design.md](embarch-umbrella/design.md) — embarch-umbrella design (setup/verify/start-Core tooling; the `embarch` binary)
- [embarch-umbrella/milestone-6.md](embarch-umbrella/milestone-6.md) — Milestone 6's execution plan (Onboarding), including the `embarch-api` and `embarch-core` steps it depends on
- [embarch-promptu/design.md](embarch-promptu/design.md) — embarch-promptu design (placeholder)
- [embarch-atlas/design.md](embarch-atlas/design.md) — embarch-atlas design (placeholder)
- [embarch-topology/design.md](embarch-topology/design.md) — embarch-topology design (implemented, merged into all three consumer repos' `main`, deployed to the live Windows Core, live-validated end to end): the suite's single abstraction for software and hardware topology
- [embarch-ui/decisions.md](embarch-ui/decisions.md) — embarch-ui: one consolidated human-facing UI, six tabs, having replaced embarch-topology's UI, embarch-study-designer's UI, and embarch-core's `/enroll` page outright; signal routing and the post-hoc Trace view live here
- [embarch-token.md](embarch-token.md) — `EMBARCH_TOKEN`'s full lifecycle: generation, storage, transport, security model, rotation, known gaps
- [embarch-features.md](embarch-features.md) — feature inventory across the suite
- [embarch-roadmap.md](embarch-roadmap.md) — Now / Next / Later
- [embarch-user-guide.md](embarch-user-guide.md) — getting started and day-to-day usage, written for a firmware engineer new to EmbArch
- [embarch-zephyr.md](embarch-zephyr.md) — relationship to Zephyr RTOS: board-qualifier grammar, revisions, snippets, sysbuild
- [embarch-glossary.md](embarch-glossary.md) — DUT, study, target, project, board qualifier, topology class, discovery kind, and other load-bearing terms, each linking to its owning doc
- [embarch-decision-reversals.md](embarch-decision-reversals.md) — assumptions reality has already overturned, one page, across the whole suite
- [embarch-parallel-agents.md](embarch-parallel-agents.md) — how background agent threads work in parallel across the suite without colliding: the supervisor/worker roles, the ownership map, the `tasks/` queue, the `status.d/` fragment mechanism, and the merge gate. **New 2026-09-02, nothing has run under it yet**
- [embarch-parallel-agents-ops.md](embarch-parallel-agents-ops.md) — running the fleet: starting a batch, sizing it against the real 5h/7d usage limits, watching it from a phone, and stopping it (closing VS Code is the kill switch, by design)
- [supervisor-log.md](supervisor-log.md) — one entry per supervisor batch, newest first; the review surface for work that landed without approval
- [embarch-dev-workflow.md](embarch-dev-workflow.md) — how to iterate locally across `embarch-core`/`embarch-api`/`embarch-umbrella` without cutting a release, and without a debug build touching a real machine's install; §4a is the reverse trip, how a Core change reaches this machine's live Windows service
- [embarch-stream-pipeline-proposal.md](embarch-stream-pipeline-proposal.md) — **inbound half accepted 2026-08-25** (folded into [embarch-study-designer/decisions.md](embarch-study-designer/decisions.md) decision 39); the outbound half — the authored `StreamSend` step for writing to a DUT's shell — is **still a proposal, not accepted**
- [history/](history/) — per-sub-project history, assembled from `changelog.d/` fragments by `scripts/build_changelog.py` (see [changelog.d/README.md](changelog.d/README.md)). Replaced the `## Changelog` section every doc used to carry, 2026-09-02.
