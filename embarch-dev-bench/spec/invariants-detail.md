# embarch-dev-bench: invariants, in full

**Status:** active, 2026-11-24.

Split verbatim from [../spec.md](../spec.md) §3 (`tasks/dev-bench/050`), when `spec.md` was in its reserve. Nothing below is reworded; the bullets are the build-time and runtime invariants about named-versus-unnamed targets, monitor windows, capacity limits, length prefixes and the manifest. Current truth: [../spec.md](../spec.md).

- **A named thing missing fails the step; an unnamed thing missing is skipped.** A selective monitor target or an `.eap` source the DUT does not have, or whose subscription did not land, fails, naming which. The subscribe-to-everything walk logs and skips each characteristic it could not subscribe, because nothing there was named, and fails only when it subscribed to nothing (decision 54).
- **An open monitor window survives the steps inside it.** A one-shot monitor step inside one is refused by name; every other step leaves the window's subscriptions and labels intact. One notification is one transcript row, however many of the bench's subscriptions hold its handle (decision 55).
- **A capacity limit refuses, never truncates.** An oversized `StudyStart`, or a manifest over the wire-length cap, is rejected by name: a `LogLine` names the cap, the value and the limit (decision 51). A malformed frame is a silent resync.
- **A length prefix is bounded by the bytes left, before any arithmetic.** Decoding treats the link as crafted input: a length the frame cannot hold refuses the frame, and no varint near 2^64 can wrap the cursor backwards (`pc_skip_len_prefixed`).
- **A manifest index the run cannot follow fails the run by name.** A `goto` naming no state, or a `remember` naming no session variable, ends the `RunProtocol` step as `Fail` in the state that named it (decision 50), never a raw array subscript.
