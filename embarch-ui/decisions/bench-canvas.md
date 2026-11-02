# embarch-ui decisions: The bench canvas

**Status:** active, 2026-11-01; 94 added 2026-11-02.

The Topology tab as a canvas drawing a saved bench as the hardware — phase 2 of [embarch-bench-editor-proposal.md](../../embarch-bench-editor-proposal.md), read-only until phase 3 — and the full-screen layout it brought; the old diagram deleted in phase 4 and its jobs done on the canvas (94). What it draws from: [bench-model.md](bench-model.md) (71, 72). Editing on it: [bench-editing.md](bench-editing.md) (80–86). Making a bench live from it: [bench-live.md](bench-live.md) (90–93). The old diagram it replaced: [topology-tab.md](topology-tab.md) (10, 43).

Index: [../decisions.md](../decisions.md). Current truth: [../spec/bench.md](../spec/bench.md).

### 76 — A part is drawn as the hardware on the shelf, showing only what is wired

**A part is drawn as the thing you would look for on a shelf** (owner, 2026-11-01). The template's `look` picks the drawing — this machine a monitor whose screen lists what is plugged in, a Nucleo-64 with its ST-LINK strip and header pins, a dev kit with its antenna, an instrument with a display, a knob and jacks, the analyzer a plain case, a probe or bridge a pod — and a connector's `kind` picks its glyph. **A look or kind with no drawing is drawn as a plain board or a plain port, never dropped**, so a newer server's vocabulary degrades rather than breaks the page.

**A part shows only its wired connectors** (owner); hovering or selecting it reveals the free ones, and **wired rows come first on every side, so revealing never moves a cable.** Stack sockets and plugs are never drawn as ports — a shield sits on its board instead (owner: stacking in the first version) — and which kinds those are is read from the vocabulary (71). **A mounted shield keeps the height of every row it could show and grows upward from its board**, so a row revealed on it pushes nothing.

**This machine's ports are named by what they carry** (owner: a hub): one per cable reaching it, labelled by the far part; with the connector added when two cables come from one part; with `→ <part>` added when that connector carries a probe whose SWD lead reaches another part. They are ordered top to bottom by the far part, so the cables do not cross.

**What cannot be resolved is drawn and says so** — 44's rule that unresolved is never absent. A part whose template is missing or unreadable is a blank dashed outline saying which, with the file's error in its inspector; a connector a cable names that its template lacks is a red-dashed port that still takes the cable; a second part under one id is drawn offset with a note, and no cable or mount can name it; a cable to a part the bench lacks is named in the notes, not drawn.

**Bench-level cables are solid and config cables dashed**, one config at a time from tabs along the bottom. A cable is identified by its two ends, so a selection follows the cable across configs, never the cable at the same index.

### 77 — The glow claims enumeration, Validate stays the only verdict, and a snapshot never rebuilds the canvas

**A `usb-host` connector glows, with its cable and its port on this machine, while its bound identity is enumerated now** (owner, 2026-11-01: a live glow in the first version): a probe among the snapshot's probes; a port among its serial ports by serial, and interface when the binding gives one; a serial-less bridge by VID and PID, only when exactly one port matches, since two is ambiguous. **The glow is not a verdict.** Decision 45 rejected a live attach badge as a role's status because "attached" is not what a human presses Validate to learn; a glow claims only enumeration, which the five-second poll did check.

**Unknown is said, never drawn dark.** Core unreachable puts every glow out; a snapshot carrying `serial_ports_error` puts the port glows out and leaves the probe glows to Core's answer; either way a line on the canvas says which enumeration is unknown. Dark would read as nothing plugged in, which nobody established — the same split as an unreadable signal list (10).

**Verdicts come only from a Validate pass**, which `app.js` sends as an event after a pass and whenever one is dropped: under the part holding a role, or a bench board's part by its probe serial (55), and gone when that role's binding changes.

**A snapshot only toggles classes.** The canvas is rebuilt by a load, a hover, a selection, a config tab, a Validate pass or an edit, never by the poll. Decision 43 had to restore a hover after every five-second rebuild; here there is no rebuild to restore after. Every listener lives on the `<svg>`, hover and selection are state re-applied on each rebuild, `bench.js` holds no interval, and the snapshot reaches it as a document event from `app.js` rather than a second stream (6).

### 78 — The Topology tab is the canvas, full screen, and every other card is a panel over it

**The owner's layout (2026-11-01)**: the canvas fills the tab with no page scroll, so the wheel zooms the bench and never fights the page for it. A bar on top holds the bench picker, the bench's path, **Validate topology** and panel buttons — Signals, Board types, Saved benches, and Old diagram until phase 4 (94). Validate's report is a fifth panel, and once a pass has run a Report button reopens it without a new pass, since it holds the only control that clears a leftover role (45); phase 3 added the editor's controls and a Checks panel (80, 81). **The canvas replaces the diagram for every bench** (owner); until the editor could enrol, the old diagram, its probe pool and its drop targets (43) lived in their panel, which phase 4 deleted (94).

**One panel at a time, anchored under the bar, scrolling inside itself.** Its button, Esc or a press outside closes it — outside meaning not a panel, a panel button, Validate, or a dialog, since the signal, board and enrol dialogs open over their panel and must not close it. **Esc closes the topmost thing**: a Topology dialog first, the way its Cancel does, leaving the panel open. Opening a panel moves focus to its first control; closing it with focus inside returns focus to the button that opened it.

**A link lands on the panel holding what it names**: `#topology?board=` opens the one with the marked row (58) — since phase 4 only when no part on the canvas is marked (94) — and the desk banner's *Review it on Topology*, which opened Saved benches for the apply report, puts the bench on the canvas instead (90). A save or delete there re-reads the canvas, since that panel writes the files it draws, and keeps its zoom, config and selection while the same bench is still listed.

### 94 — The old diagram goes, and the canvas does what it did

**Phase 4 deletes the old diagram** (owner, 2026-11-01: the canvas replaces it, 78): its role boxes, its probe pool, the enrol dialog a drop opened, the role board-type picker, the lane geometry (10), and the Old diagram panel. Each job it did has one home on the canvas:

- **binding a probe** is the tray's (83), and **enrolling it** is confirming what making the bench live proposes (90) — the ordinary `/api/enroll`, whose moved-role sentence (61) is now said on the report's Confirm;
- **a role's board type** is the inspector's (86), and a DUT's build combination its *Build as* (86, amended);
- **retracting a role** is a leftover's Retract in the live report (91), and a role outside the pair still the Validate line that finds it (45);
- **decision 43's three properties** — listeners on the `<svg>`, the target under the pointer as state redrawn on every rebuild, a drop allowed only over a target that takes it — hold for the tray's drop targets alone.

**`#topology?board=` marks the part that is the board** (58): a part holding that role, that board type, or the dev-bench board's served label. **Board types opens only when no part is marked**, and only once the canvas has read a bench, so a board both on a part and in the catalog lands on the part, never on a panel over it. `window.embarchBench.markedParts()` and `settled()` tell `app.js` which, and `embarch:bench-marked` says when to ask again.

**Left without a page caller**, and kept for API callers: `POST /api/topology/roles/{role}/board`, `POST /api/topology/link` and the old apply (90).
