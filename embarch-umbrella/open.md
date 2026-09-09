# embarch-umbrella: open

**Status:** active, 2026-09-06.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Check 13's two `umbrella/034` findings are fixed but unverified against a real bench** (decision 47): unconfigured now fails with a `setup --dev-bench-repo` fix instead of warning silently, and a `firmware_version` git can't find (this run's own `49958d34`) is its own `unresolvable` fail rather than an ordinary `stale` one. **Hardware debt:** one `doctor` run on the primary bench, checking all three codes (`not-configured`, `stale`, `unresolvable`) render as reasoned.

- **Check 15 is not a hash comparison and must not be read as one.** It catches a *cross-version* stale deploy and is blind to a same-version one: `core_version` is `CARGO_PKG_VERSION`, so a rebuild and failed deploy at one version reads as a match ([decision 34](decisions/schema-skew.md)). A content hash on `/status` would close it, `embarch-core`'s call.

- **Decision 26's `--prune` is the last designed-and-unbuilt piece here, deferred by choice** — it needs `build_dir_name` in `embarch-api`'s listing. **Check 16 argues for it:** `study_results/` is **803 MiB across 50 entries** [measured 2026-09-06]; the sweep bounds the count, not the size.

- **Check 17's two Fail branches have never met a real narrow-bound Core** ([decision 22](decisions/bind.md)) — this bench registers `--bind 0.0.0.0`, and **the loopback hit discriminates nothing**, so a run seeing only it settles neither arm. The three-step protocol that settles them, and the `install --bind 0.0.0.0` assumption under *both* fix lines, is `tasks/umbrella/033`.

- **`saved.host` is still sticky, and `doctor` check 2 still reads it** — `setup` writes it for every class though `state.rs` calls it "only meaningful for `remote`", so an old `--host` still makes check 2 infer `remote` on a `wsl-host` machine ([decision 22](decisions/bind.md)). `umbrella/026` made the Fail detail name the input (`config.core.host` or a saved one), but **the fallback's intent stays undocumented and unfixed**: it does not preserve `remote` either, and clearing it changes check 2 on real machines on a guess.

- **Check 5's not-permitted fail has never met a real permission-denied probe** (decision 18). Synthetic `/sys/bus/usb/devices` tree only, and **the primary topology cannot exercise it**: Core is on Windows, so the scan is skipped. Settling it: a Linux box running Core natively, probe attached, udev rules removed — Fail `probe-not-permitted`, then `no-probe-found` with them back. **Whether the nine vendor IDs are the right nine is also unmeasured.** Whether check 5 should route this to `embarch-core` instead of enumerating in-process is a routing question filed to `inbox/` 2026-09-09 (`Scope: suite`); a numbered `embarch-umbrella` decision on where a probe-vendor fact belongs is owed.

- **The no-stray-spaces guard cannot reach checks 4 and 12** (both `async`, no pure judge, so their
  rendered text is never tested at all). `umbrella/031` normalised both checks' bodies at the same
  interpolation points check 1 needed fixed, but a corpus still can't exercise them without a live
  Core — the untestability is what's open, not the normalisation
  ([decision 43](decisions/message-rendering.md), `tasks/umbrella/031`).

- **Config fragments or includes**, so the Core section is not copied into every firmware repo's config (decision 10). Needs an include mechanism in `embarch-api`'s loader. **Deferred, not rejected.**

- **The token mirror is closed:** `embarch-umbrella` now depends on `embarch-core-client` directly for `resolve_token` ([decision 20](decisions/mirrors.md) amendment). The config mirrors (`CoreConfig`, `ProjectConfig`) are not — no CI diff job exists, and both have drifted (task 036 state note). Depend on `embarch-core-client` for `CoreConfig` too, or build the diff job.

- **A user-level service needs no elevation on Linux or macOS** (systemd `--user`, a launch agent) **but would not start before login, defeating decision 3.** Not weighed.

- **Mirrored-mode WSL2 networking has defined behaviour and no evidence.** Only NAT has run here, and that is all that got live-validated. Decision 30's ambiguity is real either way.

- **macOS is unvalidated and has no machine to validate on.** Not blocking: a Mac-only engineer walks the guide once the primary topology is proven. **Gatekeeper may make "just download and run" false there**, the aarch64 build unsigned.

- **Check 10 still spawns the MCP server in `doctor`'s own environment, not the agent CLI's** ([decision 40](decisions/mcp.md)) — the registered `env` is applied, but a server needing something only the CLI supplies fails here and works there. **That residual is what is unexercised**: the live run hit `not-registered` and `handshake-ok`, neither of them it.
