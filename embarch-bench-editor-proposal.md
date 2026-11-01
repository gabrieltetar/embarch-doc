# Proposal: a bench editor that replaces the Topology diagram

**Status:** proposal, 2026-11-01.

Spans `embarch-ui` (almost all of it), `embarch-study-designer` and `embarch-core` (one field each), which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). A USB PD bench is a DUT, a PD partner with a shield, an analyzer in line, a load and a supply, re-cabled by hand between tests; the Topology tab can draw none of it. The owner tried a clickable mockup on 2026-11-01; what it settled is below.

## What is wrong today

**The diagram is three fixed boxes.** `renderTopologyDiagram` (`embarch-ui/assets/app.js`) draws *this machine*, `dev-bench` and `dut` at hard-coded centres, a `serial` line, a `BLE` line and one lane per signal. **A saved bench holds the same three things**: `Profile` in `src/topology.rs` is `dut`, `dev-bench` and `signals`.

**Core already holds what a PD bench needs, and the UI draws none of it**: a role-less bench board ([`embarch-topology` decision 41](embarch-topology/decisions.md)), a signal leaving one (48), an instrument (49), a DUT's bootload ports (36). **The physical half has no home at all**: which DUT port the analyzer sits on, which shield is on the partner, where the load's leads go. `embarch-core` decision 105 counts 25 typed confirmations in one PD session.

## The model

- **Part template**: a kind of device. An `id`, a `label`, a `category` (`computer`, `board`, `shield`, `instrument`, `analyzer`, `probe`, `adapter`), a `look` and its **connectors**. A connector has an `id`, a `label`, a `kind` (`usb-c`, `usb-host`, `banana`, `terminal`, `swd`, `radio`, `stack-socket`, `stack-plug`), a `side` (`left`, `right`, `top`) and `max_cables` (1). A power connector may carry a `power` role (`source`, `sink`, `drp`, `supply`, `load`, `in`, `out`, `pass`). A `usb-host` connector lists the **functions** it carries: `probe`, `vcom` with its interface, `scpi` with the instrument's default line facts, `bootload-app`, `bootload-bootloader`. A `passthrough` pair makes two connectors one bus (the CY4500's). **A template carries no serial** (`embarch-ui` decision 44).
- **This machine is a hub**: it has no ports of its own. Each cable that reaches it is a port, named by what it carries, because **Core finds a device by its USB serial and interface, never by the physical port**.
- **Part instance**: a template placed in a bench, with a position, a `label`, a `role` (`dut`, `dev-bench`, or none for a bench board), an optional `mounted_on`, a `flip`, and the **bindings** of its `usb-host` functions to identities picked from Core's enumeration.
- **Cable**: joins two connectors. **One that ends at this machine is bench-level**, shared by every config, and declares what its bound functions declare, which may be nothing (the CY4500's own link). **Every other cable belongs to a config and is physical only.**
- **Config**: a named set of part-to-part cables. **Switching configs never calls Core** (owner, 2026-11-01).

## Files

**`embarch/parts/<id>.toml`** holds the repo's templates. **The built-ins are TOML embedded in the binary and served by the same route**, with the vocabulary (kinds, which kinds join, power roles, categories, looks): the spec's rule that a vocabulary is served, never restated in `app.js`. **A repo template reusing a built-in's id is refused** (owner, 2026-11-01). **Each built-in's connector list comes from that part's manual or this suite's own docs, never a guess**; the owner chose a generic CY4500 (two USB-C in line, USB to this machine, a neutral case) over the CY4500-EPR's layout.

**`embarch/topologies/<slug>.toml`** gains `[[parts]]`, `[[cables]]` and `[[configs]]`. **`[[signals]]` stays `SignalLink` verbatim**, so the apply path is unchanged. **Today's files still load**: with no `[[parts]]`, the `dut` and `dev-bench` bindings become parts laid out as the BLE template, and the file is rewritten only when saved. **A part whose template is gone renders as *template missing*, never dropped** (decision 44).

```toml
[[parts]]
id = "partner"
template = "nucleo-g0b1re"
label = "pd-bench"              # the bench board's enrolled name
at = [420, 60]
usb.stlink = { probe = "<serial>", vcom = 1 }

[[parts]]
id = "drp"
template = "x-nucleo-drp1m1"
mounted_on = "partner"

[[cables]]                      # bench-level
from = "partner.stlink"
to = "host"

[[configs]]
name = "sink"
cables = [["dut.usb-c-1", "cy4500.in"], ["cy4500.out", "drp.usb-c"]]
```

**Routes** (UI server, JSON shaped as the TOML): `GET /api/bench/vocabulary`; `GET /api/bench/parts`, `PUT /api/bench/parts/{id}`; `GET /api/bench/benches`, `GET`/`PUT /api/bench/benches/{slug}`; `POST /api/bench/check`, which answers a bench and config with its findings. The existing `/api/topology/profiles/…` apply keeps working on the same files.

## What a cable declares

| On the canvas | Core route | When the bench goes live |
|---|---|---|
| A board type on a part holding a role | `PUT /probes/enrolled/{role}/board` | Applied: no identity claim (decision 45) |
| A probe bound on a role's part | `POST /probes/enroll {role}` | **Proposed**, confirmed through the ordinary enroll |
| A probe bound on a role-less part | `POST /probes/enroll`, no role, `name` = its label (`embarch-core` decision 83) | Proposed |
| `vcom` on the dev-bench part's cable | `POST /dev-bench/link` | Applied; deferred while the role is empty |
| A signal on a `vcom` or a bridge | `POST /signals`, `direct` | Applied |
| `scpi` on an instrument's cable | `PUT /instruments`, template line facts as defaults | Applied |
| The bootload pair on the DUT's cable | `PUT /bootload/ports` | Applied |

**Editing the live bench writes through; editing any other bench writes only its file.** Every route exists, and `embarch-core-client` wraps each.

**Making a bench live extends today's apply.** Declarations apply and report one outcome each; enrolments come back as proposals (a file is not evidence about what is plugged in). **Then the report lists what Core holds that this bench does not name**, each with its own Retract; **nothing is retracted silently** (owner, 2026-11-01), because Core's store is machine-wide, not this repo's. **Which bench and config are live is this UI's record, not the repo's**: a shared checkout would otherwise claim another machine's bench.

## The canvas

**A part is drawn as the thing you would look for on a shelf** (owner, 2026-11-01): the template's `look` picks the drawing. This machine is a monitor whose screen lists what is plugged in; a Nucleo-64 is a board with the snap-off ST-LINK strip and header pins; an instrument has a display, a knob and red/black jacks; the analyzer is a small case; a probe is a pod. A port is drawn as its kind: a USB-C receptacle, a plug, a banana pair, a terminal block, a pin header. **A repo template picks one of the served looks**; the generic look is a board.

**A part shows only its wired connectors.** Its free ones appear on intent: the part hovered or selected, or a cable being laid that they would take. **Wired rows come first, so revealing free ones never moves a cable.**

**Both gestures lay a cable**: click-then-click, or drag. While laying, a connector that fits pulses, one of another kind is hidden, and one refused says why.

**A `usb-host` connector glows when its bound identity is enumerated now.** Probes come from the snapshot; serial ports need a server-side poll of `GET /serial-ports`, pushed by SSE (decision 6). **The glow is not a verdict**: decision 45 rejected a moving attach badge as a role's status; a glow claims enumeration, which the poll did check. **Validate stays the only writer of a verdict**, drawn under the part and dropped when a binding changes. A config-level cable is always dashed.

**The canvas is not rebuilt on every snapshot**, or a dragged part vanishes; a snapshot only toggles classes. **The probe pool becomes the tray**: enumerated probes and ports no part binds, dropped onto a `usb-host` connector. Decision 43's three load-bearing properties carry over.

**Shield stacking**: a `stack-plug` dropped near a free `stack-socket` snaps on and the pair moves as one, saved as `mounted_on`. It is a fact about the bench, not a build input (`embarch-dev-bench` decision 48).

## Config slots, and a study that names one

**A host study names a config through a new optional field, `Prompt { text, bench_config }`.** The modal (`embarch-ui` decision 69) draws the change from the current config, cables to unplug and to plug, and **Confirm marks that config current.** A name the live bench lacks renders as unresolved, with the text alone.

**This is the one piece that is not UI-only.** `embarch-study-designer` decision 80 puts `deny_unknown_fields` on every host type, so the field is a type change and a `HOST_TYPE_SCHEMA_VERSION` bump; Core forwards it on `PromptPending` and resolves nothing. *Rejected: a name convention inside `text`*, which a typo breaks silently.

**It is decision 10's indirection, not a breach of it.** A study names what the bench must look like, never which cables do it. **Renaming or deleting a config a study names is refused `409`, naming the studies**; a file the scan cannot read is unscannable, never "no references".

## Rule checks

**Refused while wiring**: a connector of another kind, one already at `max_cables`, a role on two parts, one USB identity bound to two parts, two `source`-only ports on one bus.

**Warned**: two consumers on a bus and nothing sourcing it; an X-NUCLEO-DRP1M1 sourcing with nothing on CN3 (`embarch-dev-bench` decision 49); a shield on no board; a role part with no probe path to this machine; a signal whose origin has no cable path to its carrier. **Warnings, not refusals: the picture must match the wiring "including when the wiring is deliberately unusual"** (decision 10). Every check reads the description, never the hardware.

## Decisions it touches

- **`embarch-ui` 5**: every enumeration the canvas shows comes from Core over HTTP. **10**: the lane geometry goes; the carrier rule is kept and extended to configs. **43**: the drop target moves to a part's `usb-host` connector. **44, 45, 47**: the saved-bench rule stands; a role keeps two bindings; a DUT's board type is still one real scanned combination. **57**: a desk still names one saved bench.
- **`embarch-topology` 41, 48, 49**: a role-less part stays a bench board; a signal leaving it uses `origin_board`; template line facts are defaults only. **No `embarch-topology` change.**

## What is deleted

`renderTopologyDiagram`, `roleNode`, `signalEdges`, the lane and centre constants, the role-box targets in `initEnrollOnDiagram`, and `drive_topology.py`'s diagram checks, rewritten against the canvas.

## Build order

1. **Model and files**: types, built-ins and vocabulary served, today's files loading as parts, the checks. No page change.
2. **A read-only canvas beside the old diagram**: benches drawn by look, reveal on intent, live glow, Validate verdicts on parts.
3. **Editing**: the parts bin, both gestures, refusals and warnings, stacking, the tray, the part editor, save. The live bench writes through.
4. **Making a bench live**: the extended apply, proposals, the retract report. The old diagram is deleted.
5. **Config slots**, then `bench_config` and the modal's drawing with the rename/delete refusal.

## Open questions

- **Where do host studies live in a repo?** None is saved in one today; the rename/delete scan must find a config a study names. Phase 5 needs the answer.
