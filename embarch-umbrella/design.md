# embarch-umbrella: design

**Status:** draft, 2026-08-05. Bootstrapped at [gabrieltetar/embarch-umbrella](https://github.com/gabrieltetar/embarch-umbrella): the `embarch` binary builds and its full §8 command surface parses, but every command reports itself unimplemented — there is no behavior behind any of them yet. Everything below is therefore still design ahead of implementation per [DOC-PROTOCOL.md](../DOC-PROTOCOL.md) §5, same posture `embarch-api/design.md` §3.10 used for its CLI decision. Append changes to the Changelog (§12) rather than silently editing history above it.

## 1. Purpose and scope

`embarch-umbrella` is the sub-project that gets a firmware engineer from *nothing installed* to *`embarch-api build_and_flash my-project` works, from a terminal or from Claude Code* — on whatever topology their machine happens to be (Core native on Windows with the API in WSL2, both native on a Mac, both native on Linux, or Core on a separate box). It ships one binary, named `embarch` (§3 decision 2), with three jobs: **set up**, **verify**, and **start Core when it isn't already running**.

The reason it exists as its own sub-project rather than as more subcommands on an existing binary: it is the only component that knows about *both* `embarch-core` and `embarch-api`, and it is the binary a person downloads when they have neither. `embarch-api` can't hold this — it would have to install Core's OS service and register MCP servers, neither of which a thin build-orchestration layer has any business doing, and it can't be the answer to "what do I download first" when it's one of the two things being set up.

`embarch-umbrella` is **not**:
- **A process supervisor or daemon.** It has no restart loop, no health polling, no resident process. Core's own cross-platform service install (`embarch-core/design.md` §3.3) is what keeps Core running; umbrella's `up` exists only for when that isn't in place or has died (§3 decision 4).
- **In the runtime data path.** Nothing routes through umbrella after setup. It is not an MCP server, not a proxy, and deliberately not the process an MCP client spawns (§3 decision 5). If umbrella is deleted from a working machine, the stack keeps working.
- **A hardware or build layer.** It never links `probe-rs` or `serialport`, never runs a build command. Every capability it appears to have is a shell-out to `embarch-core` or `embarch-api`, or an HTTP call to Core's existing endpoints.
- **Multi-machine orchestration.** No SSH, no remote agent, no remote install. A Core on a separate box (a Pi over wifi) is started by a human on that box; umbrella only detects and verifies it (§3 decision 8).
- **A GUI.** A small EmbArch UI — a human glancing at whether Core is up, rather than asking an agent — is real anticipated scope but explicitly out of this document's v1 (§10). What v1 owes it is a stable machine-readable status contract (§3 decision 11).

## 2. Architecture overview

```
                    setup / init / doctor / status / up / down
                                    |
                                 embarch                    <- this sub-project
                          /         |          \
        shells out to     |         |           |  HTTP+Bearer (GET /status,
        embarch-core CLI  |         |           |  /dev-bench/port)
        (install/start)   |         |           v
                          |         |      embarch-core
                          |         |
                          |         +-- shells out to embarch-api CLI
                          |             (list_projects, status) and reads/writes
                          |             its config
                          |
                          +-- writes <firmware-repo>/embarch/embarch.toml
                              and registers the MCP server (local scope)

after setup, the runtime path has no umbrella in it:

Claude Code --stdio--> embarch-api --HTTP+Bearer--> embarch-core --> hardware
human ------CLI------> embarch-api ----------------^
```

Both of `embarch-api`'s front-ends stay first-class after setup: an MCP client spawning it over stdio, **and** a human running `embarch-api <subcommand>` directly (`embarch-api/design.md` §5a). Umbrella's job is to make the second one ergonomic too — a resolved config path in the environment, and the binary on `PATH` — not just to wire up the agent path.

## 3. Locked-in design decisions and rationale

1. **Language: Rust**, one static binary with no runtime dependencies, matching the rest of the suite. It must run on a machine where nothing else from EmbArch is installed yet, so a runtime (Python, Node) or a system library dependency would be self-defeating.

2. **Repo `embarch-umbrella`, binary `embarch`.** The repo name says what it is in the suite; the binary name is what a new engineer types on their first day (`embarch setup`, `embarch doctor`). `embarch-umbrella setup` was rejected purely on ergonomics — this is the most-typed command in the suite for someone who has never used it before.

3. **Core is always an installed, autostarting OS service — that, not a launcher, is the actual answer to "one button starts everything."** On the four same-machine topologies (§4), if Core autostarts at boot there is nothing for a human to start, ever: `embarch-api` is invoked per-use (spawned by an MCP client, or run directly by a human), and it finds a Core that is already up. So the problem is a *one-time setup* problem plus an *ongoing verification* problem, not a process-management problem. `embarch-core install` already exists and already handles all three OSes via the `service-manager` crate (`embarch-core/design.md` §3.3) — umbrella's contribution is making sure it actually got run, with the right environment, on the right machine.

    *Refinement from implementing this (2026-08-05): `setup` does **not** edit `PATH`, despite this decision originally listing that as one of its jobs.* Decision 14's single release archive puts all three binaries in one directory, so umbrella finds `embarch-core` as a sibling of itself with no environment surgery at all. Editing a shell rc (which shell? which of the four startup files?) or the Windows registry is invasive, easy to get subtly wrong, and awkward to undo — for a benefit the sibling lookup already delivers. `setup` prints the one `export PATH=...` line and leaves the choice to the operator.

4. **`up`/`down` exist, but as a fallback, not the main path.** They cover: the service isn't installed (someone wants to try the stack before committing to a service install), the service died, or a foreground Core is wanted for debugging. `up` prefers starting the installed service and only spawns a foreground `embarch-core run` if there is no service to start (§3 decision 7) — a directly-spawned Core dies with the shell that started it, which is a confusing failure mode to hand someone as the default.

    *Refinement from implementing this (2026-08-05): the foreground fallback is **opt-in**, not automatic.* Distinguishing "no service installed" from "start failed for some other reason" means pattern-matching each backend's error text, which is exactly the per-OS fragility decision 4 exists to avoid. So a failed `up` prints the three real options — install it, elevate, or `embarch up --foreground` — and does nothing else. `--foreground` then runs Core in the caller's terminal (blocking, Ctrl-C to stop) rather than detaching, so nobody ends up with a Core that vanished when they closed a window. A `remote` topology refuses `up`/`down` outright rather than falling back to a local binary, which would start a second, wrong Core.

5. **Umbrella is deliberately *not* the process the MCP client spawns.** The tempting alternative — register `embarch mcp` as the MCP server so that starting Claude Code brings the whole stack up — was considered and rejected for v1. It puts umbrella permanently in the stdio hot path, makes every MCP-transport problem a two-binary debugging exercise, and buys little once decision 3 means Core is already running. `.mcp.json`/local MCP registration points straight at `embarch-api`, exactly as it does today.

6. **Topology is auto-detected by probing, not declared — and only the *class* is ever persisted, never an address.** Detection builds an ordered candidate list and races a short-timeout `GET /status` at each:
   - `http://127.0.0.1:4884` — covers Core-local (Mac, Linux, Windows-native) *and* WSL2 in mirrored-networking mode, where localhost already reaches the Windows host.
   - if running under WSL2 (`/proc/version` contains `microsoft`, or `WSL_DISTRO_NAME` is set) — `http://<default-gateway>:4884`, from `ip route show default`. This is the NAT-mode WSL2 path.
   - a user-supplied host, if one was given at `setup` or is recorded in config.

   First responder wins. **A `401` counts as a hit, not a miss**, and is reported distinctly: it means Core is there and the token doesn't match, which is a completely different fix from "Core isn't running." Connection-refused/timeout is a miss.

   *Two refinements from implementing this (2026-08-05).* **"Race" means ordered-sequential, not concurrent** — ordering is the whole point, and the common miss (nothing listening) is a connection refusal that returns immediately rather than burning the per-candidate budget, so a concurrent fan-out would buy nothing and lose the preference order. The 500ms budget is only ever paid where packets are silently dropped. And a **third outcome** turned out to be worth distinguishing: something that answers HTTP with neither `200` nor `401` isn't Core at all — most likely another service squatting the port — which is not a hit, but reporting it as "nothing there" would send someone to start a Core that can't bind anyway.

   *A subtlety this leaves open:* under WSL2 with mirrored networking, a Windows-hosted Core answers at loopback and is therefore classified `local`, indistinguishable by address from a Core running inside the WSL2 guest. Harmless for addressing — both are reachable the same way — but `up` must not infer "I can start Core here" from a `local` classification without also checking whether it's under WSL2 (decision 7's elevation path). Noted in §10. What gets written down is the resolved *class* — `local`, `wsl-host`, or `remote` (plus the host, for `remote` only) — never the WSL2 gateway IP, which is dynamic and has already gone stale once in this suite's own records (`embarch-core/design.md` §7 recorded `172.29.64.1`; `embarch-api`'s real `config.toml` had `172.22.128.1`). Per §3 decision 9 the address is re-resolved at every use instead.

7. **Starting Core across the WSL2⟷Windows boundary is supported, because it's the same physical machine — but umbrella never tries to elevate itself. Elevation is required on every OS, not just Windows.** WSL2 can invoke a Windows binary directly (`/mnt/c/.../embarch-core.exe`), so `up` from the WSL2 side is mechanically possible. Controlling a *system* service, however, needs elevation — and not only on Windows: a systemd system unit wants root or a polkit prompt too, confirmed on Linux where an unprivileged `embarch-core start` fails with "Interactive authentication required" (`embarch-core/design.md` §3.3, corrected 2026-08-05 — this decision originally treated elevation as a Windows-only tax). Umbrella does not attempt self-elevation, UAC prompting, `sudo`, or an elevated helper on any platform: when the operation needs privileges, it prints the exact command to run in an elevated shell and exits nonzero. This is acceptable precisely because decision 3 makes it rare — a one-time elevated `embarch setup`, then autostart forever. Locating the Windows-side binary: `EMBARCH_CORE_EXE` env var, else the path recorded at setup, else a bounded search of the conventional install location.

8. **A Core on a genuinely separate machine is detect-and-verify only.** No SSH, no remote install, no remote start. `doctor` reports it as reachable-or-not and tells the human to go start it there. Note that this topology also **cannot flash** today: `/flash` reads `firmware_path` from Core's own local disk and there is no shared filesystem to put an artifact on (`embarch-api/design.md` §9). `doctor` says so explicitly rather than letting someone discover it as a confusing flash failure. Closing that gap is out of scope here and stays `embarch-api`'s open item.

9. **`base_url = "auto"` is implemented in `embarch-api`, not in umbrella.** Umbrella could write a resolved URL into the config at setup time, but that just relocates the staleness problem — the WSL2 gateway IP changes on WSL restart, long after setup ran. So the config gets the literal string `auto` and `embarch-api` re-runs decision 6's candidate race itself, per process, at the point it first needs Core. Umbrella and the API therefore share one resolution algorithm; it belongs to the API because the API is the thing that has to be correct at 3pm on a Tuesday, not at install time. Full schema/behavior: `embarch-api/design.md` §4, §7.

10. **Per-firmware-repo project config lives in an `embarch/` subfolder of that repo, scaffolded by `embarch init`.** Running `embarch init` inside a firmware repo produces:

    ```
    <firmware-repo>/embarch/
    ├── embarch.toml     <- a complete embarch-api config: [core] + the [[projects]] for this repo only
    └── build/           <- the build directory this project's build_command targets, kept separate
                            from whatever the engineer's own interactive `west build` uses
    ```

    Three things follow from this shape:
    - **Scoped by construction.** An `embarch-api` started with this config sees only this repo's projects, so `list_projects` in a firmware repo can't offer up an unrelated board to flash.
    - **A separate build directory is the default, not an option.** Sharing one `build/` with the engineer's interactive builds means EmbArch and the human clobber each other's build tree (different board revisions, different pristine-vs-incremental state). `init` writes `--build-dir embarch/build` into the scaffolded `build_command` and points `artifact_path` at it.
    - **It is a complete config, not a fragment.** `[core]` gets duplicated into every repo, which is real duplication — accepted for v1 because `[core]` is now three lines (`base_url = "auto"` and timeouts) and because an include/fragment mechanism is new code in `embarch-api`'s config loader. Recorded as the deliberate v1 trade-off; the fragment version is §10's open item.

11. **`doctor` and `status` are split by cost, and both carry `--json`.** `status` is one Core `/status` call — cheap enough for a future UI (§10) or a shell prompt to poll. `doctor` is the full chain (§5), including filesystem checks and a build-command resolution, which is far too heavy to poll. The `--json` shape on both is the contract a future UI consumes; it exists in v1 specifically so the UI doesn't arrive and find only human-formatted text to scrape. Human-readable output is the default on both, matching `embarch-api`'s own CLI convention (`embarch-api/design.md` §5a).

12. **Local-only integration into a firmware repo touches nothing that is committed.** For a repo owned by someone else (a client's firmware repo), `init` must not dirty tracked files. Concretely: the `embarch/` folder is excluded via `.git/info/exclude`, **not** by editing the repo's committed `.gitignore`; and the MCP server is registered at Claude Code's local (per-project, per-user) scope rather than by writing a `.mcp.json` at the repo root. Both are reversible by `embarch init --uninstall` and invisible to anyone else cloning the repo. Committing the integration later is a deliberate follow-on step, not the default — see §7 for the options and their trade-offs.

13. **`init` derives what it can from the repo, *by looking rather than assuming*, and refuses to guess the rest.** For a Zephyr/west repo it reads `build/build_info.yml`'s recorded `west.command` when one exists, because that is the only reliable answer to the `build_cwd`-vs-positional-app-path question that has already silently broken this suite once (`embarch-api/design.md` §6, §12). What it will not guess is the probe-rs `chip` name — Zephyr's board identifier and probe-rs's target name are different namespaces with no mechanical mapping — so `init` writes a placeholder plus the exact `probe-rs chip list` invocation to resolve it, and `doctor` fails loudly while the placeholder is still there. Guessing a chip name would produce a config that flashes the wrong target rather than an error.

    *Extended while implementing (2026-08-05), same principle applied twice more:* `artifact_path` is resolved by **searching `build/` for a real `zephyr.hex`** (shortest match wins) rather than assuming a layout — sysbuild nests it under `build/<app>/zephyr/` and a plain build doesn't, and which applies depends on the SDK (`embarch-dev-bench/design.md` §3 decision 4's correction). And `artifact_path_for_core` is computed from `WSL_DISTRO_NAME` when under WSL2, since the UNC form is mechanically derivable from a path that is already known. A `-p always` found in the recorded command is *reported, not removed* — with a separate build directory the user may well still want it, so that's their call to make.

14. **Distribution: one suite release archive containing all three binaries, published from this repo.** `embarch-<version>-<target>.{tar.gz,zip}` contains `embarch`, `embarch-core`, and `embarch-api`, so the getting-started path is one download rather than three, and the three binaries in a user's hands are a version-tested set rather than an arbitrary combination. Targets: `x86_64-pc-windows-msvc`, `x86_64-unknown-linux-gnu`, `aarch64-apple-darwin`, and `aarch64-unknown-linux-gnu` (for a future Pi Core). Per-repo releases still exist for developers working on one component; the suite release is what the user guide points at. `doctor` warns when the installed component versions don't match the suite manifest. This is what [embarch-roadmap.md](../embarch-roadmap.md)'s existing "Release" concept becomes concretely.

15. **Topology detection is written once here, in a deliberately liftable shape — not extracted into a shared crate.** `embarch-api` needs the identical candidate-ordering and probe logic for `base_url = "auto"` (`embarch-api/design.md` §3.11, §7), so there are exactly two consumers and one algorithm. A fourth Rust crate in the suite, versioned and released, to hold one function that takes a candidate list and returns which one answered, is more machinery than the problem justifies at this scale. The alternative accepted instead: it lives in one self-contained module here, written under a constraint — **no umbrella-specific types cross its boundary**. No CLI structs, no umbrella config types, no `anyhow` context strings that only make sense in a `doctor` run; just pure functions over plain inputs (an "am I under WSL2" bool, a gateway-IP string, a port, an optional host) returning plain outputs. That constraint is what makes it copyable into `embarch-api` verbatim, and what makes extracting it into a real crate later a move rather than a rewrite, if a third consumer ever appears.

    The honest cost is drift: two copies that must agree, with nothing mechanical enforcing it. Three things keep that visible rather than silent — the module carries a comment naming its mirror and this decision, its unit tests are copied alongside it (they're pure-function tests, so they port with no adaptation), and `doctor`'s check 3 reports *which candidate won* rather than just pass/fail, so a divergence between what umbrella resolves and what `embarch-api` resolves surfaces as two different answers on the same machine instead of as a mystery.

## 4. Topology matrix

| # | Topology | Detected class | Core startable by umbrella? | Flash works? |
|---|---|---|---|---|
| i | macOS: Core + API both native | `local` | Yes (`launchd` service) | Yes |
| ii | Linux: Core + API both native | `local` | Yes (`systemd` service) | Yes |
| iii | Windows Core + WSL2 API (**today's primary**) | `wsl-host` (or `local` under mirrored networking) | Yes, but service start needs an elevated Windows shell (§3 decision 7) | Yes, via `artifact_path_for_core`'s UNC path (`embarch-api/design.md` §9) |
| iv | Windows: Core + API both native | `local` | Yes, elevation as above | Yes |
| v | Core on a separate box (Pi over wifi), API elsewhere | `remote` | **No** — human starts it there (§3 decision 8) | **No** — artifact-transfer gap, `embarch-api/design.md` §9 |

i/ii are mechanically the simplest and are expected to work first-try; iii is the one actually in daily use and therefore the one that gets validated for real; iv is supported by construction but untested; v is partial by design and says so.

## 5. What `doctor` checks

Ordered, each check emitting a pass/warn/fail plus a concrete fix line. Several of these are not new capabilities — they are existing open questions that finally have a natural home.

| # | Check | On failure |
|---|---|---|
| 1 | `embarch-core` and `embarch-api` binaries found; versions match the suite manifest (§3 decision 14) | Where to download / which is mismatched |
| 2 | Core service installed, and running | The exact `embarch-core install` / elevated start command |
| 3 | Core reachable — reports which candidate won and the resolved class (§3 decision 6) | Distinguishes "nothing answered" from "answered 401" |
| 4 | Token resolves and matches (a `200`, not a `401`) | Points at [embarch-token.md](../embarch-token.md); for `remote`, prints the copy-paste `EMBARCH_TOKEN` line (§6) |
| 5 | At least one debug probe visible in `/status`'s probe list | Warn, not fail — a probe can legitimately be unplugged |
| 6 | `embarch-api` config loads; every project's `source_path` exists | The config-load error verbatim |
| 7 | Each project's `build_command[0]` resolves to an executable | This is `embarch-api/design.md` §12's deferred PATH/toolchain preflight, landing here rather than in the build path |
| 8 | `chip` is not still `init`'s placeholder (§3 decision 13) | The `probe-rs chip list` invocation |
| 9 | `artifact_path` is resolvable, and if `artifact_path_for_core` is set, that it names *the same file* — comparable under WSL2 by stat-ing both paths | Catches exactly the mismatch that already cost this suite a debugging session (`embarch-api/design.md` §12) |
| 10 | MCP server registered for this repo | The `claude mcp add` line |
| 11 | `study_designer_schema_version` from `/status` agrees with `embarch-api`'s compiled constant | Version-drift warning (`embarch-study-designer/design.md` §3 decision 12) |
| 12 | Dev-bench port detected (`GET /dev-bench/port`) | Informational only — a `404` is "bench not plugged in," an expected state (`embarch-core/design.md` §4) |

Check 9 is only meaningful where both paths are visible to the same process, i.e. topology iii. Checks 5, 11, and 12 are informational and never fail the run.

## 6. Token handling

Umbrella does not invent any token mechanism — [embarch-token.md](../embarch-token.md) remains the source of truth. What it adds is making the existing mechanism actually happen at setup time:

- **Same-machine topologies (i–iv):** ensure Core has started at least once, so `token_store` has generated and persisted the machine-wide token file, then confirm `embarch-api` can discover it (including the WSL2⟷Windows `/mnt/c` translation `token_discovery.rs` already does). No token value is ever written into a config file.
- **Separate-machine (v):** there is no shared filesystem, and per [embarch-token.md](../embarch-token.md) §8 this is an unsolved gap. Umbrella's contribution is not to solve it but to make it a 10-second manual step: `doctor` prints the exact `export EMBARCH_TOKEN=...` / `setx` line to run on the API machine, with the value read from the Core machine by the human.

## 7. MCP registration options

`init` uses the local-scope registration of the first row (§3 decision 12). The rest are recorded because the question "how does this get committed for the whole team" is the obvious next one, and the answer isn't the same as the local one.

| Option | Shape | Pro | Con |
|---|---|---|---|
| **Local scope** (v1) | `claude mcp add` at per-project/per-user scope, pointing at `embarch-api --config <repo>/embarch/embarch.toml` | Touches nothing tracked; per-repo scoped; trivially reversible | Every engineer runs `embarch init` themselves |
| Committed `.mcp.json`, PATH + relative config | `{"command": "embarch-api", "args": ["--config", "embarch/embarch.toml"]}` | No absolute paths, portable, works for everyone who ran `embarch setup` | Requires `embarch-api` on `PATH`; every engineer still needs their own `embarch/` folder |
| Committed `.mcp.json`, env expansion | `{"command": "${EMBARCH_API_BIN}", "args": ["--config", "${EMBARCH_API_CONFIG}"]}` | Fully machine-independent | Two env vars to get wrong, with an opaque failure when unset |
| Committed wrapper script | `{"command": "./embarch/mcp.sh"}` | One indirection point; can preflight | A shell script doesn't work on native Windows; needs a `.cmd` twin |
| Umbrella as the MCP server | `{"command": "embarch", "args": ["mcp", ...]}` | Starting the agent starts the stack | Rejected — §3 decision 5 |
| Absolute paths | `{"command": "/home/me/.../embarch-api", ...}` | Works immediately | Broken for every other engineer; non-starter if committed |

If the integration is ever committed, row 2 is the recommendation, since `embarch setup` is already the thing that puts `embarch-api` on `PATH`.

## 8. Command surface

| Command | Scope | Behavior |
|---|---|---|
| `embarch setup` | once per machine | Detect topology (§3 decision 6), install Core as a service where possible, ensure the token file exists, put both binaries on `PATH`, record the class + Windows-side Core path, then run `doctor` |
| `embarch init` | once per firmware repo | Scaffold `embarch/embarch.toml` + `embarch/build/` (§3 decision 10, 13), exclude locally, register the MCP server (§3 decision 12), then run `doctor`. `--uninstall` reverses all of it |
| `embarch doctor` | anytime | §5's full chain. `--json` |
| `embarch status` | anytime, cheap | One `/status` call: is Core up, which class, how many probes. `--json` |
| `embarch up` / `embarch down` | fallback | Start/stop Core — installed service first, foreground `embarch-core run` only if no service exists (§3 decision 4, 7) |

Exit codes follow `embarch-api`'s CLI convention (`embarch-api/design.md` §5a): `0` on success, `1` on any failure with the message on stderr (or folded into the `--json` object on stdout when `--json` is set), `2` from `clap` for a malformed invocation.

## 9. Relationship to the rest of the suite

- **`embarch-core`:** umbrella shells out to its CLI (`install`, `uninstall`, and the `start`/`stop` pair proposed in `embarch-core/design.md` §10) and calls two of its HTTP endpoints (`/status`, `/dev-bench/port`). It adds no Core capability and holds no hardware knowledge.
- **`embarch-api`:** umbrella writes its config and shells out to its CLI for verification. The `base_url = "auto"` resolution lives there, not here (§3 decision 9). Umbrella never re-implements build orchestration.
- **`embarch-study-designer` / `embarch-dev-bench`:** umbrella's only involvement is two `doctor` checks (schema-version agreement, dev-bench port presence). It does not build, flash, or configure dev-bench firmware — that stays a human `west flash` (`embarch-dev-bench/design.md` §3 decision 13).
- **`embarch-promptu`:** out of scope. Umbrella registers the MCP server; it does not install skills or prompt patterns.

## 10. Open questions / future work

- **The EmbArch UI.** Explicitly out of v1 scope, and explicitly anticipated: a small local UI where an engineer can see whether Core is connected and drive `embarch-api`'s operations by hand, without asking an agent and without typing CLI subcommands. §3 decision 11's `--json` contract on `status`/`doctor` exists to be its data source. Unresolved: whether it's a native app, a local web page served by a new process, or a tray/menubar item; and whether it drives `embarch-api` by shelling out to the CLI or by embedding it.
- **A `local` classification under WSL2 is ambiguous about *where* Core is** (§3 decision 6's refinement note): with mirrored networking, a Windows-hosted Core and a WSL2-guest-hosted Core both answer at loopback. Addressing is unaffected, but `up` needs to disambiguate before deciding whether it can start Core itself or must print an elevated Windows command (decision 7). Detection already knows whether it's under WSL2; the open part is what `up` does with that. Not yet designed, and it can't be resolved from this machine — only NAT-mode WSL2 has ever been observed here.
- **Finding the probe-rs `chip` name currently requires installing a separate tool.** `init` deliberately won't guess it (§3 decision 13), so the user has to look it up — and the documented way is `cargo install probe-rs-tools && probe-rs chip list`, which means installing a Rust toolchain during what is otherwise a download-a-binary onboarding. That's a real wart, surfaced by writing [embarch-user-guide.md](../embarch-user-guide.md) §5.1 rather than by reviewing this design. The clean fix is Core-side: `embarch-core` already links `probe-rs` as a library, so it could expose the target list as a CLI subcommand (`embarch-core chip-list [filter]`) and umbrella could offer candidates directly during `init`. Recorded as a Core open item too (`embarch-core/design.md` §10); not yet scoped into Milestone 6.
- **Config fragments / includes**, so `[core]` isn't duplicated into every firmware repo's `embarch/embarch.toml` (§3 decision 10). Needs an `include` mechanism in `embarch-api`'s config loader; deferred rather than rejected.
- **Elevation is a hard edge on every platform** (§3 decision 7). `setup` needs an elevated shell once — Administrator on Windows, root/polkit for a systemd system unit — and umbrella deliberately won't self-elevate anywhere. Whether that's acceptable onboarding friction is a real question that only a second engineer walking the guide can answer. A user-level service (systemd `--user`, launchd LaunchAgent) would avoid it on Linux/macOS but wouldn't start before login, which defeats decision 3's whole point; not yet weighed properly.
- **Nothing here is validated.** No repo, no code — and every claim about topology detection (WSL2 mirrored-vs-NAT networking, the `401`-counts-as-a-hit probe, locating a Windows-side binary from WSL2) is reasoned rather than observed. Topology iii gets validated first because it's in daily use; i/ii/iv/v are reasoned only, and macOS specifically has no machine to test on yet.
- **Version-skew policy is a warning, not an enforcement** (§3 decision 14). Whether a mismatched `embarch-core`/`embarch-api` pair should refuse to run rather than warn is unresolved; warning first, since a hard refusal on a suite with no stable releases yet would mostly obstruct development.
- **Uninstall is only specified for `init`, not for `setup`.** `embarch init --uninstall` reverses a repo integration; there's no `embarch setup --uninstall` to reverse a machine setup (service, `PATH`, token file). Worth adding before anyone else's machine is involved.

## 11. Relationship to the user guide

[embarch-user-guide.md](../embarch-user-guide.md) is written against this design — i.e. against tooling that does not exist yet — with a clearly-marked appendix carrying the manual steps that work today. That is deliberate: the guide doubles as this milestone's acceptance criteria, and the gap between "what the guide says" and "what the appendix says you actually have to do" is exactly the work [embarch-umbrella/milestone-6.md](milestone-6.md) has to close.

## 12. Changelog

- 2026-08-05 — `init` implemented, closing everything in [milestone-6.md](milestone-6.md) §3.4 except `doctor`. Decision 13 extended in place: the look-don't-assume principle it stated for `build_command` now also covers `artifact_path` (found by searching for a real artifact, since sysbuild nests it and a plain build doesn't) and `artifact_path_for_core` (derived from `WSL_DISTRO_NAME`). Decision 12's no-tracked-files requirement verified end to end — `git status` unchanged after `init`, and `--uninstall` restores `.git/info/exclude` byte for byte.
- 2026-08-05 — `setup`, `up`, and `down` implemented ([milestone-6.md](milestone-6.md) §3.3 and half of §3.4). Two refinements folded into decisions 3 and 4 from doing it: `setup` does not edit `PATH` (the release archive's sibling layout makes it unnecessary, and editing shell rc files is invasive and hard to undo — it prints the line instead), and `up`'s foreground fallback is opt-in via `--foreground` rather than automatic, since telling "no service installed" apart from other failures means parsing per-backend error text. Also new: binary location follows decision 7's documented order in `locate.rs`, only the topology *class* is persisted (never an address, `state.rs`), and a `remote` topology refuses `up`/`down` instead of starting a second, wrong Core locally.
- 2026-08-05 — `embarch-core` gained the `start`/`stop` subcommands decision 4's `up`/`down` were waiting on ([milestone-6.md](milestone-6.md) §3.6 closed), removing that §10 open item. Smoke-testing them corrected decision 7, which had framed elevation as a Windows-only tax: a systemd *system* unit needs root/polkit just as a Windows Service needs Administrator, so `setup`'s one elevated step is universal rather than a Windows quirk. §10's elevation item reworded accordingly, and it now notes the user-level-service alternative that would avoid it at the cost of not starting before login.
- 2026-08-05 — Topology detection implemented ([milestone-6.md](milestone-6.md) §3.2 closed), along with enough of `status` to exercise it. Two refinements to decision 6 folded in from doing it: "race" is ordered-sequential rather than concurrent (ordering is the point, and the common miss returns instantly), and a third probe outcome distinguishes "something answered HTTP but isn't Core" from "nothing there." One new §10 open item: under WSL2 with mirrored networking a Windows-hosted Core classifies as `local`, which is fine for addressing but not enough for `up` to know whether it can start Core itself. Verified on this machine (WSL2 detected, gateway found and probed in order) and against a mock (401 → Core up, 404 → not Core, nothing → every attempt reported); 13 unit tests, all pure, written to port into `embarch-api` unchanged.
- 2026-08-05 — Resolved [milestone-6.md](milestone-6.md) §5's open question on where topology detection lives: new decision 15 — written once here in a liftable shape (no umbrella-specific types crossing its boundary, tests that port unchanged) and copied into `embarch-api`, rather than extracted into a fourth crate for one function. Records the drift cost this accepts and the three things that keep it visible, including `doctor` check 3 reporting which candidate won rather than just pass/fail.
- 2026-08-05 — Repo bootstrapped ([milestone-6.md](milestone-6.md) §3.1 closed): Cargo project producing the `embarch` binary per decision 2, `clap` deriving the full §8 command surface, plus `CLAUDE.md`/`LICENSE`/`README.md`/`.gitignore`. Every command parses and then reports itself unimplemented with a pointer to the milestone step that implements it — deliberately, so the surface can't be mistaken for working behavior. `cargo build` and `cargo clippy --all-targets -- -D warnings` both clean; `--help`, a `--json` invocation, and a malformed invocation were all exercised. Two conventions adopted from `embarch-api` rather than invented: exit codes `0`/`1`/`2` (`embarch-api/design.md` §5a) and `tracing` to stderr so stdout stays reserved for results and `--json` (§10 there). `probe-rs`/`serialport` are deliberately absent from `Cargo.toml`, with a comment recording that they're expected to *stay* absent per §1.
- 2026-08-05 — Repo created, empty: [gabrieltetar/embarch-umbrella](https://github.com/gabrieltetar/embarch-umbrella), public, no commits.
- 2026-08-05 — Initial draft. Scoped `embarch-umbrella` via Q&A: a sixth sub-project shipping one binary (`embarch`) that owns setup, verification, and fallback Core startup — deliberately not a supervisor, not in the runtime path, and not the process an MCP client spawns. Locked in: Core-as-an-autostarting-service is the real answer to "one button starts everything" (decision 3), so setup and verification are the actual problems; topology auto-detection by racing a `GET /status` at an ordered candidate list, persisting only the class and never an address (decision 6), with `401` treated as a hit; `base_url = "auto"` implemented in `embarch-api` rather than here (decision 9); per-firmware-repo config in an `embarch/` subfolder with a separate build directory (decision 10); local-only repo integration that never touches tracked files (decision 12); `init` deriving `build_command` from `build_info.yml` but refusing to guess the probe-rs `chip` name (decision 13); one suite release archive carrying all three binaries (decision 14). `doctor` (§5) becomes the home for two previously-deferred items: `embarch-api/design.md` §12's PATH/toolchain preflight, and detection of an `artifact_path`/`artifact_path_for_core` mismatch. A future EmbArch UI is out of scope but drives decision 11's `--json` contract.
