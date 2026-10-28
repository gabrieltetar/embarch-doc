# embarch-umbrella: open

**Status:** active, 2026-09-06.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Check 13's two `umbrella/034` findings are fixed but unverified against a real bench** (decision 47): unconfigured now fails with a `setup --dev-bench-repo` fix, and a `firmware_version` git can't find (this run's own `49958d34`) is its own `unresolvable` fail, not an ordinary `stale` one. **Hardware debt:** one `doctor` run on the primary bench confirming all three codes (`not-configured`, `stale`, `unresolvable`) render as reasoned.

- **Check 15's `binary_sha256` comparison (decision 56) has never met a live pair.** Every Pass/Warn arm — matching hashes, mismatched hashes at the same `core_version`, either side missing a hash — is unit-tested against literals only. **Hardware debt:** one `doctor` run against the installed Core confirming a real same-version match renders the closed-gap Pass, and one against a deliberately stale same-version reinstall confirming the new same-version-stale-deploy Warn actually fires.

- **Decision 26's `--prune` stays deferred by choice, not blocked.** Its prerequisite, `build_dir_name` on `list-targets`, shipped 2026-09-17 (`embarch-api` decision 77) for the *default* snippet/`extra_args` combination only; a non-default build still needs `target.json` (decision 69), so `--prune` needs both. Detail: [decision 26](decisions/prune-policy.md).

- **Check 17's two Fail branches have never met a real narrow-bound Core** ([decision 22](decisions/bind.md)) — this bench registers `--bind 0.0.0.0`, and **the loopback hit discriminates nothing**, so a run seeing only it settles neither arm. The three-step protocol that settles them, and the `install --bind 0.0.0.0` assumption under *both* fix lines, is `tasks/umbrella/033`.

- **`apply_plan` now clears `saved.host` on a non-`remote` `setup` conclusion** ([decision 51](decisions/sticky-host.md)), settling decision 48. Unit-tested. **Hardware debt:** confirm the state transition on a real machine (decision 51's three-step protocol).

- **Check 5's not-permitted fail has never met a real permission-denied probe** (decision 18). Synthetic `/sys/bus/usb/devices` tree only, and **the primary topology cannot exercise it**: Core is on Windows, so the scan is skipped. Settling it: a Linux box running Core natively, probe attached, udev rules removed — Fail `probe-not-permitted`, then Pass `probes-present` with them back (the probe is then enumerated by Core itself, so `no-probe-found` cannot occur). **Whether the nine vendor IDs are the right nine is also unmeasured** (decision 49). Routing is settled ([decision 49](decisions/probe-vendors.md)).

- **Config fragments or includes**, so the Core section is not copied into every firmware repo's config (decision 10). Needs `embarch-api`'s loader to support includes. **Deferred, not rejected.**

- **Mirrored-mode WSL2 networking has defined behaviour and no evidence.** Only NAT has run here and got live-validated. Decisions 30 and 53's ambiguity is real either way.

- **macOS is unvalidated and has no machine to validate on.** Not blocking: a Mac-only engineer walks the guide once the primary topology is proven. **Gatekeeper may make "just download and run" false there**, the aarch64 build unsigned.

- **Check 10 still spawns the MCP server in `doctor`'s own environment, not the agent CLI's** ([decision 40](decisions/mcp.md)) — registered `env` applies, but a server needing something only the CLI supplies fails here, works there. **That residual is unexercised**: the live run hit `not-registered` and `handshake-ok`, neither of them it.

- **`setup`'s desk steps (decision 58) have never run for real.** Both commands are mocked in tests. **Owner debt:** one `embarch setup` on a machine with `embarch-desk` and `claude` confirming both steps report done (and that `claude plugin install embarch-desk@embarch` works with the marketplace added), then `setup --uninstall` removing both. Not to run against the live desk without meaning to: it restarts the service.
