# embarch-umbrella: open

**Status:** active, 2026-09-06.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Check 13's `umbrella/034` fixes are unverified on a real bench** (decision 47): unconfigured fails with a `setup --dev-bench-repo` fix; a `firmware_version` git can't find is `unresolvable`, not `stale`. **Hardware debt:** one `doctor` run on the primary bench showing all three.

- **Check 15's `binary_sha256` comparison (decision 56) has never met a live pair.** Unit-tested against literals only. **Hardware debt:** one `doctor` run against the installed Core confirming a real same-version match renders the closed-gap Pass, and one against a stale same-version reinstall confirming the Warn fires.

- **Decision 26's `--prune` stays deferred by choice.** Its prerequisite, `build_dir_name` on `list-targets` (`embarch-api` decision 77), covers the default build only. [Decision 26](decisions/prune-policy.md).

- **Check 17's reworded fix lines and stopped arm are unverified live** (decision 22, `umbrella/095`). **Hardware debt, owner-run** (reinstalls the service): with Core 106 deployed, register `--bind 127.0.0.1`, stop it, run `doctor` in the guest: `bound-narrow` says "stopped and bound narrow"; the printed `install --service --bind 0.0.0.0` then widens it. `bind-too-narrow` is unmeasured from a mirrored guest.

- **`apply_plan` clears `saved.host` on a non-`remote` `setup` conclusion** ([decision 51](decisions/sticky-host.md)). **Hardware debt:** decision 51's three-step protocol on a real machine.

- **Check 5's not-permitted fail has never met a real permission-denied probe** (decision 18): synthetic tree only, and the primary topology (Core on Windows) skips the scan. Settling it: a Linux box running Core natively, udev rules removed: Fail `probe-not-permitted`, then Pass with them back. **Whether the nine vendor IDs are the right nine is unmeasured** ([decision 49](decisions/probe-vendors.md)).

- **Config fragments or includes** (decision 10), so the Core section is not copied into every repo's config. Needs `embarch-api`'s loader to support includes. Deferred.

- **Mirrored-mode WSL2 networking has no evidence;** only NAT has run (decisions 30, 53).

- **macOS is unvalidated, with no machine.** **Gatekeeper may make "just download and run" false there**, the aarch64 build unsigned.

- **Check 10 spawns the MCP server in `doctor`'s environment, not the agent CLI's** ([decision 40](decisions/mcp.md)); a server needing something only the CLI supplies fails here, works there. Unexercised.

- **`setup`'s desk steps (decision 58) have never run for real;** both commands are mocked. **Owner debt:** one `embarch setup` on a machine with `embarch-desk` and `claude` confirming both steps report done (and that `claude plugin install embarch-desk@embarch` works with the marketplace added), then `setup --uninstall` removing both. It restarts the live desk's service.

- **`install-core` has never run elevated** (decisions 61, 69, 70). Windows and Linux scripts are tested as text and on a fake host; Windows's block was type-checked in a throwaway crate. **Owner debt:** (a) Windows, elevated shell, default data dir: all six steps OK, `sc qc com.embarch.core` shows `NT SERVICE\com.embarch.core`, store ACL is the service, SYSTEM, Administrators; `core-fingerprint` matches `/status`'s `keyid`. (b) Linux, `sudo embarch install-core <release>` in a scratch distro with systemd: seven steps OK, unit has `User=embarch`, `store` is `embarch` `0700`, tokens `0640 embarch:embarch-users`, you read one after re-login, fingerprint matches `keyid`; a root-made store is refused. (c) a tampered release writes nothing. Unbuilt: self-elevation, WSL2 hosts, staging pruning.
