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
- **A GUI.** That is [embarch-ui](../embarch-ui/spec.md). What umbrella owes it is a stable machine-readable status contract, which `--json` on `status` and `doctor` is: both carry `schema_version` (`JSON_SCHEMA_VERSION` in `src/main.rs`, bumped by hand when either shape changes; decision 11).

## Shape

```
        setup / init / doctor / status / up / down / deploy-core / verify-release / install-core
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

The command table (`setup`, `init`, `doctor`, `status`, `up`/`down`, `deploy-core`, `verify-release`, `install-core`) and the exit-code convention: [spec/commands.md](spec/commands.md).

## The `embarch` plugin marketplace

**What a release carries (EMB-190, 2026-11-17; written, not yet run on a tag).** `release.yml` signs each per-repo archive with cosign (3.0.4 or later) and uploads `<asset>.sigstore.json` beside it, from one `sign` job behind the `release` environment. A `suite-v<version>` tag runs `assemble-suite.yml`: it reads the component tags from `suite.toml`, verifies each component archive against its repo's `release.yml` identity, and publishes the four target archives, each target's manifest (`components`, `commits`, per-file `files` SHA-256) with its Sigstore bundle, and a build-provenance attestation per archive ([decision 14](decisions/install.md), [interfaces/verify-release.md](interfaces/verify-release.md)). The first signed suite release needs new signed component tags; cutting them is the owner's. `scripts/cut-release.py` cuts one, dry run by default: [interfaces/cut-release.md](interfaces/cut-release.md).

This repo also holds the suite's Claude Code plugin marketplace, named `embarch`: [spec/marketplace.md](spec/marketplace.md).

## The `doctor` chain

An ordered chain of eighteen checks; each emits pass/warn/fail plus a concrete fix line. A
nineteenth is designed and unbuilt — [interfaces/doctor-chain.md](interfaces/doctor-chain.md)
says so outright. That file also holds the full table: what each check does, which decision
governs it, and which never fail the run outright.

## Token handling

Umbrella invents no token mechanism — [embarch-token.md](../embarch-token.md) is the source of truth — and **writes no token value into any config file.** Of the two same-machine topologies, only `local` actually starts Core, so only there can a clean `setup` promise the machine-wide token file exists; on `wsl-host` — today's primary topology — `setup` prints the elevated command for a human to run and starts nothing itself, so it can finish with the token file still absent. Either way, its token step is a bare `Path::exists()` at the conventional path (`token_path_for`) — an existence check, not discovery. Confirming that `embarch-api` can actually read the token is the doctor chain's job: check 4 and `status` (decision 46) are the only real callers of token discovery, and `setup` is not among them. Across machines there is no shared filesystem and no solution: it prints the export line for a value the human reads off the Core machine.
