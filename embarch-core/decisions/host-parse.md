# embarch-core decisions: a host step's declared number

**Status:** active, 2026-11-25 (`tasks/core/155`, EMB-359; `embarch-study-designer` decision 108; `notes/hil/03-test.md` "The verdict"). Index: [../decisions.md](../decisions.md). Siblings: [host-study.md](host-study.md) (95), [measurements.md](measurements.md) (113), [signing.md](signing.md) (110).

### 131 — A host step's `parse` is read at step time, recorded beside the raw reply, and written as `measurements.json`; who measured comes from what the step addressed

Since `suite/062` a study may declare `parse` on an `Exchange` and a queried `Instrument`, and Core accepted it and computed nothing. Now `run_step` calls `parse_step_number` (the one function `verify` re-parses with, so they cannot disagree) **on the reply as recorded** (after the 4,096-byte cap) and the step's record in `events.json` carries `parsed {name, value, incomplete?}` beside `reply`. A step whose backend returned no reply (port unavailable, failed) has no `parsed`: its failure is the step's verdict, not a missing number's.

- **`incomplete`** is `truncated_reply` when the reply was cut (`reply_truncated`, the cap or the read's cap) and `parse_failed` when the pattern found no number (`value: null`). **A cut reply is still parsed** and may carry both marks; the number may itself be cut, so the mark is the verdict rule's to act on and the value is not hidden. Rejected: value `null` on any cut, which the shape (`null` only with `parse_failed`) does not allow.
- **`measurements.json`** is written by `host_parse.rs` after `events.json` is final and before the record is signed, so it is a subject (decision 110 lists the files present). One entry per parsed step record, in step order, teardown included, in `hil-shapes.md`'s shape: `method {kind: "parse", pattern}`, `source {file: "events.json", step, iteration?}`, `behaviours: {}` (a parse is no reducer). A study with no parse writes none.
- **`by` and `instrument` come from what the step addressed.** A signal whose origin (`SignalOrigin`, the resolver of decision 113) is the `dut` role is `by: dut`; a bench board's signal (another role, or a board by probe serial) is `bench`, `{name, kind: "board"}`, `unverified`; an `Instrument` step is `bench`, `{name, kind: "instrument"}`, `bench_image: null` (no board made it). A signal no longer declared at the end is `dut`, as in decision 113.
- **`U` stays `undeclared`**, `uncertainty` null, for a DUT's value and a bench's alike: `StepParse` declares none, and an instrument's metrology (EMB-358, EMB-360) does not reach it yet. `declared_by` names the signal and, for a DUT's, the role, scopes from the ledger (`agent` where unseen); a host study has no `study_value`.
- **A `Repeat` pass** yields one entry per pass with the same `name`; `source.iteration {list, repeat_index, pass}` tells them apart. The shape asks names unique within the file, so this is an open item ([../open.md](../open.md)).

*Rejected:* a `parsed` key on the SSE `HostStepCompleted` event (nothing reads it live; `GET /study/{id}` returns `events.json`).

**Measured vs assumed.** Proven over the scripted backend end to end through `run_job` (record, file, subject, and each of the five origins). **Not run:** on a real port, a real board's signal or a real instrument.
