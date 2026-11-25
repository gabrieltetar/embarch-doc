# EmbArch

**Status:** active, 2026-09-02.

## 1. What EmbArch is

A suite of tools for firmware engineers **spanning from software to the physical hardware bench**: a layer that interfaces PC-side tooling to a debug probe and serial console, a dev-bench sub-project for hardware-in-the-loop testing, a curated prompt and skills library for firmware-specific agent workflows, and — pulling all of it together — **the ability to give an agent like Claude Code real hardware testing capabilities on a firmware project.**

## 2. Lineage

EmbArch was originally [gabrieltetar/embarch](https://github.com/gabrieltetar/embarch), a C#/WPF desktop application for static analysis and graph visualization of embedded C/C++ codebases.

**Static analysis was always part of the scope, alongside the hardware-facing tooling.** It resurfaced as `embarch-atlas`: an analysis capability for coding agents and engineers to reason about a firmware codebase's structure, **not tied to any one protocol** — it answers over its own MCP server and its CLI alike, and is not a tool on `embarch-api`'s surface. The original GUI's role narrows accordingly, to a debug-facing feature of that.

## 3. Sub-projects

Each has four capped docs: `spec.md` for what is true now, `decisions.md` for why, `open.md` for what is unresolved, and `interfaces.md` where a reference does not fit in the spec. [DOC-PROTOCOL.md](DOC-PROTOCOL.md) is the layout, [DOC-CONVENTIONS.md](DOC-CONVENTIONS.md) the shapes scripts parse, [DOC-COMPACTION.md](DOC-COMPACTION.md) the budget, and [DOC-COMPACTION-PASS.md](DOC-COMPACTION-PASS.md) how a doc is made smaller.

| Sub-project | Purpose | Status |
|---|---|---|
| [`embarch-core`](embarch-core/spec.md) | **Owns the debug probe and the serial connection**, and chooses the flashing backend per chip family rather than always probe-rs — **the board's own declared runner wins where probe-rs does not model the part.** Exposes flash, reset, serial capture, the study surface with per-tap stream captures, and signal routing over bearer-token HTTP | Shipped, deployed, live |
| [`embarch-api`](embarch-api/spec.md) | **MCP server and CLI, for agents and humans alike** — runs a project's build and drives Core over HTTP. Neither front end is a wrapper around the other | Shipped |
| [`embarch-study-designer`](embarch-study-designer/spec.md) | The shared `no_std` library defining **the data types for hardware-in-the-loop studies** that Core, the bench firmware and the API all compile in, plus a host-only authoring half the UI calls in-process | Shipped |
| [`embarch-dev-bench`](embarch-dev-bench/spec.md) | **The physical rig that plays the DUT's BLE counterpart** — advertise, connect, GATT exchange, protocol execution — Zephyr C firmware, one shared application spanning vendor-specific west workspaces | Shipped, running real studies against a real independent DUT |
| [`embarch-outpost`](embarch-outpost/spec.md) | **The only component that ships *inside* the DUT**: a Zephyr module an engineer compiles into their own debug firmware, emitting a thread/ISR/GPIO-callback/marker timeline out a TX-only UART so a study can answer *"what was the CPU actually doing while that ran"*. **It keeps two clocks** — the DUT stamps each record from its own counter, Core stamps each *frame* on arrival; the first orders and measures within a frame, the second places the trace against every other stream in a study | **Working end to end on real silicon**: 437,789 bytes in 20 s, zero records lost |
| [`embarch-topology`](embarch-topology/spec.md) | The suite's **single abstraction for software topology** (where processes run relative to each other) **and hardware topology** (what is physically wired to what) — a shared crate Core, the API and umbrella all link and call live, in-process, **replacing detection logic that used to be duplicated across them** | Implemented, merged, deployed, live-validated |
| [`embarch-smp`](embarch-smp/spec.md) | **A Rust port of smpclient**: the SMP client Core uses to hand a signed image to a DUT's MCUboot serial-recovery bootloader over USB CDC ACM. **Never opens a port** — it speaks over a stream Core opened. Apache-2.0, unlike the rest of the suite | Built, byte-identical to the reference on 18 uploads; Core's `POST /bootload` consumes it; no hardware yet |
| [`embarch-ui`](embarch-ui/spec.md) | **One consolidated human-facing UI**, six tabs, having replaced three ad hoc surfaces outright, running as a systemd user service, plus a thin VS Code launcher that drives it. Signal routing and enrolling both live in its Topology tab — **the only human surface for either** — a post-hoc Trace view renders an outpost capture, and the Atlas tab draws an `embarch-atlas` map | Five tabs live against the real deployed Core; the Atlas tab reads files only, driven in headless Firefox |
| [`embarch-desk`](embarch-desk/spec.md) | **The work cockpit behind `embarch-ui`'s Desk tab, and the one access point to Linear and Harvest for agents**: one desk per project — a Linear project or team, a Harvest project and task, GitHub repos, firmware repos, a saved bench — each session on its own desk, the UI on the one it shows; work items joining an issue to its PRs, sessions, bench activity and time; a Claude Code plugin whose hooks turn sessions into day tiles sent to Harvest on a ✓ | Built and running on the owner's machine with every connector and the first desk; no tile sent to Harvest yet |
| [`embarch-umbrella`](embarch-umbrella/spec.md) | **The one binary a new engineer downloads**: sets up the suite on whatever topology their machine is, integrates a firmware repo, verifies the chain, and starts Core when it is not already a service. **Deliberately not a supervisor and not in the runtime path** | Shipped |
| [`embarch-chat`](embarch-chat/spec.md) | **The owner's own Claude Code chat, as a VS Code extension beside the code**: one `claude` per chat on Claude Code's own wire, every chat on a desk work item before it starts, every thread of the window's desk at a glance, the prompt library as buttons, a Haiku assistant at the input, bench cards, atlas links, and `embarch-ui`'s launcher | Shipped and deployed from a local `.vsix`. **The repo is local only, no GitHub remote, by the owner's choice** |
| [`embarch-promptu`](embarch-promptu/spec.md) | **Keeps Claude Code's memory organised, then turns a rough prompt into a good one**: a plugin plus a `promptu` CLI. Every memory gets a kind and a domain, and a no-model hook checks every memory write; from step 2, prompt patterns filled by a short quiz. Revived by the owner on 2026-10-29, reversing `embarch-chat` decision 6 | In progress: step 1 of 5 (memory) built, tested and installed in warn mode |
| [`embarch-atlas`](embarch-atlas/design.md) | A hardware atlas of one board and one firmware commit: schematics, datasheets and the MCU reference manual distilled, joined to the firmware and checked for mismatches; queried by agents over MCP, drawn for humans by embarch-ui's Atlas tab | Built on one real two-board product; repo public |
| [`embarch-fleet`](embarch-fleet/spec.md) | **The machine that runs this suite's own work in parallel** — a supervisor keeps four to six short-lived workers in flight, one repo each, runs the gate and lands them itself. Its rules live in [their own repo](../embarch-fleet/README.md) and a leg never checks it out, because a supervisor that can edit its own constraints has none | Shipped, in use |
| `embarch-doc` | This repo — the design record, the inventory, the roadmap, the guides | Ongoing |

## 4. Architecture sketch

```
Claude Code                    human, direct:                  human, in a browser:
(embarch-chat library)         `embarch-api <subcommand> ...`  http://127.0.0.1:4890
      |                                   |                             |
      | MCP (stdio)                       |                             |
      v                                   v                             v
                  embarch-api                                    embarch-ui
                        \                                           /
                         \___ embarch-core-client (HTTP+Bearer) ___/
                                          |
                                          v
                              embarch-core --probe-rs/serialport--> hardware
                                          |
                                          | serial (COBS-framed postcard)
                                          v
                                 embarch-dev-bench firmware
                          (BLE central/peripheral; power sampling deferred)

                                         the one signal that skips the bench:
   DUT firmware (embarch-outpost compiled in) --UART, TX-only--> USB bridge --> embarch-core
                                          "dev-bench bypass" — a declared route, not a workaround

setup and verification, off to the side and out of the runtime path entirely:

`embarch setup|init|doctor|status|up|deploy-core`  ->  writes embarch-api's config, installs
   (embarch-umbrella)                                  Core's OS service, registers the MCP
                                                       server, diagnoses the whole chain
```

**`embarch-api` and `embarch-ui` are peers, not layers**: the UI is Core's second HTTP+Bearer client, not a front end on the API. It enrols probes, declares signals and posts studies directly ([embarch-ui/spec.md](embarch-ui/spec.md)), with no `embarch-api` in the path and, deliberately, no `probe-rs` or `serialport` in its tree. Both reach Core through one crate, **`embarch-core-client`**, so that path has one implementation rather than two that drift; it lives *inside* the `embarch-api` repo, a packaging fact and not a dependency on the API binary.

**Umbrella is not a runtime hop, by design**: it sets the stack up and diagnoses it, then gets out of the way — **a working machine keeps working if the `embarch` binary is deleted.** It is *not* the process an MCP client spawns. Its `doctor` calls Core through `embarch-core-client`, but only to diagnose one; nothing hardware-facing runs through it.

**`embarch-chat` is not a separate hop either** — its panel runs Claude Code itself, and its library is skills and commands an agent loads directly.

**Edges the sketch leaves out**, checked against the code (EMB-304). Only the atlas's is on the path to hardware, through Core:

| From → to | How | Hard or soft |
|---|---|---|
| api → desk | HTTP: the session's desk as default project | soft: reads the desk's `desks.json` |
| ui → desk | the Desk tab's `/api/desk/*` proxy | soft: that tab only |
| atlas → api CLI | a subprocess: live register reads, Core's state | hard for the live tools |
| chat → desk | HTTP with the desk's token | soft: sent once the desk is back |
| chat → ui | its launcher runs `systemctl --user` on `embarch-ui.service` | soft: the launcher only |
| desk → promptu | runs `promptu` for the Promptu panel | soft: a 503 naming it |

**Two crates touch hardware, and their split is the invariant — not one process, and not the API.** [`embarch-topology`](embarch-topology/spec.md)'s `hardware` feature decides *which* device: it enumerates probes and ports and checks a board's recorded identity, opening a probe only to read it and never a port. `embarch-core` opens the rest, every probe session (through topology's `attach`) and every serial port, once topology has matched it ([decision 8](embarch-topology/decisions.md)); `embarch-smp` opens nothing. The topology CLI links the same feature standalone, so a human sees exactly Core's validation, and refuses enrol and validate while a Core is reachable or registered (decision 28). Umbrella's `doctor` reads `/sys/bus/usb/devices`, opening nothing.

**This replaced "topology is the only code that touches `probe-rs` or a port"**, which Core's own opens falsified. One validation, one opener per kind of access, many callers.

## 5. Principles carried across the suite

- **Single-engineer scope.** No multi-tenancy, no user or permission model, anywhere. Each engineer runs their own full stack.
- **Every hardware-facing capability is reachable both by an agent and directly by a human**, converging on the same underlying modules — **never a privileged or special code path for either.**
- **The docs are the source of truth**, and they move in the same pass as the code that changes them — not when asked. [DOC-PROTOCOL.md](DOC-PROTOCOL.md).
- **Never present an inference about what a specific piece of hardware or firmware does as established fact.** Every DUT-specific meaning is engineer-declared.
- **Rust**, for one toolchain across the stack.
- **What mechanically checks a change before it lands, per sub-project — measured 2026-09-08:**

  | Sub-project | Per-push CI | Reached by the fleet's merge gate ([protocol](../embarch-fleet/protocol.md) §10) |
  |---|---|---|
  | `embarch-study-designer` | **yes** — `test.yml`, push + PR | yes |
  | `embarch-topology` | **yes** — `test.yml`, push + PR | yes |
  | `embarch-smp` | **yes** — `test.yml`, push + PR | yes, since `smp/001` (2026-10-26) |
  | `embarch-doc` | **yes** — `docs-ci.yml`, push to `main` + PR | yes (`check-docs.py`) |
  | `embarch-api`, `embarch-core`, `embarch-umbrella` | no — `release.yml` only, tag-triggered; `embarch-umbrella` also has a manual `assemble-suite.yml` | yes |
  | `embarch-ui` | no — no `.github` directory | yes |
  | `embarch-outpost` | **partly** — `host-tests.yml`, push to `main` + PR, **host legs only** ([suite/decisions.md](suite/decisions.md) 2) | **no — no `Cargo.toml`, so the gate's `cargo` half selects nothing** |
  | `embarch-dev-bench` | **no, and never has been** — `git log --all` finds no `.github` at any commit | **no — no `Cargo.toml`, so the gate's `cargo` half selects nothing** |

  **The last two rows are the ones that matter**: the two C sub-projects are the ones the fleet's merge gate cannot reach at all, so a change there is reviewed by a human or an agent reading it and, since 2026-09-11, by `embarch-outpost`'s host-only workflow — which covers its Python decoder and record vocabulary and **no part of the module as Zephyr builds it**. That is a statement of where the suite stands, not an argument for leaving it — `embarch-dev-bench/decisions/platform.md` 9 still holds that a `native_sim` job is worth building, and suite/decisions.md 2 carries the condition that would bring `embarch-outpost`'s three Zephyr legs into CI.
- **`rustfmt` is not enforced, and nobody runs `cargo fmt`** — a sequencing decision, not a verdict on formatting, with a live reversal condition and a command-spelling trap that fails silently: [suite/decisions.md](suite/decisions.md) 1.

## 6. Index

**Start here**

| Doc | What it is |
|---|---|
| [suite/user-guide.md](suite/user-guide.md) | Getting started and day-to-day use, for an engineer new to EmbArch |
| [suite/agent-guide.md](suite/agent-guide.md) | Driving EmbArch from Claude Code, and which of its MCP tools should ask you first |
| [suite/studies-guide.md](suite/studies-guide.md) | Studies, the dev bench, and capturing a DUT trace |
| [suite/hil-guide.md](suite/hil-guide.md) | The HIL guide, for the agent first: the trust claim, choosing a mode, and a Study from question to verified zip |
| [suite/features.md](suite/features.md) | Every feature and **how far it is actually verified** |
| [suite/roadmap.md](suite/roadmap.md) | What shipped, what is in flight, what is deferred |
| [embarch-decision-reversals.md](embarch-decision-reversals.md) | **Assumptions reality has already overturned** — the best predictor of which remaining ones to distrust |
| [suite/decisions.md](suite/decisions.md) | Decisions that bind more than one sub-project and so belong to none of them — the suite-level twin of every sub-project's own `decisions.md` |

**Per sub-project** — every one has `spec.md`, `decisions.md` and `open.md`; the interface references are called out where they exist.

| Sub-project | Interface reference |
|---|---|
| [embarch-core](embarch-core/spec.md) | [interfaces.md](embarch-core/interfaces.md) — the HTTP surface |
| [embarch-api](embarch-api/spec.md) | [config.md](embarch-api/interfaces/config.md), [dev-bench-config.md](embarch-api/interfaces/dev-bench-config.md), [tools.md](embarch-api/interfaces/tools.md), [studies.md](embarch-api/interfaces/studies.md) — one table for both front ends |
| [embarch-study-designer](embarch-study-designer/spec.md) | [types.md](embarch-study-designer/interfaces/types.md), plus result types, GATT types, taps, decoders and the protocol grammar |
| [embarch-outpost](embarch-outpost/spec.md) | [wire.md](embarch-outpost/interfaces/wire.md) — the record and frame format; `integration.md` — the DUT-repo path |
| [embarch-dev-bench](embarch-dev-bench/spec.md) | — |
| [embarch-topology](embarch-topology/spec.md) | — |
| [embarch-smp](embarch-smp/spec.md) | — |
| [embarch-ui](embarch-ui/spec.md) | — |
| [embarch-desk](embarch-desk/spec.md) | [interfaces.md](embarch-desk/interfaces.md) — the HTTP surface, `embarch-chat`'s additions, the plugin, connectors, CLI |
| [embarch-chat](embarch-chat/spec.md) | [interfaces.md](embarch-chat/interfaces.md) — settings, commands and keys, the `claude` command line, the desk calls |
| [embarch-promptu](embarch-promptu/spec.md) | [interfaces.md](embarch-promptu/interfaces.md) — an index into the repo's own `docs/contract.md`: the hook, the CLI, the JSON later steps share |
| [embarch-umbrella](embarch-umbrella/spec.md) | — |

**Cross-cutting**

| Doc | What it is |
|---|---|
| [embarch-token.md](embarch-token.md) | The auth token's full lifecycle: generation, storage, transport, security model, rotation, known gaps |
| [embarch-glossary.md](embarch-glossary.md) | DUT, study, target, project, board qualifier, topology class, and the other load-bearing terms |
| [embarch-zephyr.md](embarch-zephyr.md) | Relationship to Zephyr: board-qualifier grammar, revisions, snippets, sysbuild |
| [embarch-dev-workflow.md](embarch-dev-workflow.md) | Iterating locally without touching a real install; **§4a is the reverse trip** — how a Core change reaches the live Windows service |
| [LINEAR-PROTOCOL.md](LINEAR-PROTOCOL.md) | **The shape of every issue and comment in the EmbArch Linear workspace**: a summary in the owner's voice, then fields and a type's sections in doc register; six types, ten comment kinds, a long comment as a thread. `fleet-linear.py` refuses what breaks it and `lint` finds drift |
| [SUITE-REVIEW-PASS.md](SUITE-REVIEW-PASS.md) | **The one sweep that reads every sub-project at once**, hunting what is wrong across two modules and right within each — seven dimensions, run by hand as `/suite-review`, landing as Linear issues in Backlog. Every other check here is scoped to one repo, one diff or one file |
| [bootload-proposal.md](bootload-proposal.md) | A second way to put firmware on a DUT — build, then upload the signed image through MCUboot serial recovery over USB CDC ACM. **Software path built** across `embarch-smp`, `embarch-topology`, `embarch-core` and `embarch-api`; **still a proposal** until it has run on the first DUT's hardware |
| [embarch-stream-pipeline-proposal.md](embarch-stream-pipeline-proposal.md) | **Inbound half accepted and built**; the outbound half — an authored step that writes to a DUT and confirms the reply — is **still a proposal** |
| [embarch-host-study-proposal.md](embarch-host-study-proposal.md) | Host-run studies, operator prompts, SCPI bench instruments and a USB PD bench: **proposal**; phases 1–3 built (the PD bench app, instruments, host studies and the prompt, its UI modal included), no host study yet run on a bench; left: a numeric SCPI parse, designer rows |
| [embarch-desk-sessions-proposal.md](embarch-desk-sessions-proposal.md) | **Finishing an issue from the Desk**: the session drafts the PR, sent from the Desk; the issue to In Review on open; the worktree removed on merge. Start work and live sessions are built (`embarch-desk` 43–45). **Proposal** |
| [embarch-hil-proposal.md](embarch-hil-proposal.md) | **How an agent runs hardware-in-the-loop**: a Study (one bench, a report), a Test (a suite's tests across benches) and Live: **proposal** |
| [embarch-hil-evidence-proposal.md](embarch-hil-evidence-proposal.md) | **HIL evidence an agent cannot forge**: Core under its own account signs every record, the agent in a dev container, the person's acts on a card: **proposal** |
| [embarch-release-signing-proposal.md](embarch-release-signing-proposal.md) | **Signed releases**: Sigstore keyless signing in CI, one signed manifest per suite release, checked before an attested install: **proposal** |
| [embarch-atlas-planes-proposal.md](embarch-atlas-planes-proposal.md) | **The atlas in seven planes** (specifications, hardware, firmware, platform, design, external interfaces, measured), each with its own version and update procedure, and one plane-tagged join; the design plane read live through the desk: **proposal** |
| [embarch-analog-capture-proposal.md](embarch-analog-capture-proposal.md) | **One audio-rate analog signal on a bench** (a contact microphone at 32 ksps): four routes compared, the dev bench's analog input with a USB CDC sample link chosen 2026-11-24: **proposal** |
| [notes/](notes/README.md) | **Research intake while a design is shaped**, one folder per design and one file per subtopic; folds into a proposal and is deleted. [notes/hil/](notes/hil/README.md) is the first |
| [embarch-fleet/spec.md](embarch-fleet/spec.md) | **Start here for the fleet** — what it is, the three windows, what lives in which repo, and what it deliberately does not do |
| [the protocol](../embarch-fleet/protocol.md) | How background agent threads work in parallel across the suite without colliding: the listener, the leg, the relay |
| [running the fleet](../embarch-fleet/ops.md) | Running the fleet: arming the listener, latching the pump, sizing a leg, watching it from a phone, stopping it |
| [the risks](../embarch-fleet/risks.md) | The fleet's risk register — what each design choice traded away, and what its failure looks like |
| [embarch-remote-surfaces.md](embarch-remote-surfaces.md) | The four things that reach this suite from outside the terminal, and which one is the remote control |
| [supervisor-log.md](../embarch-fleet/supervisor-log.md) | One entry per unit, newest first — the review surface for work that landed without approval |
| [history/](history/) | Per-sub-project history, assembled from `changelog.d/` fragments |

**Deleted, not indexed:** the 22 shipped milestone docs and implementation guides, 334 KB, folded into their sub-projects' own docs. **A `milestone-N.md` named in prose elsewhere is one of these** — recoverable with `git show <rev>:<path>`.
