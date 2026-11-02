# embarch-ui: the bench editor

**Status:** active, 2026-11-01.

What is true now of the bench editor's model, its files and routes (phase 1) and the canvas the Topology tab now is (phase 2). Editing it, phase 3, and its config slots, phase 5: [bench-editing.md](bench-editing.md); making it live, phase 4, and which config is live: [bench-live.md](bench-live.md); a host study's prompt naming a config: decision 99. Why: decisions 71–79 ([../decisions.md](../decisions.md)). Routes and events: [../interfaces/bench.md](../interfaces/bench.md). Unresolved: [../open/bench.md](../open/bench.md). What the tab shows: [tabs.md](tabs.md).

## The model

- **A part template** is a kind of device: an `id` (a slug, and its file name), a `label`, a `category`, a `look`, and the connectors a human would cable. A connector has a `kind`, a `side`, `max_cables` (1 unless stated), optionally a `power` role, and on a `usb-host` the functions it carries to this machine: `probe`, `vcom` (with its interface when known), `scpi` (with the instrument's default line facts), `bootload-app`, `bootload-bootloader`. A `passthrough` pair makes two power connectors one bus. **A template carries no serial** (44).
- **Twelve built-ins**, TOML embedded in the binary: `this-machine`, `nucleo-g0b1re`, `x-nucleo-drp1m1`, `x-nucleo-snk1m1`, `cy4500`, `nrf54l15dk`, `debug-probe`, `usb-uart-bridge`, `usb-c-breakout`, `bench-supply`, `scpi-load`, `generic-board`. **A repo adds its own** as `embarch/parts/<id>.toml`.
- **This machine is a hub**: `this-machine` has `hub = true` and no connectors, and each cable that reaches it is a port.
- **A bench** is `embarch/topologies/<slug>.toml`, the saved bench (44) with three more lists: `[[parts]]` — a template placed, with an `id`, `label`, `at`, `role` (`dut`, `dev-bench` or none for a bench board), `mounted_on`, `flip`, `board` (the role's board type) and `usb`, the identity each function on each connector is bound to; `[[cables]]`, the bench-level ones, each ending at this machine and shared by every config; and `[[configs]]`, each a name and its part-to-part cables. `[[signals]]` is `SignalLink`, as before. A cable end is `<part>.<connector>`, or `<part>` alone for a hub.
- **Legacy files**: one with no `parts` key loads with its `dut` and `dev-bench` laid out as the BLE dev bench (73).

## The canvas

The Topology tab is the canvas, full screen (78): the bench picked in its bar, drawn as the hardware (76) with a live glow and Validate's verdicts (77), and edited there ([bench-editing.md](bench-editing.md)). The Saved benches panel still saves the old shape from what Core holds, refusing a file with parts (74); its Open puts a bench on the canvas (90).

## Invariants

- **The vocabulary is served, never restated in browser code** (the spec's rule for every vocabulary): kinds, which kinds join, the hub's kind, power classes, categories and which are bench boards, looks, functions and what a config may be called come from `GET /api/bench/vocabulary`, the same lists a file is parsed against (71). Which kinds are never cabled is derived from it, not listed in `bench.js`.
- **No bench route but making a bench live calls Core, and none reads hardware.** The checks read the description, never the bench in front of you (72); making a bench live is [bench-live.md](bench-live.md)'s (90).
- **Every `/api/bench` route refuses `409` with no project open, whatever the body** — the vocabulary and the built-ins included, since empty lists would read as "this repo has no benches".
- **A repo template reusing a built-in's id is refused**: `409` on a write, an `errors` entry on a read (71).
- **A file that will not load is listed in `errors`, never dropped**, and so is a directory that cannot be read and a file name no route could address; an entry about one template or bench names its `id` or `slug`, so a part using an unreadable template says *unreadable*, not *missing*.
- **Reading never rewrites.** A legacy file is written in the new shape only when it is saved (73).
- **A save names the `version` it read and never renames**; nothing is written outside the repo, through a link, or before its bytes read back as what was saved (74).
- **A save refuses only what makes a file unreadable or ambiguous** — a cap, two parts under one id, a `usb` key that is no connector, two configs under one name, a config name no host study could write (97), a name with no letter or digit. A broken rule is a finding, so a bench that breaks one still saves (72).
- **A snapshot only toggles classes on the canvas, never rebuilds it.** A load, a hover, a selection, a config tab, a Validate pass or an edit rebuilds it, so a selection or a hover survives the poll (77).
- **The glow means a bound probe or serial port is enumerated now, and is not a verdict.** A serial-less `{vid, pid}` binding glows only when exactly one enumerated port matches; two is ambiguous and nothing glows. **Core unreachable, or a snapshot carrying `serial_ports_error`, makes port glows unknown and says so in words**, never the dark of nothing plugged in; probe glows follow only whether Core answered (77).
- **Verdicts are drawn only from a Validate pass**, under the part holding the role or a bench board's part by its probe serial, and dropped when that role's binding changes (45, 77), an edit moves it off the part they were placed on (85) or a make-live changes its board type or link (93).
- **`bench.js` holds no interval**; `drive_bench.py` checks it.
- **What cannot be resolved is drawn, never dropped**: a part whose template is missing or unreadable, a connector a cable names that its template lacks, a second part under one id (76).
