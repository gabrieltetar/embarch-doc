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
| `embarch-core` | Owns the debug probe and serial connection; exposes `/status`, `/flash`, `/reset`, `/serial-log`, `/dev-bench/port` over bearer-token-authed HTTP | Shipped | [embarch-core/design.md](embarch-core/design.md) |
| `embarch-api` | MCP server and CLI for Claude Code and humans alike; runs a project's build and drives Core over HTTP | Shipped | [embarch-api/design.md](embarch-api/design.md) |
| `embarch-dev-bench` | Physical rig that plays the DUT's BLE counterpart (advertise/connect/GATT exchange) and samples power during a `Study`, per `embarch-study-designer`'s types — Zephyr-based C firmware, one shared application spanning multiple vendor-specific west workspaces | Implementation in progress at [gabrieltetar/embarch-dev-bench](https://github.com/gabrieltetar/embarch-dev-bench): shared `app/` (serial protocol, stubbed FFI, BLE bridge real+stub) with the real bridge now covering the full `Action`/`GattOperation` surface (advertise, connect in both roles, GATT read/write/notify/indicate/subscribe/stream-capture); `native_sim` workspace built and verified end to end (`west build` + a live Hello/HelloAck/demo-sequence run + all ztest cases passing); `nordic`/nRF54L15DK workspace now builds too against NCS v3.4.0 (real BLE code compiled and linked, FLASH 13% / RAM 13%), but has never been flashed or run on a physical board | [embarch-dev-bench/design.md](embarch-dev-bench/design.md) |
| `embarch-study-designer` | Shared, `no_std` Rust library defining the data types for hardware-in-the-loop studies (BLE interaction + power profiling) that `embarch-core`, `embarch-dev-bench` firmware, and `embarch-api` all compile in | Types/tools implemented and tested ([gabrieltetar/embarch-study-designer](https://github.com/gabrieltetar/embarch-study-designer)); not yet consumed by `embarch-core`/`embarch-api` as a Cargo dependency | [embarch-study-designer/design.md](embarch-study-designer/design.md) |
| `embarch-umbrella` | The one binary (`embarch`) a new engineer downloads: sets up the suite on whatever topology their machine is, integrates a firmware repo, verifies the whole chain (`doctor`), and starts Core when it isn't already a running service. Deliberately not a supervisor and not in the runtime path | In progress at [gabrieltetar/embarch-umbrella](https://github.com/gabrieltetar/embarch-umbrella): every command in the surface — `setup`, `init`, `doctor`, `status`, `up`/`down` — is implemented. Release CI is verified fully end-to-end now, all three repos: real releases, and a real assembled `suite-v0.1.0` archive (`assemble-suite.yml`, after fixing a real `pipefail`/glob bug its first run caught) that `doctor` check 1 has actually validated a manifest against. Milestone 6's first Definition-of-Done bullet is now genuinely met: one archive download plus an elevated `embarch setup` produces a real, running Core on the daily-use Windows+WSL2 machine, `doctor` all green — after finding and fixing a real bug where Core had never actually registered as a Windows service (it just ran like a console program; Windows silently killed every real start attempt after 30 seconds). Only `doctor` check 11 (`embarch-study-designer` schema version) is still a stub, since that sub-project isn't a dependency of `embarch-core`/`embarch-api` yet. Milestone 6's last step — dogfooding the user guide — is underway; several real doc bugs found and fixed so far, detail in [milestone-6.md](embarch-umbrella/milestone-6.md) §3.8 | [embarch-umbrella/design.md](embarch-umbrella/design.md) |
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
                                                                            |
                                                                            | serial (UART/USB CDC,
                                                                            | COBS-framed postcard)
                                                                            v
                                                                   embarch-dev-bench firmware
                                                                (BLE central/peripheral + power sampling)

setup / verification, off to the side and out of the runtime path entirely:

`embarch setup|init|doctor|status|up`  ->  writes embarch-api's config, installs Core's OS service,
   (embarch-umbrella)                      registers the MCP server, diagnoses the whole chain
```

`embarch-umbrella` isn't a runtime hop either, and that's a deliberate design constraint rather than an accident of scope: it sets the stack up and diagnoses it, then gets out of the way — a working machine keeps working if the `embarch` binary is deleted. It is specifically *not* the process an MCP client spawns ([embarch-umbrella/design.md](embarch-umbrella/design.md) §3 decision 5), and it is not a supervisor: `embarch-core`'s own OS-service install is what keeps Core running (§3.3 there), which is what leaves nothing for a human to start on any same-machine topology.

`embarch-promptu` isn't a separate runtime hop — it's skills and prompt patterns Claude Code loads directly. Everything hardware-facing still funnels through `embarch-api` → `embarch-core` → the probe/serial connection, with `embarch-dev-bench` as the physical fixture sitting at that hardware boundary once it exists — reached over a new serial hop off `embarch-core` (planned, not yet implemented; see [embarch-study-designer/design.md](embarch-study-designer/design.md) §2, §5). `embarch-core`, `embarch-api`, and `embarch-dev-bench` firmware are all expected to compile in `embarch-study-designer`'s shared data types once that work starts, so the study data crossing this new hop doesn't drift into three independently-maintained definitions. embarch-api itself is reachable two ways — over MCP by Claude Code, or directly via its own CLI subcommands by a human with no agent in front of them (`embarch-api/design.md` §2, §3.10) — mirroring the same MCP-vs-CLI convergence embarch-core already established for its own two front-ends (`embarch-core/design.md` §2, §9).

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
- [embarch-study-designer/design.md](embarch-study-designer/design.md) — embarch-study-designer design (shared study-data-types library)
- [embarch-study-designer/milestone-3.md](embarch-study-designer/milestone-3.md) — embarch-study-designer's milestone 3 execution plan (Study Designer, design-only)
- [embarch-umbrella/design.md](embarch-umbrella/design.md) — embarch-umbrella design (setup/verify/start-Core tooling; the `embarch` binary)
- [embarch-umbrella/milestone-6.md](embarch-umbrella/milestone-6.md) — Milestone 6's execution plan (Onboarding), including the `embarch-api` and `embarch-core` steps it depends on
- [embarch-promptu/design.md](embarch-promptu/design.md) — embarch-promptu design (placeholder)
- [embarch-atlas/design.md](embarch-atlas/design.md) — embarch-atlas design (placeholder)
- [embarch-token.md](embarch-token.md) — `EMBARCH_TOKEN`'s full lifecycle: generation, storage, transport, security model, rotation, known gaps
- [embarch-features.md](embarch-features.md) — feature inventory across the suite
- [embarch-roadmap.md](embarch-roadmap.md) — Now / Next / Later
- [embarch-user-guide.md](embarch-user-guide.md) — getting started and day-to-day usage, written for a firmware engineer new to EmbArch
- [embarch-zephyr.md](embarch-zephyr.md) — relationship to Zephyr RTOS (placeholder)
- `*.changelog-archive.md` files (one per doc whose Changelog `scripts/archive-changelog.py` has trimmed, e.g. [embarch.changelog-archive.md](embarch.changelog-archive.md)) — not individually indexed here since each lives beside its source doc and is linked from the top of that doc's own `## Changelog` section

## 7. Changelog

*Older entries archived to [embarch.changelog-archive.md](embarch.changelog-archive.md).*

- 2026-08-14 — Zephyr/west live target discovery (`discovery = "zephyr-west"`) implemented across all three repos, closing a real gap `embarch init` found mid-milestone: a hand-maintained `[[projects]]` entry can't safely represent "several real boards/variants/revisions, some combinations of which don't actually exist" the way a live, file-backing-validated scan can. `embarch-core` gained `POST /resolve-chip` (Zephyr SoC name → probe-rs chip, validated against probe-rs's own target registry); `embarch-api` gained live `list_targets`, new `board`/`variant`/`revision`/`app` params on `build`/`flash`/`build_and_flash`/`reset`, and the file-backing check itself (does a hardware revision's overlay/defconfig actually exist, rather than trusting what `board.yml` merely declares); `embarch-umbrella`'s `init` scaffolds the minimal schema instead of guessing one board, and `doctor` checks 7-9 branch on `discovery`. `discovery = "static"` (today's schema) is unchanged and remains the default. Verified as real cross-repo interop against a synthetic fixture modeling the actual healthband finding, plus a real running Core — not three components independently unit-tested in isolation. Full detail: `embarch-core/design.md` §3 decision 8, `embarch-api/design.md` §3 decision 12, `embarch-umbrella/design.md` §3 decision 17, [milestone-6.md](embarch-umbrella/milestone-6.md) §3.9.
- 2026-08-11 — Three `embarch-doc` maintenance chores automated (full detail in `DOC-PROTOCOL.md`'s own changelog): `scripts/check-links.py` and new `scripts/check-staleness.py` now run in CI on every push/PR (`.github/workflows/docs-ci.yml`); new `scripts/archive-changelog.py` trims each doc's Changelog to its most recent entries, run weekly by `.github/workflows/changelog-archive.yml` via a PR. This doc's own §7 (this section) and six other docs' Changelogs got their first trim as part of standing the tool up — see each `*.changelog-archive.md` sibling for what moved. `check-staleness.py`'s first run also caught and fixed a real, pre-existing status disagreement in `embarch-study-designer/design.md`.
- 2026-08-12 — Real, first-ever Windows service install of `embarch-core` caught a genuine bug: it never implemented the `StartServiceCtrlDispatcherW` handshake Windows requires, so SCM killed every start attempt after 30 seconds (Win32 1053) even though Core itself worked fine — every prior test had used a throwaway foreground instance instead of a real boot-service install. Fixed (`embarch-core` `v0.1.1`), verified end-to-end on the real daily-use machine: clean install, clean start, `doctor` all green. Milestone 6's first Definition-of-Done bullet is now genuinely met (§3 row updated; full detail in [milestone-6.md](embarch-umbrella/milestone-6.md) §3.8 and `embarch-core/design.md`).
- 2026-08-11 — `assemble-suite.yml` triggered for real (once the user set up `gh` auth with real admin rights on the repo) and caught a genuine bug on its first-ever run: an `ls a.tar.gz b.zip | head -n1` line fails under `pipefail` whenever only one glob matches, which is every target. Fixed and verified — all four targets clean, and `doctor` check 1 passed against the resulting real `suite-v0.1.0` manifest for the first time (§3 row updated; full detail in [milestone-6.md](embarch-umbrella/milestone-6.md) §3.7/§3.8 and `embarch-umbrella/design.md`). Milestone 6's release engineering is now fully done, end to end.
- 2026-08-11 — `embarch-umbrella`'s own `v0.1.0` tag pushed and released clean across all four targets on the first try — the permission-classifier denial that blocked this same push earlier in the day didn't recur. All three repos now have a real `v0.1.0` release (§3 row updated). Milestone 6's last step, dogfooding the user guide, is now underway ([milestone-6.md](embarch-umbrella/milestone-6.md) §3.8): several real doc bugs already found and fixed directly in [embarch-user-guide.md](embarch-user-guide.md) by running the real released binaries, ahead of `assemble-suite.yml` (which still needs a human to trigger — this session's `gh` auth lacks the admin rights `workflow_dispatch` needs) and the still-pending elevated-Windows Core install / real board flash.
- 2026-08-11 — Release CI verified against real `v0.1.0` tags: `embarch-api` released clean across all four targets first try; `embarch-core` caught and fixed a real gap (`libudev-dev` missing on the native Linux runner) and then released clean too (§3 row updated). `embarch-umbrella`'s own tag, and the suite-archive assembly it unlocks, is still pending a human push — the agent's own push to that one repo was repeatedly denied by a local permission classifier. Full detail in `embarch-umbrella/design.md` and `milestone-6.md`'s own changelogs.
- 2026-08-10 — Release CI written for all three repos plus `embarch-umbrella`'s suite-archive assembly workflow (§3 row updated; [embarch-umbrella/milestone-6.md](embarch-umbrella/milestone-6.md) §3.7). `doctor` check 1 now reads the resulting suite manifest when one is present. Unverified end-to-end — no tag has been pushed on any repo, so none of the four per-target build legs has actually run; only the manifest-reading side was smoke-tested, by hand. §3.8 (dogfood the guide) is all that's left in Milestone 6.
- 2026-08-10 — `embarch-umbrella`'s `doctor` implemented (§3 row updated), closing out every command in [embarch-umbrella/milestone-6.md](embarch-umbrella/milestone-6.md) §3.4 — `setup`/`init`/`doctor`/`status`/`up`/`down` are all real now, with only §3.7 (release CI) and §3.8 (dogfood the guide) left in Milestone 6. Smoke-testing `doctor` against a live throwaway `embarch-core` and the real healthband repo surfaced a small but real bug shared by `embarch-core` and `embarch-api`: neither had `--version` wired up on its CLI, so `doctor`'s binaries-found check had nothing to report — fixed in both. Full detail in `embarch-umbrella/design.md`'s own changelog (new decision 16).

