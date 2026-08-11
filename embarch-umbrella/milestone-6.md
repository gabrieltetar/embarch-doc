# embarch-umbrella: milestone 6 — Onboarding

**Status:** draft, 2026-08-05. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 6. See [design.md](design.md) for the durable architecture record this plan folds decisions back into once it ships, and [embarch-user-guide.md](../embarch-user-guide.md) for the guide that doubles as this milestone's acceptance criteria (§5).

**Note on doc layout:** [DOC-PROTOCOL.md](../DOC-PROTOCOL.md) §3 puts each sub-project's half of a milestone in its own `milestone-N.md`. This milestone's `embarch-api` and `embarch-core` halves are one and two steps respectively (§3.5, §3.6), so they're recorded here rather than in near-empty files of their own. If either grows past a couple of steps during execution, split it out then.

## 1. Goal

Make the EmbArch suite something a firmware engineer who has never seen it can install and use, on their own machine, without a conversation. Concretely: one archive to download, one command to set up, one command to integrate a firmware repo, and one command that tells them what's wrong when something is. Today none of that exists — the working path is "clone five repos, install a Rust toolchain, hand-write a TOML config with a WSL2 gateway IP in it, and know that `west build`'s output directory doesn't land where you'd guess."

This is also the milestone that makes the suite testable by someone other than its author, which is the only way the four non-primary topologies (`design.md` §4) ever get validated.

## 2. Scope

- **New sub-project:** `embarch-umbrella` — repo, binary `embarch`, the `setup`/`init`/`doctor`/`status`/`up`/`down` surface (`design.md` §8).
- **`embarch-api`:** `base_url = "auto"` (`design.md` §3 decision 9).
- **`embarch-core`:** `start`/`stop` CLI subcommands, so umbrella isn't re-implementing per-OS service control the `service-manager` crate already encapsulates (`design.md` §10).
- **Release engineering:** the suite release archive carrying all three binaries, four targets (`design.md` §3 decision 14). Spans all three repos' CI but is one pattern replicated, not three designs.
- **Docs:** [embarch-user-guide.md](../embarch-user-guide.md) rewritten from placeholder into the actual getting-started guide — already done ahead of the code, deliberately, so the guide is the specification rather than a post-hoc description.
- **Validation topology:** iii (Windows Core + WSL2 API), the one in daily use. i/ii/iv are expected to work by construction and are validated opportunistically; v (Pi) is partial by design and validated only to "detected as `remote`, says flashing won't work."
- **Out of scope:** the EmbArch UI (`design.md` §10 — a real want, its own future milestone); config fragments/includes; the artifact-transfer gap that blocks flashing from a separate machine; `embarch-promptu`; committing the repo integration (local-only per `design.md` §3 decision 12).

## 3. Steps

### 3.1 Repo bootstrap — **done, 2026-08-05**

Cloned as a sibling of the other sub-projects (`DOC-PROTOCOL.md` §2's layout is what makes `../embarch-doc/...` relative links work from inside it), and bootstrapped: Cargo project producing the `embarch` binary, `clap` (derive) for the full `design.md` §8 command surface, `CLAUDE.md` carrying the `DOC-PROTOCOL.md` pointer (§6 there), MIT `LICENSE`, `README.md`, `.gitignore`. Every command parses and then reports itself unimplemented with a pointer to the step below that implements it. `cargo build` / `cargo clippy --all-targets -- -D warnings` clean.

Dependencies are `clap`, `anyhow`, `tracing`, `tracing-subscriber` only. `reqwest`/`rustls`, `serde`/`serde_json`, and `toml` are recorded in `Cargo.toml` as a comment and get added by §3.2–§3.4 when there is behavior that needs them, rather than declared unused now. `probe-rs` and `serialport` stay absent permanently — umbrella holds no hardware knowledge (`design.md` §1).

### 3.2 Topology detection — **done, 2026-08-05**

`src/topology.rs` (pure, mirrored — no I/O, no umbrella-specific types on its boundary), `src/env.rs` (`/proc/version`, `WSL_DISTRO_NAME`, `ip route show default`), `src/probe.rs` (the `reqwest` call). 13 unit tests, all pure, written to port into `embarch-api` unchanged; `resolve` is generic over an async probe closure, so the race itself is tested with no network at all.

Two design refinements came out of implementing it, folded back into `design.md` §3 decision 6: the "race" is ordered-sequential rather than concurrent, and a third outcome (`NotCore`) distinguishes another service on the port from nothing at all. One new open item, `design.md` §10: a `local` classification under WSL2 mirrored networking doesn't tell `up` whether Core is startable from here.

Verified on this WSL2 machine (detects WSL2, finds gateway `172.22.128.1`, probes loopback then gateway in order) and against a mock (`401` → Core up, exit 0; `404` → "answered but isn't Core", keeps looking; nothing → every attempt listed, exit 1).

**This is the piece `embarch-api` also needs (§3.5), and the answer is: write it once here, liftable — not a shared crate** (`design.md` §3 decision 15, which carries the reasoning and the drift mitigations). Concretely, for this step: one self-contained module, no umbrella-specific types crossing its boundary, unit tests written so they port to `embarch-api` unchanged, and a comment in the module naming its future mirror. §3.5 then copies module and tests together rather than reimplementing the race.

### 3.3 `setup` — **done, 2026-08-05**

Detect the topology (§3.2), then, driven by the detected class:

- `local`: run `embarch-core install`, start the service, confirm the token file got generated.
- `wsl-host`: locate the Windows-side `embarch-core.exe` (`design.md` §3 decision 7's env-var-then-recorded-path-then-search order), and — since installing/starting a Windows service needs elevation — print the exact elevated command rather than attempting it. Record the located path.
- `remote`: prompt for the host, verify reachability, print the manual `EMBARCH_TOKEN` line (`design.md` §6).

Then: persist the class (and host, for `remote`) — never an address — and finish by pointing at `status`.

Shipped as described, with two deviations recorded in `design.md` decisions 3 and 4: `PATH` is *not* edited (the release archive's sibling layout removes the need, and editing shell rc files is invasive), and setup ends by pointing at `embarch status` rather than `doctor`, which doesn't exist yet. Binary location lives in `locate.rs`, state in `state.rs`; both are unit-tested.

### 3.4 `init`, `doctor`, `status`, `up`/`down`

- **`init`** — **done, 2026-08-05.** Scaffolds `embarch/embarch.toml` per decision 10, derives `build_command` from `build/build_info.yml`, and — beyond the plan — derives `artifact_path` by *finding* a real `zephyr.hex` rather than assuming a layout (sysbuild nests it, a plain build doesn't) and computes `artifact_path_for_core` from `WSL_DISTRO_NAME`. `chip` stays a `CHANGE-ME` placeholder per decision 13. Excludes via `.git/info/exclude`, registers the MCP server at local scope, and `--uninstall` reverses all three, restoring the exclude file to its prior contents. Two deviations: it doesn't pre-create `embarch/build/` (west creates it, and an empty directory would be a lie about having built), and it ends by pointing at `status` rather than `doctor`, which doesn't exist yet.
- **`doctor`** — **done, 2026-08-10.** All twelve checks in `design.md` §5, each pass/warn/fail plus a fix line, plus `--json`. Checks 6-9 needed a read-only, unvalidated mirror of `embarch-api`'s config shape (new `config.rs`) and check 4 needed its exact token-resolution fallback chain (new `token.rs`, lifted from `embarch-api/src/token_discovery.rs` — the same liftable-copy pattern `design.md` §3 decision 15 already established for topology detection, now applied a second time). Checks 7 and 9 close the two previously-deferred `embarch-api` items as planned. Smoke-tested for real, not just unit-tested: a throwaway `embarch-core` on a scratch port exercised checks 2-5/12 against a live authenticated `200`, a live `401` (wrong token), and a live `404` (no dev-bench); the real healthband repo's `embarch.toml` exercised checks 1/6/7/8/9 against real binaries and a real config. That smoke test surfaced a real bug in both `embarch-core` and `embarch-api`: neither had `--version` wired up on its clap CLI, so check 1 had nothing to report — fixed in both (one-line `#[command(...)]` addition each). Two checks are implemented but can only ever report their own current limitation rather than a real pass/fail, both by design rather than oversight: check 1's version-vs-suite-manifest comparison has no manifest to compare against until §3.7 ships, and check 11's schema-version agreement has nothing to read on either side until `embarch-study-designer` becomes a real Cargo dependency of `embarch-core`/`embarch-api` (`embarch.md` §3 — not yet true). `cargo build`/`cargo clippy --all-targets -- -D warnings`/`cargo test` (57 tests) clean.
- **`status`** — one `/status` call, `--json` (decision 11).
- **`up`/`down`** — **done, 2026-08-05.** Installed service first via `embarch-core start`/`stop` (§3.6); the foreground fallback became opt-in (`--foreground`) rather than automatic, and a `remote` topology refuses both outright (`design.md` §3 decision 4's refinement).

### 3.5 `embarch-api`: `base_url = "auto"` — **done, 2026-08-05**

Accept the literal string `auto` in `[core].base_url`, resolving it via §3.2's race at the point Core is first needed rather than at config load. Two details that matter:

- **Resolution must be lazy in CLI mode.** `embarch-api`'s startup Core-reachability check is MCP-mode-only by design (`embarch-api/design.md` §7), and `list_projects` deliberately works with Core down. Resolving `auto` eagerly at config load would regress both.
- **Add an optional `[core].host`** for the `remote` class, and keep `[core].port` (default `4884`) so `auto` has something to build candidates from.

Both details were honored, and the real `config.toml`/`config.example.toml` now use `auto` — the stale `172.22.128.1` is gone. `topology.rs`/`env.rs`/`probe.rs` were copied over from umbrella and all 13 topology tests passed unmodified, demonstrating decision 15's liftability claim rather than just asserting it. One unplanned fix came out of smoke-testing: CLI subcommands are kebab-case while MCP tools are snake_case, and every doc claimed snake_case for both (`embarch-api/design.md` §5a now states the split).

### 3.6 `embarch-core`: `start`/`stop` subcommands — **done, 2026-08-05**

Add `start`/`stop` alongside `run`/`install`/`uninstall`/`detect-dev-bench`, wrapping the `service-manager` crate's own start/stop so per-OS service control stays in the one place that already does per-OS service logic (`embarch-core/design.md` §3.3). No new hardware or HTTP surface. Keeps `design.md` §3 decision 4's `up`/`down` from re-deriving `sc.exe`/`systemctl`/`launchctl` handling in a second codebase. Shipped with no is-it-already-running pre-check, deliberately — backends disagree on whether starting a running service errors or no-ops. Smoke-testing surfaced a correction to `design.md` §3 decision 7: elevation is needed on every OS, not just Windows.

### 3.7 Release engineering — **written, 2026-08-10; unverified — no tag pushed yet**

A CI workflow per repo (`.github/workflows/release.yml` in each of `embarch-core`, `embarch-api`, `embarch-umbrella`) building release binaries for `x86_64-pc-windows-msvc`, `x86_64-unknown-linux-gnu`, `aarch64-apple-darwin`, `aarch64-unknown-linux-gnu` on a `v*.*.*` tag push, plus `embarch-umbrella/.github/workflows/assemble-suite.yml`, which pulls one already-tagged release of each component and assembles the suite archive (`embarch-<version>-<target>.{tar.gz,zip}`) plus an `embarch-manifest.json` `doctor`'s check 1 now reads (`design.md` §3 decision 14).

Both open questions this step's plan flagged are resolved, not just answered in the abstract — they're what the workflow files actually do: `aarch64-apple-darwin` needs no cross-compilation at all, because GitHub's `macos-14`-hosted runner is itself Apple Silicon (native build; still unsigned, which the guide has to mention — Gatekeeper on first run); and `windows-latest` already ships the VS Build Tools C++ workload `embarch-core`'s MSVC link needs (`embarch-core/design.md` §7's own local-build note), so nothing extra is installed for that leg. The one target that *is* a real cross-compile is `aarch64-unknown-linux-gnu` (no free aarch64-linux GitHub runner exists), and only `embarch-core` needs more than a bare cross-linker for it — its `probe-rs`/`serialport` dependencies pull in `libudev-sys`, so its release workflow uses `cross` (Docker-based, via a new `Cross.toml` that installs `libudev-dev:arm64` into the container first) where `embarch-api`/`embarch-umbrella` just install `gcc-aarch64-linux-gnu` on the host runner.

`assemble-suite.yml` is deliberately manual (`workflow_dispatch`, three release-tag inputs plus a suite version), not chained automatically off any one component's tag push — which three versions form a version-tested suite release is a decision, not a mechanical consequence of one repo pushing a tag.

**What "unverified" means concretely:** every workflow file parses as valid YAML and was written against well-established GitHub Actions patterns (`dtolnay/rust-toolchain`, `taiki-e/install-action` for `cross`, `softprops/action-gh-release`), but none has actually run — that only happens on a real tag push, which wasn't done as part of writing this (an outward-facing action: it creates real public GitHub Releases and spends Actions minutes across three repos). The one piece that *was* exercised for real: `doctor`'s manifest-reading half, smoke-tested by hand against a crafted `embarch-manifest.json` sitting next to real binaries — both a matching-versions pass and a deliberately-mismatched fail. The untested piece most likely to need a second pass is the `libudev-dev:arm64` install inside the `cross` container for `embarch-core`'s `aarch64-unknown-linux-gnu` leg.

### 3.8 Dogfood the guide

Walk [embarch-user-guide.md](../embarch-user-guide.md) start to finish on the real Windows+WSL2 machine, from a state as close to clean as is practical, and record every place it's wrong, out of order, or assumes knowledge. The guide's Appendix A (the manual path that works today) should shrink to nothing as §3.1–§3.7 land; whatever is left in it when this milestone closes is the honest residue.

## 4. Definition of done

- One archive download plus `embarch setup` produces a machine where `embarch status` reports Core up, on topology iii.
- `embarch init` in the healthband firmware repo produces a working `embarch/embarch.toml`, a locally-registered MCP server, and a clean `doctor` — with nothing tracked by that repo modified (`git status` clean).
- `embarch doctor` catches, with an actionable message, each of: Core not running, wrong token (`401`), `chip` still a placeholder, `build_command[0]` not on `PATH`, and an `artifact_path_for_core` that doesn't name the same file as `artifact_path`.
- `base_url = "auto"` survives a WSL2 restart (i.e. a changed gateway IP) with no config edit — the specific failure this milestone exists to eliminate.
- `embarch-api build_and_flash healthband-roadrunner` flashes the real board through a config produced entirely by `embarch init`, with no hand-editing and no `--firmware-path` override. (This also finally closes `embarch-api/design.md` §12's two RESOLVED-but-not-hardware-revalidated items.)
- Claude Code, opened in the firmware repo, can call `build` and `serial_log` without a permission prompt and `flash`/`reset` with one.
- The user guide has been walked by its author on the real machine (§3.8), and Appendix A reflects only what genuinely still has to be done by hand.

## 5. Open questions / risks carried into execution

- **The guide is written against tooling that doesn't exist**, on purpose (`design.md` §11). The risk is the normal one for design-ahead-of-code: some of it will turn out to be wrong when implemented. The mitigation is §3.8 — the guide is not "done" until it's been walked.
- **Windows elevation** (`design.md` §3 decision 7) is the friction point most likely to make onboarding feel bad, and it can't be designed away — installing a Windows service requires admin. Unknown whether one elevated command at setup reads as acceptable or as a wall.
- **WSL2 networking mode changes the answer to "is Core at localhost."** Mirrored mode says yes, NAT mode says no. `design.md` §3 decision 6's candidate order handles both, but only NAT mode has ever been observed on this machine — mirrored mode is reasoned, not tested.
- **macOS is entirely unvalidated** and has no machine to validate on. Deliberately not blocking: ship it, and have a Mac-only engineer walk the guide once topology iii is proven (a later milestone, not this one).
- **`aarch64-apple-darwin` code signing / Gatekeeper** (§3.7) may make the "just download and run" promise false on macOS specifically.
- **RESOLVED** — §3.2's detection is written once in umbrella in a liftable shape and copied into `embarch-api`, not extracted into a shared crate (`design.md` §3 decision 15). The residual risk this accepts is drift between the two copies; the mitigations are a mirrored-module comment, tests that port unchanged, and `doctor` check 3 reporting *which* candidate won so a divergence shows up as two different answers rather than as a mystery.
- **`embarch setup --uninstall` doesn't exist** (`design.md` §10). Not needed to close this milestone, but the first engineer who wants to remove EmbArch from their machine will need it.

## 6. Changelog

- 2026-08-10 — §3.7 written: release CI in all three repos plus `embarch-umbrella`'s suite-archive assembly workflow, and `doctor` check 1 now reads the resulting manifest when one is present. Both of §3.7's open questions resolved by what the workflows actually do (macOS: `macos-14` runner is native Apple Silicon; Windows: `windows-latest` already has the VS Build Tools). Unverified end-to-end — no tag has been pushed on any repo yet, so the four build legs (including the new `libudev` cross-install for `embarch-core`) have never actually run; only `doctor`'s manifest-reading half was exercised, by hand. Only §3.8 remains in this milestone.
- 2026-08-10 — §3.4's `doctor` done — the last unimplemented command. Two new liftable-copy modules (`token.rs`, `config.rs`) alongside the existing `topology.rs` one; `setup.rs`'s `infer_class` extracted and made `pub` so `doctor`'s check-2 fix line and `setup`'s own install/start command can never disagree. Smoke-tested against a live throwaway `embarch-core` (real `200`/`401`/`404` paths) and the real healthband repo's config, which surfaced and fixed a real bug in `embarch-core`/`embarch-api`: neither had `--version` wired up, so check 1 had nothing to report. Remaining in this milestone: §3.7 (release CI) and §3.8 (dogfood the guide).
- 2026-08-05 — §3.4's `init` done. Only `doctor` remains in §3.4, then §3.7 and §3.8.
- 2026-08-05 — §3.3 and §3.4's `up`/`down` done, with `locate.rs`/`state.rs` underneath them. Two refinements folded back into `design.md` decisions 3 and 4 (no `PATH` editing; opt-in foreground fallback). Remaining: §3.4's `init` and `doctor`, §3.7, §3.8.
- 2026-08-05 — §3.6 done: `embarch-core start`/`stop` shipped, unblocking `up`/`down`. Correction folded back into `design.md` §3 decision 7 and §10 — elevation is universal, not Windows-only. Remaining: §3.3, the rest of §3.4, §3.7, §3.8.
- 2026-08-05 — §3.5 done: `base_url = "auto"` shipped in `embarch-api`, `topology.rs` lifted verbatim with its tests intact, and the live stale-gateway-IP bug in the real config closed. Remaining: §3.3, the rest of §3.4, §3.6, §3.7, §3.8.
- 2026-08-05 — §3.2 done: topology detection implemented and verified against this machine and a mock, plus a partial §3.4 `status` so it isn't dead code. Two refinements and one new open item folded back into `design.md`. Remaining: §3.3, the rest of §3.4, §3.5, §3.6, §3.7, §3.8.
- 2026-08-05 — §5's shared-crate-vs-liftable-copy question resolved in favour of a liftable copy; §3.2 and §3.5 updated to say so, reasoning recorded as `design.md` §3 decision 15.
- 2026-08-05 — §3.1 done: repo bootstrapped, `embarch` binary building with the full §8 command surface parsing and every command reporting itself unimplemented. Nothing else in this plan has started. Deviation from the plan as written, recorded here rather than silently: `reqwest`/`serde`/`toml` were left out of `Cargo.toml` until the steps that need them, so the bootstrap declares no unused dependencies.
- 2026-08-05 — Repo created empty; §3.1 rewritten to cover only what bootstrap still requires (clone as a sibling, Cargo project, `CLAUDE.md`/`LICENSE`/`README.md`).
- 2026-08-05 — Initial draft, scoping Milestone 6 (Onboarding): the new `embarch-umbrella` sub-project, `base_url = "auto"` in `embarch-api`, `start`/`stop` in `embarch-core`, the suite release archive, and the rewritten user guide that doubles as the acceptance criteria.
