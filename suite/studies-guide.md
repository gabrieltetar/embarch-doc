# EmbArch: studies, the dev bench, and DUT traces

**Status:** active, 2026-09-02. Continues [user-guide.md](user-guide.md), which gets EmbArch working in the first place.

## 1. Dev bench and studies

> **Partly usable.** The endpoints and CLI are implemented and have run against a real bench and a real DUT. **What is missing is hardware**: power-sampling hardware (deferred by decision), GPIO and analog stimulus, and any physical DUT connector. Read this as "how the parts that exist work"; the tutorial is the HIL guide's Study section, which §1 points at.

`embarch-dev-bench` is a second board — **a test fixture, not your DUT** — that plays your device's BLE counterpart on demand. **Instead of manually pairing with a phone to check whether your peripheral advertises correctly, you describe what should happen and the bench does it, reproducibly, every build.**

The unit of work is a **study** ([glossary](../embarch-glossary.md): it runs on this bench or on Core's own host runner), an ordered list of steps with pass/fail checks. A **step is never a power-sampling window**: that step kind was retired at wire schema v9 (`embarch-study-designer` decision 39), and a capture of any kind is authored as a declared **tap**, never as a step.

**The walkthrough is in the HIL guide, not here.** Writing a study, running it, reading its losses and publishing it are the Study section: `embarch-api guide hil study` ([hil-guide.md](hil-guide.md)), with a complete worked study (`embarch-api/tests/fixtures/ble_gatt_rate_study.json`) and the truncation, reflash and address rules, each stated there once. (A capture is truncated when retention rotation deleted an older segment or the bench reported dropping records.) Field by field: [embarch-study-designer/interfaces/types.md](../embarch-study-designer/interfaces/types.md). This guide keeps what that one leaves out: this bench's measured behaviour (§3 to §3b); DUT traces are [trace-guide.md](trace-guide.md).

Add `--raw` to a fetch for the byte-for-byte bytes instead of the rendered CSV, and use `--out` rather than piping when a capture is not text. **The older per-channel commands are gone** — `study-power-data`, `study-waveform-data` and `study-gatt-data` were retired 2026-09-11, because they could not report truncation and `study-stream-data` can.

## 2. Saying which firmware a study is for

What a study's `requires` and `--reflash` do, that EmbArch never runs `git checkout`, and what `--allow-version-mismatch` writes into the result are the HIL guide's Study section 2 (`embarch-api guide hil study`). Two things it leaves out: `--reflash` takes `none` (the default), `dev-bench`, `dut` or `both`; and `none` is the default because flashing is the destructive half, so a study that observes a board you flashed by hand does not overwrite it.

**One limit worth knowing: nothing can read a firmware version back off a DUT.** When EmbArch says a run flashed a particular version, it means **"this run built and flashed *this tree*, at this revision"**, derived by running `git describe` in your project. **The bench is different — it reports its own version over its link, so that one is a real measurement.**

**The UI can do all of this too, since 2026-09-18.** A study's Build card turns the same check-build-flash-reset sequence on per study, storing the board, app and snippets it wants rather than a build anybody produced once ([`embarch-ui` decision 38](../embarch-ui/decisions/firmware-build.md)). A study can also say **which outpost trace mode it needs**, and Core reads that off the DUT's own header frame before step 1 and refuses a run against firmware that is not in it — the one thing a DUT genuinely does report about itself.

Where it plugs in: your DUT keeps its own probe on Core, and **the bench connects to Core over a second, separate serial link** that Core auto-detects. **One bench, one DUT, one study at a time**; testing two DUTs means two independent Core-plus-bench pairs.

Flashing the bench itself goes through EmbArch like anything else: `build-and-flash-dev-bench`, then `reset-dev-bench` — **flashing halts the chip rather than starting it running** — or `--reflash dev-bench` to do it as part of a run.

## 3. Where a study's data lands, and the knobs that keep it off your disk

Core writes each run to `study_results/<study_id>/` under its own machine-wide data directory — the same place the token lives. Inside: the run's pass/fail result, and one file per capture the study declared, named after that capture.

**Captures are the one thing EmbArch writes that has no natural size limit** — a stream can run as long as the study does, and studies accumulate run after run. Two environment variables **on Core's process** control that, and they are **the first knobs you may actually need to turn**:

| Variable | Default | What it does |
|---|---|---|
| `EMBARCH_STREAM_MAX_BYTES` | 32 MiB | Cap per capture file. Past it the file rotates, **keeping the most recent data** — worst case a little under twice this per capture on disk. `0` means no cap. **When rotation actually drops data, the run's result says so rather than handing you a short capture that looks complete** |
| `EMBARCH_STUDY_RESULTS_KEEP` | 50 | How many past runs to keep, swept on each new study. `0` disables the sweep — **what you want if you are archiving results yourself** |

**Both defaults are reasoned rather than measured.** Raise the first if a real run is being truncated; raise or zero the second if you need history.

A third, rarer one is a DUT signal's line rate when Core reads it on its own serial port rather than through the bench, and **it belongs on the signal**: declare its `baud` ([trace guide](trace-guide.md) step 1). **`EMBARCH_SIGNAL_BAUD`** is only the fallback for a signal that declares none, default 1000000. **Either way it must match what the DUT transmits at, and nothing can check that for you: if they disagree, every frame fails its CRC and the capture looks exactly like a firmware bug.** On this bench that is `460800` — **the ceiling of the link rather than a preference**, since the USB-UART bridge refuses to open above 750000 and the SoC has no baud between 460800 and 921600, **so it is the only value both ends can produce.**

**On an installed Core these are not shell variables.** Core runs as a service, so it reads its environment from the service registration — on Windows, the service's own `Environment` value in the registry — **and the service must be restarted for a change to take.**

## 3a. A study that actually ran, and where the DUT half stops

**One study has been run end to end by the fleet against the real bench** [measured 2026-09-06, `dev-bench` probe `001057729826`, hardware ID `6fcddc36cb781b71`, both roles validated live first]. It is the two-step `BleAdvertise` self-test — **`embarch-api/tests/fixtures/self_test_study.json`** — submitted with `reflash` at its `none` default — **nothing was built and nothing was flashed** — and it passed 2 of 2 steps. Its provenance came back `dev_bench_source: ReportedByDevBench, dev_bench_version: 49958d34` against a `Declared` firmware version of `any`, which is §2's asymmetry showing up in a real result: the bench's version is a measurement and the DUT's is a claim.

**Read that for exactly what it is: the bench half works and the DUT was never involved.** No step in it connects, so none of this bench's DUT-side lore was exercised. A green study is **not** yet evidence that a study reaches a DUT here.

**Reaching a DUT means a `BleConnect` step, and it needs to be told which peripheral.** Its own design (study-designer decision 43) records that connecting to "whichever DUT shows up first" is not usable on a real bench: consecutive runs of one study reached visibly different peripherals, none of them the DUT, and every study then failed with "service not found on DUT" — true, and completely misleading. So a real study sets `target_address` or `target_name`; `embarch-api/tests/fixtures/ble_connect_worked_example.json` is the worked form, round-tripped by `embarch-api/tests/ble_connect_fixture.rs`.

**How to find out what to put there is the HIL guide's** (run a `BleConnect` whose `target_name` nothing has, and read the census). What it leaves out: a failed name match does not return a bare timeout, it reports what *was* on the air in the step's own `fail_reason`. That is the scan, which is why there is no separate scan action; a blank name means "no filter", so the nonsense name is the whole trick.

**Run against this bench** [measured 2026-09-06, one 20 s step], the failing step came back:

```
no name match; 3/3 named: '<name>', '<name>', '<name>',
```

Three named advertisers, and **not one of them attributable to the DUT**.

**The two counts are how many advertisers were on the air and how many of those advertised a name** (`embarch-dev-bench` decision 46). `3/3` above means the list is complete; `2/10` means eight advertisers exist that this line can never show you. Captures taken before that decision landed read `on air:` with no counts — and a list with no counts is a lower bound you cannot measure.

The census works and is a measurement, but **nothing links a BLE advertiser to an enrolled probe automatically** — enrolment identifies a board by hardware ID and debug probe, the census by advertised name, and no code relates them. **Since `embarch-dev-bench` decision 44 the log sink (not the 64-byte `fail_reason`) records an advertiser's Manufacturer Specific Data**, and for this bench's DUT family the client firmware's source claims those bytes end with the device ID Core reads over the debug probe. **Unconfirmed on air** — a convention read off source, `tasks/api/029` is the pending live test, and a DUT that sends no manufacturer data gets none of it. Deciding which advertiser is your DUT stays the operator's.

**Do not take the name from `CONFIG_BT_DEVICE_NAME`.** Decision 43 records, as a measured finding rather than a caution, that **the DUT's real advertised name turned out not to be its configured one at all.** The census is the authority; the Kconfig is a guess that has already been wrong here once.

**And read that `fail_reason` knowing it truncates.** It is capped at 64 bytes and the run above hit the cap exactly, ending mid-list on a trailing comma — **there is no marker saying so.** The `, ...` you may see appended is a different, rarer signal: it means the bench's own 256-entry census overflowed, not that the string was cut. **A trailing comma is the only tell, and a list that happens to end on a name boundary has none at all**, so treat a full-looking `fail_reason` as a lower bound on what was advertising.

**And it lists only advertisers that sent a *name*.** `scan_seen_names_summary()` in `ble_bridge_real.c` skips every nameless entry, however much of the 64 bytes is left; decision 46's `2/10 named` makes that absence visible, not filled. **Measured against this bench** [measured 2026-09-06, two 20 s censuses five minutes apart, `dev-bench` `6fcddc36cb781b71`]: **10 advertisers on the air both times, 2 of them named**; `fail_reason` read `no name match; on air: 'GABRIEL', 'pod-36e017c'` — nothing truncated, and **eight advertisers missing anyway**, four of them connectable.

**So a `fail_reason` census with no plausible DUT in it is not evidence that the DUT is off the air**: a nameless DUT cannot appear there, and `target_name` cannot reach it either. **The bench's log sink is the census** — `report_scan_seen()` writes one line per advertiser, with address, connectability and whether a name was advertised at all — and it is the only complete one. Read `dev-bench.log` in Core's log directory, not the step's `fail_reason`.

**A failed address-filtered connect writes that census too** (`embarch-dev-bench` decision 46, 2026-09-10); before it, `report_scan_seen()` ran only on the name-filtered path. **Firmware older than that decision logs none there** — no census in `dev-bench.log` after a failed address connect means an old build, not empty air.

## 3b. Connecting by address, and the two ways that goes wrong

**`target_address` reaches an advertiser that `target_name` cannot**, and it has now been exercised: a `BleConnect` at `C4:82:E1:42:B1:26 (public)` — connectable, **no name advertised**, therefore invisible to every `fail_reason` census — connected and its `GattDiscover` returned three services and eight characteristics [measured 2026-09-06, study `bd39085d9aa34162a1a555494642ae43`, both steps `Pass`]. So a nameless DUT is reachable; you just cannot find it by name.

**The byte order is the HIL guide's rule, and it has been checked on the air.** `C4:82:E1:42:B1:26` is `[196, 130, 225, 66, 177, 38]` with `kind: "Public"`, exactly as `bt_addr_le_to_str` prints it in the census log, verified by connecting with it, above. **It is written down in three places, and the type is one of them**: `embarch-study-designer/src/ids.rs` states it on `BleAddress` itself (both `BleAddressKind`s, never reversed in that crate); `embarch-study-designer/interfaces/types.md` states it in prose; and `ble_bridge_real.c`'s `to_bt_addr` reverses it for Zephyr with a comment saying so. A wrong guess still fails *silently* — the step simply never matches — which is why the type saying it matters (`embarch-dev-bench` decision 23).

**Whether an address off a census is durable depends on which kind it is, and "random" does not mean "rotating".** A BLE random address is one of three sub-types, told apart by the **top two bits of its most significant (leftmost, as printed) byte** — a Bluetooth Core Spec fact (Vol 6 Part B §1.3.2), not an inference about any DUT: `11` **static random**, which does not rotate at all; `01` **resolvable private**, which does; `00` **non-resolvable private**, which also does. A Zephyr peripheral with privacy off advertises a *static* random address — `embarch-dev-bench` decision 17 chose exactly that, reproducibility over privacy realism — **so `target_address` is perfectly durable for the ordinary DUT, and it is the leftmost nibble that tells you.**

**The two censuses above measure it** [measured 2026-09-06]. All four **public** addresses were identical across both. Of the six random ones in the first census, the three static (`C3:DD:…`, `E1:94:…`, `C1:93:…`, all `11`) were still there five minutes later; **the two that vanished were `74:92:DB:7F:0C:D8` (`01`, resolvable private) and `34:BA:69:68:4C:05` (`00`, non-resolvable)**, replaced by two new private ones. Four of six random addresses survived, three of them by construction.

**So the rule is decision 43's, and no broader than that**: an address remains the precise filter, and it is a *rotating private* address — not a random one — that cannot be authored ahead of time. A DUT that rotates inside a scan window is a measured fact about a particular DUT (`suite/roadmap.md`), not a property of the address type.

**And when it goes stale, the study names the step that ran out of time.** Connecting to `74:92:DB:7F:0C:D8` between those two censuses timed out at its 15 s step budget [measured 2026-09-06, study `dd340b2a36a39aeba94f4f15b4da61f0`]. A run like it now reports:

```
dev-bench stopped the study early: step 'connect' timed out
```

**That is Core's format string as of [`embarch-core` decision 45](../embarch-core/decisions/studies.md), not a second measurement** — the study id above predates the fix, and the Core that ran it said *"the StepResult saying which step failed did not arrive"* while its `events.json.partial` held `{"step_name":"connect","outcome":"TimedOut", …}`. That wording is now reached **only** when no step outcome was recorded at all, so on a Core with decision 45 it means what it says. Meet it on an older Core and read it as "a step timed out", then confirm against `events.json.partial` under that study's `study_results/` directory.

## 4. Wiring a DUT signal in, and reading the trace afterwards

**Moved to [trace-guide.md](trace-guide.md) on 2026-11-25, verbatim**: declaring a signal and its route, adding an outpost trace tap, and reading the timeline and its load repartition.

## 5. Recording an audio-rate analog signal

> **Partly built, nothing run on a board yet.** The firmware, Core, the live view and the export are written and tested without hardware. **Not yet measured on a board:** block rate and lost blocks, noise floor, VDD accuracy, link throughput, and the order your OS lists the bench's three USB ports in ([open list](../embarch-dev-bench/open/analog.md)). **An nRF52840 DK is the only board with the backend**; the nRF54L15 DK bench cannot sample.

One analog sensor (e.g. a microphone breakout) on a dev kit, no DUT: [dev-bench decisions 60 to 66](../embarch-dev-bench/decisions/analog.md), [spec](../embarch-dev-bench/spec/analog.md).

**1. Wire it.** Power the front end from the DK's VDD, **3.3 V** once the image has set REGOUT0 (it writes it at boot when unset, decision 65), and take its output to **A0 (P0.03)**. **The input range is 0 to VDD**: a signal centred on 0 V needs a bias or a coupling capacitor, or its negative half clips. **BUTTON2 is the marker**: each press and release is stamped into the recording.

**2. Enrol the bench.** Plug the DK's *nRF USB* port in. It shows up as one device, VID `0xEBAC`, with three serial ports: control, samples and SMP. **Core must record the control port's USB identity (VID, PID, serial, interface)**; the SEGGER ID detection matches does not apply. Core accepts it on `POST /dev-bench/link` as `control_port` ([core decision 124](../embarch-core/decisions/probes.md)); **`embarch-api` has no flag or tool field for it yet**: `dev-bench-link` takes only `--serial` and `--interface`. Core takes the samples port as the next one after it in interface order, and refuses the study, saying why, when it finds none ([core decision 126](../embarch-core/decisions/analog-capture.md)).

**3. Declare the study.** In the study's JSON ([study-designer](../embarch-study-designer/interfaces/analog.md)): an `AnalogInput { sample_hz, channel }` tap (one per study, whole-study), a `record_checks` entry with `AnalogBlocks { channels, samples_per_block }` naming it, and a `session`. **The Study Designer has no form for these yet.** `sample_hz` must be in about 7.8 to 200 kHz, and **the board runs the nearest rate its 16 MHz timer gives** (44100 asked runs at 44077): the header says so and Core records a `rate_mismatch` row ([decision 66](../embarch-dev-bench/decisions/analog.md)).

**The session** is a Start prompt, sampling, then a Done prompt, capped at **5 minutes**. It declares `run_fields` (free text, `required` or not, saved with the study), `max_duration_ms` and an `export_dir`. A session's recording is exempt from retention ([core decision 125](../embarch-core/decisions/streams.md)). **Nothing raises the Start and Done prompts at run time yet** (Core has no code for it at this commit), so do not rely on them.

**4. Read the live view.** Past 50,000 samples a series is drawn as columns, each from its lowest to highest value, so a short burst still shows. **A block that reached the ADC's top or bottom is drawn in the warning colour**: the input clipped, so lower the gain ([ui decision 105](../embarch-ui/decisions/live-series.md)).

**5. Export.** `embarch-api export-audio <study_id> --name <tap> --study-file <study.json> [--out-dir]` writes 16-bit mono WAV at the declared rate, **one file per gap-free segment**, each with cue points for the marker presses and an **Audacity label file** (`.txt`) beside it, and a `-gaps.csv` ([api decision 130](../embarch-api/decisions/audio-export.md)). It refuses a tap with no declared rate, several channels or no verified block, and says which.

**A gap** means a block never arrived: the bench counted it lost, or one failed its CRC and was refused. Core places each block by its index, never its arrival time, so a gap keeps its length, and `<tap>.events.csv` lists it (`gap`, `marker`, `marker_unplaced`, refusals). **A `rate_mismatch` row** says the board's header rate differs from the declared one. Core and the export use the declared rate, so a file asked at 44100 and run at 44077 plays about 0.05 % fast.
