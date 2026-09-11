# embarch-umbrella: spec

**Status:** active, 2026-09-05.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md).

## What it is

The sub-project that gets a firmware engineer from *nothing installed* to *`embarch-api build_and_flash my-project` works, from a terminal or from an agent* — on whatever topology their machine happens to be. One binary, `embarch`, with three jobs: **set up**, **verify**, and **start Core when it isn't already running**. Both of `embarch-api`'s front-ends stay first-class after setup, and **the human one is as much umbrella's job as the agent path**.

It is its own sub-project because **it is the only component that knows about both `embarch-core` and `embarch-api`**, and `embarch-api` cannot hold it: **it cannot be the answer to "what do I download first" when it is one of the two things being set up.**

Not:

- **A process supervisor.** No restart loop, no health polling, no resident process. Core's own service install keeps it running.
- **In the runtime data path.** Nothing routes through it after setup. **If umbrella is deleted from a working machine, the stack keeps working.**
- **A hardware or build layer, with two named exceptions.** It never links `probe-rs` or `serialport`; every other capability it appears to have is a shell-out to `embarch-core` or `embarch-api`, or an HTTP call to Core. **(1)** `doctor` check 5 reads world-readable `/sys/bus/usb/devices` in-process, no elevation, to see a probe an unprivileged enumeration can't ([18](decisions/doctor.md)); its nine vendor IDs are unmeasured (open.md). **It stays here rather than routing to Core because it is not the fact `embarch-topology` holds** — those three VIDs pick a *serial port* and include one chip with no debug capability at all, so there is nothing shared to route ([49](decisions/probe-vendors.md)). **(2)** `deploy-core` runs `cargo build` over `embarch-core`'s source ([32](decisions/deploy.md)).
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

An ordered chain of eighteen checks; each emits pass/warn/fail plus a concrete fix line. The
full table — what each check does, which decision governs it, and which never fail the run
outright — is [interfaces/doctor-chain.md](interfaces/doctor-chain.md).

## Token handling

Umbrella invents no token mechanism — [embarch-token.md](../embarch-token.md) is the source of truth — and **writes no token value into any config file.** On a same-machine topology `setup` starts Core once so the machine-wide token file exists, then confirms `embarch-api` can discover it. Across machines there is no shared filesystem and no solution: it prints the export line for a value the human reads off the Core machine.
