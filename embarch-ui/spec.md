# embarch-ui: spec

**Status:** active, 2026-09-13. Repo: [gabrieltetar/embarch-ui](https://github.com/gabrieltetar/embarch-ui).

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Reference: [interfaces.md](interfaces.md).

## What it is

The one place a firmware engineer looks to exercise suite features **by hand** — day to day, not just when an agent needs a hardware read. It replaced three separate ad hoc UI surfaces outright rather than adding a fourth: `embarch-topology`'s read-only board view, `embarch-study-designer`'s standalone study builder, and Core's own enroll page. All three are retired.

It is **not** a build-toolchain project, not embedded in VS Code as a webview, not a second owner of hardware mutation, and not a replacement for `embarch-api`'s MCP/CLI surface — agents keep talking to `embarch-api`.

## Shape

```
embarch-ui (one Rust binary, axum, zero-build)
  |
  +-- links embarch-study-designer  (in-process: merged action list, custom-action
  |                                  registry, study building, outpost trace decode
  |                                  — pure data, no I/O)
  +-- links embarch-core-client     (the one implementation of "reach Core over
  |                                  HTTP+Bearer", shared with embarch-api)
  +-- links embarch-topology only transitively, through embarch-core-client, and
  |   only its `software` feature — never the `hardware` one, so neither
  |   probe-rs nor serialport is in the tree (decisions/wiring.md)
  |
  +-- HTTP + Bearer --> embarch-core
        every hardware-adjacent call, read or write:
          POST /probes/enroll · POST/GET/DELETE /signals · GET /serial-ports
          GET /probes/enrolled · GET /alerts · GET /status
          GET /dev-bench/port · GET /dev-bench/hello
          POST /study · GET /study/{id} · GET /study/{id}/steps
          GET /study/{id}/streams · GET /study/{id}/stream/{name}
          GET /study/{id}/stream/{name}/load
        GET /logs/recent, and nothing else under /logs. The Debug tab's
        Core-side backlog is one call to it on open; its live tail is a
        server-side re-poll of the same endpoint (500-line tail, every 2 s,
        diffed so only genuinely new lines are published; a failed poll is
        logged server-side and the next tick retries). There is no SSE
        alternative: Core's GET /logs/stream was retired in 2026-09
        (tasks/core/021) having never acquired a caller — /logs/recent is
        the only log route Core serves.

vscode-extension/ (thin, TypeScript)
  pre-flights the address before spawning the binary, stops what it spawned,
  and shows the page in the system browser — focusing the window and tab
  already open, matched on the page title (decision 28), rather than opening
  a second one. Renders nothing itself
```

**It never links `embarch-topology`'s `hardware` feature, and the reason is load-bearing:** a board read done in-process would enumerate whichever machine `embarch-ui` runs on, not Core's. The crate itself is in the tree transitively (`embarch-core-client` depends on it, `software` feature only); what stays out is every hardware-touching path, which is what the `probe-rs`/`serialport` invariant below actually measures.

## The six tabs

One persistent left sidebar, one top status bar, client-side navigation by URL fragment (`#topology`, `#live-study`). A fragment names a tab and nothing else, since `#trace?study=<id>&tap=<name>` went with the Trace tab (decision 31).

| Tab | What it does |
|---|---|
| **Dashboard** | Active study and alert cards, live |
| **Topology** | The board/probe diagram, the alert list, and **signal routing** — the one human surface for declaring a DUT signal's route |
| **Study Designer** | **Authoring and saving** a study; running and watching moved to Live Study (decision 31), and its Run buttons post and switch tabs. Steps, the two `requires` fields, security levels, GATT capture taps and their record framing, `RunProtocol` steps against the repo's `.eap` manifests, the dev-bench log level, the declared-GATT picker, the custom-action registry and payload layouts (author, edit, delete), and an `.eap` text editor |
| **Enroll** | Submits to Core's enroll endpoint |
| **Live Study** | Runs a saved study and watches it land, or opens any past one and reads it back. One long page of stacked cards: run/open with the studies list, status, steps filling in live, the event feed, one console per `Text` tap, the **Time chart** (every stream on one axis), the outpost trace chart, and one data card per tap |
| **Debug** | Live log tail, switchable between Core (server-side poll of `GET /logs/recent`) and `embarch-api` (its rolling file); both reach the browser as this UI's own `lines` SSE event |

Everything live reaches the browser as **SSE** served by this binary; there is no client-side interval polling anywhere (no `setInterval` in `app.js`). Where a source has no push surface this repo consumes, the polling is server-side and the browser never sees it — the Debug tab's two log feeds are both that shape.

## Invariants

- **Every hardware-adjacent call, read or write, goes over HTTP+Bearer to Core.** Verified structurally: neither `probe-rs` nor `serialport` appears in `cargo tree -e normal`.
- **The UI never decides for itself which version provenance counts as verified** — that is answered server-side and rendered, never re-derived in JavaScript.
- **A trace whose build ID did not match is never rendered as a *named* trace.** It renders unnamed, with Core's reason verbatim, every lane the raw pointer or vector number it is.
- **A dropped-record gap is drawn as a gap**, as an overlay over the records that survived, never bridged into a continuous timeline.
- **An axis tier is chosen once per view, never per span**, and one row missing the stamp its tier needs drops the whole view down a tier.
- **A capture that opens with records from before the DUT reset loses the prefix, not the microsecond axis**, and only where the clock is already refused; what was dropped is stated in the axis note ([decisions/trace-rows.md](decisions/trace-rows.md) 19).
- **A row the trace decoder refused is counted, never merely skipped**, and "every row in the capture" is said only when the refused and capped counts are both zero.
- **The run badge's counter names the step *now running*, not the count finished** (decision 20). Core's `current_step` is the index of the last step that *finished*, so the badge adds two and clamps to `total_steps`; `null` reads as step 1, and a zero-step study gets no counter.
- **A limit enforced server-side is *served*, never restated in `app.js` — and so is a vocabulary.** The action entries and labels, the eighteen scalar types, the five log levels (with which is the default and the prose under each), the four caps and the three advisory dev-bench capacities all come from the crate ([`embarch-study-designer` decision 73](../embarch-study-designer/decisions/authoring.md)), and a test asserts `app.js` holds no copy of any of them. **An empty served vocabulary is an empty picker, which is a refusal**, never a guessed list.
- **An advisory capacity never gates**: the three dev-bench caps come from a build that may not be the bench in front of you, so a study past one says so and Run stays enabled. **A capacity this tab could not read renders as *unknown*, never as "within caps"**, and `POST /preflight` builds the whole list server-side — two of the three cannot be computed in a browser at all.
- **A destructive edit that would break a saved study is refused, naming the studies.** Deleting or renaming a registered action, a payload layout or an `.eap` file scans `embarch/studies/` first and answers `409` with the studies and the steps in them. **A file the scan cannot read is reported as unscannable, never as "no references"** — a directory it cannot fully read is not permission to delete. The refusal leaves the form filled.
- **A capture that was not checked never reads as clean.** `StreamRef.records` absent means no record framing was declared, a different fact from "every record verified"; an empty capture reads "nothing to check", which is why the browser does not use `RecordReport::all_verified()`.
- **A step outcome is read by one decoder for both wire shapes** (decision 23); an unrecognised shape renders visibly wrong, never a pass or a dash.
- **A capped ring says it is capped** — the feed, each console and each live series are bounded server-side and count what they dropped ("showing the last 5,000 of 8,412"), and a series **decimates rather than dropping its oldest**, saying it shows one point in N (decision 31).
- **A partial console line is shown as partial.** A `Text` chunk arrives verbatim and can end mid-line ([`embarch-core` decision 70](../embarch-core/decisions/streams.md)); the remainder is never padded into a line the tap did not send.
- **`lagged` is displayed, never swallowed**, and this UI's own broadcast overrun is a *different* fact from embarch-core's: the first says the disk record is complete and this feed is not, the second that a reload catches up.
- **`interrupted` is never rendered as completed or failed** ([`embarch-core` decision 69](../embarch-core/decisions/study-record.md)), and **a terminal status is never un-said by a later poll** — embarch-core's registry can still report `running` for the moment between the last step landing and the job closing.
- **A post-run re-read replaces a card only where its own read succeeded**, so a tap embarch-core will not serve keeps what the live feed put there.
- **A shared axis reads `core_rx_utc_ms` and nothing else** — a study CSV's `rx_utc_ms` is dev-bench uptime under one name ([suite decision 3](../suite/decisions.md)). A mark is placed, unplaceable or uncertain; an unplaceable one is a gutter count, never a guessed position; the tier is chosen once and an improvement is an epoch bump, never a silent move. Live, a mark is placed once and never re-placed ([decisions/time-chart.md](decisions/time-chart.md)).
- **Unreadable is rendered as unreadable, not as a mismatch or an empty list.** A bench that is not plugged in has no version to disagree with; a Core that answered `404` to the signals route has not told you there are no signals.

## The trace chart

SVG with server-side aggregation, so **the element count is bounded by pixels × lanes, not by the dataset**. **Filtering changes the drawing and nothing else: the load repartition stays computed across every lane, and says so** — a denominator that quietly followed a view filter would be a measurement of nothing ([decisions/trace-chart.md](decisions/trace-chart.md)). It is a card on the Live Study tab now, on whichever study that tab has open, rather than a view addressed on its own. Reference numbers, the bin-fetch endpoint and the two served view caps: [interfaces.md](interfaces.md).

## Verification technique

Two instruments this UI established, both because "tested in Rust, never looked at" is how its worst defects hid:

- **A headless-Firefox harness, and `tests/browser/` is the one to reach for.** It drives the **running binary** through geckodriver against a stub embarch-core, which is what makes the five states a bench will not produce on demand testable at all — an interrupted study, an unparseable one, a `lagged` frame, a chunk that ends mid-line, and a study with neither a trace nor any data. It found a real defect on its first run; `tests/browser/README.md` has the shape. The older in-page harness re-evaluates `app.js`'s IIFE body against a real DOM (there is no `node` on this bench): there, strip the app's own `DOMContentLoaded` initializer first, or it re-renders every panel from fetches that fail under `file://`.
- **Driving the deployed binary itself** with real clicks. The assets are `include_str!`-embedded, so **the deployed artifact is the only thing that can be checked** for anything that depends on them.
- **A static id guard** (`tests/element_ids.rs`, decision 24) over the id surface only, catching the one shape of the above that a text scan over both assets can: no id declared twice, and no `getElementById`/`sdEl`/`trEl`/`sigEl` lookup dangling.
