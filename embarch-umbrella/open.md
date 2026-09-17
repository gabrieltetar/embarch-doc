# embarch-umbrella: open

**Status:** active, 2026-09-06.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Check 13's two `umbrella/034` findings are fixed but unverified against a real bench** (decision 47): unconfigured now fails with a `setup --dev-bench-repo` fix instead of warning silently, and a `firmware_version` git can't find (this run's own `49958d34`) is its own `unresolvable` fail rather than an ordinary `stale` one. **Hardware debt:** one `doctor` run on the primary bench, checking all three codes (`not-configured`, `stale`, `unresolvable`) render as reasoned.

- **Check 15 is not a hash comparison and must not be read as one.** It catches a *cross-version* stale deploy and is blind to a same-version one: `core_version` is `CARGO_PKG_VERSION`, so a rebuild and failed deploy at one version reads as a match ([decision 34](decisions/schema-skew.md)). A content hash on `/status` would close it, `embarch-core`'s call.

- **Decision 26's `--prune` stays deferred by choice, not blocked.** Its prerequisite — `build_dir_name` on **`list-targets`** (the target menu; `embarch-api` has no multi-study listing, so this was never a "study listing" gap) — shipped 2026-09-17 (`embarch-api` decision 77), for the *default* snippet/`extra_args` combination only. A non-default build still needs `target.json` (decision 69) to attribute it, so `--prune` needs both sources, never `list-targets` alone. (`study_results/`'s 803 MiB is a separate, already count-bounded gap — see decision 26's amendment — not evidence for this one.)

- **Check 17's two Fail branches have never met a real narrow-bound Core** ([decision 22](decisions/bind.md)) — this bench registers `--bind 0.0.0.0`, and **the loopback hit discriminates nothing**, so a run seeing only it settles neither arm. The three-step protocol that settles them, and the `install --bind 0.0.0.0` assumption under *both* fix lines, is `tasks/umbrella/033`.

- **`apply_plan` now clears `saved.host` on a non-`remote` `setup` conclusion** ([decision 51](decisions/sticky-host.md)), settling what decision 48 left open. Covered by a unit test over the state transition. **Hardware debt:** confirm on a real machine — a real `--host` given, a real `local` re-run, a real `doctor` after.

- **Check 5's not-permitted fail has never met a real permission-denied probe** (decision 18). Synthetic `/sys/bus/usb/devices` tree only, and **the primary topology cannot exercise it**: Core is on Windows, so the scan is skipped. Settling it: a Linux box running Core natively, probe attached, udev rules removed — Fail `probe-not-permitted`, then Pass `probes-present` with them back (restoring the rules lets Core enumerate the probe itself, which `check_probes` reads off `a.probes` before the USB-tree scan is ever consulted — `no-probe-found` needs a zero count *and* nothing on the bus, which a permitted, attached, known-VID probe cannot produce). **Whether the nine vendor IDs are the right nine is also unmeasured** — a question about the list's contents, not its home. The routing half is **settled**: the list stays here ([decision 49](decisions/probe-vendors.md)), and moves only if something other than `doctor`'s own message ever consumes it.

- **Config fragments or includes**, so the Core section is not copied into every firmware repo's config (decision 10). Needs an include mechanism in `embarch-api`'s loader. **Deferred, not rejected.**

- **Mirrored-mode WSL2 networking has defined behaviour and no evidence.** Only NAT has run here, and that is all that got live-validated. Decisions 30 and 53's ambiguity is real either way.

- **macOS is unvalidated and has no machine to validate on.** Not blocking: a Mac-only engineer walks the guide once the primary topology is proven. **Gatekeeper may make "just download and run" false there**, the aarch64 build unsigned.

- **Check 10 still spawns the MCP server in `doctor`'s own environment, not the agent CLI's** ([decision 40](decisions/mcp.md)) — the registered `env` is applied, but a server needing something only the CLI supplies fails here and works there. **That residual is what is unexercised**: the live run hit `not-registered` and `handshake-ok`, neither of them it.
