# embarch-ui decisions: Editing a bench

**Status:** active, 2026-11-01.

Editing on the Topology tab's canvas — phase 3 of [embarch-bench-editor-proposal.md](../../embarch-bench-editor-proposal.md): what an edit may decide in the browser, where a new cable goes, the tray, leaving unsaved edits, when a Validate verdict stays drawn, and what the inspector writes. The canvas it edits: [bench-canvas.md](bench-canvas.md) (76–78). The part editor: [part-editor.md](part-editor.md) (87). The model and the routes: [bench-model.md](bench-model.md) (71, 72, 88) and [saved-benches.md](saved-benches.md) (73–75).

Index: [../decisions.md](../decisions.md). Current truth: [../spec/bench-editing.md](../spec/bench-editing.md).

### 80 — Edits stay in the browser until Save, and Save writes the file and nothing else

**An explicit Save, with undo and redo in the browser** (owner, 2026-11-01). Every edit changes the bench held in the page, undo reaches back to the last load, and the bar says *unsaved changes* until **Save** — the button or Ctrl/⌘+S — `PUT`s the bench naming the `version` it read (74). Content is compared in one canonical spelling, so undoing back to what the file says is no change. **Phase 3 writes files only** (owner, 2026-11-01): the live bench's write-through moved to phase 4, so no gesture on the canvas calls Core.

**A `409` offers Reload only when the file changed on disk, never an overwrite**, which would put the page's copy over a hand edit it never read. Every bench route's `409` names which it is in `x-embarch-refusal` — `version-changed`, `unparseable`, `rename`, `exists`, `builtin-id`, `no-project` — beside the sentence, so the browser keys on a word, not on wording; only `version-changed` is cured by reading the file again, and any other is said in the server's words.

**A save's answer is about the bench it was sent for.** One landing after that bench has left the screen — a project switch made from another window, which could not ask — is dropped whole: no version adopted, no dialog about the old repo's file over the new one.

### 81 — Every verdict while editing is the server's, a shield's included

**Laying a cable decides nothing in the browser** (72). Pressing a free connector asks `POST /api/bench/candidates` for the unsaved bench and the config on screen, and every end is drawn by its verdict: `ok` pulses, `refused` is red with its sentence beside the pointer and in a notice when picked, `hidden` is not revealed. Both gestures lay one (owner): click then click, or drag and release. While a `usb-host` cable is laid the hub shows a *new USB* slot carrying the server's verdict for the hub. **An edit ends a cable being laid**, since its verdicts were for the bench before it.

**A shield stacks by the same route** (owner: stacking by gesture). Asked from a stack plug, `candidates` answers where its part may be mounted — each stack socket on another part `ok`, or `refused` when that board already carries what its sockets take or sits on the part being placed — and everything else `hidden`, from one mount map and one walk per request, so 72's "indexed once per request" holds. **A dragged shield snaps only onto a board the server offered, within 70 units of where it would sit**; a refused board close by says why, and dragged off a board it unmounts. A part dropped from the bin is asked about the same way. A `candidates` call that fails says it could not ask, and the shield lands unmounted. `mounted_on` stays a fact about the bench, not a build input (`embarch-dev-bench` decision 48).

**Findings come from `POST /api/bench/check`**, 250 ms after the last edit, load or config switch — `bench.js`'s one timer, a debounce and not a poll. Errors and warnings mark the parts and cables they name, and a Checks panel, one more panel over the canvas under 78's rules, lists them. **A check that could not run is unknown, `?`, never "nothing to report".**

### 82 — A cable to this machine is bench-level, any other goes in the config on screen, and the first makes config A

Within 72's rule that a config holds only part-to-part cables (owner): **a cable ending at the hub joins `[[cables]]`, and every other goes into the config on screen** (owner, 2026-11-01). **A bench with no config gets one, `A`, with its first part-to-part cable, and a notice says so** (owner). **Adding, renaming and deleting a config is phase 5** (owner, 2026-11-01).

**A new bench is `POST`ed holding this machine — the first served built-in that is a hub — at `[20, 110]`, and config `A`**, from the picker's *New bench…*, which asks about unsaved edits first. **A placed part takes its template's id, or the first free `<id>-<n>` from 2**, so a cable end can name it and nobody types one. Deleting a part takes its cables in every config — unless another part still answers to its id — and lifts the shields on it where they stand.

### 83 — The probe pool becomes the tray, the one place the browser picks a target

**Decision 43's pool is a row under the canvas**, so it never covers a part: the probes and serial ports the snapshot lists that no part binds. Unknown is said — Core not answering, ports not listed — never an empty tray. **A chip is dropped, or clicked and then a connector clicked, on a `usb-host` connector whose template carries the function**: a probe where it carries `probe`, a port where it carries any other, a dialog asking which when it carries several. **This is the one place `bench.js` picks targets itself**, from served data, because no route judges a binding; the save and the next check re-judge the file (`binding-bad-connector`, `binding-bad-function`, `usb-identity-twice`). 43's three properties carry over: the `<svg>`'s listeners, the connector under the pointer as state redrawn on every rebuild, and a drop allowed only over a connector that takes the item.

**A binding is written in the narrowest of 73's spellings that finds the port again**: a probe or a port by serial; `{serial, interface}` when sibling ports share that serial; `{vid, pid}` for a serial-less port, plus `interface` when another serial-less port shares them. A port with neither serial nor VID/PID cannot be dragged. **A binding matching more than one enumerated port is written and warned as ambiguous**, never refused.

### 84 — Unsaved edits are asked about before they are left, and dropped only where the switch lands

**Leaving unsaved edits asks first** (owner, 2026-11-01): another bench, *New bench…*, another tab, another repo, or a desk on another repo opens the editor's dialog — *Discard changes* or *Keep editing* — and a reload or a closed tab gets the browser's own prompt. The part editor's changed draft counts too, and one Discard drops both. **Nothing goes until the switch happens**: a bench or project that loads replaces the edits; a repo path that will not open, or a Cancel on a new bench's name, keeps them; only a tab switch, which cannot fail, discards at once. A save on its way is waited for first — a discard under it would leave the old content marked unsaved for the next Save to write back. Closing the desk, or opening one on the same repo, asks nothing.

**A project switch takes the old repo's bench off at once**, its file errors and Validate's verdicts with it, `reading…` until the new repo answers, so nothing can save it into the new repo. One made from another window could not ask, and a note under the canvas says the edits were not saved.

### 85 — A Validate verdict stays on the part it was placed on

Extends 77. **A verdict is placed when a pass's verdicts arrive or a bench loads** — on the part holding the role, or a bench board's part by the probe it binds — **and drawn only while that part still holds it.** A role edit, a tray bind or an unbind never moves one onto a part Validate never checked; an edit that moves the role or the probe takes the verdict off, and a note under the canvas says which and to validate again. **Each pass carries a stamp** (`pass` on `embarch:verdicts`), new per pass and unchanged while a verdict is merely dropped, so a second pass with the same words re-places every verdict: it checked the bench as it stands.

### 86 — The inspector writes a part's board type, never its build combination

The floating inspector (76) edits the selected part: its label, its role from the served `roles`, its board type, flip, delete, and an unbind per USB binding. **The board type is picked from `GET /api/topology/pickers`** — the catalog for `dut`, the supported pair for `dev-bench`, as the role picker reads them (45) — **and only `board` is written.** The revision and variant pin stays in `embarch/boards.toml` (47): the inspector shows what the scan builds the board as and edits none of it ([../open/bench.md](../open/bench.md)). **Clearing a role clears its board type**, which is the role's (45).
