# embarch-ui: roles, bindings and the catalog row

**Status:** active, 2026-11-06.

Settled rules moved verbatim from [spec.md](../spec.md) invariants.

- **A role is a fixed slot holding two independent bindings** (44, 45): which **probe** serves it, and which **board type** is in it. A probe moves between boards and only two are ever identified, so neither is an attribute of the other and either can be declared alone. A **board type is a shape**, listed in the repo's `embarch/boards.toml`, which **Rescan only adds to**; the dev-bench picker is the suite's own supported pair, served by the binary.
- **A catalog row lists what this repo can build it as** (47): its revisions and its variants — **not its apps, which are the study's axis** (49) — the pinned combination marked and a pin the scan no longer backs marked as stale. Never a cross product: Zephyr backs a pair only where a file does. The board type goes to Core; **the combination goes to `embarch/boards.toml` and Core is never told a revision**.
- **Picking a board type opens nothing**, and **leaves a stale `hardware_id` in place** so a validate pass can say the silicon no longer matches. Binding a probe is the only act that reads an identity, attaching as that board type's chip — **looked up, never typed** (48): a row stating none takes its targets' SoC through Core's `/resolve-chip`; a stated chip wins, nothing is written back, and an unanswerable one refuses here.
