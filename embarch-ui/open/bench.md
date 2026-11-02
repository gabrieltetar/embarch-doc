# embarch-ui open: the bench editor

**Status:** active, 2026-11-01.

Unresolved in the bench editor's built half. Current truth: [../spec/bench.md](../spec/bench.md). Index: [../open.md](../open.md).

- **The two PD shields' power connectors are drawn as `terminal`, unconfirmed.** `embarch-dev-bench`'s pd-bench README gives the X-NUCLEO-DRP1M1's CN2 and CN3 as two-pin power connectors (UM2891 Fig. 9) and the X-NUCLEO-SNK1M1's VBUS output, but neither's physical type, so both built-ins carry the generic two-wire kind and say so in a comment. A wrong kind draws the wrong glyph and lets the wrong cable join. **Trigger:** UM2891 and the SNK1M1's manual read for the connector type, and each built-in corrected from them.

- **No built-in board has a connector a signal can ride part to part**, so a legacy BLE bench with a `via-dev-bench` signal warns `signal-no-path`: its DUT is drawn as the generic board, whose one connector is USB to this machine, and a signal path never runs through this machine (decision 72). The warning is right about the description and says nothing about the wire. **Trigger:** a repo template for that DUT with the pin header the bench wires, and the cable drawn; the part editor and the canvas can now draw both (80, 87).

- **The old `/api/topology/profiles/{slug}` delete and apply still slugify the URL path**, where every `/api/bench` route refuses a path that is not a slug with `400`: `Bench-A` reaches `bench-a` there. **Trigger:** phase 4, which replaces apply; or the next change to either route.

- **Unknown keys in a bench file are dropped when it is saved** — in a legacy role table, a part, a cable, a config or the top level — because a bench loads tolerantly (decision 44's "tolerant on the load path") and is written from what was loaded (decision 73). A part template is strict, so it is listed instead. **Trigger:** the first hand-added key someone expects the editor to keep.

- **At phone width the shell's fixed sidebar leaves the canvas little room**: in a 480 px window the stage is 264 px wide [measured 2026-11-01, `drive_bench.py`]. A panel spans the stage, but more room is a shell change for every tab, not this one's. **Trigger:** the UI used on a phone or a narrow window.

- **A tray drop target gets no server verdict, and the binding's spelling is the browser's** (decision 83): `bench.js` picks the connectors a chip may land on from served templates, and writes serial, `{serial, interface}` or `{vid, pid}` itself. The save and the next check re-judge the file, so a wrong pick is caught after it, not refused before. **Trigger:** a binding the browser offers that the check then flags, or a second surface needing the same spelling — then a route answers both.

- **The inspector writes a role's board type but not its build combination** (decision 86): the revision and variant pin in `embarch/boards.toml` is still picked on the Old diagram's role box (47), which phase 4 deletes. **Trigger:** phase 4; the pin needs a home on the canvas before that panel goes.

- **The canvas does not edit `[[signals]]`.** A bench's signals are written back as they were read, and declaring one is still the Signals panel's, which writes Core (10). **Trigger:** phase 4, where a signal on a `vcom` or a bridge declares from the drawing.

- **A changed part draft kept open by a project switch offers no way to carry it over** (decision 87): its Save is disabled, and moving the template to the new repo means copying it out by hand. **Trigger:** the first time someone needs a template in a second repo.
