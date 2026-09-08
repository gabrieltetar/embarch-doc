# embarch-umbrella: spec

**Status:** active, 2026-09-05.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md).

## What it is

The sub-project that gets a firmware engineer from *nothing installed* to *`embarch-api build_and_flash my-project` works, from a terminal or from an agent* — on whatever topology their machine happens to be. One binary, `embarch`, with three jobs: **set up**, **verify**, and **start Core when it isn't already running**. Both of `embarch-api`'s front-ends stay first-class after setup, and **the human one is as much umbrella's job as the agent path**.

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
| `embarch init` | once per firmware repo | Scaffold the repo's `embarch/` config, exclude it locally, register the MCP server, then run `doctor`. **An inferred board is never written as fact, and several recorded builds are all named rather than one picked** (decision 41). `--uninstall` reverses all of it; committing the integration for a team is a follow-on step it does not take (decision 12) |
| `embarch doctor` | anytime | The full check chain. `--json`. **Nothing in it deletes anything** — `--prune` is unbuilt (decision 26) |
| `embarch status` | anytime, cheap | Is Core up, which class, how many probes — the latter needs a second, authenticated `GET /status`, and no-token/unauthorized/unreachable are reported as themselves, never as a probe count of `0` (decision 46). `--json` |
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
| 8 | Chip is not still the placeholder (static); at least one real target exists (zephyr-west) — by shelling out to the located `embarch-api`'s own listing (decision 17) |
| 9 | Artifact paths name **the same file**; for zephyr-west, that the path translation itself succeeds |
| 10 | Registered **and answering**: reads the registration out of the agent CLI's own config by the binary it names rather than only the key `embarch`, spawns it, and completes one JSON-RPC `initialize` over stdio within 10 s. An entry with nothing to spawn is a warn, never a pass (decisions 23, 37, 40) |
| 11 | The study-designer schema versions: Core's served host version against the **located `embarch-api`**'s compiled one, plus **Core's own `compatible` verdict** on the bench's wire version, plus this binary's own constant as a mixed-install warn. The `/dev-bench/hello` fetch behind that verdict, and behind check 13, gets its own 10 s budget rather than the 500 ms the reads get (decision 44) |
| 12 | Dev-bench port detected — informational; absent is an expected state |
| 13 | Dev-bench firmware version matches the local checkout's `git describe` — no checkout configured, and a reported id no longer in that checkout's history, are each their own fail rather than a warn or an ordinary mismatch (decision 47) |
| 14 | Which program Core would flash each chip family with, by running the located binary — on `wsl-host`, the service's own exe, **measured** (decision 38). Unlocatable is one skip worded per class, not a flashing verdict — each wording is reachable only before *that* class's own `setup` finishes (decision 31) |
| 15 | The running Core's `core_version` is the located `embarch-core` binary's — a **cross-version** stale deploy, and blind to a same-version one |
| 16 | `study_results/` entries and their bytes **at the directory it names**, and build directories per project — informational (decisions 26, 39) |
| 17 | Core's bind address matches what this topology needs — the class `setup` recorded, against the address `/status` was reached at and against the service's own registered `--bind` (decision 22) |
| 18 | Tail of Core's log file, informational — **design-only** ([embarch-core](../embarch-core/decisions/logging.md)'s daily-rolling log) |

Checks 12, 15 and 16 never fail the run outright; **5, 11, 13 and 17 do**, each only for the states its row names ([decisions/schema-skew.md](decisions/schema-skew.md) for why 11 is allowed to). A number a check simply could not obtain is a warn naming which one, never a pass.

**A row naming several arms says which have run, not only which were written.** `measured` above cites a live run (decision 38); prose alone, as check 14's per-class skip wording is, means reasoned but not observed — the convention this table now follows.

1-17 are what the code emits; **18 is designed and unbuilt, and it is not the only such item** — 26's `--prune` half sits *inside* a shipping command, marked above where it lives, and [open.md](open.md) carries whether it is still wanted. 18's number moves if something is built before it. `--json`'s per-check object — its fields, always present, and which carry a `code` (checks 1, 5, 10, 13, 14, 17) or a `path` (check 16) — is [decisions/reporting.md](decisions/reporting.md)'s contract.

Every `detail` and `fix` is **one line with no run of two or more spaces**; another program's raw output is normalised at the point it is interpolated, not exempted from the rule ([decision 43](decisions/message-rendering.md)).

## Token handling

Umbrella invents no token mechanism — [embarch-token.md](../embarch-token.md) is the source of truth — and **writes no token value into any config file.** On a same-machine topology `setup` starts Core once so the machine-wide token file exists, then confirms `embarch-api` can discover it. Across machines there is no shared filesystem and no solution: it prints the export line for a value the human reads off the Core machine.
