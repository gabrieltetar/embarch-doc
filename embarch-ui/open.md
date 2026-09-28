# embarch-ui: open

**Status:** active, 2026-09-13.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Whether `embarch-ui` belongs in the suite release archive is undecided** — [`embarch-umbrella`](../embarch-umbrella/decisions/install.md) decision 14's and the suite's. `assemble-suite.yml` ships three binaries, not this one, so a fresh `embarch setup` can't author or read back a trace. **Documentation half closed** (`tasks/suite/019`): [user-guide](../suite/user-guide.md) §3, [studies-guide](../suite/studies-guide.md) §4. **Trigger:** first non-owner engineer walks the studies guide end to end.

- **The run dialog does not read a *stored* study's build spec.** It knows the step table's Build card and says so; a run-only file's spec is in the file, and the dialog names which case it is, not the wrong study's build. **Trigger:** running a saved study with a build spec from the Live Study tab and wanting to see what it will flash before it does. Decision 38.

- **A flash or a reset that fails mid-run has never been watched.** The build-failure branch was driven on hardware 2026-09-19 (deliberate syntax error) and is closed; still only unit-tested are the two steps after it — a `POST /flash` Core refuses, and a reset that does not take. Both would surface as a `failed` frame at phase `build` with a Core error in it, and neither has been seen. **Trigger:** unplug the DUT's probe between build finish and flash start, the cheap way to produce the first one.

- **A trace's placement has been checked against GATT and holds, but never against a power capture** (validation: `embarch-ui` decision 34). No study on Core's disk carries a `Samples` tap, so the sample strip and struct lane are covered by unit tests only, and outpost wire constants stay unmeasured defaults. **Still unrun:** the same placement check against a real power capture, once one exists.

- **The end-to-end `/study/{id}/streams` cost over real HTTP is still unmeasured.** The row cap's own decode/encode cost at scale is measured, in-process, up to 1M rows (`embarch-ui` decision 21) — not covered are the three awaited Core calls (`study_streams`, `get_study_stream`, `study_steps`) `decode_trace` makes before `parse` runs. Re-measure against a live Core before calling the in-process number the whole cost.

- **A signal mismatch has nowhere durable to land**, so a declared-but-wrong signal shows up in the Topology tab or nowhere. Closed upstream as not-needed-yet; two-part trigger: half fired (declarable through this tab), half not (no wire, no bridge). Carried by the row's own carrier cell, not the alert list.

- **The live Time chart has never been driven by a trace.** Its no-trace half ran on the bench 2026-09-18 (`bds-ppg-drain`, 12 steps, 349 s): live and post-hoc agree to 3 ms on the axis and to the mark on GATT. **The traced half is unrun** — the `outpost` signal's declared route is `direct/port_serial=5` and no such device is present, so nothing has exercised `LiveAxis`'s anchor path, the epoch bump on a late header, or the non-monotone refusal against a real clock. **Trigger:** the outpost bridge attached and the signal re-declared against it. Unparks `tasks/core/093`.

- **The stale-prefix drop has never met a real stale prefix** (decision 19): tested against crafted fixtures both ways, but the case it exists for — **18 records** a real capture opened with, buffered in the USB-UART bridge past `embarch-core`'s open-time purge — has not been replayed. **Hardware debt, the owner's session:** run a study, open its Trace tab, check the axis note reports a dropped prefix where the capture fell to ms. Until then, `STALE_PREFIX_MAX_ROWS` (512) is an assumption about a bridge FIFO nobody has measured.

- **A saved study is never checked against the `.eap` file it was built from**, so the tab can offer a protocol whose text no longer matches what the study carries. The check is server-side, owned by `embarch-study-designer` — its [open.md](../embarch-study-designer/open.md) carries the question and trigger; this repo's half is only where a divergence would be *shown*. Named here so a reader does not conclude the silence is a design choice.

- **The `Debug` level's clamp note has never fired.** Legs E and J of `tasks/ui/070` ran on a live nRF54L15 bench 2026-09-18 and closed everything else: the same study at `Off` and at `Debug` captured **0 vs 7,440 bytes** on the reserved `dev-bench` tap, so the level reaches the firmware and acts on it. What did not fire is the clamp itself — `app/prj.conf` is `CONFIG_LOG_DEFAULT_LEVEL=4` with runtime filtering, so `Debug` is *reachable* and there is nothing to report; a deliberately quieter build is needed to see it. **Delivery is proven** (the same `send_log_line` channel carried 129 lines); only the trigger is unexercised.
