# embarch-ui: editing a bench

**Status:** active, 2026-11-01.

What is true now of phase 3 of [embarch-bench-editor-proposal.md](../../embarch-bench-editor-proposal.md): a bench edited on the Topology tab's canvas and saved to its file, and a repo's part templates edited in the part editor. What it edits: [bench.md](bench.md). Why: decisions 80–89 ([../decisions.md](../decisions.md)). Routes and events: [../interfaces/topology.md](../interfaces/topology.md). Unresolved: [../open/bench.md](../open/bench.md). What the tab shows: [tabs.md](tabs.md).

## On the canvas

The bar gains **+ Part**, opening the parts bin, a drawer down the canvas's left that stays open while parts are placed; **undo** and **redo**; *unsaved changes*; **Save**; and **Checks**, a panel whose button counts the errors and warnings. Under the canvas, the **tray** row lists what is plugged in and on no part. A notice line over the canvas says what an edit did that the drawing does not — a config made, a refusal, a save — until the next edit or a click on it.

- **Placing.** A bin card is dragged onto the canvas, or clicked to land mid-view. Built-ins come first, then this repo's own with *Edit*, the template files that would not load, and *New part…*.
- **Cabling.** Press a free connector, then click another or drag and release on it; every end is drawn by the server's verdict, a refusal saying why. A wired connector selects its cable.
- **Stacking.** A shield dragged near a board's headers snaps on where the server offers it; dragged off, it unmounts.
- **Binding.** A tray chip dropped, or clicked and then a connector clicked, on a `usb-host` connector that carries its function binds it.
- **The inspector** edits the selected part's label, role and board type, flips or deletes it, and unbinds each USB binding; a selected cable can be deleted.
- **Keys.** Del deletes the selection, a part with its cables in every config; F flips; Ctrl/⌘+Z undoes; Ctrl/⌘+Shift+Z or Ctrl/⌘+Y redoes; Ctrl/⌘+S saves; Esc puts down what is in hand ([tabs.md](tabs.md) has the order).
- **New bench…** in the picker asks for a name and creates a bench holding this machine and config `A`.

## The part editor

`assets/bench-parts.js`, served at `/bench-parts.js` and loaded after `bench.js`: one repo template edited in a dialog over the Topology tab, opened by the bin's *Edit* and *New part…*. Its fields: the id (fixed once the file exists), label, subtitle, category, look, width, min height and rows top; a connectors table — id, label, kind, side, a power role on a kind that takes one, max cables; add up to the served cap, move, remove — with the functions a hub-kind connector carries, an interface and the line facts where the vocabulary says (a text fact shown escaped, `\r\n`); and passthrough pairs, whose ends follow a renamed connector and go with a removed one. Beside them, the canvas's own drawing of the template, following every edit. A built-in opens read-only with *Copy to this repo*; a file the server could not load opens on its error. Enter in a field saves.

## Invariants

- **Every verdict while editing is the server's** (81). Every cable verdict and every mount verdict comes from `POST /api/bench/candidates` — a stack plug's `from` answers where its part may mount — and every finding from `POST /api/bench/check`. **The tray's drop targets are the one exception**, picked from served data and re-judged by the save and the check (83).
- **The check runs 250 ms after the last edit, load or config switch**: `bench.js`'s only timer, and no interval. **One that could not run shows `?` and says the findings are unknown**, never "nothing to report".
- **Edits stay in the browser until Save, which names the `version` it read** (80). **A `409` offers Reload only for `x-embarch-refusal: version-changed`**, never an overwrite; any other is a notice in the server's words.
- **Phase 3 writes files only, never Core** (80): `bench.js` calls `/api/bench/*` and reads `GET /api/topology/pickers`, nothing else.
- **Unsaved edits — the bench's, or the part editor's draft — are asked about before a bench, tab, project or desk switch and on reload, and dropped only once the switch lands**, a tab switch at once (84).
- **A save's answer that lands after its bench has gone is dropped whole** (80), and **a project switch takes the old repo's bench, notes and verdicts off at once**, showing `reading…` (84).
- **A Validate verdict is drawn only on the part it was placed on**, taken off with a note when an edit moves the role or the probe, and placed afresh by a new pass, told apart by its `pass` stamp (85).
- **A cable to this machine is bench-level, and any other goes in the config on screen**; the first part-to-part cable on a bench with no config creates config `A`, and the notice says so (82).
- **A tray binding is written as the narrowest spelling that finds the port again**, and one matching several enumerated ports is written and warned as ambiguous (83).
- **The inspector writes only `board`**, never the revision or variant pin, and clearing a role clears it (86).
- **The part editor offers only the served lists, rules and limits** (88). A value a list lacks is kept, marked *(not in this build)* and sent; **every refusal is the server's text verbatim**, naming the field by its path; a number field is text, sent as typed (87).
- **A changed part draft asks before Cancel, Esc or another part replaces it**; a project switch keeps it on screen with Save disabled; leaving the tab closes an unchanged dialog; a `PUT` answered `404` offers *Save as new* (87).
