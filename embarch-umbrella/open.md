# embarch-umbrella: open

**Status:** active, 2026-09-03.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **One of check 11's four live unknowns survives**: **`/dev-bench/hello`'s `compatible` field**, which needs a bench ([decision 35](decisions/schema-skew.md)). **Discovery, not skew:** check 11 reads Core's v17 and cannot ask `embarch-api` for its own — **check 1 does not locate that binary** here.

- **Check 15 catches a *cross-version* stale deploy, not a same-version one.** `core_version` is `CARGO_PKG_VERSION`, so a rebuild and failed deploy at one version reads as a match. Better than nothing, but **it is not a hash comparison and must not be read as one.** A content hash on `/status` would close it, `embarch-core`'s call.

- **Decision 26's `--prune` is the last designed-and-unbuilt piece here, deferred by choice** — it needs `build_dir_name` in `embarch-api`'s listing. **Check 16's first live number argues for it:** `study_results/` is **809 MiB across 50 entries**; the sweep bounds the count, not the size.

- **Check 17's two Fail branches have never met a real narrow-bound Core** ([decision 22](decisions/bind.md)) — this bench registers `--bind 0.0.0.0`. One Core installed `--bind 127.0.0.1` on a `wsl-host` machine settles them, **each arm its own half**: stopped, `bound-narrow` must Fail where a wide registration does not; running, `bind-too-narrow` must Fail where a wide one Passes `bind-matches-registered`. **The loopback hit discriminates nothing**, so a run seeing only it settles neither. **Third step, same machine: does `embarch-core install --bind 0.0.0.0` rewrite an already-registered narrow service, or refuse it?** Never run against one, and it is the assumption under *both* fix lines — if it errors, the diagnosis is right and the whole remedy wrong.

- **Check 8's shell-out has never run against a real `embarch-api`.** Injected exit codes and stdout only; the argument order and `{success, targets}` shape are read off `embarch-api`'s source, not observed. **Predicted here: a warn**, `embarch-api not located`. One `embarch doctor --json` settles it.

- **Check 5's not-permitted fail has never met a real permission-denied probe** (decision 18). Synthetic `/sys/bus/usb/devices` tree only, and **the primary topology cannot exercise it**: Core is on Windows, so the scan is skipped. Settling it: a Linux box running Core natively, probe attached, udev rules removed — Fail `probe-not-permitted`, then `no-probe-found` with them back. **Whether the nine vendor IDs are the right nine is also unmeasured.**

- **Config fragments or includes**, so the Core section is not copied into every firmware repo's config (decision 10). Needs an include mechanism in `embarch-api`'s loader. **Deferred, not rejected.**

- **Nothing mechanical keeps the token and config mirrors in step with `embarch-api`'s originals** (decisions 16, 20). The guarding CI diff job **was never implemented**; decision 15's reversal removed only the third mirror. Extract them into a shared crate, or build it.

- **A user-level service needs no elevation on Linux or macOS** (systemd `--user`, a launch agent) **but would not start before login, defeating decision 3.** Not weighed. Self-elevation also fails the no-GUI/no-TTY case (CI, a headless session), which still needs decision 7's print-the-command fallback.

- **Mirrored-mode WSL2 networking has defined behaviour and no evidence.** Only NAT has run here, and that is all that got live-validated. Decision 30's ambiguity is real either way.

- **macOS is unvalidated and has no machine to validate on.** Not blocking: a Mac-only engineer walks the guide once the primary topology is proven. **Gatekeeper may make "just download and run" false there**, the aarch64 build unsigned.

- **Check 10 still spawns the MCP server in `doctor`'s own environment, not the agent CLI's** ([decision 40](decisions/mcp.md)). The registered `env` is applied now the entry is read structurally, so a server needing one of *those* is covered; one needing something only the CLI supplies fails here and works there. **And the rebuilt check has never run live.**

- **Whether `init` should warn on a repo holding more than one recorded build** is undecided. On a real repo it took whichever it found first — **an ad hoc dev board's, not the production board the prior config targeted** — and cannot know which is real. Decision 17's zephyr-west discovery answers that structurally; **a static-discovery repo with several recorded builds still silently gets one picked for it.**
