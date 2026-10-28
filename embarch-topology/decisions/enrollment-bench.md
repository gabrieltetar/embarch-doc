# embarch-topology decisions: A bench board, and the early powered check

**Status:** active, 2026-10-09.

Split verbatim from [enrollment.md](enrollment.md), 2026-10-28, once that file sat in its reserve. Decision 41, a board enrolled with no role, and decision 16, the early powered check; `enrollment.md` keeps a pointer for 41 because other sub-projects cite that path by name for it.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 41 — A bench board is enrolled with no role, and is keyed by its probe

**A board can need flashing without filling a slot.** A USB PD partner (a Nucleo with a sink shield, driven over its console) is flashed and reset like any board, and the identity gate is what makes that safe. But it is neither the DUT nor the dev bench. Enrolling it under `dev-bench` would push out the real dev bench, and inventing a role is what decision 35 closed.

**So the empty role, `NO_ROLE`, means "a bench board": enrolled, identity-checked, and holding no role.** Nothing addresses a bench board by role. A project names its probe serial (`embarch-api` `probe_serial`), and `validate_serial`, the gate on `/flash` and `/reset`, needs only the serial to be enrolled. A bench board is not a third role. No study, signal or link declaration can name it, and `CANONICAL_ROLES` stays the pair.

**Two rules follow, both in `upsert`'s family.** `upsert` applies role uniqueness only to a row holding a role. Otherwise every bench board would displace the others, the same collision decision 35's boardless rows had. And `remove_by_role("")` removes nothing, because the empty role names no one board. `remove_by_probe` retracts a bench board, and it opens no probe, for the reason `remove_by_role` gives.

### 16 — An early powered check, instead of the raw access-port error chain

**Found live:** the real DUT enrolled that session turned out to be **genuinely unpowered**, and every attach attempt failed with a generic error **a human has to already know how to read.** The probe's own sensed target-voltage pin is read immediately before attach at both of this crate's attach sites, and a reading under a threshold **fails fast naming the actual likely cause.** Not every probe type supports the reading, and an ambiguous or plausible one just proceeds — **best-effort diagnosis, not a new hard gate.**
