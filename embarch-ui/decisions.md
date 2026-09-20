# embarch-ui: decisions

**Status:** active, 2026-09-02.

Why the UI is shaped this way. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md).

Decision numbers are permanent and address this sub-project, not a file. Cite them as `embarch-ui decision N`.

| Group | Decisions | What it settles |
|---|---|---|
| [decisions/shape.md](decisions/shape.md) | 1, 2, 3, 9, 28 | One consolidated process, zero-build, the VS Code launcher, the repo; Start focuses the window and tab already open, matched on the page title |
| [decisions/wiring.md](decisions/wiring.md) | 5, 6, 24, 26 | Every hardware-adjacent call over HTTP to Core; SSE everywhere; the static element-id guard; Core-unreachable as a renderable state, not a crash |
| [decisions/shell.md](decisions/shell.md) | 4, 8, 25, 42 | The shell's sections, fragment navigation, the design system, the brand-vs-accent split, and the typefaces served by the binary rather than a CDN |
| [decisions/debug-tab.md](decisions/debug-tab.md) | 7, 13 | Log streaming, and why `embarch-api`'s logs are a file instead |
| [decisions/topology-tab.md](decisions/topology-tab.md) | 10 (routing), 43 | Signal routing: the one human surface for declaring a wire; and enrolling a board by dropping a probe onto the diagram, the Enroll tab folded in |
| [decisions/topology-boards.md](decisions/topology-boards.md) | 44 | A role is a fixed slot and a board is a name: the project's board catalog, retracting a role, saved benches that propose rather than enrol, and the validate pass that replaced the alert list |
| [decisions/trace-view.md](decisions/trace-view.md) | 10 (trace), 27 | What a trace renders, on which clock, the load repartition, and why the decode-to-lanes pipeline stays duplicated with `embarch-core`'s `outpost_load.rs` |
| [decisions/trace-rows.md](decisions/trace-rows.md) | 19, 21 | Dropping a stale pre-reset head, and the served row cap |
| [decisions/trace-chart.md](decisions/trace-chart.md) | 10 (chart) | Zoom, pan, exact aggregation, the study-step row |
| [decisions/outcome-decode.md](decisions/outcome-decode.md) | 23 | One outcome decoder for both wire shapes |
| [decisions/trace-transfer.md](decisions/trace-transfer.md) | 18 | Server-side binning: the view asks for the window it draws |
| [decisions/study-designer.md](decisions/study-designer.md) | 11, 12, 14, 20, 22 | Version fields, security level, declared GATT, opening a project, the run badge's counter, the stream-name cap |
| [decisions/designer-panels.md](decisions/designer-panels.md) | 41 | The Study Designer's panel layout: one apply-study path, build options behind a button, static firmware analysis as an explicit action, one "Define the wire" panel |
| [decisions/firmware-build.md](decisions/firmware-build.md) | 38, 39, 40 | A study builds its own DUT firmware: the ordered snippet picker, the three-state outpost mode, the build as a phase of a run, where its log is read, and when a saved study's version is rewritten |
| [decisions/study-authoring.md](decisions/study-authoring.md) | 29, 30 | The `.eap` editor dialog, and running a saved study as it is on disk |
| [decisions/gatt-capture.md](decisions/gatt-capture.md) | 15, 16, 17 | Per-characteristic taps, characteristic names, the target dialog |
| [decisions/time-chart.md](decisions/time-chart.md) | 34, 35, 36, 37 | One axis for every stream a study produced: `core_rx_utc_ms` as the only clock read, a tier chosen once and never promoted, and the three states of a mark |
| [decisions/live-study.md](decisions/live-study.md) | 31, 32, 33 | One tab that runs a study and reads one back: the server-side session rings, the console rule, and what the browser is handed already decoded |
