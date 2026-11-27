# embarch-api decisions: The study event stream

**Status:** active, 2026-09-07.

`lagged` and a dropped stream as facts rather than errors, the fallback-to-polling
shape, and where the SSE client and Core's `StudyEvent` reader live. Split out
of [core-link.md](core-link.md) on 2026-09-07, verbatim: that file was 22 bytes
from its 12,288 B cap and these two entries are the half a first live run against
a real `embarch-core` (`tasks/api/001`) is expected to rewrite —
`tasks/api/026`'s `In flux: yes`.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Reaching Core otherwise: [core-link.md](core-link.md).

### 48 — `lagged` is a fact, a dropped stream is a mode change, and neither is an error
Core emits `event: lagged` *deliberately* when a subscriber falls behind its broadcast buffer, in preference to silently skipping messages. A client that surfaced that as a stream error would destroy the thing it was built for: it is a fact about **this subscriber**, and the study's own record on disk is untouched. So it is reported and counted, the stream continues past it, and both front-ends say in as many words that the complete record is still `GET /study/{id}`.

**A stream that drops falls back to polling rather than reconnecting.** Core's handler subscribes to a `tokio::sync::broadcast` channel and reads no `Last-Event-ID`, so a reconnect would resume at "now" with a hole of unknown size and nothing to notice it — exactly what `lagged` exists to prevent. Polling reads the authoritative record instead, and every fallback announces itself and why. A refused subscription (an older Core, a proxy) takes the same path. Genuine failures are neither mechanism answering, and **a 404 from the opening poll, stream open or not** (2026-10-26, `tasks/api/137`): Core's SSE route opens for any id and its keep-alives defeat the idle timeout, so an unknown id would follow forever. Any other opening-poll failure still follows live.

**`interrupted` is terminal and its own outcome.** A `.partial` record with no job behind it is never moved on by Core, so `is_terminal_status` includes it and it is never reported as `completed` or `failed`. CLI exit 1, `study_watch` `complete: true` with `status: "interrupted"` and a `note`.

**Subscribe first, then poll once.** Core holds the stream open indefinitely, so a study that finished *before* the subscribe emits no `StatusChanged` and would hang a listener; the opening poll is what catches it. The order is load-bearing the other way too — polling first leaves a gap an event can fall into.

**Two kinds of incompleteness, reported as two.** Core's `lagged` and this crate's own `max_events` cap ([decision 47](tool-wrapping.md)) are different facts with different remedies, and a caller told only "some events are missing" cannot tell them apart.

### 49 — The event-stream client lives in `embarch-core-client`, and Core's `StudyEvent` is read there leniently
Same argument as decisions 37/38: `embarch-ui` reaches Core the same way this crate does, and a second SSE implementation there would be the mirrored-copy risk that extraction exists to remove. It also buys testability without widening this package's own `lib` surface ([decisions](tests.md) 46) — the decoder and the follow loop are `pub` in a library crate `tests/` can already reach, so nothing had to move out of the binary.

**One definition of Core's wire, on Core's side; the client keeps two lenient readers (2026-11-27, `tasks/api/226`).** `embarch-core-wire` ([`embarch-core` decision 164](../../embarch-core/decisions/wire.md)) defines `StudyEvent`, the hello answer, the outpost load answer and `LEASE_GATED`, and `embarch-core-client` path-depends on it. **Taken from it, re-exported under the names the client always had:** `LoadAnswer`, `LoadSummary`, `LoadSubject` and `lease_gate::LEASE_GATED`. The mirrors and the lease test that passed when Core's checkout was absent are gone: a route Core gates is now in the client's table by construction. **Kept, and why:** `StudyEvent` and `HelloAckResponse` stay the client's own types, as the older-Core tolerance decided here. The shared types are strict, and an older Core's frame would read as `Unrecognized`: `StepCompleted`'s three stamps and `core_rx_utc_ms` on `SampleBatch`, `GattTranscript` and `StreamText` are `Option` here, and the hello's four newer fields too, which decisions 58/60 require so the one route that answers "is the board on the link the verified one" never becomes a deserialization error. Taking the shared types also changes what `embarch-ui` and this package's CLI match (`Option` stamps, flat `PromptPending` fields, `answered_by` as a string, `StudyEvent`'s inherent helpers), so it is not a swap a client can make alone. **The mirror's drift risk is paid by tests, not by a copy of Core's file:** one test takes each variant's pinned wire line through `embarch-core-wire`'s own type, then the client's, and requires the same JSON back, and another does the hello; both fail when Core moves a field, with no checkout to be absent. Measured: `cargo test --workspace` and clippy green. **Not done:** replacing the two lenient types with the shared ones, which needs the consumers changed first (filed).

An unknown `kind`, an unknown `event:` name and unparseable data are **one reported "I did not understand this frame"**, not an error, and a variant Core grows that the client lacks is exactly that (`GattTranscript` was the first).

The SSE wire decoder is a separate byte-fed module with no I/O at all, because every framing failure worth fearing — a frame split across TCP reads, a `\r\n` straddling that split, a keep-alive comment between frames — is a pure function of a byte sequence and should be testable as one.
