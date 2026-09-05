# embarch-ui: decisions

**Status:** active, 2026-09-02.

Why the UI is shaped this way. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md).

Decision numbers are permanent and address this sub-project, not a file. Cite them as `embarch-ui decision N`.

| Group | Decisions | What it settles |
|---|---|---|
| [decisions/shape.md](decisions/shape.md) | 1, 2, 3, 9 | One consolidated process, zero-build, the VS Code launcher, the repo |
| [decisions/wiring.md](decisions/wiring.md) | 5, 6 | Every hardware-adjacent call over HTTP to Core; SSE everywhere |
| [decisions/shell.md](decisions/shell.md) | 4, 8 | The six-section shell, fragment navigation, the design system |
| [decisions/debug-tab.md](decisions/debug-tab.md) | 7, 13 | Log streaming, and why `embarch-api`'s logs are a file instead |
| [decisions/topology-tab.md](decisions/topology-tab.md) | 10 (routing) | Signal routing: the one human surface for declaring a wire |
| [decisions/trace-view.md](decisions/trace-view.md) | 10 (trace) | What a trace renders, on which clock, and the load repartition |
| [decisions/trace-chart.md](decisions/trace-chart.md) | 10 (chart) | Zoom, pan, exact aggregation, the study-step row |
| [decisions/trace-transfer.md](decisions/trace-transfer.md) | 18 | Server-side binning: the view asks for the window it draws |
| [decisions/study-designer.md](decisions/study-designer.md) | 11, 12, 14 | Version fields, security level, declared GATT, opening a project |
| [decisions/gatt-capture.md](decisions/gatt-capture.md) | 15, 16, 17 | Per-characteristic taps, characteristic names, the target dialog |
