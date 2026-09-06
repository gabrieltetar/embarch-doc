# embarch-umbrella: open

**Status:** active, 2026-09-03.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Two of check 11's four live unknowns survive one real run** (2026-09-05, owner's machine); the other two agreed ([decision 35](decisions/schema-skew.md)). Open: **`core_version`**, which the running Core does not serve at all (it predates `embarch-core` decision 13; the redeploy that fixes it did not land), and **`/dev-bench/hello`'s `compatible` field**, which needs a bench. **The same run settles [decision 38](decisions/topology.md)'s `wsl-host` arm**: whether `sc.exe qc` locates the live Core, and so whether check 14 answers at all here.

- **Check 15 catches a *cross-version* stale deploy, not a same-version one.** `core_version` is `CARGO_PKG_VERSION`, so a rebuild-and-failed-deploy at the same version reads as a match. Better than nothing — `deploy-core` has reported `landed` with nothing installed, its own check comparing byte length — but **it is not a hash comparison and must not be read as one.** A content hash on `/status` would close it, and that is `embarch-core`'s call.

- **Three designed pieces are confirmed unbuilt; open is whether each is still wanted.** Decisions 22(a-c), 27/29 and 17's amendment (26's reporting half shipped as check 16, its `--prune` half deferred on 17's amendment — now two decisions' blocker).

- **Check 5's not-permitted fail has never met a real permission-denied probe** (decision 18). Unit-tested against a synthetic `/sys/bus/usb/devices` tree only, and **the primary topology cannot exercise it at all** — Core is on Windows here, so the scan is correctly skipped. Settling it needs a Linux box running Core natively, a probe attached and its udev rules removed: Fail `probe-not-permitted`, then warn `no-probe-found` with the rules back. **Whether the nine vendor IDs are the right nine is also unmeasured.**

- **Config fragments or includes**, so the Core section is not copied into every firmware repo's config (decision 10). Needs an include mechanism in `embarch-api`'s loader. **Deferred, not rejected.**

- **Nothing mechanical keeps the token and config mirrors in step with `embarch-api`'s originals** (decisions 16, 20). The guarding CI diff job **was never implemented**, and decision 15's reversal removed only the third mirror. Extract them into a shared crate, or build the job.

- **A user-level service would need no elevation on Linux or macOS** (systemd `--user`, a launch agent) **but would not start before login, defeating decision 3.** Not weighed. Self-elevation also does not help the no-GUI/no-TTY case — CI, a headless session — which still needs decision 7's print-the-command fallback.

- **Mirrored-mode WSL2 networking has defined behaviour and no evidence.** Only NAT has ever run here, so **NAT is what got live-validated.** Decision 30's ambiguity is real either way; the mode that creates it is untested.

- **macOS is unvalidated and has no machine to validate on.** Deliberately not blocking: a Mac-only engineer walks the guide once the primary topology is proven. **Gatekeeper may make "just download and run" false there**, the aarch64 build being unsigned.

- **`claude mcp get`'s output was read at last, and check 10's assumed format is wrong** (2026-09-05, CLI 2.1.261): name, `Scope:`, `Status:`, nothing else — **no `Command:`, no `Args:`** — so `parse_registered_command` can only return `UnreadableEntry` and the 10 s handshake is unreachable. No `--json` on `mcp get` or `mcp list`; the command and args are in `~/.claude.json` under `projects.<cwd>.mcpServers`. Two more: the working registration is named `embarch-api` while `MCP_SERVER_NAME` is `embarch`, so the check says *not registered* beside a connected server; and `claude` lives in the VS Code extension, never on `PATH`, so from a terminal only the `no-cli` arm is reachable. **Open is the fix** — read `~/.claude.json`, or drop the spawn and trust `Status:` — because either changes what decision 23 claims. It also still ignores `Environment:`, spawning in doctor's environment rather than the registered one.

- **Whether `init` should warn on a repo holding more than one recorded build** is undecided. On a real repo it read whichever it found first — **an ad hoc dev board's, not the production board the prior config targeted** — and cannot know which is the "real" one. Decision 17's zephyr-west discovery answers it structurally for such a repo, but **a static-discovery repo with several recorded builds still silently gets one picked for it.**
