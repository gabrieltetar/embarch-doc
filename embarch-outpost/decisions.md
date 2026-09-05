# embarch-outpost: decisions

**Status:** active, 2026-09-02.

Why it is the way it is, split by mission. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). `scripts/check-decision-refs.py` resolves every one.

| Load this for | Decisions |
|---|---|
| [The module and its boundary](decisions/module.md) — a Zephyr module in someone else's firmware | 1, 14, 21 |
| [What gets traced](decisions/tracing.md) — kernel hooks, markers, and keeping itself out of its own trace | 2, 6, 19 |
| [Naming what the wire reports](decisions/naming.md) — a pointer and a vector number become names | 7, 8 |
| [The transport](decisions/transport.md) — a lock-free ring, overflow, and the drain loop's fixed point | 3, 5, 20 |
| [The record layout](decisions/layout.md) — three layouts in three days, and what each traded | 4 |
| [Two clocks](decisions/clocks.md) — which measures, which places, and a join that refuses | 17, 18 |
| [The manifest](decisions/manifest.md) — what makes IDs on the wire acceptable | 9 |
| [Capture and routing](decisions/capture.md) — study-scoped, post-hoc, carrier as a bench fact | 10, 11, 12, 13 |
| [The bench](decisions/hardware.md) — the first consumer, and the wire that turned out not to exist | 15, 16 |

**Two lessons this sub-project produced that generalise past it**, both recorded in their own decisions and worth naming here:

- **A wire change is not done when the DUT emits it — it is done when every host that decodes it has been re-measured against it.** Layout 3 restored the DUT's clock and `embarch-ui` kept timing spans by frame arrival for a day, reporting the outpost's own drain thread at **78% of a capture** where the DUT's clock says **1.6%**. Nothing was wrong with the wire; the host was reading the older of the two clocks it carried.
- **Three correct measurements can support a wrong conclusion if they share an unexamined premise.** A day of bring-up, across three diagnoses, went into a trace being transmitted perfectly into a pin with nothing attached — because the board being built was not the board on the bench, and *which board is on the desk* had been inferred from a stale build artifact by the tool that exists to forbid exactly that inference.
