# EmbArch: studies, the dev bench, and DUT traces

**Status:** active, 2026-09-02. Continues [user-guide.md](user-guide.md), which gets EmbArch working in the first place.

## 1. Dev bench and studies

> **Partly usable.** The endpoints and CLI are implemented and have run against a real bench and a real DUT. **What is missing is hardware**: power-sampling hardware (deferred by decision), GPIO and analog stimulus, and any physical DUT connector. Read this as "how the parts that exist work", not a tutorial you can follow end to end.

`embarch-dev-bench` is a second board — **a test fixture, not your DUT** — that plays your device's BLE counterpart on demand. **Instead of manually pairing with a phone to check whether your peripheral advertises correctly, you describe what should happen and the bench does it, reproducibly, every build.**

The unit of work is a **study**: an ordered list of steps, each a BLE action or a power-sampling window, with pass/fail checks.

```sh
embarch-api run-study --study-file my-study.json     # returns a study_id
embarch-api study-status <study_id>                  # pending | running | completed | failed
embarch-api list-study-streams <study_id>            # what it captured, and whether anything was lost
embarch-api study-stream-data <study_id> --name power --out power.csv
```

**Read `list-study-streams` before you read a capture.** It lists every capture the study declared, how many bytes each wrote, and — **the column that matters** — whether it was **truncated**. A truncated capture is a short one: either retention rotation deleted an older segment, or the bench reported dropping records. **Nothing else in the suite will tell you, and a short capture read as a complete one is the failure this whole area is built to prevent.** A capture listed with 0 bytes was declared and produced nothing, **which is a different problem from one that was never declared.**

Add `--raw` to a fetch for the byte-for-byte bytes instead of the rendered CSV, and use `--out` rather than piping when a capture is not text. The older per-channel commands still work for one release and **cannot report truncation.**

## 2. Saying which firmware a study is for

A study declares the bench and DUT builds it is meant to run against, and **`"any"` is a legal, explicit answer for either.** Core checks the bench's declaration against what the bench actually reports and **refuses the study before any step runs** if they disagree, naming both strings.

`--reflash` says what to do about a disagreement:

```sh
embarch-api run-study --study-file my-study.json --reflash dev-bench
embarch-api run-study --study-file my-study.json --reflash dut --project my-firmware
```

`none`, the default, means **"run against what is already on the boards"** — flashing is the destructive half, and **a study that just observes a board you flashed by hand should not quietly overwrite it.** The others rebuild and reflash **from your working tree exactly as it stands right now.**

**EmbArch will not run `git checkout` for you, ever.** If your tree is not at the revision the study asks for, **the run fails, names both revisions, and stops before touching the board. Moving your tree is your call, not a test harness's.**

`--allow-version-mismatch` runs anyway, **and the override is written into the result** naming what was required and what actually ran — **so a result that was waved through never looks like one that met its requirements.**

**One limit worth knowing: nothing can read a firmware version back off a DUT.** When EmbArch says a run flashed a particular version, it means **"this run built and flashed *this tree*, at this revision"**, derived by running `git describe` in your project. **The bench is different — it reports its own version over its link, so that one is a real measurement.**

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

A third, rarer one: **`EMBARCH_SIGNAL_BAUD`** sets the line rate when Core reads a DUT signal on its own serial port rather than through the bench. **It has to match what the DUT actually transmits at, and nothing can check that for you: if they disagree, every frame fails its CRC and the capture looks exactly like a firmware bug.** Its real value on this bench is `460800` — **which is the ceiling of the link rather than a preference**, since the USB-UART bridge refuses to open above 750000 and the SoC has no baud between 460800 and 921600, **so it is the only value both ends can produce.** Note what that costs: **1000000 is this variable's own default**, so a link that could run at 1 Mbaud would need no setting at all, and one that cannot **leaves you keeping two numbers in step by hand** — this variable and the DUT's own configured speed.

**On an installed Core these are not shell variables.** Core runs as a service, so it reads its environment from the service registration — on Windows, the service's own `Environment` value in the registry — **and the service must be restarted for a change to take.**

## 3a. A study that actually ran, and where the DUT half stops

**One study has been run end to end by the fleet against the real bench** [measured 2026-09-06, `dev-bench` probe `001057729826`, hardware ID `6fcddc36cb781b71`, both roles validated live first]. It is the two-step `BleAdvertise` self-test, submitted with `reflash` at its `none` default — **nothing was built and nothing was flashed** — and it passed 2 of 2 steps. Its provenance came back `dev_bench_source: ReportedByDevBench, dev_bench_version: 49958d34` against a `Declared` firmware version of `any`, which is §2's asymmetry showing up in a real result: the bench's version is a measurement and the DUT's is a claim.

**Read that for exactly what it is: the bench half works and the DUT was never involved.** No step in it connects, so none of this bench's DUT-side lore was exercised — not `ble speed fast`, not `meas_sched stop` before `hrm_start`, not `CONFIG_LOG` off. A green study is **not** yet evidence that a study reaches a DUT here.

**Reaching a DUT means a `BleConnect` step, and it needs to be told which peripheral.** Its own design (study-designer decision 43) records that connecting to "whichever DUT shows up first" is not usable on a real bench: consecutive runs of one study reached visibly different peripherals, none of them the DUT, and every study then failed with "service not found on DUT" — true, and completely misleading. So a real study sets `target_address` or `target_name`.

**How to find out what to put there: run a `BleConnect` whose `target_name` no device could have.** A failed name match does not return a bare timeout — the bench reports what *was* on the air, in the step's own `fail_reason`. That is the scan, and it is why there is no separate scan action. A blank name means "no filter", so the nonsense name is the whole trick.

**Run against this bench** [measured 2026-09-06, one 20 s step], the failing step came back:

```
no name match; 3/3 named: '<name>', '<name>', '<name>',
```

**The two counts are how many advertisers were on the air and how many of those advertised a name** (`embarch-dev-bench` decision 46). `3/3` above means the list is complete; `2/10` means eight advertisers exist that this line can never show you. Captures taken before that decision landed read `on air:` with no counts — and a list with no counts is a lower bound you cannot measure.

three named advertisers and **not one of them attributable to the DUT**. Two things that reads on, and they are different facts: the census works and is a measurement, and **nothing here links a BLE advertiser to an enrolled probe automatically** — enrolment identifies a board by hardware ID and debug probe, the census identifies it by advertised name, and no code relates them. **As of `embarch-dev-bench` decision 44 the census can at least carry a byte string worth comparing by hand**: the per-advertiser log sink (not the 64-byte `fail_reason`) now records an advertiser's Manufacturer Specific Data element when it sent one, and for this bench's DUT family the client firmware's own source claims those payload bytes are the tail of the same device ID Core reads over the debug probe. **Read that as unconfirmed on air** — it is a client-firmware convention read off source, `tasks/api/029` is the pending live test, and a DUT that sends no manufacturer data gets none of it. Deciding which advertiser is your DUT is still the operator's, not the bench's.

**Do not take the name from `CONFIG_BT_DEVICE_NAME`.** Decision 43 records, as a measured finding rather than a caution, that **the DUT's real advertised name turned out not to be its configured one at all.** The census is the authority; the Kconfig is a guess that has already been wrong here once.

**And read that `fail_reason` knowing it truncates.** It is capped at 64 bytes and the run above hit the cap exactly, ending mid-list on a trailing comma — **there is no marker saying so.** The `, ...` you may see appended is a different, rarer signal: it means the bench's own 256-entry census overflowed, not that the string was cut. **A trailing comma is the only tell, and a list that happens to end on a name boundary has none at all**, so treat a full-looking `fail_reason` as a lower bound on what was advertising. The complete per-advertiser record — address, connectable or not, name — goes to the bench's log sink, not into the study result.

**Read it knowing something larger than truncation, too: `fail_reason` lists only the advertisers that advertised a *name* — but it now tells you how many it is leaving out.** `scan_seen_names_summary()` in `ble_bridge_real.c` skips every entry whose name is empty, so a device advertising no local name is absent from that list whether or not the 64 bytes ran out. That gate is unchanged; what changed with `embarch-dev-bench` decision 46 is that the line says `2/10 named` rather than nothing, so the absence is visible instead of silent. **Measured against this bench** [measured 2026-09-06, two 20 s censuses five minutes apart, `dev-bench` `6fcddc36cb781b71`]: **10 advertisers on the air both times, 2 of them named.** The `fail_reason` said `no name match; on air: 'GABRIEL', 'pod-36e017c'` — well under 64 bytes, nothing truncated, and **eight advertisers missing from it anyway**, four of them connectable.

**That changes what "not one of them attributable to the DUT" is allowed to mean.** A DUT that advertises without a local name cannot appear in `fail_reason`, and `target_name` cannot reach it either — the name filter has nothing to match. So a `fail_reason` census with no plausible DUT in it is **not** evidence that the DUT is off the air; it is equally consistent with a nameless DUT. **The bench's log sink is the census** — `report_scan_seen()` writes one line per advertiser, with address, connectability and whether a name was advertised at all — and it is the only complete one. Read `dev-bench.log` in Core's log directory, not the step's `fail_reason`.

**That second gate is gone** (`embarch-dev-bench` decision 46, 2026-09-10). `report_scan_seen()` used to sit inside the `if (scan_name[0] != '\0')` branch of the connect timeout, so a `BleConnect` filtered by **address alone** that found nothing logged no census at all and you had to ask for one with a nonsense *name*. It now runs on **both** filter paths: a failed address-filtered connect writes the full per-advertiser census too. **Firmware older than that decision still has the gate** — if `dev-bench.log` holds no census after a failed address connect, that is which build is flashed, not an empty air.

## 3b. Connecting by address, and the two ways that goes wrong

**`target_address` reaches an advertiser that `target_name` cannot**, and it has now been exercised: a `BleConnect` at `C4:82:E1:42:B1:26 (public)` — connectable, **no name advertised**, therefore invisible to every `fail_reason` census — connected and its `GattDiscover` returned three services and eight characteristics [measured 2026-09-06, study `bd39085d9aa34162a1a555494642ae43`, both steps `Pass`]. So a nameless DUT is reachable; you just cannot find it by name.

**The bytes go in display order, most significant first.** `C4:82:E1:42:B1:26` is `[196, 130, 225, 66, 177, 38]` with `kind: "Public"`, exactly as `bt_addr_le_to_str` prints it in the census log — verified by connecting with it, above. **It is written down in three places now, and the type is one of them**: `embarch-study-designer/src/ids.rs` states it on `BleAddress` itself as of 2026-09-06 — display order, most significant first, the same for both `BleAddressKind`s, and nothing in that crate reverses it; `embarch-study-designer/interfaces/types.md` states it in prose; and `ble_bridge_real.c`'s `to_bt_addr` reverses it for Zephyr with a comment saying so. A wrong guess still fails *silently* — the step simply never matches — which is why the type saying it matters. **`embarch-dev-bench` decision 23 claimed the crate already said it, and it did not**; `tasks/dev-bench/009` amends that decision.

**Whether an address off a census is durable depends on which kind it is, and "random" does not mean "rotating".** A BLE random address is one of three sub-types, told apart by the **top two bits of its most significant (leftmost, as printed) byte** — a Bluetooth Core Spec fact (Vol 6 Part B §1.3.2), not an inference about any DUT: `11` **static random**, which does not rotate at all; `01` **resolvable private**, which does; `00` **non-resolvable private**, which also does. A Zephyr peripheral with privacy off advertises a *static* random address — `embarch-dev-bench` decision 17 chose exactly that, reproducibility over privacy realism — **so `target_address` is perfectly durable for the ordinary DUT, and it is the leftmost nibble that tells you.**

**The two censuses above measure it** [measured 2026-09-06]. All four **public** addresses were identical across both. Of the six random ones in the first census, the three static (`C3:DD:…`, `E1:94:…`, `C1:93:…`, all `11`) were still there five minutes later; **the two that vanished were `74:92:DB:7F:0C:D8` (`01`, resolvable private) and `34:BA:69:68:4C:05` (`00`, non-resolvable)**, replaced by two new private ones. Four of six random addresses survived, three of them by construction.

**So the rule is decision 43's, and no broader than that**: an address remains the precise filter, and it is a *rotating private* address — not a random one — that cannot be authored ahead of time. A DUT that rotates inside a scan window is a measured fact about a particular DUT (`suite/roadmap.md`), not a property of the address type.

**And when it goes stale, the study names the step that ran out of time.** Connecting to `74:92:DB:7F:0C:D8` between those two censuses timed out at its 15 s step budget [measured 2026-09-06, study `dd340b2a36a39aeba94f4f15b4da61f0`]. A run like it now reports:

```
dev-bench stopped the study early: step 'connect' timed out
```

**That is Core's format string as of [`embarch-core` decision 45](../embarch-core/decisions/studies.md), not a second measurement** — the study id above predates the fix, and against the Core that produced it the very same run said *"the StepResult saying which step failed did not arrive"*. **It had arrived**: `events.json.partial` for that study holds `{"step_name":"connect","outcome":"TimedOut", …}`, written by the code that then denied it, which pointed a reader at the serial link over a stale address. The "did not arrive" wording is now reached **only** when no step outcome was recorded at all — a frame that failed to decode never reaches the writer — so on a Core new enough to have decision 45 it means what it says. If you meet the old message on an older Core, read it as "a step timed out" and confirm against `events.json.partial` under that study's `study_results/` directory.

## 4. Wiring a DUT signal in, and reading the trace afterwards

A study can record more than pass/fail: **if your DUT's firmware has the [embarch-outpost](../embarch-outpost/decisions.md) Zephyr module compiled in, it emits a thread/ISR/marker timeline out a TX-only UART**, and a study can capture it.

**This section needs `embarch-ui`, which is not in the release archive** — build it from [its own repo](https://github.com/gabrieltetar/embarch-ui), per [the user guide](user-guide.md) §3. Declaring a signal has a CLI; **adding a trace tap and reading the trace back do not.**

Two things have to be true first, **in the UI or, since
[`embarch-api` decision 67](../embarch-api/decisions/surface.md), from a terminal**:
`declare-signal`, `list-signals`, `remove-signal`, `dev-bench-link`, each also an MCP tool.

**1. Tell EmbArch where the wire goes.** **A cable between two headers is invisible to software — nothing can detect it — so it can only be stated.** In the **Topology** tab, declare a signal: give it a name (that is what a study taps it by) and pick a route.

- **direct** — straight to a serial port on the machine running Core, **bypassing the bench.** You pick the port from a list **Core itself enumerates, because a port on *your* machine is not necessarily a port on Core's.** This is what the outpost uses today, **for a hardware reason rather than a preference: the bench has no spare pins for it yet.**
- **via dev-bench** — the signal terminates on bench pins and the bench relays it. **Nothing here has the pins yet, but declaring it is a one-field change when it does, and no saved study has to be rewritten — a study names the *signal*, never the cable.**

**Declaring the same name again moves the route. That is the intended way to rewire, not a mistake.**

**2. Add a tap to the study.** In the Study Designer, add an outpost trace tap: name the output and pick the signal. **A study whose tap names a signal nothing has declared is refused before it runs, which is why step 1 comes first.**

**Then read it.** The **Trace** tab renders the recorded timeline — one lane per thread, one for CPU idle, one per interrupt, with your own markers as ticks. Wheel to zoom, drag to pan.

Below it is the **load repartition**: for each thread, interrupt and idle, how many times it ran, how long for, and what share of the window that is. **Read the coverage line above the table first** — it says what fraction of the window the firmware reported dropping records across, and **a repartition computed over an interval with dropped records is not a measurement.**

**Two things in that table are deliberate and look like arithmetic errors:**

- **The shares do not add up to 100%.** **An interrupt runs *inside* whatever it interrupted, so its time is counted twice on purpose**; and Zephyr's idle thread is reported both as its own records and as an ordinary thread, **so those two rows are the same time measured two ways and are never added together. Where they disagree, the disagreement is information** — some idle periods had no closing record.
- **A "not counted" column with time in it.** A span crossing a dropped-record gap, or missing its start or end record, **is drawn so you can see it happened, but its width is a *shape* rather than a duration** — so it is kept out of the total and reported separately. **The entry count still includes it: how many times something ran is not in doubt even when how long is.**

**Three things it will tell you that are easy to misread as bugs, and are not:**

- **Threads shown as `0x08058240` instead of names.** Some of a real build's threads have no symbol a tool can read a name from, so the trace shows the pointer it actually has. **A made-up name on a real timeline is worse than a number.**
- **Red hatched bands.** The firmware dropped records there, and says how many. **Records that *survived* inside a band are still drawn: the band means "this interval is incomplete", not "nothing happened here".**
- **"This trace has no names."** The manifest describing your build did not match the firmware that produced the capture — usually because **the board was flashed out of band between the study's flash and its run.** The timeline is real and readable, it just has no labels. **What EmbArch refuses to do is apply the *wrong* manifest, which would relabel every thread and marker and produce something that reads perfectly and is entirely wrong.**

**One honest caveat about the numbers.** The instrument works on real hardware — a real capture runs at tens of KB/s and decodes with zero records lost — **but every timing-related default in it is still an unmeasured guess, and the instrumentation's own overhead is deliberately uncharacterised.** Nothing has yet compared a trace's placement against a second stream in the same study. **Treat the first real trace as data about the trace, not just about your firmware.**

**And a practical one if you are wiring this up yourself: the pin your board's schematic labels as the debug UART's transmit pin is not necessarily the one your firmware transmits on.** On the board this was first tried against, **the build had been targeting a different board revision entirely**, so the bytes went out a pin nothing was connected to — **and that looks exactly like broken firmware.** Confirm the board revision you are building for before you suspect anything else, then flash something that prints and watch for it.

