# embarch-api decisions: The shared firmware-build crate

**Status:** active, 2026-09-18.

Why `config`/`zephyr`/`resolve`/`build`/`json_out` left this repo's `src/` for a sibling crate, what came with them and what deliberately did not, and the one behaviour that changed on the way past.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The Core client's own extraction, which this follows: [client-crate.md](client-crate.md). What a build resolves: [zephyr-scan.md](zephyr-scan.md), [build.md](build.md).

### 78 — The build machinery moves into `embarch-firmware-build`, a second sibling rather than more of the first

`embarch-ui` decision 11 said reflashing was terminal-only and named its reason honestly: **this crate owns the project config and the build machinery, and `embarch-ui` cannot depend on this crate** — no such dependency direction exists in the suite. It listed three options and took the third, "land the rest and name the gap". **The fourth was never considered: move the machinery somewhere both can reach.**

That is exactly what `embarch-core-client` already did in 2026-08-24, between the same two crates, for the same reason — `reflash.rs`'s own doc comment records it. So the five modules `embarch-ui` needs move to `crates/embarch-firmware-build`: `config`, `zephyr`, `resolve`, `build`, `json_out`.

***Rejected: adding them to `embarch-core-client`.*** That crate is a *Core client*; ~4,300 lines of Zephyr scanning and subprocess management is not a client of anything. Decision 66's argument for keeping a shared crate inside this tree rather than in a tenth repo applies unchanged, and produces a second sibling under `crates/` rather than one crate about two subjects.

**`json_out` came along, and it is the only non-obvious member.** `build::write_target_manifest` writes `target.json` through it, and decision 50 says the manifest's version stamp and the `--json` surface's are the same number — so the stamper has to sit wherever the build machinery does. This crate re-exports it, so `embarch_api::json_out` resolves for every caller and `cli.rs`'s `no_json_reaches_stdout_except_through_json_out` guard is untouched.

**Deciding *which* config path to load is not part of the move.** `Config::load_from_path` went; the `--config` / `EMBARCH_API_CONFIG` / cwd resolution stayed in `main.rs`, because `embarch-ui` answers that question differently. `config.example.toml` stayed too — it is the file an operator copies and `README.md` names it by that path — so the schema's own test reaches up out of the crate to validate it rather than validating a second copy that could drift.

**Nothing else changed, and it landed alone to prove it.** `main.rs` re-imports `config`/`resolve` at the crate root exactly the way it already re-imported `build`, so every `crate::config::…` path in `cli.rs`, `tools.rs`, `reflash.rs` and `dev_bench.rs` resolves unmodified. Two visibility edits were forced by the crate boundary and are the whole diff outside the moves: `resolve::format_base_address` goes `pub(crate)` → `pub`, and `zephyr` is not re-imported at all because nothing outside `resolve`/`config` ever named it. The same 218 tests pass on both sides of the commit. It is a `default-members` entry for the reason decision 56 made `embarch-core-client` one: otherwise the unamended gate command skips its unit tests entirely.

**It links no hardware, and must not start.** A build is `west` in a subprocess and files on disk; flashing stays behind `embarch-core-client`, over HTTP to Core, for both callers alike (decisions 37/38). `embarch-ui`'s own invariant — zero `probe-rs` and zero `serialport` in `cargo tree -e normal` — is unchanged by depending on this.

**`reflash.rs`'s never-move-the-tree rule survives the move by construction.** Nothing in the new crate spawns `git` for anything but a read, and `the_reflash_path_never_moves_the_tree` still lives in this crate and still guards this crate's path.

### 79 — `BuildLocks::run_build_streaming`, because a reader who is waiting is not a tool response

`run_build` captures both pipes and hands back the text at the end, which is right for an MCP tool result and useless to a UI rendering a build as a phase of a run in progress: a Zephyr build is tens of seconds of silence and then a wall.

So the drain takes an optional `LineSink` — `Arc<dyn Fn(BuildStream, &str) + Send + Sync>`, shared by both drain tasks and therefore cloneable, `Send + Sync` and `'static`. `run_build` is unchanged and stays the right call here.

**The sink sees every line, including the ones the returned text drops.** `OUTPUT_CAP_BYTES` exists to bound a tool response; a live reader is not a tool response, and truncating what it sees would make the card and the stored log disagree about a build they watched together.
