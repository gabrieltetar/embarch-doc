# embarch-umbrella: open

**Status:** active, 2026-09-03.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **One of check 11's four live unknowns survives**: **`/dev-bench/hello`'s `compatible` field**, which needs a bench ([decision 35](decisions/schema-skew.md)). **Newly open, and it is discovery rather than skew:** check 11 reads Core's v17 and cannot ask `embarch-api` for its own, because **check 1 does not locate that binary** on this machine.

- **Check 15 catches a *cross-version* stale deploy, not a same-version one.** `core_version` is `CARGO_PKG_VERSION`, so a rebuild-and-failed-deploy at the same version reads as a match. Better than nothing — `deploy-core` has reported `landed` with nothing installed, its own check comparing byte length — but **it is not a hash comparison and must not be read as one.** A content hash on `/status` would close it, and that is `embarch-core`'s call.

- **Two designed pieces are confirmed unbuilt; open is whether each is still wanted.** Decisions 22(a-c) and 27/29. 17's amendment shipped 2026-09-05, so 26's `--prune` is deferred by choice; it still needs `build_dir_name` in `embarch-api`'s listing. **Check 16's first live number argues for it:** `study_results/` is **809 MiB across 50 entries**, and the sweep bounds the count, not the size.

- **Check 8's shell-out has never run against a real `embarch-api`.** Unit-tested against injected exit codes and stdout only; the argument order and the `{success, targets}` shape are read off `embarch-api`'s source, not observed. **Predicted here: a warn**, `embarch-api not located`, since check 1 does not find it on this machine. One `embarch doctor --json` settles it.

- **Check 5's not-permitted fail has never met a real permission-denied probe** (decision 18). Unit-tested against a synthetic `/sys/bus/usb/devices` tree only, and **the primary topology cannot exercise it at all** — Core is on Windows here, so the scan is correctly skipped. Settling it needs a Linux box running Core natively, a probe attached and its udev rules removed: Fail `probe-not-permitted`, then warn `no-probe-found` with the rules back. **Whether the nine vendor IDs are the right nine is also unmeasured.**

- **Config fragments or includes**, so the Core section is not copied into every firmware repo's config (decision 10). Needs an include mechanism in `embarch-api`'s loader. **Deferred, not rejected.**

- **Nothing mechanical keeps the token and config mirrors in step with `embarch-api`'s originals** (decisions 16, 20). The guarding CI diff job **was never implemented**, and decision 15's reversal removed only the third mirror. Extract them into a shared crate, or build the job.

- **A user-level service would need no elevation on Linux or macOS** (systemd `--user`, a launch agent) **but would not start before login, defeating decision 3.** Not weighed. Self-elevation also does not help the no-GUI/no-TTY case — CI, a headless session — which still needs decision 7's print-the-command fallback.

- **Mirrored-mode WSL2 networking has defined behaviour and no evidence.** Only NAT has ever run here, so **NAT is what got live-validated.** Decision 30's ambiguity is real either way; the mode that creates it is untested.

- **macOS is unvalidated and has no machine to validate on.** Deliberately not blocking: a Mac-only engineer walks the guide once the primary topology is proven. **Gatekeeper may make "just download and run" false there**, the aarch64 build being unsigned.

- **Check 10 still spawns the MCP server in `doctor`'s own environment, not the agent CLI's** ([decision 40](decisions/mcp.md)). The registered `env` is applied now that the entry is read structurally, so a server needing one of *those* variables is covered; one needing something the CLI's environment supplies and `doctor`'s does not will fail here and work there. **And the rebuilt check has never run live** — every claim about check 10 before 2026-09-05 was made against a parse of a format that does not exist.

- **Whether `init` should warn on a repo holding more than one recorded build** is undecided. On a real repo it read whichever it found first — **an ad hoc dev board's, not the production board the prior config targeted** — and cannot know which is the "real" one. Decision 17's zephyr-west discovery answers it structurally for such a repo, but **a static-discovery repo with several recorded builds still silently gets one picked for it.**
