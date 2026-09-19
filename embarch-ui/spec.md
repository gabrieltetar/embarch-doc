# embarch-ui: spec

**Status:** active, 2026-09-13. Repo: [gabrieltetar/embarch-ui](https://github.com/gabrieltetar/embarch-ui).

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Reference: [interfaces.md](interfaces.md).

## What it is

The one place a firmware engineer looks to exercise suite features **by hand** — day to day, not just when an agent needs a hardware read. It replaced three ad hoc UI surfaces outright rather than adding a fourth: `embarch-topology`'s board view, `embarch-study-designer`'s standalone builder, and Core's enroll page, all three retired.

It is **not** a build-toolchain project, not a VS Code webview, not a second owner of hardware mutation, and not a replacement for `embarch-api`'s MCP/CLI surface — agents keep talking to `embarch-api`. It does now *invoke* a build, through the same crate `embarch-api` does; owning the machinery and calling it are different things.

## Shape

```
embarch-ui (one Rust binary, axum, zero-build)
  |
  +-- links embarch-study-designer  (in-process: merged action list, custom-action
  |                                  registry, study building, outpost trace decode
  |                                  — pure data, no I/O)
  +-- links embarch-core-client     (one implementation of "reach Core over
  |                                  HTTP+Bearer", shared with embarch-api)
  +-- links embarch-firmware-build  (config, west scan, target resolution and the
  |                                  build itself — also shared with embarch-api;
  |                                  a subprocess and files, no hardware)
  +-- links embarch-topology only transitively, through embarch-core-client,
  |   and only its `software` feature — never `hardware`, so neither probe-rs
  |   nor serialport is in the tree (decisions/wiring.md)
  |
  +-- HTTP + Bearer --> embarch-core
        every hardware-adjacent call, read or write: enrollment, signals,
        serial ports, alerts, status, both dev-bench routes, the whole /study
        family, and POST /flash + POST /reset where a study builds its own
        DUT firmware (the build is local, the flash and reset are not).
        interfaces.md has the exact list.
        GET /logs/recent, and nothing else under /logs: Core's /logs/stream
        was retired in 2026-09 having never acquired a caller. The Debug
        tab's backlog is one call on open; its tail is a server-side re-poll
        of it, diffed so only new lines are published.

vscode-extension/ (thin, TypeScript)
  pre-flights the address, spawns and stops the binary, and shows the page in
  the system browser — focusing the window and tab already open, matched on
  the page title (decision 28). Renders nothing itself
```

**It never links `embarch-topology`'s `hardware` feature, and the reason is load-bearing:** a board read done in-process would enumerate whichever machine `embarch-ui` runs on, not Core's. The crate is in the tree transitively (`embarch-core-client`, `software` feature only); what stays out is every hardware-touching path, which is what the `probe-rs`/`serialport` invariant below measures.

## The six tabs

One persistent left sidebar, one top status bar, client-side navigation by URL fragment (`#topology`, `#live-study`). A fragment names a tab and nothing else, since `#trace?study=<id>&tap=<name>` went with the Trace tab (decision 31).

| Tab | What it does |
|---|---|
| **Dashboard** | Active study and alert cards, live |
| **Topology** | The board/probe diagram, the alert list, and **signal routing** — the one human surface for declaring a DUT signal's route |
| **Study Designer** | **Authoring and saving** a study; running it is Live Study's (decision 31). Four panels (decision 41): **project**, whose **Static firmware analysis** submenu runs the GATT extractor; the **study toolbar**, whose **Build options…** dialog has the two `requires` fields, the dev-bench log level and the **Build card**, summarised on the page; **steps**; and **Define the wire** — taps, `.eap` manifests and editor, the action registry, layouts. The Build card (decision 38): board/app/variant/revision, an **ordered** snippet list, west flags, a three-state outpost mode per header flag, off by default and unavailable-with-a-reason off a configured project |
| **Enroll** | Submits to Core's enroll endpoint |
| **Live Study** | Runs a saved study and watches it land, or opens any past one and reads it back. One long page of stacked cards: run/open with the studies list, the **build card** where this run builds its own firmware (each line as it arrives, then the flashed version), status, steps filling in live, the event feed, one console per `Text` tap, the **Time chart** (every stream on one axis), the trace chart, and one data card per tap |
| **Debug** | Three sources: two live tails — Core (server-side poll of `GET /logs/recent`) and `embarch-api` (its rolling file), both reaching the browser as this UI's own `lines` SSE event — and **builds**, stored rather than tailed, every firmware build this UI ran, kept locally and picked from a list (decision 39) |

Everything live reaches the browser as **SSE** served by this binary; there is no client-side interval polling (no `setInterval` in `app.js`). Where a source has no push surface, the polling is server-side and the browser never sees it.

## Invariants

- **Every hardware-adjacent call, read or write, goes over HTTP+Bearer to Core.** Verified structurally: neither `probe-rs` nor `serialport` is in `cargo tree -e normal`. **A firmware build is not one of them** — `west` in a subprocess and files on disk; its flash and reset still go to Core.
- **A snippet list is ordered end to end**: picker, stored `Study` and `west -S` are one sequence, sorted into a set by nothing (reversals row 114). **A saved study's `firmware_version` is rewritten only after a waved-through mismatch, never over `any`** (decision 40).
- **The UI never decides which version provenance counts as verified** — that is answered server-side and rendered, never re-derived in JavaScript.
- **A trace whose build ID did not match is never rendered as a *named* trace**: it renders unnamed, with Core's reason verbatim, every lane the raw pointer or vector number it is.
- **A dropped-record gap is drawn as a gap**, overlaid on the records that survived, never bridged into a continuous timeline.
- **An axis tier is chosen once per view, never per span**: one row missing the stamp its tier needs drops the whole view a tier.
- **A capture opening with pre-reset records loses the prefix, not the microsecond axis**, only where the clock is already refused, and the axis note says what went ([decisions/trace-rows.md](decisions/trace-rows.md) 19). **A refused row is counted, never merely skipped**: "every row in the capture" is said only when the refused and capped counts are both zero.
- **The run badge names the step *now running*, not the count finished** (decision 20): Core's `current_step` is the last step that *finished*, so the badge adds two and clamps to `total_steps`; `null` reads as step 1, and a zero-step study gets no counter.
- **A limit enforced server-side is *served*, never restated in `app.js` — and so is a vocabulary.** The action entries and labels, the eighteen scalar types, the five log levels (which is the default, and the prose under each), the four caps, the three advisory dev-bench capacities and the eight outpost header-flag names all come from the crate ([`embarch-study-designer` decision 73](../embarch-study-designer/decisions/authoring.md)), and a test asserts `app.js` holds no copy. **An empty served vocabulary is an empty picker, which is a refusal**, never a guessed list.
- **An advisory capacity never gates**: the three dev-bench caps come from a build that may not be the bench in front of you, so a study past one says so and Run stays enabled. **One this tab could not read renders as *unknown*, never as "within caps"**; `POST /preflight` builds the list server-side, since two of the three cannot be computed in a browser.
- **A destructive edit that would break a saved study is refused, naming the studies.** Deleting or renaming a registered action, a payload layout or an `.eap` file scans `embarch/studies/` first and answers `409` with the studies and their steps, leaving the form filled. **A file the scan cannot read is unscannable, never "no references"** — a directory it cannot fully read is not permission to delete.
- **A capture that was not checked never reads as clean.** An absent `StreamRef.records` means no framing was declared, a different fact from "every record verified"; an empty capture reads "nothing to check", which is why the browser does not use `RecordReport::all_verified()`.
- **One decoder reads a step outcome in both wire shapes** (decision 23); an unrecognised one renders visibly wrong, never a pass or a dash.
- **A capped ring says it is capped** — the feed, each console and each live series are bounded server-side and count what they dropped ("the last 5,000 of 8,412"); a series **decimates rather than dropping its oldest**, saying it shows one point in N (decision 31).
- **A partial console line is shown as partial**: a `Text` chunk arrives verbatim and can end mid-line ([`embarch-core` decision 70](../embarch-core/decisions/streams.md)), and the remainder is never padded into a line the tap did not send.
- **`lagged` is displayed, never swallowed**, and this UI's own broadcast overrun is a *different* fact from Core's: the first says the disk record is complete and this feed is not, the second that a reload catches up.
- **`interrupted` is never rendered as completed or failed** ([`embarch-core` decision 69](../embarch-core/decisions/study-record.md)), and **a terminal status is never un-said by a later poll** — Core's registry can still report `running` between the last step landing and the job closing.
- **A post-run re-read replaces a card only where its own read succeeded**, so a tap Core will not serve keeps what the live feed put there.
- **A shared axis reads `core_rx_utc_ms` and nothing else** — a study CSV's `rx_utc_ms` is dev-bench uptime under one name ([suite decision 3](../suite/decisions.md)). A mark is placed, unplaceable or uncertain; unplaceable is a gutter count, never a guessed position; the tier is chosen once and an improvement is an epoch bump. Live, a mark is placed once ([decisions/time-chart.md](decisions/time-chart.md)).
- **Unreadable renders as unreadable, not as a mismatch or an empty list.** A bench not plugged in has no version to disagree with; a Core answering `404` to the signals route has not said there are no signals.

## The trace chart

SVG with server-side aggregation, so **the element count is bounded by pixels × lanes, not by the dataset**. **Filtering changes the drawing and nothing else: the load repartition stays computed across every lane, and says so** — a denominator quietly following a view filter would be a measurement of nothing ([decisions/trace-chart.md](decisions/trace-chart.md)). It is a card on the Live Study tab, on whichever study that tab has open. Reference numbers, the bin-fetch endpoint and the two served view caps: [interfaces.md](interfaces.md).

## Verification technique

Instruments this UI established, because "tested in Rust, never looked at" is how its worst defects hid:

- **A headless-Firefox harness, and `tests/browser/` is the one to reach for.** It drives the **running binary** through geckodriver against a stub embarch-core — the assets are `include_str!`-embedded, so the deployed artifact is the only thing that can be checked — which is what makes the five states a bench will not produce on demand testable at all — an interrupted study, an unparseable one, a `lagged` frame, a chunk ending mid-line, and a study with neither a trace nor any data. `drive_build.py` is its sibling for the Build card and the builds source. It found a real defect on its first run; `tests/browser/README.md` has the shape.
- **A static id guard** (`tests/element_ids.rs`, decision 24), catching the one shape of the above a text scan can: no id declared twice, no `getElementById`/`sdEl`/`trEl`/`sigEl` lookup dangling.
