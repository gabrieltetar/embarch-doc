# EmbArch

**Status:** draft, 2026-07-17.

## 1. What EmbArch is

EmbArch is a suite of tools for firmware engineers that spans from software to the physical hardware bench: a layer that interfaces PC-side tooling to a debug probe and serial console, a dev-bench sub-project for hardware-in-the-loop testing, a curated prompt/skills library for firmware-specific agent workflows, and — pulling all of it together — the ability to give an agent like Claude Code real hardware testing capabilities on a firmware project.

## 2. Lineage

EmbArch was originally [gabrieltetar/embarch](https://github.com/gabrieltetar/embarch), a C#/WPF desktop application for static analysis and graph visualization of embedded C/C++ codebases — a "firmware-first architecture analysis and exploration platform" that turned a codebase into an interactive structural graph.

Static analysis and graph visualization of a firmware codebase was always part of EmbArch's scope, alongside the hardware-facing tooling — it's just not prioritized right now, so it's paused rather than dropped. It will resurface as `embarch-atlas`: an analysis capability meant to be used by Claude Code and other coding agents (and by engineers directly) to reason about a firmware codebase's structure, not tied to any one protocol — MCP is a plausible transport `embarch-api` could expose it over, not the defining shape of the capability itself. The original C#/WPF GUI's role narrows accordingly: it becomes a debug/dev-facing feature of `embarch-atlas` — useful for visually inspecting the graph while working on the analysis engine — rather than the product itself. See [embarch-roadmap.md](embarch-roadmap.md)'s Later bucket.

## 3. Sub-projects

| Sub-project | Purpose | Status | Doc |
|---|---|---|---|
| `embarch-core` | Owns the debug probe and serial connection; exposes `/status`, `/flash`, `/reset`, `/serial-log` over bearer-token-authed HTTP | Shipped | [embarch-core/design.md](embarch-core/design.md) |
| `embarch-api` | MCP server and CLI for Claude Code and humans alike; runs a project's build and drives Core over HTTP | Shipped | [embarch-api/design.md](embarch-api/design.md) |
| `embarch-dev-bench` | Physical rig that actively stimulates DUT inputs and senses outputs — real hardware-in-the-loop testing, not just power/reset/probe passthrough | Planned | [embarch-dev-bench/design.md](embarch-dev-bench/design.md) |
| `embarch-promptu` | Curated library of firmware-specific Claude Code skills, subagents, and prompt patterns | Planned | [embarch-promptu/design.md](embarch-promptu/design.md) |
| `embarch-atlas` | Static analysis and graph visualization of a firmware codebase, for use by agents and engineers; the original C#/WPF GUI survives as its debug/dev feature | Paused, no repo yet | [embarch-atlas/design.md](embarch-atlas/design.md) |
| `embarch-doc` | This repo — design docs, feature inventory, roadmap, user guide | Ongoing | [DOC-PROTOCOL.md](DOC-PROTOCOL.md) |

## 4. Architecture sketch

```
Claude Code (using embarch-promptu skills)          human, direct: `embarch-api <subcommand> ...`
      |                                                              |
      | MCP (stdio)                                                  |
      v                                                              v
                            embarch-api --HTTP+Bearer--> embarch-core --probe-rs/serialport--> hardware
                                                                                                    ^
                                                                                                    |
                                                                                           embarch-dev-bench
                                                                                       (stimulus/sensing fixture)
```

`embarch-promptu` isn't a separate runtime hop — it's skills and prompt patterns Claude Code loads directly. Everything hardware-facing still funnels through `embarch-api` → `embarch-core` → the probe/serial connection, with `embarch-dev-bench` as the physical fixture sitting at that hardware boundary once it exists. embarch-api itself is reachable two ways — over MCP by Claude Code, or directly via its own CLI subcommands by a human with no agent in front of them (`embarch-api/design.md` §2, §3.10) — mirroring the same MCP-vs-CLI convergence embarch-core already established for its own two front-ends (`embarch-core/design.md` §2, §9).

## 5. Design principles carried across the suite

- **Single-engineer scope.** No multi-tenancy, no user/permission model, anywhere in the suite — each engineer runs their own full stack. See `embarch-api/design.md` §3.1 and `embarch-core/design.md` §1.
- **Every hardware-facing capability is reachable both by an agent (MCP/HTTP) and directly by a human (CLI), converging on the same underlying modules — never a privileged or special code path for either.** See `embarch-core/design.md` §2/§9 and `embarch-api/design.md` §2/§3.10.
- **Design doc as source of truth.** Each sub-project that exists gets its own `design.md` under a subfolder in `embarch-doc`, treated as the durable record superseding whatever chat produced it — not a conversation transcript.
- **Docs are proactively maintained, not requested.** Claude Code updates the relevant design doc as a normal part of doing the work, per [DOC-PROTOCOL.md](DOC-PROTOCOL.md) — not only when asked to.
- **Rust**, for the two services that exist today (`embarch-core`, `embarch-api`), for one toolchain across the stack.

## 6. Index

- [DOC-PROTOCOL.md](DOC-PROTOCOL.md) — how docs in this repo are organized and kept up to date
- [embarch-core/design.md](embarch-core/design.md) — embarch-core design
- [embarch-core/milestone-1.md](embarch-core/milestone-1.md) — embarch-core's milestone 1 execution plan (Flash)
- [embarch-core/milestone-1-implementation-guide.md](embarch-core/milestone-1-implementation-guide.md) — diagnoses and turns embarch-core's milestone-1 `EMBARCH_TOKEN`/Windows-service gap (§3.5) into a ready-to-run agent prompt
- [embarch-core/milestone-2.md](embarch-core/milestone-2.md) — embarch-core's milestone 2 execution plan (Token)
- [embarch-core/milestone-2-implementation-guide.md](embarch-core/milestone-2-implementation-guide.md) — ready-to-run agent prompts implementing embarch-core's milestone-2 code work
- [embarch-api/design.md](embarch-api/design.md) — embarch-api design
- [embarch-api/milestone-1.md](embarch-api/milestone-1.md) — embarch-api's milestone 1 execution plan (Flash)
- [embarch-api/milestone-1-implementation-guide.md](embarch-api/milestone-1-implementation-guide.md) — copy-pasteable agent prompts implementing embarch-api's milestone-1 code work
- [embarch-api/milestone-2.md](embarch-api/milestone-2.md) — embarch-api's milestone 2 execution plan (Token)
- [embarch-api/milestone-2-implementation-guide.md](embarch-api/milestone-2-implementation-guide.md) — ready-to-run agent prompts implementing embarch-api's milestone-2 code work
- [embarch-dev-bench/design.md](embarch-dev-bench/design.md) — embarch-dev-bench design (placeholder)
- [embarch-promptu/design.md](embarch-promptu/design.md) — embarch-promptu design (placeholder)
- [embarch-atlas/design.md](embarch-atlas/design.md) — embarch-atlas design (placeholder)
- [embarch-token.md](embarch-token.md) — `EMBARCH_TOKEN`'s full lifecycle: generation, storage, transport, security model, rotation, known gaps
- [embarch-features.md](embarch-features.md) — feature inventory across the suite
- [embarch-roadmap.md](embarch-roadmap.md) — Now / Next / Later
- [embarch-user-guide.md](embarch-user-guide.md) — user guide (placeholder)
- [embarch-zephyr.md](embarch-zephyr.md) — relationship to Zephyr RTOS (placeholder)

## 7. Changelog

- 2026-07-17 — Initial draft.
- 2026-07-20 — Restructured per-sub-project docs into subfolders (`embarch-core/design.md`, etc.); added `DOC-PROTOCOL.md`.
- 2026-07-20 — Added `embarch-zephyr.md` placeholder.
- 2026-07-20 — Synced the suite-level docs with `embarch-api/design.md`'s new CLI subcommand interface (§3.10, §5a there): updated §3's `embarch-api` row, §4's architecture sketch (human/CLI path), and added a new §5 design principle generalizing the MCP-vs-CLI convergence now shared by both `embarch-core` and `embarch-api`.
- 2026-07-20 — §6 Index was missing every `milestone-N.md` file that already existed in the repo; added `embarch-core/milestone-1.md`, `embarch-api/milestone-1.md`, and the new `embarch-api/milestone-1-implementation-guide.md` so the index stays exhaustive per DOC-PROTOCOL.md §5.
- 2026-07-21 — Added `embarch-core/milestone-1-implementation-guide.md` to §6's index.
- 2026-07-21 — Added [embarch-token.md](embarch-token.md), consolidating `EMBARCH_TOKEN` lifecycle content out of `embarch-core/design.md` and `embarch-api/design.md`; added it to §6's index.
- 2026-07-21 — Added Milestone 2 (Token) to [embarch-roadmap.md](embarch-roadmap.md): replaces the insecure `dev-token-change-me` fallback with an auto-generated, machine-wide token file per [embarch-token.md](embarch-token.md)'s revised design. Added `embarch-core/milestone-2.md`, `embarch-core/milestone-2-implementation-guide.md`, `embarch-api/milestone-2.md`, and `embarch-api/milestone-2-implementation-guide.md` to §6's index.
