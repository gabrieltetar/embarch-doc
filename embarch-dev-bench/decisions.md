# embarch-dev-bench: decisions

**Status:** active, 2026-09-02.

Why it is the way it is, split by mission. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-PROTOCOL.md](../DOC-PROTOCOL.md) §7.2–7.4). They address the *sub-project*, not a file, which is what let them move out of `design.md` §3 into these eight files without touching one of the references pointing at them. `scripts/check-decision-refs.py` resolves every one.

| Load this for | Decisions | Size |
|---|---|---|
| [Platform and build system](decisions/platform.md) — one RTOS, west workspaces, the Rust staticlib | 1, 2, 3, 5, 8, 9, 16, 20 | 5.9 KB |
| [Boards](decisions/boards.md) — which board is the bench, and why it changed twice | 4, 10, 24, 26, 43 | 6.7 KB |
| [The Core link](decisions/link.md) — the serial hop, detection, flashing, the handshake, two hardware ceilings | 6, 7, 12, 13, 18, 19, 25, 30, 35, 36 | 9.4 KB |
| [BLE behaviour](decisions/ble.md) — pairing, addressing, scanning, security | 11, 15, 17, 23, 31, 32, 33, 34, 37 | 10.8 KB |
| [Dispatching a study](decisions/dispatch.md) — steps, discovery, monitoring windows | 14, 21, 22, 27, 28 | 8.7 KB |
| [Capture taps](decisions/capture.md) — byte forwarding, notify routing, the tap never closed | 29, 40, 42 | 7.8 KB |
| [Running an `.eap` protocol](decisions/protocols.md) — the state-machine interpreter | 41 | 5.8 KB |
| [Logging](decisions/logging.md) — a framed log backend, and per-study verbosity | 38, 39 | 10.1 KB |

Decisions 9, 13 and 22 are reversals of earlier positions in this same doc and are kept where their subject lives rather than in a separate list; each says what it reversed and why.
