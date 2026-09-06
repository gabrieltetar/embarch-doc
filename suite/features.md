# embarch: feature inventory

**Status:** active, 2026-09-02.

**What is built, how far it has been verified, and who owns it.** One row per capability, grouped by sub-project. **Assembled from [features.d/](../features.d/README.md), never edited here** — a hand-edit is reverted by the next `scripts/build_features.py`. Deliberately a *pointer*: the reasoning is in the owning decision, never restated here.

**Verified** is the column that matters, and it is not a synonym for Status. **unit** — mocked or synthetic tests only, no live process. **local** — a real running Core, repo or CI on this machine, but no physical probe or board. **hw** — validated against an actual probe, board, or a genuine OS service install. **n/a** — not shipped.

A `Status` of `Shipped` with a caveat spells the caveat out; a bare `Shipped` has none worth stating. Decision numbers cite the sub-project's own `decisions.md`.

## embarch-core

| Feature | Status | Verified | Decision |
|---|---|---|---|
| `GET /status` — connected probes, plus `study_designer_schema_version` and `core_version` (which Core build answered) | Shipped | unit, hw | §4, 13 |
| `POST /flash` — flash from a local path | Shipped | hw | §4 |
| `POST /reset` | Shipped | hw | §4 |
| `GET /serial-log` — bounded capture | Shipped | hw | §4 |
| `GET /dev-bench/port` — link auto-detection by vendor VID plus product/serial/interface, and its CLI | Shipped | hw | 21 |
| `POST /resolve-chip` — Zephyr SoC name → probe-rs target, validated against probe-rs's own registry | Shipped | local | 8 |
| `embarch-core chip-list` — enumerate the target database, no hardware needed | Shipped | local | 34 |
| Bearer-token auth on every endpoint | Shipped | hw | §4 |
| `hw_lock` — serializes all hardware access | Shipped | unit | 4 |
| Cross-platform service install and control | Shipped — **all four need elevation on every OS, not just Windows** | hw | 3 |
| `start`/`stop` CLI subcommands | Shipped — smoke-tested on Linux only | hw | 3 |
| Auto-generated machine-wide token file | Shipped | unit | §6 |
| Service environment token passthrough | Shipped | unit | 3 |
| Serial bridge to dev-bench (`/study*`, `/dev-bench/hello`) | Shipped | hw | 21 |
| Erase on flash | Shipped — **the brick hazard is closed: no backend maps it to a chip erase** | hw | 32, 36 |
| Flashing backend per chip family, preferring the board's own runner | Shipped | hw | 36 |
| Unframed-byte reporting — a reset banner on a shared console UART no longer reads as silence | Shipped | hw | 40 |
| Multi-probe selection beyond "first found" | Todo — design resolved (a serial selector), unbuilt | n/a | 9 |
| ESP-IDF bootloader flashing fallback | Todo — explicitly out of v1 scope | n/a | 18 |
| Per-caller identity beyond one shared token | Todo | n/a | §6 |

## embarch-api

| Feature | Status | Verified | Decision |
|---|---|---|---|
| `list_projects`, `status`, `build`, `flash`, `build_and_flash`, `reset`, `serial_log` — MCP tools | Shipped | hw | §5 |
| `list_targets` + `list-targets` — live target discovery (`zephyr-west`); a `static` project's one target (itself) | Shipped — the hand-authored `[[projects.targets]]` menu is **retired**, refused at config load, having never been selectable | local | 12, 53 |
| `discovery = "zephyr-west"` — per-call board/variant/revision/app resolution, file-backing-validated, replacing a hand-maintained static entry | Shipped | local | 12 |
| `[projects.default_target]` — a `zephyr-west` base selection a call narrows from, per field, so a repo growing a board does not start erroring unchanged calls | Shipped — documented as truth since it was decided, **built 2026-09-04**; refused at config load for a `static` project | unit | 20 |
| `snippets = ["none"]` — the reserved literal forcing zero snippets over a configured `default_snippets` | Shipped — documented as truth since it was decided, **built 2026-09-04**; a mixed list, or an app really declaring a `none` snippet, is refused naming the ambiguity | unit | 21 |
| CLI subcommands for every tool (kebab-case, unlike the snake_case tools) — **a superset, not a mirror**: `versions` has no MCP twin | Shipped | hw | §5a |
| `versions` — the compiled study-designer host type schema version, readable with no config and no live Core | Shipped; `doctor` check 11 reads it as of 2026-09-04 | unit | 52 |
| `run_study`/`study_status`/`study_*_data` — submit and read a study | Shipped — seals filled and capacity refused host-side before the HTTP call, the refusal naming field and limit | hw | §5 |
| `study-status --follow` / `study_watch` — live study events over SSE, `lagged` reported not raised, polling fallback | Shipped, never against a real Core | unit | 48, 49 |
| `validate`/`alerts` — topology validation and the alert log | Shipped | local | 35 |
| Artifact freshness check (mtime before and after) | Shipped | unit | §6 |
| `target.json` beside each `zephyr-west` build directory — the resolved selection, so a listing stays attributable past its `-args<hash>` segment | Shipped — documented as truth since it was decided, **built 2026-09-05**; absent means unattributable, never orphaned | unit | 19 |
| Per-project build concurrency lock | Shipped | n/a | §6 |
| Token discovery plus WSL2⟷Windows path translation | Shipped | local | 38 |
| `base_url = "auto"` — Core's address resolved per process at first use | Shipped — never against a real remote Core | local | §7 |
| `base_address` as a per-project field — a config-driven flash path | Shipped | unit | 44 |
| `[dev_bench]` board/chip/flash-format/artifact-path/base-address | Shipped | hw | 45 |
| Rolling **per-user** logfile, surfaced in the UI's Debug tab | Shipped | unit | 43 |
| Artifact transfer to a Core on a genuinely separate machine | Todo — design resolved (multipart upload), unbuilt | n/a | 15 |
| Config hot-reload | Todo | n/a | — |
| `PATH`/toolchain preflight | **Moved** — lands as an umbrella `doctor` check | n/a | §12 |
| The UNC artifact path | **Retired** — it only ever worked against a foreground Core, never the installed service | hw | §9 |
| `schema_version` on every `--json`/MCP object, stamped by one serializer | Shipped | unit | 24, 50 |
| `error_kind` — a machine-readable failure kind | **Retired** — never built; needs Core to serve error codes at all | n/a | 16, 50 |
| `soc_chip_overrides` — a per-project SoC→chip escape hatch, consulted before Core's `/resolve-chip` | **Retired unbuilt 2026-09-05** — the short-circuit would skip the registry validation that is Core's whole claim to the table, and the fact is per-silicon, not per-project; a config declaring the key now fails at load naming the retirement | unit | 13 |

## embarch-dev-bench

| Feature | Status | Verified | Decision |
|---|---|---|---|
| Shared firmware: COBS/postcard protocol, handshake, framed log lines | Shipped | hw | 6 |
| BLE bridge: advertise, connect either role, discover, monitor-all | Shipped | hw | 11 |
| Interrupt-driven inbound RX — **fixes a silent 128-byte ceiling that dropped every larger message** | Shipped | ztest | 36 |
| GATT capture window spanning steps | Shipped | hw | 30 |
| Central-side pairing callbacks — **without them an authenticated link is unreachable whatever a study asks** | Shipped | hw | 34 |
| Busy-means-wait on a security request already in flight | Shipped | hw | 37 |
| `CONFIG_LOG` forwarded to Core, per-study level, flushed before every level change | Shipped | hw | 38, 39 |
| Firmware on the nRF54L15DK, built, flashed and handshaking | Shipped | hw | 43 |
| Protocol interpreter for engineer-declared `.eap` files | Shipped | ztest, hw | 41 |
| End-of-study tap closing — **a whole-study tap's truncated flag was unfalsifiable** | Shipped | hw | 42 |
| `DataExchange` read-result observability | **Open question, not a diagnosed gap** | hw | §4 |
| Stimulus and sensing hardware-in-the-loop rig | Proposed | n/a | — |

## embarch-study-designer

| Feature | Status | Verified | Decision |
|---|---|---|---|
| Shared `no_std` study data types — a real dependency of Core, the API and the firmware | Shipped | unit, hw | §3 |
| Vendor-defined GATT catalog, resolving to real UUIDs end to end | Shipped | unit, hw | 41 |
| Authored step timing (`delay_before_ms`) | Shipped | hw | §4 |
| Connect to a named DUT by advertised-name scan | Shipped | hw | 43 |
| Free-text/raw GATT payload authoring alongside the registry | Shipped | unit | 35 |
| Per-characteristic GATT capture, decoded against an engineer-declared struct | Shipped | hw | 52-55 |
| Characteristics **and services** named, not numbered, in every picker | Shipped | hw | 56 |
| Static GATT extraction across the whole repo, scoped by the repo's own ignore rules | Shipped | unit, local | 57 |
| BLE security elevation as an authored step | Shipped | hw | 44 |
| Dropping the bond mid-study, with a bond scoped to one study | Shipped | local | 46 |
| Dev-bench link same-chip verification via the handshake's reported identity | Shipped | hw | 47 |
| **Engineer-declared DUT protocols** (`.eap`: types, grammar, validator, interpreter, three seals) | Shipped, runnable end to end | ztest, hw | 58-62 |
| One generic **inbound** stream pipeline (declared source, sink, scope, encoding) | Shipped | hw | 39 |
| Study version requirements, operator-selected reflash, provenance on a result | Shipped — **the UI half is deliberately not built** | hw | 40 |
| Declared GATT table on a study, reconciled against live discovery | **Design-only, no code** | n/a | 45 |
| Post-hoc validation | **Retired** — fully typed, wired into two repos, and it never once ran | n/a | 48 |
| The **outbound** half of the stream pipeline (send a string, confirm the reply) | Proposed — [proposal](../embarch-stream-pipeline-proposal.md) | n/a | — |
| Feature-matrix CI — every feature cell built on every push, the two narrow ones with `cargo build` so dev-dependency feature unification cannot hide a break; plus a guard that fails if a `release.yml` ever appears without `verify-version` | Shipped — all fourteen steps run green locally before landing; `ffi` type-checks the `extern "C"` surface but no staticlib cross-link exists to assert; the release guard was run against five shapes, none of them a real tag | local | 64, 65 |

## embarch-outpost

| Feature | Status | Verified | Decision |
|---|---|---|---|
| MCU load tracing on the DUT: tracing hooks, markers, GPIO dispatch, TX-only UART, build-ID-matched manifest | **Working end to end on real silicon**: 437,789 bytes in 20 s off a real nRF54L15, 43,948 records, zero lost | ztest, hw | §3 |
| **Two clocks** — the DUT stamps each record from its own counter, Core stamps each frame on arrival | Shipped (record layout 3) | hw | 4, 17 |
| Manifest generation from the linked ELF — ISR and thread names, including a shared-trampoline handler and DWARF-typed kernel objects | Shipped — 20 of 20 threads and 13 real ISRs on a real image | local | 7, 8 |
| Batch-fill framing — took the link's duty cycle from 99% to 37% | Shipped | hw | 20 |
| Every Kconfig wire constant | **Unmeasured defaults**, and the instrumentation's own overhead is deliberately uncharacterised | n/a | §5 |

## embarch-topology

| Feature | Status | Verified | Decision |
|---|---|---|---|
| One shared crate for software and hardware topology, called live in-process by three consumers | Shipped, merged, deployed | hw | 2, 3 |
| Enrollment storage — which board holds which role, human-declared | Shipped | hw | 14 |
| Enrolling by probe serial, so two visible boards need no isolating | Shipped | hw | 15 |
| Early powered-target check instead of a raw access-port error chain | Shipped | hw | 16 |
| Declared dev-bench link **serial**, distinct from its JTAG probe's | Shipped | hw | 17 |
| Declared dev-bench link **interface** — closes the two-VCOM-on-one-probe gap the DK bench exposed | Shipped | hw | 20 |
| A `role` is unique — moving one onto different silicon displaces the old row and says so | Shipped | hw | 20 |
| Nordic arm of the self-reported-identity comparison — **the gate had never once run against Nordic silicon** | Shipped | hw | 21 |
| DUT signal links and the dev-bench-bypass route | Shipped — declared, stored and resolved; **validation has no caller and no wire has been read** | unit, hw | 18 |
| Live push of a mismatch alert | **Retired** — the durable log plus a fixed UI link replaced it | local | 19 |

## embarch-umbrella

| Feature | Status | Verified | Decision |
|---|---|---|---|
| `embarch setup` — per-machine setup with topology auto-detection, a real install and real `PATH` | Shipped, `--dry-run` included (2026-09-04) — **the Windows registry half is type-checked, not run** | local | 3, 21, 28 |
| `embarch init` — scaffold a repo's config plus local MCP registration | Shipped | local | 10, 12 |
| `init`/`doctor` support for live target discovery | Shipped, **decision 17's amendment included as of 2026-09-05**: check 8 shells out to `embarch-api list-targets` and umbrella's own approximating scanner is deleted. The shell-out is unit-tested against injected output, **never yet run against a real `embarch-api`** — check 1 does not locate that binary on this machine | unit | 17 |
| Topology auto-detection (ordered loopback → WSL2 gateway → explicit host; `401` counts as finding Core) | Shipped | local | 6 |
| `embarch status` — where Core is, `--json` | Partial — reachability, address and class; no probe count | local | 11 |
| `embarch doctor` — the whole chain, `--json` | Shipped, seventeen checks. **What is still unbuilt no longer sits in the tail of the table**: 22(b) firewall and 22(c) disk space are retired unbuilt (2026-09-05), the log-tail row is designed and unbuilt, and `--prune` sits inside a shipping command, deferred rather than pending (decision 26) | local | §5, 18, 22, 26 |
| `doctor` check 1 — binaries found, **topology-aware**: on `wsl-host` it reads the Windows service's own `BINARY_PATH_NAME` to locate Core, and a missing local `embarch-core` is a warn where none belongs rather than a fail | Shipped — **the `sc.exe qc` read has never run inside `doctor` on the live machine**, where check 1 was the first line's false red; the owed live run settles it | unit | 38 |
| `doctor` check 5 — zero probes is a warn, except on Linux with Core local, where a known debug-probe vendor ID still in `/sys/bus/usb/devices` is **Fail — attached but not permitted**, with the udev fix line | Shipped — **never met a real permission-denied probe**: unit-tested against a synthetic sysfs tree, and the primary topology (Core on Windows) skips the scan by design | unit | 18, 37 |
| `doctor` check 10 — the MCP server is registered **and answers**: finds the registration in the agent CLI's own config by the binary it names, spawns it, one `initialize` over its stdio, 10 s; answered, failed and timed out stay distinct in `--json`'s `code` | Shipped — **the `claude mcp get` format it shipped parsing does not exist**, so until 2026-09-05 it could reach neither of its real verdicts (decision 40); the rebuild is unverified live | unit | 23, 37, 40 |
| `doctor` check 11 — schema skew: Core's served host version against the **located `embarch-api`**'s, via `embarch-api --json versions`; unaskable is a warn naming why, never a fall back to `embarch`'s own constant, which survives as a mixed-install warn | Shipped, never run against a live Core, a flashed bench or an installed `embarch-api` | unit | 33, 35, 36 |
| `doctor` check 13 — stale dev-bench firmware | Shipped | hw | 19 |
| `doctor` check 14 — flashing backend per chip family | Shipped — **reaches Core's binary on `wsl-host` at last** (decision 38), having skipped behind check 1 on the one live run; it invokes the exe under the WSL user's environment rather than the service account's, which is open | hw | 31, 38 |
| `doctor` check 15 — the running Core's `core_version` is the located build; catches a **cross-version** stale deploy only | Shipped, never run against a live Core | unit | 34 |
| `doctor` check 16 — `study_results/` entries and bytes **at the directory it names**, plus per-project build directories; informational, never fails | Shipped, and it **measures rather than deletes**: results retention is `embarch-core`'s `EMBARCH_STUDY_RESULTS_KEEP`, and build-dir `--prune` waits on something that can name a valid target. The resolved path reaches `--json` as `path`; **which directory it resolves on `wsl-host` is still unverified live** | unit | 26, 39 |
| `doctor` check 17 — Core's bind address against what this topology needs: the class `setup` recorded versus the address `/status` answered at, and versus the service's registered `--bind`, the only evidence that tells a narrow bind from a wide one | Shipped — turns "Core unreachable" into "Core bound where you cannot reach it". A loopback hit alone now warns `bind-unproven` instead of failing, and **no branch has met a real narrow-bound Core**: synthetic evidence only, this bench registering `--bind 0.0.0.0` | unit | 22 |
| `embarch up`/`down` — fallback start/stop, including across the WSL2 boundary | Shipped — never started a real Core | local | 4, 7, 30 |
| Suite release archive — three binaries, four targets | Shipped, real tags and a real assembled archive | local | 14 |
| Release CI asserts each repo's `Cargo.toml` version matches its pushed tag | Shipped in all four repos that release; the other four still have no release workflow. Proven by running the step, not by a tag | n/a | 27, 29 |
| `embarch deploy-core` — one-command deploy onto the live Windows service, **verifying the binary actually changed** | Shipped — **the verification compared a byte count and reported `landed` through a cancelled elevation** | hw | 32 |

## embarch-ui

| Feature | Status | Verified | Decision |
|---|---|---|---|
| One consolidated human-facing UI, six tabs, replacing three ad hoc surfaces | Shipped, live-validated against the deployed Core | local, hw | 1, 4 |
| Study Designer tab — editable step table, registration, discovery, run-and-watch | Shipped | local | 11 |
| Saved-study library in the firmware repo | Shipped | local | 14 |
| Opening a firmware repo from the tab, and creating a study in it | Shipped | local | 14 |
| Selective-monitor targets in a grouped dialog rather than a wall of inline checkboxes | Shipped | local | 17 |
| Post-hoc **Trace** view — lanes, gap bands as overlays, per-subject load repartition, a chart bounded by pixels not dataset, a projected study-step row | Shipped | local | 10 |
| Signal routing in the Topology tab — **the only human surface there is** | Shipped | hw | 10 |
| Debug tab — live log tail for Core and for `embarch-api` | Shipped | local | 7, 13 |
| Reflash selector in the run dialog | **Deliberately not built** — it is `embarch-api` orchestration | n/a | 11 |
| Windowed trace fetch — the Trace view asks the server for the window it draws, binned, rather than pulling a whole capture | Shipped — **the spans were the 13 MB, not part of it**: first paint is 12.7 KB + 30.5 KB and a window costs 1–6 ms. Pinned against the browser aggregation it replaces; driven against the real binary in headless Firefox, never against a live Core or a real DUT capture | local | 18 |
| A capture that opens with pre-reset records loses the prefix, not its microsecond axis — the Trace view drops the stale leading run and says how many went | Shipped — **never met a real prefix**: both signs covered by crafted fixtures, and the 18-record bridge-buffered case that motivates it has not been replayed through it | unit | 19 |

## Not yet a sub-project

| Feature | Status | Verified | Decision |
|---|---|---|---|
| Curated firmware-specific skills and prompt library (`embarch-promptu`) | Proposed | n/a | — |
| Agent-facing codebase structural analysis (`embarch-atlas`) | Proposed | n/a | — |
