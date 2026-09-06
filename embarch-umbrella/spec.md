# embarch-umbrella: spec

**Status:** active, 2026-09-05.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md).

## What it is

The sub-project that gets a firmware engineer from *nothing installed* to *`embarch-api build_and_flash my-project` works, from a terminal or from an agent* — on whatever topology their machine happens to be. One binary, `embarch`, with three jobs: **set up**, **verify**, and **start Core when it isn't already running**.

It is its own sub-project because **it is the only component that knows about both `embarch-core` and `embarch-api`**, and `embarch-api` cannot hold it: **it cannot be the answer to "what do I download first" when it is one of the two things being set up.**

Not:

- **A process supervisor.** No restart loop, no health polling, no resident process. Core's own service install keeps it running.
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
```

Both of `embarch-api`'s front-ends stay first-class after setup, and **umbrella's job is to make the human one ergonomic too**, not just to wire up the agent path.

## Topology matrix

| Topology | Class | Core startable by umbrella? | Flash works? |
|---|---|---|---|
| macOS, both native | `local` | Yes (launchd) | Yes |
| Linux, both native | `local` | Yes (systemd) | Yes |
| **Windows Core + WSL2 API — today's primary** | `wsl-host`, or `local` under mirrored networking | Yes; the service start needs elevation | Yes, via the Windows-visible artifact path |
| Windows, both native | `local` | Yes, elevation as above | Yes |
| Core on a separate box | `remote` | **No** — a human starts it there | Yes, via multipart upload |

**Only the third is validated for real**, the one in daily use; the fourth is supported by construction but untested, and the fifth is partial by design and says so.

## Command surface

| Command | Scope | Behaviour |
|---|---|---|
| `embarch setup` | once per machine | Detect topology, install Core as a service, ensure the token file exists, copy all three binaries to the canonical per-user location and put it on `PATH`, record the class and the Windows-side Core path, then run `doctor`. `--uninstall` reverses it; **`--dry-run` runs every detection step and prints the plan — install, `PATH` write, service call, elevation — changing nothing** (decision 21); `--dev-bench-repo` records the checkout the staleness check compares against |
| `embarch init` | once per firmware repo | Scaffold the repo's `embarch/` config, exclude it locally, register the MCP server, then run `doctor`. `--uninstall` reverses all of it |
| `embarch doctor` | anytime | The full check chain. `--json`. **Nothing in it deletes anything** — `--prune` is unbuilt (decision 26) |
| `embarch status` | anytime, cheap | One status call: is Core up, which class, how many probes. `--json` |
| `embarch up` / `down` | fallback | Installed service first; foreground Core only with `--foreground` |
| `embarch deploy-core` | WSL2 → Windows service, during development | Sync, build natively, stop/copy/start under one elevation, **verify the binary changed**. `--dry-run`, `--print-script`, and overrides for every probed or saved path |

Exit codes follow `embarch-api`'s convention: `0` success, `1` failure with the message on stderr (or folded into the JSON object under `--json`), `2` a malformed invocation.

## The `doctor` chain

Ordered; each emits pass/warn/fail plus a concrete fix line.

| # | Check |
|---|---|
| 1 | Both binaries found; versions match the suite manifest. **A missing `embarch-core` is a warn where none belongs** (`wsl-host`, `remote`), and the Windows service's own registration is read to find one (decision 38) |
| 2 | Core service installed, and running |
| 3 | Core reachable — reports **which candidate won** and the resolved class |
| 4 | Token resolves and matches (a `200`, not a `401`) |
| 5 | At least one probe visible — a count off `/status`. Zero is a warn, **except on Linux with Core on this machine**, where a known debug-probe vendor ID in `/sys/bus/usb/devices` is **Fail — attached but not permitted**, with the udev fix line (decision 18) |
| 6 | `embarch-api` config loads; every project's source path exists |
| 7 | Each project's build entrypoint resolves to an executable — branching on discovery kind |
| 8 | Chip is not still the placeholder (static); at least one live target is file-backing-valid (zephyr-west) — counted by this crate's own approximating scanner, **not** `embarch-api`'s listing, which decision 17's amendment asked for and is unbuilt |
| 9 | Artifact paths name **the same file**; for zephyr-west, that the path translation itself succeeds |
| 10 | Registered **and answering**: it spawns the exact registered command and completes one JSON-RPC `initialize` over its stdio within 10 s. Answered, failed and timed out stay distinct in `--json` (decisions 23, 37); an entry whose command line it cannot read is a warn, never a pass |
| 11 | The study-designer schema versions: Core's served host version against the **located `embarch-api`**'s compiled one — shelled out for, and a warn naming why when it cannot be asked — plus **Core's own `compatible` verdict** on the wire version the flashed bench reports, and this binary's own constant as a mixed-install warn |
| 12 | Dev-bench port detected — informational; absent is an expected state |
| 13 | Dev-bench firmware version matches the local checkout's `git describe` |
| 14 | Which program Core would flash each chip family with, by running the located binary — on `wsl-host`, the service's own exe; unlocatable says what is missing (decision 38) |
| 15 | The running Core's `core_version` is the located `embarch-core` binary's — a **cross-version** stale deploy, and blind to a same-version one |
| 16 | `study_results/` entries and their bytes, and build directories per project — informational, never fails, **deletes nothing** (decision 26) |
| 17 | Core's bind address matches what the detected topology needs — **design-only** |
| 18 | Firewall state, best-effort, informational — **design-only** |
| 19 | Free disk space behind the build and results directories — **design-only** |
| 20 | Tail of Core's log file, informational — **design-only** ([embarch-core](../embarch-core/decisions/logging.md)'s daily-rolling log) |

Checks 12, 15 and 16 never fail the run outright; **5 and 11 do**, each only for the one state its row names — and check 11's failing is the point of it, since a host-version disagreement means no study can be submitted, and a bench Core refusing at the handshake means none can run. A number a check simply could not obtain is a warn naming which one, never a pass.

Numbers 1-16 are what the code emits and what `--json` carries — `n`, `name`, `status`, `detail`, `fix`, plus a `code` naming *which* outcome where a check has more states than statuses (decision 37; checks 1, 5, 10, 14). 17-20 are designed and unbuilt; their numbers move if something is built before them.

**Designed-and-unbuilt is not only a tail of the table**: decision 22, 26's `--prune` half and 17's amendment each sit *inside* a shipping command or check, marked above where it lives. [open.md](open.md) carries whether each is still wanted.

## Token handling

Umbrella invents no token mechanism — [embarch-token.md](../embarch-token.md) is the source of truth — and **writes no token value into any config file.** At setup time on a same-machine topology it ensures Core has started at least once, so the machine-wide token file exists, then confirms `embarch-api` can discover it. Across machines there is no shared filesystem and no solution: it prints the exact export line for a value the human reads off the Core machine.

Committing a repo integration for a whole team is a follow-on step `init` does not take; its shape is [decision 12](decisions/projects.md).
