# embarch: local dev workflow

**Status:** draft, 2026-08-17. How to iterate on `embarch-core`/`embarch-api`/`embarch-umbrella` locally without cutting a release, and without a debug build silently touching a real machine's install.

## 1. Short answer

**No — never use a release build to develop against, and you rarely need `--release` at all for iteration.** A debug build (`cargo build`, no flag) is faster to compile and behaves identically for everything except raw speed. Reach for `--release` only when actually producing the thing you (or CI) will ship — the release-CI workflows already do this per-repo (`embarch-roadmap.md`'s Release section); it's not something a dev loop needs.

The three code-bearing repos — `embarch-core`, `embarch-api`, `embarch-umbrella` — are independent Cargo projects, not a workspace (`embarch-user-guide.md` §11's layout). Build each on its own: `cargo build` inside that repo, nothing cross-repo needed to compile.

## 2. Wiring a dev `embarch-core` + `embarch-api` together

This is already fully supported by existing config, no code changes needed:

1. Run a dev Core in the foreground, on a port that won't collide with a real installed service (default `4884`):
   ```sh
   cd embarch-core
   EMBARCH_TOKEN=dev-token cargo run -- run --port 4885
   ```
2. Point a dev `embarch-api` config at it explicitly — `base_url` set to a literal address, not `"auto"`, **always wins outright** over auto-detection (`embarch-api/design.md` §3.11, §7):
   ```toml
   [core]
   base_url = "http://127.0.0.1:4885"
   token = "dev-token"

   [[projects]]
   name = "scratch"
   source_path = "/tmp/scratch-fw"
   build_command = ["true"]
   artifact_path = "nonexistent.hex"
   chip = "nRF54L15"
   ```
3. Run the dev `embarch-api` directly against it, no install/PATH involved:
   ```sh
   cd embarch-api
   cargo run -- --config /path/to/dev-config.toml status
   ```
   Or point an MCP client at the debug binary directly, e.g. `claude mcp add embarch-dev -- /path/to/embarch-api/target/debug/embarch-api --config /path/to/dev-config.toml`.

Nothing here touches a real installed Core, a real token file, or `PATH` — it's two foreground processes on a scratch port, talking over an explicit `base_url`.

## 3. Testing `embarch-umbrella` changes — the dangerous one

`embarch-umbrella`'s `setup` (decision 28, `embarch-umbrella/design.md` §3) **writes to real, shared machine state**: it copies binaries into the canonical per-user install location, and edits `PATH` for real — the Windows registry (`HKCU\Environment\Path`) or your actual `~/.bashrc`/`~/.zshrc`. Running `cargo run -- setup` straight from a dev checkout, with no precautions, will silently overwrite your real, working install with an untested debug build and mutate your real shell config. Don't do that by default.

**Prefer unit tests first.** `install.rs`/`locate.rs`'s logic is written to be tested without touching the real filesystem/registry at all (`cargo test` — the pure functions and idempotent file operations are exactly what decision 28's own test suite exercises). This is how decision 28 was verified originally; reach for a live `setup` run only to confirm the parts unit tests structurally can't reach (an actual registry write taking effect, a real shell picking up the new `PATH`).

**If you do need a live run, sandbox it — on Unix, override both of these together:**
```sh
export XDG_DATA_HOME=/tmp/embarch-dev-test/data   # redirects canonical_bin_dir()
export HOME=/tmp/embarch-dev-test/home            # redirects which rc files get edited
mkdir -p "$XDG_DATA_HOME" "$HOME"
touch "$HOME/.bashrc"                              # ensure_sourced only touches rc files that already exist
cargo run -- setup
```
**`XDG_DATA_HOME` alone is not enough** — `install.rs`'s rc-file editing (`ensure_path_unix`) reads the real `$HOME` directly to find `.bashrc`/`.zshrc`, independent of `XDG_DATA_HOME`. Overriding only one of the two still edits your real shell config even though the binaries land somewhere harmless.

**On Windows, there is currently no equivalent sandbox.** `install.rs`'s registry code always opens the real `HKCU\Environment` — there's no env-var-style redirect the way Unix has via `HOME`. Until one exists (worth adding if this becomes frequent — a `EMBARCH_TEST_REGISTRY_ROOT`-style override, or reusing decision 21's still-unimplemented `--dry-run`), a live Windows test of the registry-write path means touching the real per-user registry. Treat it as reversible rather than harmless: `setup --uninstall` removes exactly what `setup` added, so run it after testing, and confirm with `reg query HKCU\Environment` (or the System Properties GUI) that nothing unexpected remains.

**To exercise `up`/`down`/`status`/`doctor` without ever calling `setup`'s install step at all**, point umbrella straight at dev binaries via the existing override env vars rather than relying on PATH or the canonical location:
```sh
export EMBARCH_CORE_EXE=/path/to/embarch-core/target/debug/embarch-core
export EMBARCH_API_BIN=/path/to/embarch-api/target/debug/embarch-api   # locate_api's own override, see locate.rs
cargo run -- status
```

## 4. Windows-specific code, checked from Linux/WSL2

This sandbox (and possibly yours) has no MSVC linker, so `cargo build --target x86_64-pc-windows-msvc` for the full `embarch-umbrella` binary fails on native-TLS dependencies (`aws-lc-sys`, pulled in via `reqwest`) that need a real C toolchain for that target — unrelated to any Windows-`cfg`-gated code you write yourself. To type-check Windows-only logic (registry code, anything behind `#[cfg(windows)]`) without a full build:

1. Extract just the Windows-`cfg`-gated module into a standalone throwaway crate (a `Cargo.toml` depending only on what that module needs — e.g. `winreg`, `anyhow` — not the whole `embarch-umbrella` dependency tree).
2. `cargo check --target x86_64-pc-windows-msvc` against that crate — this only type-checks and borrow-checks, no linking, so it works even without an MSVC toolchain present.
3. This catches real API-usage mistakes (wrong `winreg` signature, wrong types) but **not** runtime behavior — a real Windows machine is still the only way to confirm the registry write actually takes effect and a new shell actually picks up the change.

`rustup target list --installed` needs `x86_64-pc-windows-msvc` present for this to work at all; add it with `rustup target add x86_64-pc-windows-msvc` if it isn't.

## Changelog

- 2026-08-17 — Initial draft, written directly out of testing `embarch-umbrella` decision 28 (canonical install + real PATH mutation) for the first time — the exact case that made "don't run this against your real machine casually" worth writing down.
