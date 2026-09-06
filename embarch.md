# EmbArch

**Status:** active, 2026-09-02.

## 1. What EmbArch is

A suite of tools for firmware engineers **spanning from software to the physical hardware bench**: a layer that interfaces PC-side tooling to a debug probe and serial console, a dev-bench sub-project for hardware-in-the-loop testing, a curated prompt and skills library for firmware-specific agent workflows, and — pulling all of it together — **the ability to give an agent like Claude Code real hardware testing capabilities on a firmware project.**

## 2. Lineage

EmbArch was originally [gabrieltetar/embarch](https://github.com/gabrieltetar/embarch), a C#/WPF desktop application for static analysis and graph visualization of embedded C/C++ codebases.

**Static analysis was always part of the scope, alongside the hardware-facing tooling — it is paused rather than dropped.** It will resurface as `embarch-atlas`: an analysis capability for coding agents and engineers to reason about a firmware codebase's structure, **not tied to any one protocol** — MCP is a plausible transport, not the defining shape of the capability. The original GUI's role narrows accordingly, to a debug-facing feature of that.

## 3. Sub-projects

Each has four capped docs: `spec.md` for what is true now, `decisions.md` for why, `open.md` for what is unresolved, and `interfaces.md` where a reference does not fit in the spec. [DOC-PROTOCOL.md](DOC-PROTOCOL.md) is the layout, [DOC-CONVENTIONS.md](DOC-CONVENTIONS.md) the shapes scripts parse, [DOC-COMPACTION.md](DOC-COMPACTION.md) the budget, and [DOC-COMPACTION-PASS.md](DOC-COMPACTION-PASS.md) how a doc is made smaller.

| Sub-project | Purpose | Status |
|---|---|---|
| [`embarch-core`](embarch-core/spec.md) | **Owns the debug probe and the serial connection**, and chooses the flashing backend per chip family rather than always probe-rs — **the board's own declared runner wins where probe-rs does not model the part.** Exposes flash, reset, serial capture, the study surface with per-tap stream captures, and signal routing over bearer-token HTTP | Shipped, deployed, live |
| [`embarch-api`](embarch-api/spec.md) | **MCP server and CLI, for agents and humans alike** — runs a project's build and drives Core over HTTP. Neither front end is a wrapper around the other | Shipped |
| [`embarch-study-designer`](embarch-study-designer/spec.md) | The shared `no_std` library defining **the data types for hardware-in-the-loop studies** that Core, the bench firmware and the API all compile in, plus a host-only authoring half the UI calls in-process | Shipped |
| [`embarch-dev-bench`](embarch-dev-bench/spec.md) | **The physical rig that plays the DUT's BLE counterpart** — advertise, connect, GATT exchange, protocol execution — Zephyr C firmware, one shared application spanning vendor-specific west workspaces | Shipped, running real studies against a real independent DUT |
| [`embarch-outpost`](embarch-outpost/spec.md) | **The only component that ships *inside* the DUT**: a Zephyr module an engineer compiles into their own debug firmware, emitting a thread/ISR/marker timeline out a TX-only UART so a study can answer *"what was the CPU actually doing while that ran"*. **It keeps two clocks** — the DUT stamps each record from its own counter, Core stamps each *frame* on arrival; the first orders and measures within a frame, the second places the trace against every other stream in a study | **Working end to end on real silicon**: 437,789 bytes in 20 s, zero records lost |
| [`embarch-topology`](embarch-topology/spec.md) | The suite's **single abstraction for software topology** (where processes run relative to each other) **and hardware topology** (what is physically wired to what) — a shared crate Core, the API and umbrella all link and call live, in-process, **replacing detection logic that used to be duplicated across them** | Implemented, merged, deployed, live-validated |
| [`embarch-ui`](embarch-ui/spec.md) | **One consolidated human-facing UI**, six tabs, having replaced three ad hoc surfaces outright, plus a thin VS Code launcher. Signal routing lives in its Topology tab — **the only human surface for it** — and a post-hoc Trace view renders an outpost capture | Six tabs live against the real deployed Core |
| [`embarch-umbrella`](embarch-umbrella/spec.md) | **The one binary a new engineer downloads**: sets up the suite on whatever topology their machine is, integrates a firmware repo, verifies the chain, and starts Core when it is not already a service. **Deliberately not a supervisor and not in the runtime path** | Shipped |
| [`embarch-promptu`](embarch-promptu/design.md) | Curated library of firmware-specific agent skills, subagents and prompt patterns | Planned, no repo |
| [`embarch-atlas`](embarch-atlas/design.md) | Static analysis and graph visualization of a firmware codebase, for agents and engineers | Paused, no repo |
| [`embarch-fleet`](embarch-fleet/spec.md) | **The machine that runs this suite's own work in parallel** — a supervisor keeps four to six short-lived workers in flight, one repo each, runs the gate and lands them itself. Its rules live in [their own repo](../embarch-fleet/README.md) and a leg never checks it out, because a supervisor that can edit its own constraints has none | Shipped, ten legs run |
| `embarch-doc` | This repo — the design record, the inventory, the roadmap, the guides | Ongoing |

## 4. Architecture sketch

```
Claude Code (using embarch-promptu skills)     human, direct: `embarch-api <subcommand> ...`
      |                                                              |
      | MCP (stdio)                                                  |
      v                                                              v
                     embarch-api --HTTP+Bearer--> embarch-core --probe-rs/serialport--> hardware
                                                         |
                                                         | serial (COBS-framed postcard)
                                                         v
                                                embarch-dev-bench firmware
                                             (BLE central/peripheral + power sampling)

                                         the one signal that skips the bench:
   DUT firmware (embarch-outpost compiled in) --UART, TX-only--> USB bridge --> embarch-core
                                          "dev-bench bypass" — a declared route, not a workaround

setup and verification, off to the side and out of the runtime path entirely:

`embarch setup|init|doctor|status|up|deploy-core`  ->  writes embarch-api's config, installs
   (embarch-umbrella)                                  Core's OS service, registers the MCP
                                                       server, diagnoses the whole chain
```

**Umbrella is not a runtime hop, and that is a design constraint rather than an accident of scope**: it sets the stack up and diagnoses it, then gets out of the way — **a working machine keeps working if the `embarch` binary is deleted.** It is specifically *not* the process an MCP client spawns.

**`embarch-promptu` is not a separate hop either** — skills and prompt patterns an agent loads directly. **Everything hardware-facing still funnels through the API to Core to the probe**, with the bench as the physical fixture at that boundary.

## 5. Principles carried across the suite

- **Single-engineer scope.** No multi-tenancy, no user or permission model, anywhere. Each engineer runs their own full stack.
- **Every hardware-facing capability is reachable both by an agent and directly by a human**, converging on the same underlying modules — **never a privileged or special code path for either.**
- **The docs are the source of truth**, and they move in the same pass as the code that changes them — not when asked. [DOC-PROTOCOL.md](DOC-PROTOCOL.md).
- **Never present an inference about what a specific piece of hardware or firmware does as established fact.** Every DUT-specific meaning is engineer-declared.
- **Rust**, for one toolchain across the stack.
- **`rustfmt` is not enforced, and nobody runs `cargo fmt`** (decided 2026-09-06). No gate checks formatting — not [the protocol](../embarch-fleet/protocol.md) §10, not any repo's CI — and none is being added yet. **This is a sequencing decision, not a verdict on formatting**, and the honest form of it is: adopting is worth doing, doing the expensive half first is not. Measured across the six Rust crates on that date: `cargo fmt` would rewrite **87 files, 1,289 hunks, 1,947 existing lines**, largest `embarch-api` and `embarch-study-designer` at 24 files each. `embarch-outpost` and `embarch-dev-bench` have no `Cargo.toml` and are not in scope. **Formatting without a check decays**: `embarch-umbrella` went 172 → 212 hunks over eleven commits in thirteen hours, monotonically, on 2026-09-05. So the format-the-world commit buys nothing durable until the check exists, and **the check that makes it stick belongs in §10, which is the repo owner's alone.** The `git blame` objection is *not* the reason — `.git-blame-ignore-revs` answers that cheaply, and nothing similarly cheap answers decay. **Reversal condition: the moment a formatting check is added to §10 or to any repo's CI, the format-the-world commits land in the same sitting — one per crate, separate from any behaviour change.** **When that check is wired, neither spelling of the command is simply right, and getting it wrong fails silently rather than loudly.** A cargo command run at a repo root reaches **the packages it selects**, and a path-dependency crate that is not a workspace member is not one of them — the same blind spot for `fmt`, for `clippy --all-targets` and for `test` alike. Bare `cargo fmt --check` used to miss `embarch-api/crates/embarch-core-client` entirely — 6 files, 43 hunks — and pass green with them unformatted. `cargo fmt --all --check` reaches those, and it *also* reaches sideways through `path = "../…"` into sibling **repos**, which is why a naive per-repo `--all` sum triple-counts `embarch-study-designer` and `embarch-topology` — so a per-repo gate spelled `--all --check` fails `embarch-api` on another repo's files. **The check must cover every crate inside the repo and nothing outside it, and which spelling does that depends on the repo's manifest**: scope `--all --check` to the repo's own tree, or run `--check` once per in-repo crate. **Workspace membership is what actually closes it**, and `embarch-api` took that route on 2026-09-06 for the clippy instance ([decision 56](embarch-api/decisions/tests.md)) — so there, bare `--check` and `-p embarch-api -p embarch-core-client --check` now agree on **24 files, all in-repo** (18 plus the sub-crate's 6), where `-p` previously *refused* outright. **`--all` is unchanged by that**: still 57 files, **33 of them outside the repo** — `embarch-study-designer` 24, `embarch-topology` 9 — and the `embarch-topology` reach is *transitive*, through `embarch-core-client`, so dropping the direct sibling dep would not close it. **The two subcommands do not read the same manifest field** — bare `cargo fmt` follows `members`, bare `cargo clippy --all-targets` follows `default-members` — so a manifest carrying only `members` fixes `fmt` and leaves `clippy` blind. **No other repo in the suite is behind this**: `embarch-api/crates/embarch-core-client` is the only nested in-repo crate anywhere in it, swept 2026-09-06 (`tasks/doc/017`). Meanwhile the trap this is meant to close is **not** closed: a worker that types `cargo fmt` gets a diff dozens of files wide that `check-ownership.py` allows — in a code repo a worker owns the whole tree — and nothing a worker reads says not to. Closing it is a change to the fleet's own instructions and is the owner's; it is filed as `tasks/doc/014`, `Owner: required`, and until it lands this bullet is a decision without a mechanism.

## 6. Index

**Start here**

| Doc | What it is |
|---|---|
| [suite/user-guide.md](suite/user-guide.md) | Getting started and day-to-day use, for an engineer new to EmbArch |
| [suite/studies-guide.md](suite/studies-guide.md) | Studies, the dev bench, and capturing a DUT trace |
| [suite/features.md](suite/features.md) | Every feature and **how far it is actually verified** |
| [suite/roadmap.md](suite/roadmap.md) | What shipped, what is in flight, what is deferred |
| [embarch-decision-reversals.md](embarch-decision-reversals.md) | **Assumptions reality has already overturned** — the best predictor of which remaining ones to distrust |

**Per sub-project** — every one has `spec.md`, `decisions.md` and `open.md`; the interface references are called out where they exist.

| Sub-project | Interface reference |
|---|---|
| [embarch-core](embarch-core/spec.md) | [interfaces.md](embarch-core/interfaces.md) — the HTTP surface |
| [embarch-api](embarch-api/spec.md) | [config.md](embarch-api/interfaces/config.md), [tools.md](embarch-api/interfaces/tools.md), [studies.md](embarch-api/interfaces/studies.md) — one table for both front ends |
| [embarch-study-designer](embarch-study-designer/spec.md) | [types.md](embarch-study-designer/interfaces/types.md), plus GATT types, taps, decoders and the protocol grammar |
| [embarch-outpost](embarch-outpost/spec.md) | [wire.md](embarch-outpost/interfaces/wire.md) — the record and frame format; `integration.md` — the DUT-repo path |
| [embarch-dev-bench](embarch-dev-bench/spec.md) | — |
| [embarch-topology](embarch-topology/spec.md) | — |
| [embarch-ui](embarch-ui/spec.md) | — |
| [embarch-umbrella](embarch-umbrella/spec.md) | — |

**Cross-cutting**

| Doc | What it is |
|---|---|
| [embarch-token.md](embarch-token.md) | The auth token's full lifecycle: generation, storage, transport, security model, rotation, known gaps |
| [embarch-glossary.md](embarch-glossary.md) | DUT, study, target, project, board qualifier, topology class, and the other load-bearing terms |
| [embarch-zephyr.md](embarch-zephyr.md) | Relationship to Zephyr: board-qualifier grammar, revisions, snippets, sysbuild |
| [embarch-dev-workflow.md](embarch-dev-workflow.md) | Iterating locally without touching a real install; **§4a is the reverse trip** — how a Core change reaches the live Windows service |
| [embarch-stream-pipeline-proposal.md](embarch-stream-pipeline-proposal.md) | **Inbound half accepted and built**; the outbound half — an authored step that writes to a DUT and confirms the reply — is **still a proposal** |
| [embarch-fleet/spec.md](embarch-fleet/spec.md) | **Start here for the fleet** — what it is, the three windows, what lives in which repo, and what it deliberately does not do |
| [the protocol](../embarch-fleet/protocol.md) | How background agent threads work in parallel across the suite without colliding: the listener, the leg, the relay |
| [running the fleet](../embarch-fleet/ops.md) | Running the fleet: arming the listener, latching the pump, sizing a leg, watching it from a phone, stopping it |
| [the risks](../embarch-fleet/risks.md) | The fleet's risk register — what each design choice traded away, and what its failure looks like |
| [embarch-remote-surfaces.md](embarch-remote-surfaces.md) | The four things that reach this suite from outside the terminal, and which one is the remote control |
| [supervisor-log.md](../embarch-fleet/supervisor-log.md) | One entry per supervisor batch, newest first — the review surface for work that landed without approval |
| [history/](history/) | Per-sub-project history, assembled from `changelog.d/` fragments |

**Deleted, not indexed:** the 22 shipped milestone docs and implementation guides, 334 KB, folded into their sub-projects' own docs. **A `milestone-N.md` named in prose elsewhere is one of these** — recoverable with `git show <rev>:<path>`.
