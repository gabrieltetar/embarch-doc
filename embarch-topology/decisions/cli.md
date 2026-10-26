# embarch-topology decisions: The CLI's guard and role set

**Status:** active, 2026-10-26.

### 45 — The guard probes the port the operator names, and the CLI enrols and retracts bench boards as Core does

**Decision 28's guard looked only at Core's default port.** Core's `run --port` can listen elsewhere, so with Core on another port the guard found nothing and `enroll`, `unenroll`, `set-board`, `validate` and `set-dev-bench-link` ran in-process beside a live Core, the second writer decision 28 exists to refuse. Found by the 2026-10-25 review. **A global `--core-port` (default `DEFAULT_CORE_PORT`) now sets the port the guard resolves**, and the refusal prints the port it probed and says to set `--core-port` if Core listens elsewhere. It is a flag, not a scan: nothing here can know which port an operator gave Core, and probing many ports on every mutation would be a cost every local-bootstrap run pays. **Measured:** a test binds a local listener on an OS-assigned port and the guard refuses naming it; **not measured:** a Core on a non-default port the operator forgot to name is still invisible, by design.

**The CLI and Core now accept the same roles on enroll** (decision 35's pair, plus decision 41's empty role for a bench board). `--role` defaults to empty, and an empty role without `--name` is refused with Core's sentence, because a bench board is told apart only by its name. `set-board` and `validate` still require a canonical role, as Core's `PUT /probes/enrolled/{role}/board` does; the empty role there now says `--role is required`. **`unenroll` gains `--probe-serial`** (exactly one of it and `--role`, enforced by clap), calling `hardware::unenroll_probe`, the same retraction as Core's `DELETE /probes/by-serial/{serial}`; the role path is unchanged. Neither change touches a public type: the binary calls existing functions.

**`status --host`'s help text said a declared host skips loopback and the WSL2 gateway; it does not.** `software::candidates` probes loopback first, the gateway second and the named host last, deliberately (its doc comment), so a Core on this machine wins over the named host. The help now says that.
