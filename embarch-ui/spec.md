# embarch-ui: spec

**Status:** active, 2026-09-04. Repo: [gabrieltetar/embarch-ui](https://github.com/gabrieltetar/embarch-ui).

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md).

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
  +-- does NOT link embarch-topology, at all, deliberately
  |
  +-- HTTP + Bearer --> embarch-core
        every hardware-adjacent call, read or write:
          POST /probes/enroll · POST/GET/DELETE /signals · GET /serial-ports
          GET /probes/enrolled · GET /alerts · GET /status
          GET /dev-bench/port · GET /dev-bench/hello
          POST /study · GET /study/{id} · GET /study/{id}/steps
          GET /study/{id}/streams · GET /study/{id}/stream/{name}
        GET /logs/stream (SSE live tail) · GET /logs/recent (backfill)

vscode-extension/ (thin, TypeScript)
  spawns/stops the binary, opens the system browser, renders nothing itself
```

**It does not link `embarch-topology`, and the reason is load-bearing:** a board read done in-process would enumerate whichever machine `embarch-ui` runs on, not Core's.

## The six tabs

One persistent left sidebar, one top status bar, client-side navigation by URL fragment (`#topology`, `#trace?study=<id>&tap=<name>`).

| Tab | What it does |
|---|---|
| **Dashboard** | Active study and alert cards, live |
| **Topology** | The board/probe diagram, the alert list, and **signal routing** — the one human surface for declaring a DUT signal's route |
| **Study Designer** | Authoring a study: steps, the two `requires` fields, security levels, GATT capture taps, the declared-GATT picker, opening a firmware project |
| **Enroll** | Submits to Core's enroll endpoint |
| **Trace** | Renders a completed study's outpost capture: lanes, gap bands, a load repartition, a study-step row |
| **Debug** | Live log tail, switchable between Core (over HTTP) and `embarch-api` (from its rolling file) |

Everything live is **SSE**; there is no client-side interval polling anywhere.

## Invariants

- **Every hardware-adjacent call, read or write, goes over HTTP+Bearer to Core.** Verified structurally: neither `probe-rs` nor `serialport` appears in `cargo tree -e normal`.
- **The UI never decides for itself which version provenance counts as verified** — that is answered server-side and rendered, never re-derived in JavaScript.
- **A trace whose build ID did not match is never rendered as a *named* trace.** It renders unnamed, with Core's reason verbatim, every lane the raw pointer or vector number it is.
- **A dropped-record gap is drawn as a gap**, as an overlay over the records that survived, never bridged into a continuous timeline.
- **An axis tier is chosen once per view, never per span**, and one row missing the stamp its tier needs drops the whole view down a tier.
- **A capture that opens with records from before the DUT reset loses the prefix, not the microsecond axis** (decision 19) — and only where the clock is already refused, so an inherent 13 µs inversion never costs a record. The count dropped and how far their clock sat is stated in the axis note; `rows` counts what was kept.
- **A row the trace decoder refused is counted, never merely skipped** — a line short of nine fields, or a `frame_index` that is not a number. The Records card states `rows_unparsed` when it is non-zero and says "every row in the capture" only when it and the cap count are both zero.
- **A limit enforced server-side is *served*, never restated in `app.js`.**
- **Unreadable is rendered as unreadable, not as a mismatch or an empty list.** A bench that is not plugged in has no version to disagree with; a Core that answered `404` to the signals route has not told you there are no signals.

## Design system

Dark-first developer console, togglable to light. IBM Plex Sans for UI text, Plex Mono for data and log lines. An oklch token system: one cyan accent, green/amber/red semantics, chroma and lightness held across hues. Hand-authored components — stat cards, status badges, data tables, pill toggles, chip inputs, a terminal-styled console, and a `.dialog`/`.dialog-backdrop` modal used in five places. No bundler.

## The trace chart

The reference reference-dut capture is the working shape to design against: **147.5 s, 225,606 rows, 112,801 spans, 26 lanes.** Wheel zooms at the pointer, drag pans, the window is clamped to the capture. Lanes scroll vertically with the axis and step row pinned; they can be filtered, hidden and reordered, and **filtering changes the drawing and nothing else** — the load repartition stays computed across every lane and says so.

It stays SVG. Sub-pixel spans aggregate into per-pixel occupancy runs per lane, so **the element count is bounded by pixels × lanes, not by the dataset**: ~2,500 rects worst case, 27 ms to redraw. Aggregation is exact — a run splits wherever a gap, a below-resolution flag or an open edge changes.

**That aggregation runs on the server, and the view asks for the window it is about to draw** (decision 18). `GET /api/trace/{study}/{tap}/bins?from&to&width` returns at most `width` runs per lane; the view's own payload carries no spans at all, only each lane's `span_count`. The spans were not part of the payload, they were the payload — 12.6 MB of a 12.6 MB JSON on a reference-shaped capture — so first paint is **12.7 KB + 30.5 KB** and a window costs **1–6 ms** end to end. The browser never draws from a window's bins that is not the window it is drawing.

Two view caps: **250,000 rows per view**, reported rather than swallowed, and a name-length limit applied where a name is chosen rather than at submit.

## Verification technique

Two instruments this UI established, both because "tested in Rust, never looked at" is how its worst defects hid:

- **A headless-Firefox harness** that re-evaluates `app.js`'s IIFE body against a real DOM (there is no `node` on this bench) and renders against real serialized server responses. Strip the app's own `DOMContentLoaded` initializer before rendering — it fires *after* an inline harness script and re-renders every panel from fetches that fail under `file://`.
- **Driving the deployed binary itself** with real clicks. The assets are `include_str!`-embedded, so **the deployed artifact is the only thing that can be checked** for anything that depends on them.
