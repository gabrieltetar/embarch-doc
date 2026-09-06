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
| `embarch setup` | once per machine | Detect topology, install Core as a service, ensure the token file exists, copy all three binaries to the canonical per-user location and put it on `PATH`, record the class and the Windows-side Core path, then run `doctor`. `--uninstall` reverses it; **`--dry-run` prints the whole plan and changes nothing** (decision 21); `--dev-bench-repo` records the checkout check 13 compares against |
| `embarch init` | once per firmware repo | Scaffold the repo's `embarch/` config, exclude it locally, register the MCP server, then run `doctor`. **An inferred board is never written as fact, and several recorded builds are all named rather than one picked** (decision 41). `--uninstall` reverses all of it |
| `embarch doctor` | anytime | The full check chain. `--json`. **Nothing in it deletes anything** — `--prune` is unbuilt (decision 26) |
| `embarch status` | anytime, cheap | One status call: is Core up, which class, how many probes. `--json` |
| `embarch up` / `down` | fallback | Installed service first; foreground Core only with `--foreground` |
| `embarch deploy-core` | WSL2 → Windows service, during development | Sync, build natively, stop/copy/start under one elevation, **verify the binary changed**. `--dry-run`, `--print-script`, and overrides for every probed or saved path |

Exit codes follow `embarch-api`'s convention: `0` success, `1` failure with the message on stderr (or folded into the JSON object under `--json`), `2` a malformed invocation.

## The `doctor` chain

Ordered; each emits pass/warn/fail plus a concrete fix line.

| # | Check |
|---|---|
| 1 | Both binaries found; versions match the suite manifest. **A missing `embarch-core` is a warn where none belongs** (`wsl-host`, `remote`). Each binary is found by a **reading** where one exists, never `PATH` alone (decisions 38, 42) |
| 2 | Core service installed, and running |
| 3 | Core reachable — reports **which candidate won** and the resolved class |
| 4 | Token resolves and matches (a `200`, not a `401`) |
| 5 | At least one probe visible — a count off `/status`. Zero is a warn, **except on Linux with Core on this machine**, where a known debug-probe vendor ID in `/sys/bus/usb/devices` is **Fail — attached but not permitted**, with the udev fix line (decision 18) |
| 6 | `embarch-api` config loads; every project's source path exists |
| 7 | Each project's build entrypoint resolves to an executable — branching on discovery kind |
| 8 | Chip is not still the placeholder (static); at least one real target exists (zephyr-west) — by shelling out to the located `embarch-api`'s own listing, **warn naming why** where it cannot be asked (decision 17) |
| 9 | Artifact paths name **the same file**; for zephyr-west, that the path translation itself succeeds |
| 10 | Registered **and answering**: it reads the registration out of the agent CLI's own config, by the binary it names rather than only the key `embarch`, spawns it and completes one JSON-RPC `initialize` over its stdio within 10 s. Answered, failed and timed out stay distinct in `--json` (decisions 23, 37, 40); an entry with nothing to spawn is a warn, never a pass |
| 11 | The study-designer schema versions: Core's served host version against the **located `embarch-api`**'s compiled one — shelled out for, and a warn naming why when it cannot be asked — plus **Core's own `compatible` verdict** on the wire version the flashed bench reports, and this binary's own constant as a mixed-install warn |
| 12 | Dev-bench port detected — informational; absent is an expected state |
| 13 | Dev-bench firmware version matches the local checkout's `git describe` |
| 14 | Which program Core would flash each chip family with, by running the located binary — on `wsl-host`, the service's own exe; unlocatable says what is missing (decision 38) |
| 15 | The running Core's `core_version` is the located `embarch-core` binary's — a **cross-version** stale deploy, and blind to a same-version one |
| 16 | `study_results/` entries and their bytes **at the directory it names**, and build directories per project — informational (decisions 26, 39) |
| 17 | Core's bind address matches what this topology needs — the class `setup` recorded against the address `/status` was reached at, and against the service's own registered `--bind`, which is the only evidence that tells a narrow bind from a wide one (decision 22) |
| 18 | Tail of Core's log file, informational — **design-only** ([embarch-core](../embarch-core/decisions/logging.md)'s daily-rolling log) |

Checks 12, 15 and 16 never fail the run outright; **5, 11 and 17 do**, each only for the states its row names ([decisions/schema-skew.md](decisions/schema-skew.md) for why 11 is allowed to). A number a check simply could not obtain is a warn naming which one, never a pass.

Numbers 1-17 are what the code emits and what `--json` carries — `n`, `name`, `status`, `detail`, `fix`, a `code` where a check has more states than statuses (checks 1, 5, 10, 14, 17), and a `path` where it resolved a directory (check 16) — both `null` elsewhere, never absent ([decisions/reporting.md](decisions/reporting.md)). 18 is designed and unbuilt; its number moves if something is built before it.

**Designed-and-unbuilt is not only the tail of the table**: 26's `--prune` half sits *inside* a shipping command, marked above where it lives. [open.md](open.md) carries whether it is still wanted.

## Token handling

Umbrella invents no token mechanism — [embarch-token.md](../embarch-token.md) is the source of truth — and **writes no token value into any config file.** On a same-machine topology `setup` starts Core once so the machine-wide token file exists, then confirms `embarch-api` can discover it. Across machines there is no shared filesystem and no solution: it prints the export line for a value the human reads off the Core machine.

Committing a repo integration for a whole team is a follow-on step `init` does not take; its shape is [decision 12](decisions/integration.md).
