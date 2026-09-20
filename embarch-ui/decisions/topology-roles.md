# embarch-ui decisions: Roles hold two bindings, and a board is a type

**Status:** active, 2026-09-20.

What a role *is* after decision 45 corrected the model decision 44 set up ([topology-boards.md](topology-boards.md)): two independent bindings — a probe and a board type — and a board that is a shape rather than a piece of hardware.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 45 — A probe and a board are two separate bindings, and a board is a *type*

**Two corrections to decision 44, made by the bench owner, and both were conceptual rather than cosmetic.**

**First: a probe is not an attribute of a board.** Decision 44 read the enrolment row as "this board, with its probe", which is why its dialog asked for a board *and* which probe served it as one act. On a real bench one probe is moved between three boards over a week, and only two probes are ever identified at all — the DUT's and the dev bench's. So a role holds **two independent bindings**: which probe serves it, and which board is in it. Drag-and-drop stays because it is the natural gesture for the first one; clicking the board name on the box is the second.

**Second: a board is a *type*, not a unit of hardware.** `embarch/boards.toml` lists `nrf54l15dk`, the shape — what Zephyr means by a board — not "the DK in my drawer". Two identical DKs are one board type, and what tells the two physical units apart is the hardware ID read through whatever probe is on one of them. Decision 44's catalog was written as an inventory of individual boards, which is why its entries wanted names like `wearable-rev6` and why "which board is in this role" read as a question detection could answer. It cannot: **a board type is what a run builds for, and the identity behind it is what `validate` checks.**

### The row gains an optional half, rather than the board half living elsewhere

`EnrolledBoard` now carries `role` + `name` + `chip` always, and `probe_serial` + `hardware_id` + `confirmed_at_utc_ms` only when a probe has been bound ([`embarch-topology` decision 35](../../embarch-topology/decisions/enrollment.md), [`embarch-core` 75](../../embarch-core/decisions.md)). **A role with a board and no probe is a real state** — it is what a bench is in while it is being described — and the old shape could not represent it at all.

*Rejected: keeping Core's row as a pure probe binding and putting the board half in the project.* It would have avoided touching four repos, and the owner's own answer put the board beside the probe: one role is one row, and a UI joining two stores is a UI that can show them disagreeing.

**`PUT /probes/enrolled/{role}/board` opens nothing.** That is the property the whole design rests on: picking a board type is a statement about the bench, not about silicon, so it works with the boards unplugged and it never blocks on hardware. **It deliberately leaves a stale `hardware_id` in place** — changing the board type in a role usually means different silicon is on that probe now, and the recorded ID is what makes `validate` *say so*. Clearing it would turn a detectable disagreement into a row that has simply never been checked.

### The diagram absorbed the roles table

A table of two roles next to a picture of the same two roles was the same redundancy the Enrol tab had (43), one fold later. So the box carries both bindings and nothing else: **the role as its title, the board type under it as a click target, and a status line that is blank until Validate topology has run.** The chip left the picture — it is a property of the board type, listed where board types are listed.

**A status that appeared on its own would be a claim nobody made**, so the badge is written only by a Validate pass, keyed by role, and dropped the moment that role's board or probe changes underneath it. The five-second snapshot poll never touches it. *Rejected: keeping the live attach badge* — "attached" says where a probe is, which is not what a human presses Validate to learn.

**Retracting had to find a new home**, and the two cases are different. A canonical role is retracted from the picker that sets it. A **leftover role is in neither box** — it is a row from before the vocabulary closed — so its only control is on the validate line that finds it. Without that, the fold would have re-opened exactly the gap decision 44 closed: a row the only surface that can see it cannot clear.

### The catalog is scanned, and the file wins

A board type is a west target, and the repo already knows which ones it builds for — so **Rescan** merges the scan into `embarch/boards.toml` and a hand-written entry is never overwritten. **A rescan can only add.** A board type in the file that the scan does not find is *kept and counted*, never deleted: a repo builds for boards on branches that are not checked out, and a catalog that silently shrank when someone switched branches would be worse than one that is occasionally generous.

The dev-bench picker is a different list and deliberately not the catalog: the two board types `embarch-dev-bench`'s firmware supports, served from the binary like every other vocabulary. **A bench is a piece of the suite, not a project's board**, and offering one the bench firmware cannot be built for would be offering a bench that cannot exist.

### A study no longer stores a board

`BuildSpec`'s `board`, `variant` and `revision` leave the Study Designer: a run reads them from the board type in the **DUT role**, at the moment it runs. The same saved study then runs on whatever is on the bench today — the same reason a study names a signal and never a carrier (10). What stays on the study is what is genuinely its own: the app, the ordered snippets, the west args, the outpost mode flags.

**A study saved before this still carries a board, and it is neither obeyed nor silently dropped.** The role wins, and the build log says so by name before anything is built — "this study names X, the DUT role holds Y, building for the role". Opening such a study does not rewrite its file.

**Driven in a real browser**, 47 checks: the roles table gone, the box titled by role with the board type under it and no chip, no status before a pass and a verdict on the box after one, the DUT picker reading the project catalog while the bench picker holds the suite's fixed pair, a board type set with no probe opened, a probe bound afterwards taking its chip from that type, a leftover role cleared from the report line that found it, and a role retracted from its own picker.

