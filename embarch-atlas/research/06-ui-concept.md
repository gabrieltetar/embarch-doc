# The human surface of atlas: a first UI concept

**Status:** draft, 2026-09-29.

A design discussion held before the document-edition backend exists: atlas
widened from code structure to **schematics, datasheets, the MCU reference
manual and the product requirements, joined to the firmware**. The owner's
answers are recorded as held intent, not decisions. Nothing is built, and the
owner will go no further until the backend lands. When `embarch-atlas`
resumes, this note folds into [`../design.md`](../design.md) with the rest of
this folder.

The full-fidelity version sits machine-local, beside the backend research it
was written against, with a clickable mockup. That mockup carries client
names, so it stays off this repo. This copy keeps the concept, the reasoning
and the numbers, with the client specifics replaced by placeholders (`<part>`,
`<driver>`, `<board>`).

## Context this assumes

- **Atlas outputs live in the firmware repo**, under `<fw>/embarch/atlas/`:
  local, and excluded from git.
- **An atlas is fixed to one board and one firmware commit.** There can be
  many.
- **Every fact is cited** (doc + page/section) and cross-checked. A fact that
  fails the check is marked unverified.
- **Datasheet distillations are tiered and board-independent:** short card →
  distilled section → raw page. Wiring comes from the schematic analysis.
- **Agents reach atlas through an MCP server and a CLI.** The UI is the third
  surface, for humans.
- **The first artifacts** are the distilled documents; the pin/net map (MCU
  pin → net → far-end part pin → DT node → driver); and the mismatch report
  (schematic vs. DT vs. code vs. datasheet).

## Owner's answers (2026-09-29)

| Question | Answer |
|---|---|
| When the UI is opened | Reviewing a new atlas; mid-debug across HW/SW; writing a driver. Checking an agent's cited claim was offered and not picked |
| Who reads it | The owner and other firmware developers, each with the full EmbArch suite installed |
| Relation to the agent | **Independent reader.** The UI and the agent never talk; both read the same atlas |
| Where it sits | A browser tab beside VS Code, as embarch-ui already works |
| The picture | *"On the higher level the FW app and how it interacts with other systems, then the middlewares in between the app and driver, underneath the drivers the different components and how they are interconnected. One area of the map is a feature; on top is the high-level code and on the bottom the components and the signals."* |
| Feature areas | Graph clustering |
| Layers | External systems + requirements; app; middleware; drivers; SoC peripherals + pins; components + signals |
| Devicetree | **Not a layer.** *"The atlas is going to replace the DT, kind of, in a more extensive way; it's two separate concepts. The disagreement is on the atlas generated from the DT, not the DT itself."* |
| Other boards and units | *"Just as a simple incoming signal through the port; explain what is plugged there."* |
| Component granularity | Everything: every resistor, capacitor and test point is drawn |
| A node on a code layer | A module; zooming in reveals its functions |
| Mismatch triage | Centre the map on the problem, in red |
| Triage verdicts | None. The UI is read-only |
| Unverified facts | Dashed outline, amber, and flagged in the panel |
| Citations | Tiered, like the docs: card → distilled section → page → raw PDF |
| Code citations | Jump into VS Code |
| What it opens on | The whole map with the problem count; next/previous walks from one problem to the next |
| Comparing two atlases | Later |
| Rendering | *"What would look good but be simple enough?"* The recommendation below was taken |

## Concepts, ranked

1. **An Atlas tab in embarch-ui, drawn as a projected SVG stack map. Chosen.**
   The binary reads the open project's atlas directory and computes the layout
   server-side. The browser projects it into flat swimlanes or tilted 3D
   planes. It fits every embarch-ui constraint: no library (so
   [embarch-ui decision 2](../../embarch-ui/decisions/shape.md) holds
   untouched), one binary, and no Core call at all. It costs a file contract
   with a backend whose stack is still open, and one more tab in `app.js`.
2. **The same tab drawn with three.js (WebGL).** Free orbiting, and smoother
   past about 2,000 nodes. It would be the first third-party script inside the
   binary (~700 KB, embedded the way the fonts are), which amends decision 2.
   Clicks need ray-casting and labels need sprites. Headless Firefox renders
   WebGL in software, so the browser tests the UI relies on would be
   unreliable.
3. **Atlas serves its own page** (`embarch-atlas serve`, next to its MCP
   server). The backend's stack stays free of embarch-ui's. But it is a second
   localhost UI, against embarch-ui decision 1 ("one UI for the whole
   project"). It only pays off for readers without the suite, and there are
   none.
4. **A static HTML export per atlas.** Needs no server and can be sent. But it
   is a second renderer to keep in step, and client page images travel inside
   the file. Worth adding later as an export of concept 1.

A VS Code webview was not proposed: embarch-ui decision 3 already rejected it,
for reasons that hold here.

## The concept

### Where it lives

A sixth embarch-ui tab, `#atlas`. It reads files in the **open project**, and
with none open it refuses, naming the project control, like every other
project-scoped surface. It touches no hardware and makes **no Core call**, so
it keeps working when Core is unreachable. The invariants embarch-ui already
holds carry over unchanged:

- A page explains nothing it can show.
- A vocabulary is served, never restated in `app.js`: layer names, node kinds,
  check classes, statuses.
- Unreadable renders as unreadable. A section not yet distilled says so; it is
  never an empty panel.
- The UI never decides what counts as verified. It renders the status the
  atlas stored.
- A fragment names a tab and nothing else, so there are no deep links to a
  node. That matches "independent reader".

### Layers

| Layer | A node is | Comes from |
|---|---|---|
| External + requirements | An external system (a mating unit, a host device, a battery), and a requirements section | the requirements doc; interface records |
| App | A module under the app directory | `compile_commands.json`, the source tree |
| Middleware | A project library, or a Zephyr subsystem the build enables | same, plus `.config` |
| Drivers | An out-of-tree driver, or an in-tree Zephyr driver the build compiles | `DT_DRV_COMPAT` in the TUs; the ELF |
| SoC peripherals + pins | An enabled peripheral and every MCU pin | the build's EDT, the MCU datasheet pin table, the SVD |
| Components + signals | Every part on the board; **nets are the edges between them** | the schematic netlist and BOM |

**Devicetree is not drawn.** A DT node appears as the label on a **binding
edge**, the link from a driver to the part it drives (`<part>@<addr>`). A
property appears as the label on a driver → pin edge (`enable-gpios`). When
the atlas's firmware-side model (from DT and code) disagrees with its hardware
side (from the schematic and datasheets), the mismatch marks the atlas entity:
the pin, the part or the link. The DT line sits in the evidence panel as one
citation among the others.

**Feature areas** are the clusters of a community-detection pass over the
cross-layer graph. Each cluster is one column that runs through every plane.
A cluster has no human name, so it is labelled after its most-connected part
or driver. That label is a fact about the graph, not a claim about what the
feature does, and the inspector calls it a cluster, never a feature.

### Projection

Each node has a world position `(x, y)` on its layer's plane and a layer
index `L`. One parameter `T` runs from flat (0) to 3D (1). The elevation `e`
goes from 90° down to 36°, and a small yaw `ψ` from 0 to −9°. `Z` is the
layer's height and `S` the spacing between the flat bands:

```
x' = x·cos ψ − y·sin ψ
y' = x·sin ψ + y·cos ψ
screen = ( x', y'·sin e − Z·cos e + L·S·(1 − T) )
```

At `T = 0` that is swimlanes. At `T = 1` it is stacked planes, seen from above
and in front. It is about 15 lines of orthographic JavaScript. Nodes are
billboards: they stay upright at every tilt, so labels stay readable. Pan is a
drag, zoom is the wheel at the pointer, and a key animates the tilt.

**The layout is computed server-side and is the same on every load.** Clusters
give x-ranges. Nodes are placed inside their cluster and layer by a seeded
pass, and positions are keyed by the node's native ID. So a part keeps its
place across reloads, and later across two atlases, which makes a diff view
cheap. It is the division of labour the trace chart already uses (embarch-ui
decision 18): the server shapes the data, the browser draws it.

### Scale

The MCU board of the first target product is roughly 500 parts, 1,300 pins
and 240 nets. The map is therefore about 700 nodes and 1,300–1,500 edges.
That is within what SVG handles here: the trace chart redraws ~2,500 rects in
27 ms. The real tab should pan by moving one group transform and re-project
only on a tilt. The mockup re-projects everything on every frame, which is
fine at its 200 nodes and not at 2,000.

### Level of detail

| Zoom | Shown |
|---|---|
| overview | Module, peripheral, part and port boxes; parts by part number; subtitles hidden |
| mid | Pin names |
| deep | Each module's public functions, and the designators of passives and test points |

### Selection is a chain

Clicking a node highlights its chain up and down the stack and dims the rest.
The inspector lists the chain one row per layer, each item clickable and
labelled with the net or DT node that links it. Three rules keep one part from
lighting up the whole board. All three were found by running the mockup:

1. **A shared hub is shown but not walked through.** Hubs are bus peripherals
   and in-tree Zephyr drivers; otherwise one part on a bus lights up every
   other part on it. The exception: a selected pin opens its own peripheral.
2. **Neighbours on the board are shown, not followed.** One hop along a
   board-level net, then stop. Passives appear only around a part the chain
   actually reached.
3. **The driver-to-part binding is its own edge**, labelled with the DT node,
   and drawn only while it is on a chain. Without it, a bus-only part's
   driver is reachable only through the hub rule 1 closes.

### Other boards and units

Per the owner, a board-to-board connector or a unit-to-unit interface is drawn
as a **port**: a node on the component plane that signals come in through. Its
card has two parts:

- **What is plugged there:** the other board, and each far-end part per
  signal, in the pin map's own format (`<board>:<ref>-<pin> via
  <board>:<conn>-<n> → <board>:<conn>-<m>`).
- **The interface record:** kind (`ffc`, `wire`, `pogo`), which connectors
  mate, the pin map (e.g. `reversed:<n>`), the source (engineer-declared or
  name-inferred), and the agreement check (`k/n names agree`).

An interface that is only inferred renders amber until the engineer declares
it. IDs are board-qualified everywhere (`<board>:<ref>`): on the first target,
hundreds of designators repeat across the boards, with different parts behind
them.

## Problems

- **The map opens fitted**, with a red mismatch count and an amber unverified
  count. Next/previous centres the map on each problem, pulses it and opens
  its evidence.
- **"Checks run" comes before the problems.** On the first target, the
  valuable output of the join was what *passed*: every I²C device matched to
  its address strap, every signal GPIO landing on its DT pin. About two thirds
  of the ~100 candidates were one expected class, "connected pin with no DT
  use". So the default panel lists each check class with its pass count, and
  folds the expected findings (debug pins, test-point-only nets) into a count.
- **A mismatch's evidence is a table of sources:** schematic, firmware,
  datasheet. Each row is that source's claim, with its own tiered citation
  underneath. The disagreement reads without opening a document, and each
  claim is one click from its page.
- **Unverified** means a fact failed its cross-check: dashed, amber, flagged.
  Red is kept for real disagreements between sources.

## Citations

| Tier | What opens | From |
|---|---|---|
| Card | The fact's line from the part's card | tier-1 file |
| Section | The distilled section file, verbatim | tier-2 file |
| Page | The page image with the cited region boxed | a page render plus the fact's bbox |
| PDF | The raw PDF at `#page=N`, in the browser's own viewer | served by the binary from the atlas's document store |

- **The page coordinate is the physical 1-based PDF index**, the same one the
  agent-side tools use.
- **Schematic facts can carry an exact box.** An Altium Smart-PDF export
  places an invisible anchor word on every pin, part, net label and port, and
  each anchor has a bbox.
- **Datasheet facts get a box only where the extractor kept one.** Without
  one, the page shows unboxed, never with a guessed box.
- **A code citation** shows a short excerpt and an **Open in VS Code** link
  (`vscode://vscode-remote/wsl+<distro>/<path>:<line>`). Beside it is one
  state, *unchanged since <atlas commit>* or *changed since*, from
  `git diff --quiet <commit> -- <path>`. A changed file still opens, and the
  state says the line may have moved.
- **Documents are served from localhost only.** The page loads nothing
  external, and client material never leaves the machine.

## What the UI does not do

- Write anything: no verdicts, notes or edits to the atlas.
- Start a build, an atlas update or an agent session.
- Draw the devicetree.
- Compare two atlases (later; the stable layout keeps that door open).
- Touch hardware or Core.

## What it needs from the backend

The agent-side MCP surface answers one question at a time (trace one pin,
page through the mismatch report). A map needs the whole graph at once. These
requirements are for whoever designs the backend:

1. **A graph export per atlas.**
   - Nodes: stable native ID, layer, kind, label, status (verified,
     unverified, mismatch), provenance (exact, heuristic, inferred,
     engineer-declared, llm-inferred).
   - Edges: kind (dependency, binding, net, interface), net name or DT node,
     status, provenance.
   - Best as a JSON file written next to the store. embarch-ui already has
     `serde_json`, while reading a SQLite store would add a C-compiled
     dependency.
2. **An atlas index:** each atlas's board, commit, build date and source
   hashes.
3. **A checks-run summary** per class, with pass and fail counts.
4. **Mismatch records** as claim-per-source rows, each with a citation, plus
   the IDs of the entities they mark.
5. **Structured citations:** doc ID + hash + physical page + section ID +
   bbox where known; for code, path + line at the atlas commit.
6. **A page render** of every page a fact cites, so the UI never parses a
   PDF.
7. **Public function lists per module**, for the deepest zoom.
8. **Interface records** in the shape above.

## Rough effort, once the backend emits the export

| Part | Estimate |
|---|---|
| Server: atlas index, graph load, clustering and layout, tier-file and page routes, git state for code links | about 2 days |
| Browser: projection, level of detail, chain walk, inspector, tiers | 3–4 days |
| `tests/browser/` coverage through geckodriver | about 1 day |

These are planning numbers, not measurements.

## Open questions

1. **In a multi-board product, which boards fill the component plane?** Only
   the MCU's board, with the rest behind their connector ports (the literal
   reading of the owner's answer, and what the mockup draws)? Or every board?
   The pin map traces far ends across boards either way, so only the drawing
   differs.
2. **Where does clustering run?** In the UI server, as presentation? Or in the
   backend, so agents share the same feature areas? And should clusters be
   pinned across atlases, so a diff does not reshuffle the columns?
3. **Requirement links will be inferred, and so amber.** The landscape survey
   found no evidence of reliable doc → existing-code link recovery on
   firmware. Accept an amber top layer, or hide requirement links until a
   check for them exists?
4. **Which atlas opens by default:** the newest for the open project, or the
   one whose commit is nearest HEAD?
