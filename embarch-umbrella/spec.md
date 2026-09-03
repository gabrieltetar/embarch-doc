# embarch-umbrella: spec

**Status:** active, 2026-09-03.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md).

## What it is

The sub-project that gets a firmware engineer from *nothing installed* to *`embarch-api build_and_flash my-project` works, from a terminal or from an agent* — on whatever topology their machine happens to be. One binary, `embarch`, with three jobs: **set up**, **verify**, and **start Core when it isn't already running**.

It exists as its own sub-project because **it is the only component that knows about both `embarch-core` and `embarch-api`, and it is the binary a person downloads when they have neither.** `embarch-api` cannot hold this: it would have to install Core's OS service and register MCP servers, and **it cannot be the answer to "what do I download first" when it is one of the two things being set up.**

It is **not**:

- **A process supervisor.** No restart loop, no health polling, no resident process. Core's own service install keeps Core running; `up` exists only for when that is not in place or has died.
- **In the runtime data path.** Nothing routes through it after setup. **If umbrella is deleted from a working machine, the stack keeps working.**
- **A hardware or build layer.** It never links `probe-rs` or `serialport` and never runs a build command. Every capability it appears to have is a shell-out to `embarch-core` or `embarch-api`, or an HTTP call to Core.
- **Multi-machine orchestration.** A Core on a separate box is started by a human on that box.
- **A GUI.** That is [embarch-ui](../embarch-ui/spec.md). What umbrella owes it is a stable machine-readable status contract, which `--json` on `status` and `doctor` is.

## Shape

```
        setup / init / doctor / status / up / down / deploy-core
                              |
                           embarch
                    /         |          \
   shells out to    |         |           |  HTTP+Bearer: GET /status,
   embarch-core CLI |         |           |  /dev-bench/port, /dev-bench/hello
   (install/start)  |         |           v
                    |         |      embarch-core
                    |         +-- shells out to embarch-api CLI, and
                    |             reads/writes its config
                    +-- writes <firmware-repo>/embarch/embarch.toml
                        and registers the MCP server (local scope)

after setup, the runtime path has no umbrella in it:
  agent --stdio--> embarch-api --HTTP+Bearer--> embarch-core --> hardware
  human --CLI----> embarch-api ----------------^
```

Both of `embarch-api`'s front-ends stay first-class after setup — an MCP client over stdio **and** a human running it directly. **Umbrella's job is to make the second one ergonomic too**, not just to wire up the agent path.

## Topology matrix

| Topology | Class | Core startable by umbrella? | Flash works? |
|---|---|---|---|
| macOS, both native | `local` | Yes (launchd) | Yes |
| Linux, both native | `local` | Yes (systemd) | Yes |
| **Windows Core + WSL2 API — today's primary** | `wsl-host`, or `local` under mirrored networking | Yes; the service start needs elevation | Yes, via the Windows-visible artifact path |
| Windows, both native | `local` | Yes, elevation as above | Yes |
| Core on a separate box | `remote` | **No** — a human starts it there | Yes, via multipart upload |

The first two are mechanically simplest and expected to work first try; **the third is the one actually in daily use and therefore the one that gets validated for real**; the fourth is supported by construction but untested; the fifth is partial by design and says so.

## Command surface

| Command | Scope | Behaviour |
|---|---|---|
| `embarch setup` | once per machine | Detect topology, install Core as a service, ensure the token file exists, copy all three binaries to the canonical per-user location and put it on `PATH`, record the class and the Windows-side Core path, then run `doctor`. `--uninstall` reverses it; `--dev-bench-repo` records the checkout the staleness check compares against. **`--dry-run` is designed and unbuilt** (decision 21) |
| `embarch init` | once per firmware repo | Scaffold the repo's `embarch/` config, exclude it locally, register the MCP server, then run `doctor`. `--uninstall` reverses all of it |
| `embarch doctor` | anytime | The full check chain. `--json`. **`--prune` is designed and unbuilt** (decision 26), and so is the unconditional half that reports result counts and build-directory combinations — nothing measures or cleans either today |
| `embarch status` | anytime, cheap | One status call: is Core up, which class, how many probes. `--json` |
| `embarch up` / `down` | fallback | Installed service first; foreground Core only with `--foreground` |
| `embarch deploy-core` | WSL2 → Windows service, during development | Sync, build natively, stop/copy/start under one elevation, **verify the binary changed**. `--dry-run`, `--print-script`, and overrides for every probed or saved path |

Exit codes follow `embarch-api`'s convention: `0` on success, `1` on failure with the message on stderr (or folded into the JSON object when `--json` is set), `2` for a malformed invocation.

## The `doctor` chain

Ordered; each check emits pass/warn/fail plus a concrete fix line.

| # | Check |
|---|---|
| 1 | Both binaries found; versions match the suite manifest |
| 2 | Core service installed, and running |
| 3 | Core reachable — reports **which candidate won** and the resolved class |
| 4 | Token resolves and matches (a `200`, not a `401`) |
| 5 | At least one probe visible — a count off `/status`, warn on zero. The Linux **"not permitted" versus "unplugged"** branch is **designed and unbuilt** (decision 18) |
| 6 | `embarch-api` config loads; every project's source path exists |
| 7 | Each project's build entrypoint resolves to an executable — branching on discovery kind |
| 8 | Chip is not still the placeholder (static); at least one live target is file-backing-valid (zephyr-west) |
| 9 | Artifact paths name **the same file**; for zephyr-west, that the path translation itself succeeds |
| 10 | The registration entry exists — one `claude mcp get`. **Spawning the registered command and completing a handshake is designed and unbuilt** (decision 23), so registered-but-broken still passes |
| 11 | The study-designer schema versions: Core's served host version against this binary's compiled one, plus **Core's own `compatible` verdict** on the wire version the flashed bench reports |
| 12 | Dev-bench port detected — informational; absent is an expected state |
| 13 | Dev-bench firmware version matches the local checkout's `git describe` |
| 14 | Which program Core would flash each chip family with |
| 15 | The running Core's `core_version` is the located `embarch-core` binary's — a **cross-version** stale deploy, and blind to a same-version one |
| 16 | Core's bind address matches what the detected topology needs — **design-only** |
| 17 | Firewall state, best-effort, informational — **design-only** |
| 18 | Disk space behind the build and results directories — **design-only** |
| 19 | Tail of Core's log file, informational — **design-only** (the file is [embarch-core](../embarch-core/decisions/logging.md)'s single daily-rolling log) |

Checks 12 and 15 never fail the run outright, and neither does check 5 — **every state check 5 can currently report is a pass or a warn**, because the branch that was to fail is one of the unbuilt ones. **Check 11 does fail**, and that is the point of it: a host-version disagreement means `embarch-api` will refuse to submit a study, and a bench Core refuses at the handshake means no study can run either. A number it simply could not obtain is a warn naming which one, never a pass.

Numbers 1-15 are what the code emits and what `--json` carries; 16-19 are designed and unbuilt, and their numbers move if something is built before them.

**Designed-and-unbuilt is not only a tail of the table.** Audited against the source on 2026-09-03: decisions 18 (check 5's not-permitted branch), 21 (`setup --dry-run`), 22 (checks 16-18), 23 (check 10's handshake) and 26 (`doctor --prune`) are all designed and unbuilt, and each of the first four sits *inside* a command or a check that otherwise ships — which is why the doc claimed them. Decision 17's amendment is a fifth: check 8 still counts zephyr-west targets with this crate's own scanner ([decisions/projects.md](decisions/projects.md)), not `embarch-api`'s listing.

## Token handling

Umbrella invents no token mechanism; [embarch-token.md](../embarch-token.md) is the source of truth. It makes the existing one happen at setup time: on a same-machine topology, ensure Core has started at least once so the machine-wide token file exists, then confirm `embarch-api` can discover it — **no token value is ever written into a config file.** On a separate machine there is no shared filesystem and this is an unsolved gap; **umbrella's contribution is not to solve it but to make it a ten-second manual step**, printing the exact export line with the value read from the Core machine by the human.

## Committing a repo integration

`init` uses per-project, per-user local-scope MCP registration. If the integration is ever committed for a whole team, **the recommendation is a checked-in registration naming `embarch-api` on `PATH` with a repo-relative config path** — no absolute paths, portable, and **`embarch setup` is already the thing that puts the binary on `PATH`.** Every other shape loses: env expansion is two variables to get wrong with an opaque failure when unset, a wrapper script needs a Windows twin, absolute paths are broken for every other engineer, and umbrella-as-the-MCP-server is refused outright (decision 5).
