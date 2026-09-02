# embarch-study-designer: Stream taps

**Status:** active, 2026-09-02.

A declared capture channel: where bytes come from, how long it lives, how it renders, what it is called.

Every sequence and string is fixed-capacity ([../decisions/limits.md](../decisions/limits.md) holds each bound). Index: [types.md](types.md). Why: [../decisions.md](../decisions.md).

## Stream taps

**`StreamTap { id, name, source, encoding, scope }`** — `id` is the wire handle and is its own index in the list; `name` names the output file and nothing else. `dev-bench` is a **reserved** name, rejected at pre-flight, because it belongs to the reserved log tap.

**`StreamSource`** — `GattNotify { service_uuid, characteristic_uuid }`, `PowerFrontEnd { sample_hz }`, `GattTranscript`, `DevBenchLog`, `Signal { name }`. The first four are dev-bench-mediated; a signal is read by Core itself, with the carrier resolved live by topology, **and the tap is identical either way**.

**`StreamEncoding`** — `Raw`, `Text`, `Samples { layout, unit, channel_id }`, `GattTranscript`, `OutpostTrace`, `Struct { decoder }`. **This is the only place a byte payload acquires a meaning, it is always engineer-declared, and no component ever guesses one.**

**`StreamScope`** — `WholeStudy`, or an inclusive step range. **Wire records** are open / chunk-batch / close, where a record is arrival-stamped bytes and never decoded values. `dropped` is carried **on close**, so a stream that lost data says so rather than presenting a shorter, plausible capture as complete. Neither open nor close carries a step index: when a tap opens is a property of its declared scope.

**That guarantee is only as good as the close, and for whole-study taps there wasn't one** until dev-bench stopped ending a run by syncing scopes one step past the last — which closes a step window and leaves a whole-study tap open, correctly, since the predicate covers every index. No close meant no `dropped`, meant `truncated: false` however much had been lost. **Nothing in this crate was wrong; the sentence above was simply unreachable for one of the two scopes it applies to.**

**`StreamRef` deliberately did not grow a `note` field**, and the reasoning is worth keeping: it rides inside `StudyResult`, which crosses the dev-bench wire, so growing it is a **host schema bump for a fact produced by Core after dev-bench has finished and meaningless to it.** Core exposes its own index over a route instead. `truncated` stays the one thing this type says about incompleteness, and it says it about the *capture*, which is dev-bench's business.

**The reserved log tap's id is the declared count** — free by construction, since a declared tap's id is its own index, so the first index past the end can never collide. **That single rule is what lets both ends agree on the handle without either sending it.**

**`validate_taps`** holds pre-flight's rules here rather than in Core, so there is no second copy to drift: id equals index, no blank, reserved or duplicated name, no inverted or out-of-bounds step range. **That last exists because both failures produce a capture that is silently empty**, which is the failure decisions 34 and 36 were each opened by.

