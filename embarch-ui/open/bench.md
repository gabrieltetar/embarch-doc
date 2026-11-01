# embarch-ui open: the bench editor

**Status:** active, 2026-11-01.

Unresolved in the bench editor's built half. Current truth: [../spec/bench.md](../spec/bench.md). Index: [../open.md](../open.md).

- **The two PD shields' power connectors are drawn as `terminal`, unconfirmed.** `embarch-dev-bench`'s pd-bench README gives the X-NUCLEO-DRP1M1's CN2 and CN3 as two-pin power connectors (UM2891 Fig. 9) and the X-NUCLEO-SNK1M1's VBUS output, but neither's physical type, so both built-ins carry the generic two-wire kind and say so in a comment. A wrong kind draws the wrong glyph and lets the wrong cable join. **Trigger:** UM2891 and the SNK1M1's manual read for the connector type, and each built-in corrected from them.

- **No built-in board has a connector a signal can ride part to part**, so a legacy BLE bench with a `via-dev-bench` signal warns `signal-no-path`: its DUT is drawn as the generic board, whose one connector is USB to this machine, and a signal path never runs through this machine (decision 72). The warning is right about the description and says nothing about the wire. **Trigger:** a repo template for that DUT with the pin header the bench wires, and the cable drawn; phase 3's editor is the first surface that can draw it.

- **The old `/api/topology/profiles/{slug}` delete and apply still slugify the URL path**, where every `/api/bench` route refuses a path that is not a slug with `400`: `Bench-A` reaches `bench-a` there. **Trigger:** phase 4, which replaces apply; or the next change to either route.

- **Unknown keys in a bench file are dropped when it is saved** — in a legacy role table, a part, a cable, a config or the top level — because a bench loads tolerantly (decision 44's "tolerant on the load path") and is written from what was loaded (decision 73). A part template is strict, so it is listed instead. **Trigger:** the first hand-added key someone expects the editor to keep.

- **At phone width the shell's fixed sidebar leaves the canvas little room**: in a 480 px window the stage is 264 px wide [measured 2026-11-01, `drive_bench.py`]. A panel spans the stage, but more room is a shell change for every tab, not this one's. **Trigger:** the UI used on a phone or a narrow window.
