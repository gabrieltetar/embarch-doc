# embarch-topology decisions: `validate`'s freshness timestamp

**Status:** active, 2026-09-07.

The `validate` call's own timestamp, distinct from the enrolled record's. What live validation asserts about the silicon itself is [validation.md](validation.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 26 — `validate` gains a second timestamp, additively; the enrolled record's own one is not renamed

A live `validate` call's only timestamp was `EnrolledBoard::confirmed_at_utc_ms` — enrolment time, unmoving until someone re-enrolls. Read next to `ok: true` on a call that just re-verified live hardware, that reads as *when this check ran*, and the two roles on the dev bench proved it can rank two equally-fresh validations six days apart (`tasks/topology/009`, the supervisor's own reproduction).

**The fix adds a field; it does not rename the one that misleads.** A rename is a wire-schema change with hand-maintained mirrors in three other repos (`embarch-api`'s `crates/embarch-core-client` and MCP `validate` tool, `embarch-umbrella`'s doctor, `embarch-ui`'s Topology tab) — `suite`-scoped work outside a `topology` worker's reach (`../../embarch-fleet/protocol.md` §8), and half-landing it here is exactly this suite's worst-named failure mode. An added field is safe by construction: every existing mirror keeps deserializing.

`validate_serial`/`validate_role` keep their exact signatures, returning a bare `EnrolledBoard` — **this crate is linked live, in-process** (decisions 2, 3, 8), not called over the wire, so a signature change on them is a same-instant compile break for every linked consumer, not a staged rollout the way a JSON field addition is. `embarch-core`'s existing `hardware::flash`/`reset` and dev-bench-handshake call sites go on compiling unchanged. The additive surface is two new functions, `validate_serial_timed`/`validate_role_timed`, returning a new `Validation { board: EnrolledBoard, validated_at_utc_ms: u64 }` — the enrolled record plus the instant *this* live check's hardware-ID compare passed. This crate's own CLI (`embarch-topology validate`) is the first caller switched over, printing both instants side by side.

**`embarch-core` is a fifth consumer the task's own enumeration did not name**, and the one that matters most for closing this: it is the in-process caller that actually assembles `POST /validate`'s JSON body (`{ok, role, hardware_id, confirmed_at_utc_ms}`) from the `EnrolledBoard` these functions return, so the new field only reaches the wire once its own `/validate` handler switches to `validate_role_timed`/`validate_serial_timed` and adds `validated_at_utc_ms` to that body. An `inbox/` drop records this for `embarch-core`, alongside the three the task named (`embarch-api`, `embarch-umbrella`, `embarch-ui`). **That condition has since fired**: `embarch-core`'s `/validate` handler switched to `validate_role_timed` and populates `validated_at_utc_ms` on the wire (`embarch-core` decision 50; see `embarch-topology/spec.md`).
