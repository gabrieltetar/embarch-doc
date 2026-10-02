# embarch-ui decisions: The Atlas tab

**Status:** active, 2026-10-01.

A sixth tab that draws the open project's `embarch-atlas` output: firmware modules, the MCU's peripherals and pins, and every part on every board, as one stacked map. The research it folds in was `embarch-atlas/research/06-ui-concept.md`; git holds it.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 52 — An SVG stack map that draws a file the atlas writes, and decides nothing

The tab reads `<project>/embarch/atlas/atlases/<id>/graph.json` and draws it: flat swimlanes, tiltable to stacked planes, one column per feature cluster. **Clustering and layout run in `embarch-atlas`, not here** (owner, 2026-10-01): agents share the same feature areas, positions are keyed by native ID so a part keeps its place across rebuilds, and this binary only lists atlases and serves files. Read-only, no Core call; layer, kind, status and symbol names are served in the file. It opens on the atlas built at HEAD, else the newest. Requirement links stay hidden until a check for them exists (owner). A selection is a chain up and down the stack; a hub (peripheral, in-tree Zephyr module, the MCU) is shown, not walked through. *Rejected:* three.js (first third-party script, WebGL untestable in headless Firefox); atlas serving its own page (a second localhost UI, against decision 1); a static HTML export (a second renderer, client pages inside a sendable file).

### 53 — Every part is a generic schematic symbol, its pins labelled with the net and the firmware's name

Owner, 2026-10-01. ANSI shapes (zigzag resistor, plates, diode, transistor; an IC or connector is a box) with stubs placed by `embarch-atlas`. **Inside a box: the pin's name (`SDA`), never its package number**, which says nothing here; a connector shows numbers. Outside each stub: the net, then, where the MCU drives that net, its port and DT use (`I2C1_SDA · PB9 · i2c1_sda`). Both boards are drawn, one band each, mated connectors in the first column. **Connections are net labels; a wire is drawn only for the selection**, from beyond the label, and a hub (the MCU, a mated connector) draws none: its nets open one at a time from a label click. Labels exist only when one pin pitch is ≥ 11 px. *Rejected:* wires always (a hairball at ~240 nets); only the MCU's board, others behind a port.

### 54 — Citation tiers open the source; a page is rendered on first request

A problem is rows of claims per source, each with its citation. A document cite opens its card, its tier-2 section, the page with the cited box, or the PDF at `#page=N`; a code cite shows the lines at the atlas's commit, *unchanged/changed since*, and a VS Code link. **The page is rendered by this binary with `pdftoppm` on first request** into `<atlas>/cache/pages/`, not by the atlas build: a build would render hundreds of pages nobody opens, and one render costs ~0.4 s. A cache, not atlas content. Document paths come from the graph's `docs` table, so nothing here parses a PDF or guesses where one is.
