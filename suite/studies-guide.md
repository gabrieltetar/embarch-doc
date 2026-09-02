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

## 4. Wiring a DUT signal in, and reading the trace afterwards

A study can record more than pass/fail: **if your DUT's firmware has the [embarch-outpost](../embarch-outpost/decisions.md) Zephyr module compiled in, it emits a thread/ISR/marker timeline out a TX-only UART**, and a study can capture it. Two things have to be true first, **both done in the UI** — there is deliberately no CLI for either.

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

