# EmbArch: wiring a DUT signal in, and reading its trace

**Status:** active, 2026-11-25. Moved verbatim from [studies-guide.md](studies-guide.md) §4, which continues [user-guide.md](user-guide.md) and sets a direct signal's line rate in its §3.

A study can record more than pass/fail: **if your DUT's firmware has the [embarch-outpost](../embarch-outpost/decisions.md) Zephyr module compiled in, it emits a thread/ISR/marker timeline out a TX-only UART**, and a study can capture it.

**This section needs `embarch-ui`, which is not in the release archive** — build it from [its own repo](https://github.com/gabrieltetar/embarch-ui), per [the user guide](user-guide.md) §3. Declaring a signal has a CLI; **adding a trace tap and reading the trace back do not.**

Two things have to be true first, **in the UI or, since
[`embarch-api` decision 67](../embarch-api/decisions.md), from a terminal**:
`declare-signal`, `list-signals`, `remove-signal`, `dev-bench-link`, each also an MCP tool.

**1. Tell EmbArch where the wire goes.** **A cable between two headers is invisible to software, so it can only be stated.** In the **Topology** tab, open **Signals** and declare a signal: give it a name (that is what a study taps it by) and pick a route. **A direct signal also takes its `baud`** ([studies guide](studies-guide.md) §3); the tab has no field for it yet, so use `embarch-api declare-signal ... --baud <rate>` or the `declare_signal` tool.

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
