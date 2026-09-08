# embarch-api decisions: The study event stream

**Status:** active, 2026-09-07.

`lagged` and a dropped stream as facts rather than errors, the fallback-to-polling
shape, and where the SSE client and Core's mirrored `StudyEvent` live. Split out
of [core-link.md](core-link.md) on 2026-09-07, verbatim: that file was 22 bytes
from its 12,288 B cap and these two entries are the half a first live run against
a real `embarch-core` (`tasks/api/001`) is expected to rewrite —
`tasks/api/026`'s `In flux: yes`.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Reaching Core otherwise: [core-link.md](core-link.md).

### 48 — `lagged` is a fact, a dropped stream is a mode change, and neither is an error
Core emits `event: lagged` *deliberately* when a subscriber falls behind its broadcast buffer, in preference to silently skipping messages. A client that surfaced that as a stream error would destroy the thing it was built for: it is a fact about **this subscriber**, and the study's own record on disk is untouched. So it is reported and counted, the stream continues past it, and both front-ends say in as many words that the complete record is still `GET /study/{id}`.

**A stream that drops falls back to polling rather than reconnecting.** Core's handler subscribes to a `tokio::sync::broadcast` channel and reads no `Last-Event-ID`, so a reconnect would resume at "now" with a hole of unknown size and nothing to notice it — exactly what `lagged` exists to prevent. Polling reads the authoritative record instead, and every fallback announces itself and why. A refused subscription (an older Core, a proxy) takes the same path; the only genuine failure is neither mechanism answering.

**Subscribe first, then poll once.** Core holds the stream open indefinitely, so a study that finished *before* the subscribe emits no `StatusChanged` and would hang a listener; the opening poll is what catches it. The order is load-bearing the other way too — polling first leaves a gap an event can fall into.

**Two kinds of incompleteness, reported as two.** Core's `lagged` and this crate's own `max_events` cap ([decision 47](tool-wrapping.md)) are different facts with different remedies, and a caller told only "some events are missing" cannot tell them apart.

### 49 — The event-stream client lives in `embarch-core-client`, and Core's `StudyEvent` is mirrored there
Same argument as decisions 37/38: `embarch-ui` reaches Core the same way this crate does, and a second SSE implementation there would be the mirrored-copy risk that extraction exists to remove. It also buys testability without widening this package's own `lib` surface ([decisions](tests.md) 46) — the decoder and the follow loop are `pub` in a library crate `tests/` can already reach, so nothing had to move out of the binary.

**Core's `StudyEvent` is mirrored rather than shared.** The real type lives in Core's binary crate and is `Serialize`-only; lifting it into `embarch-study-designer` is a cross-repo wire change and not one sub-project's to make. The mirror's cost is that a variant Core grows and this does not is undecodable — paid down by treating an unknown `kind`, an unknown `event:` name and unparseable data as **one reported "I did not understand this frame"** rather than an error. Core has already grown one variant (`GattTranscript`) that `embarch-core/interfaces.md` still does not list, so this is not hypothetical.

The SSE wire decoder is a separate byte-fed module with no I/O at all, because every framing failure worth fearing — a frame split across TCP reads, a `\r\n` straddling that split, a keep-alive comment between frames — is a pure function of a byte sequence and should be testable as one.
