# embarch-api decisions: Hardware selection and identity

**Status:** active, 2026-09-11.

The tools that name, enroll, cross-check, or enumerate one specific physical board or port — `enroll_probe`, `validate`/`alerts`, `dev_bench_hello`, `list_serial_ports` — and why none of them picks one on a caller's behalf. Split out of [tool-wrapping.md](tool-wrapping.md) on 2026-09-11, verbatim (`tasks/api/063`): that file was 66 B from its 12,288 B cap. Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 34 — `enroll_probe`, wrapping Core's enrollment endpoint
The two-layer wrapping every other Core capability gets. **No selection params**: enrollment is not build-target selection but "record which physical probe I mean" — the precedent for anything not project-shaped. **The guided flow is conversational, not a single call**, and enforcement is not client-side: Core's refusal on anything but exactly one attached probe is what makes "plug in only the board you mean" hold. No new config schema — the resulting table is Core-local knowledge.

### 35 — `validate` and `alerts`, and "relay, don't auto-open" confirmed for the agent path
A mismatch comes back naming recorded vs. live hardware ID with the fix-it URL **as plain text** — never fetched or opened, mirroring the CLI and Core's posture toward callers; whatever is in the human's hands decides. These are the suite's only end-to-end exercise of that leaning from the agent side, so it is confirmed rather than reasoned-about.

### 59 — `dev_bench_hello`, and `link_identity` is a stable string on purpose
`GET /dev-bench/hello` (`embarch-core` `study::hello_handler`) is the only route in
the suite that serves the JTAG-read identity, the bench's own self-reported
identity, and how they relate, together — and until now nothing on this crate's
MCP surface reached it (`tasks/api/036`). Wrapped as `dev_bench_hello`: no params,
no project selection, since the route itself takes none.

**Mirrors Core's own serialized `HelloAckInfo` field-for-field, not
`embarch_topology::hardware`'s comparison type** — the two are never checked
against each other (this crate cannot link the `hardware` feature, the same
constraint `SignalLink`'s own mirror lives under), so a struct built from the
wrong side compiles and passes its own tests while failing against a real Core.
`embarch-core-client`'s `HelloAckResponse` gained `self_reported_hardware_id`,
`link_identity` and `probe_hardware_id` alongside the three fields it already
had; no route parsed those three before this, so nothing existing could regress.
**All three are `Option<String>` with `#[serde(default)]`, per [core-link](core-link.md)
58 — never a bare required field — for the reason decision 60 below writes out
in full: `embarch-core` 47 renamed one of them, and an older Core serves none of
them under these names.**

**`link_identity` is reported as its own string field, never folded into
`compatible` or any boolean.** Today's real value for every chip is
`"undeclared"` (Core §3 decision 35): the comparison could not be made, which is
not the same fact as "verified" and must not render as one. A caller reading
only `compatible` and ignoring this field has thrown away the one thing this
route exists to report — so the tool description spells out all four possible
values (`match`/`mismatch`/`not-reported`/`undeclared`) and says outright that
the latter two are not a pass.

**`409` and `502` get distinct error text in the tool, not only distinct HTTP
status.** `409` (`DevBenchBusyError`) means a study already has the link and
this call was refused rather than raced — a wait-and-retry, not a fault. `502`
(`DevBenchHandshakeError`) means the handshake itself failed — a real bench
problem. Collapsing both into one generic failure message would send an agent
to the wrong next action either way, so both the client (two downcastable error
types) and the tool description (which states the call opens and closes the
bench link, so a `409` mid-study is not read as a bug) say which is which.

### 60 — `dev_bench_hello`'s three identity fields are optional, and absence renders as its own third state
Decision 59's first draft made `self_reported_hardware_id`, `link_identity` and
`probe_hardware_id` bare required `String`s, and it was refused at the merge:
`embarch-core` decision 47 (`tasks/core/020`) renamed `hardware_id` to
`self_reported_hardware_id` on the same day this route's mirror was written, and
against a Core older than that rename `serde` fails the *whole* response on the
missing key, so every call to this tool would have returned a deserialization
error instead of the identity cross-check it exists to report — exactly the
failure [client-crate](client-crate.md) decision 58 was written an hour earlier to end.
The fields are now `Option<String>` with `#[serde(default)]`, per that decision.

**The tool never computes a verdict of its own from the two hardware IDs.**
Core already serves `link_identity` — its own answer to the cross-check —
and re-deriving one client-side would be this crate asserting a semantic it
did not measure, the exact failure `embarch-topology` decision 20 paid for.
Core's answer is surfaced, never replaced.

**`None` and the board's own `"not-reported"` are two different facts and
must never collapse into one rendering.** `"not-reported"` is *the board*
declining to state an identity — a real, declared bench answer. `None` is
*this Core* not having the field at all — a fact about the deployed Core's
age, not about the bench. Rendering an absent field as `"not-reported"` (or
as an empty string, `null`, `-`, or `"unknown"`) would make an unreported
Core version look like a bench that spoke and declined, which is the
regression this decision exists to close off; a `None` renders as a full
sentence saying this Core did not send it.

**Two rendering states, and one must never be reachable from the other.**
*Complete* — all three fields present — renders each verbatim under its own
label, with a trailing note that `"not-reported"`/`"undeclared"` are the
board's own answers, not confirmations. *Incomplete* — any of the three is
`None` — leads with a line stating the cross-check is **unavailable** and
naming which field(s) this Core did not send, citing `embarch-core` 47 as the
known cause and `embarch-api` 58 as why the client tolerates it instead of
failing; any still-present fields may render below that line, never above it
and never in a shape that reads as a completed comparison.

**Why "unavailable" and not a failure.** Decision 58 exists precisely so an
older Core degrades instead of erroring — returning an error here would be
the `api/045` behaviour that decision existed to end, and rendering a partial
answer as a pass would be worse than either. Unavailable is the third, honest
option.

### 70 — `list_serial_ports`/`list-serial-ports` take no parameters, and `serial_log` never calls either automatically
`GET /serial-ports` enumerates every USB serial port Core's own machine currently has plugged in, unfiltered — no project, vendor, or search parameter exists on the route or on either front end wrapping it. Narrowing a raw USB descriptor list down to "the DUT's console" is not enumeration, it is a judgment about what a physical port is *for*, so both the tool and the CLI subcommand stop at reporting: `port_name`, `detected_by` (always `"enumerated"` here), and whatever `vendor_id`/`product_id`/`serial_number`/`product`/`interface` Core's OS descriptor read reports, any of which can be `null`. An empty list is a real answer — nothing plugged into Core's machine — not an error.

**`serial_log` never reaches for this list on its own.** A `port` unresolved after falling back to the project's configured `serial_port` is a plain error naming the project, never a call to `list_serial_ports` followed by a guess. Several ports routinely enumerate at once — dev-bench's own bridge, a DUT's console UART, unrelated USB peripherals — and only whichever party asked (a human, or the agent acting for one) knows which one is the DUT's console right now. Picking automatically would be this crate inferring a hardware fact it cannot observe, exactly what [spec.md](../spec.md) §2 refuses: a wrong automatic choice is indistinguishable from a correct one until it silently opens the wrong board's boot log instead of erroring.

**`GET /serial-ports` and `GET /dev-bench/port` answer different questions and neither substitutes for the other.** The former is every enumerated port, unnarrowed; the latter is Core's own VID-filtered match for dev-bench's bridge specifically ([interfaces/tools-build-flash.md](../interfaces/tools-build-flash.md)). `serial_log`'s fallback chain stops at the project's configured port and never reaches into either list — a caller who wants dev-bench's own link uses `dev_bench_hello`/`dev_bench_link`, not this route.

**Shipped under `tasks/api/041`, decision filed here under `tasks/api/063`** once that leg's burndown rule against new numbers no longer applied.
