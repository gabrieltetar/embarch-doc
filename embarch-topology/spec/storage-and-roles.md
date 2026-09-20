# embarch-topology spec: Storage and roles

**Status:** active, 2026-09-17.

Split verbatim from [../spec.md](../spec.md), 2026-09-17, once `tasks/topology/055`'s three
correctness fixes pushed that file to 9,826/10,240 B — 414 B left (`tasks/topology/057`). This
section's mission (enrollment's write-time role uniqueness, and a declared link serial/interface's
guess-and-clear semantics) is distinct from "Shape" and "What validation asserts", which stay in
[../spec.md](../spec.md). Nothing below is reworded from the version that moved.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

**There are two roles and a board's name is a separate field** (decision 35, [`embarch-ui` 44](../../embarch-ui/decisions/topology-boards.md)). `CANONICAL_ROLES` is `dev-bench` and `dut`; `is_canonical_role` is the check, applied on the **write** path by `embarch-core`'s `POST /probes/enroll` and by this crate's own CLI, and by nothing on the load path — a store predating the rule still loads, foreign row and all, and `remove_by_role` (`DELETE /probes/enrolled/{role}`) is what clears one. `EnrolledBoard.name` is the board's own label: recorded verbatim, compared against nothing here, and resolved — where anything resolves it — against a firmware repo's `embarch/boards.toml`, which is not on this machine.

**A role holds two independent bindings** (decision 35's 2026-09-20 amendment, [`embarch-ui` 45](../../embarch-ui/decisions/topology-roles.md)): which probe serves it (`probe_serial`/`hardware_id`/`confirmed_at_utc_ms`, written together by `enroll`, all `None` until one is bound) and which **board type** is in it (`name`/`chip`, written by `set_role_board`, which opens nothing). A board type is a shape a repo builds for, not a piece of hardware; the physical unit is identified by `hardware_id`. Changing the type leaves a recorded `hardware_id` in place on purpose, so `validate` reports the disagreement instead of the row forgetting it.

**Enrolling keeps a role unique going forward:** it displaces any other board already holding that role, and returns the displaced row rather than dropping it silently (decision 20). **That uniqueness is a write-time rule, not a store invariant** — nothing on the load path checks it, so a hand-edited or pre-2026-08-31 `enrollment.toml` can still hold two rows sharing a role. If it does, only the first (by file order) comes back as displaced; any further row sharing that role is removed with no record.

**A declared link serial or interface can also be *unset*** (`set-dev-bench-link --clear-serial`/`--clear-interface`): `NotFound` names which rule emptied the candidate list and routes to clearing it (decision 27).

**A detected port says whether it was guessed** — the result carries how many candidates the lowest-interface rule chose among, **so a caller reports "COM16, guessed among 2" rather than "COM16".**

**The declared *interface* decides which of the two VCOMs is the console** — `COM16` and `COM17` differ in nothing else a detector can read, and it is wired to the **higher** one. Remove the declaration and resolution does not bail — it warns, sorts by interface, takes the lowest, and reports the wrong port **as a guess** (decision 20).

**`guessed_among`'s trigger is an *under-declared* bench, not a crowded one** — adding probes cannot produce a guess while an interface is declared.
