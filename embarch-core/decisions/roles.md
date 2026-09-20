# embarch-core decisions: What a role is made of

**Status:** active, 2026-09-20.

The two halves of a role — the board type in it and the probe bound to it — and the vocabulary that keeps a role from being a name. Split verbatim from [enrollment.md](enrollment.md) on 2026-09-20 when that file reached its reserve; nothing below is reworded from the version that moved. The surface those routes sit on is still [enrollment.md](enrollment.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 75 — The role vocabulary closes on the write path, a board's name rides beside it, and a role can be retracted

**Core is where the vocabulary is enforced, because Core is the one writer.** `POST /probes/enroll` answers `400` to any `role` outside `dut`/`dev-bench` ([`embarch-topology` decision 35](../../embarch-topology/decisions/enrollment.md), felt in [`embarch-ui` 44](../../embarch-ui/decisions/topology-boards.md)) — the refusal names both roles *and* says where a board name goes, since the failure it prevents is someone putting a name in the role field, which is exactly what this bench had done (`client-nucleo`). The check sits after `hw_lock` and before the enroll call, so it costs no probe attach and is reachable in a test with no hardware attached.

**Only the write path.** Nothing re-validates a row already in `enrollment.toml`: an old store must keep loading, and a row hidden by a stricter loader is a board a human cannot see or clear. It stays visible through `GET /probes/enrolled` and goes through the route below.

**`name` is carried, not understood.** Optional on the wire (`#[serde(default)]`), echoed in the response, and never compared against anything — the catalog that gives it meaning is a file in a *firmware repo*, which Core does not read. An absent name records as empty, never as a name Core derived from the chip.

**`DELETE /probes/enrolled/{role}` is the counterpart enrolling never had.** `204` on a removal, `404` when nothing held that role — the same deliberate `404` `DELETE /signals/{name}` answers, for the same reason: a caller retracting a row it believed existed should learn it did not. It takes `hw_lock` as an enrollment-file writer, and **opens no probe**: a board that is unplugged, or that no longer answers, is the one most likely to be getting cleared, so requiring an attach would make the common case the impossible one. A role outside the canonical pair is accepted here deliberately — that is the row this route exists to remove.

### 76 — The board half is its own route, and a role with no probe is a `404` rather than a `503`

**`PUT /probes/enrolled/{role}/board` writes the half of a role that claims nothing about silicon** (`embarch-ui` decision 45, [`embarch-topology` 35](../../embarch-topology/decisions/enrollment.md)): which board *type* is in it. It opens no probe, which is the property everything else about it follows from — a bench is usually described before it is wired, and a route that needed an attach would refuse exactly then. It takes `hw_lock` because it writes the enrollment file, not because it touches hardware, the same posture as `/dev-bench/link` and `/signals`.

**It leaves a recorded `hardware_id` alone**, deliberately. Changing a role's board type usually means different silicon is on that probe now, and the recorded ID is what lets `POST /validate` *say so*. Clearing it here would turn a detectable disagreement into a row that has merely never been checked — the difference between "these are different boards" and "nobody has looked", which this suite keeps apart everywhere else.

**A role that holds a board type but no probe answers `404` on `/validate`, not `503`.** `503`/`not_attached` means the declaration exists and the hardware is missing, so retrying once it is plugged in is the fix; this is the *declaration* missing, and no amount of plugging in changes it until a human binds a probe. It is the same shape as the not-enrolled `404` above, and telling the two apart by status is what lets a caller decide whether to wait or to ask for a setup step.
