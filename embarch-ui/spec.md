# embarch-ui: spec

**Status:** active, 2026-09-04. Repo: [gabrieltetar/embarch-ui](https://github.com/gabrieltetar/embarch-ui).

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
          GET /study/{id}/gatt-data
        GET /logs/recent, and nothing else under /logs. The Debug tab's
        Core-side backlog is one call to it on open; its live tail is a
        server-side re-poll of the same endpoint (500-line tail, every 2 s,
        diffed so only genuinely new lines are published; a failed poll is
        logged server-side and the next tick retries). There is no SSE
        alternative: Core's GET /logs/stream was retired in 2026-09
        (tasks/core/021) having never acquired a caller — /logs/recent is
        the only log route Core serves.

vscode-extension/ (thin, TypeScript)
  spawns/stops the binary, opens the system browser, renders nothing itself
```

**It never links `embarch-topology`'s `hardware` feature, and the reason is load-bearing:** a board read done in-process would enumerate whichever machine `embarch-ui` runs on, not Core's. The crate itself is in the tree transitively (`embarch-core-client` depends on it, `software` feature only); what stays out is every hardware-touching path, which is what the `probe-rs`/`serialport` invariant below actually measures.

## The six tabs

One persistent left sidebar, one top status bar, client-side navigation by URL fragment (`#topology`, `#trace?study=<id>&tap=<name>`).

| Tab | What it does |
|---|---|
| **Dashboard** | Active study and alert cards, live |
| **Topology** | The board/probe diagram, the alert list, and **signal routing** — the one human surface for declaring a DUT signal's route |
| **Study Designer** | Authoring a study: steps, the two `requires` fields, security levels, GATT capture taps, the declared-GATT picker, opening a firmware project |
| **Enroll** | Submits to Core's enroll endpoint |
| **Trace** | Renders a completed study's outpost capture: lanes, gap bands, a load repartition, a study-step row |
| **Debug** | Live log tail, switchable between Core (server-side poll of `GET /logs/recent`) and `embarch-api` (its rolling file); both reach the browser as this UI's own `lines` SSE event |

Everything live reaches the browser as **SSE** served by this binary; there is no client-side interval polling anywhere (no `setInterval` in `app.js`). Where a source has no push surface this repo consumes, the polling is server-side and the browser never sees it — the Debug tab's two log feeds are both that shape.

## Invariants

- **Every hardware-adjacent call, read or write, goes over HTTP+Bearer to Core.** Verified structurally: neither `probe-rs` nor `serialport` appears in `cargo tree -e normal`.
- **The UI never decides for itself which version provenance counts as verified** — that is answered server-side and rendered, never re-derived in JavaScript.
- **A trace whose build ID did not match is never rendered as a *named* trace.** It renders unnamed, with Core's reason verbatim, every lane the raw pointer or vector number it is.
- **A dropped-record gap is drawn as a gap**, as an overlay over the records that survived, never bridged into a continuous timeline.
- **An axis tier is chosen once per view, never per span**, and one row missing the stamp its tier needs drops the whole view down a tier.
- **A capture that opens with records from before the DUT reset loses the prefix, not the microsecond axis** (decision 19) — and only where the clock is already refused, so an inherent 13 µs inversion never costs a record. The count dropped and how far their clock sat is stated in the axis note; `rows` counts what was kept.
- **A row the trace decoder refused is counted, never merely skipped** — a line short of nine fields, or a `frame_index` that is not a number. The Records card states `rows_unparsed` when it is non-zero and says "every row in the capture" only when it and the cap count are both zero.
- **The run badge's counter names the step *now running*, not the count finished** (decision 20). Core's `current_step` is the index of the last step that *finished*, so the badge adds two and clamps to `total_steps`; `null` reads as step 1, and a zero-step study gets no counter.
- **A limit enforced server-side is *served*, never restated in `app.js`** — and since `suite/017`, so is a **vocabulary**. The Study Designer's built-in action picker renders the entries and labels the crate serves ([`embarch-study-designer` decision 73](../embarch-study-designer/decisions/authoring.md)); it used to hold its own hardcoded array of nine, beside a served list it filtered out and discarded, and the discarded one had been two variants stale since that crate's decision 53.
- **A step outcome is read by one decoder for both wire shapes** (decision 23); an unrecognised shape renders visibly wrong, never a pass or a dash.
- **Unreadable is rendered as unreadable, not as a mismatch or an empty list.** A bench that is not plugged in has no version to disagree with; a Core that answered `404` to the signals route has not told you there are no signals.

## Design system

Dark-first developer console, togglable to light. IBM Plex Sans for UI text, Plex Mono for data and log lines. An oklch token system: one cyan accent, green/amber/red semantics, chroma and lightness held across hues. `--brand` holds the logo's red for the wordmark and header glyph only — it is the same colour as `--danger`, so it is never the accent (decision 25). Hand-authored components — stat cards, status badges, data tables, pill toggles, chip inputs, a terminal-styled console, and a `.dialog`/`.dialog-backdrop` modal used in five places. No bundler.

## The trace chart

It stays SVG with server-side aggregation, so **the element count is bounded by pixels × lanes, not by the dataset**, never bridged into a client-side redraw of the whole capture. **Filtering changes the drawing and nothing else: the load repartition stays computed across every lane, and says so** — a denominator that quietly followed a view filter would be a measurement of nothing ([decisions/trace-chart.md](decisions/trace-chart.md)). Reference numbers, the bin-fetch endpoint and the two served view caps: [interfaces.md](interfaces.md) — *The trace chart*.

## Verification technique

Two instruments this UI established, both because "tested in Rust, never looked at" is how its worst defects hid:

- **A headless-Firefox harness** that re-evaluates `app.js`'s IIFE body against a real DOM (there is no `node` on this bench) and renders against real serialized server responses. Strip the app's own `DOMContentLoaded` initializer before rendering — it fires *after* an inline harness script and re-renders every panel from fetches that fail under `file://`.
- **Driving the deployed binary itself** with real clicks. The assets are `include_str!`-embedded, so **the deployed artifact is the only thing that can be checked** for anything that depends on them.
- **A static id guard** (`tests/element_ids.rs`, decision 24) over the id surface only, catching the one shape of the above that a text scan over both assets can: no id declared twice, and no `getElementById`/`sdEl`/`trEl`/`sigEl` lookup dangling.
