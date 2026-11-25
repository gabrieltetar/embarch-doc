# embarch-study-designer decisions: A host step's number and a prompt's kind

**Status:** active, 2026-11-25.

Fields on host-run studies, additive to decision 80 (in [study.md](study.md)) and 88 (in [host-prompt.md](host-prompt.md)). Who reads them: `embarch-core`'s step-time parse and prompt rules, and `embarch-api`'s `verify`, both later units of the HIL Test phase.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 108 — A host step reads one number out of its reply, and a prompt says who may answer it

**Decided 2026-11-25** (EMB-352, unit T.1 of [the HIL plan](../../notes/hil/14-implementation-plan.md); `tasks/suite/062`, run by the leg as a suite pass, since the new fields broke `embarch-core`'s and `embarch-ui`'s `main` the moment the crate landed; amends 88 and 99 with dated pointers and 101's gating, each otherwise standing).

**`parse` on `Exchange`, and on an `Instrument` with `query`**: `StepParse {name, pattern, unit}`, the step-time measurement of [the HIL notes](../../notes/hil/03-test.md) ("The verdict"). `name` is the measurement's, at most `MAX_MEASUREMENT_NAME_LEN` bytes, no control, line-breaking or bidi character, no edge whitespace, and **unique within the study across every parse and every observation prompt's answer**, steps, teardown and `Repeat` inner steps alike; `pattern` is a `regex` pattern with **exactly one capture group**, at most `MAX_HOST_PATTERN_LEN` bytes; `unit` one of `measures::UNITS`. A parse on an `Instrument` without `query` is refused: there is no reply. **One parse per step**, the plan's recommendation, which the owner may strike.

**`parse_step_number(reply, parse) -> Result<f64, Incomplete>`** is the one reading, so Core at step time and `verify` from the recorded reply cannot disagree: the pattern's first match in the reply, its capture trimmed, read by the crate's number grammar ([hil-pdf.md](hil-pdf.md), decision 103) as **exactly one number spanning the whole capture**. No match, a capture that did not take part, a capture holding anything but one number (`5012V`, `1 2`, `n/a`) or a non-finite value is `parse_failed`. Behind `std` and `reducers`, since it needs `regex` and returns the reducers' `Incomplete`; **`number_grammar` moved from `pdf-text` to `std`** for it, and `pdf-text` implies `std`, so no build that had the grammar loses it. Still never a comparison: decision 80's "no action carries an expected value" stands, and a parse says how to read a number, not what it should be.

**`kind` on `Prompt`**: `setup`, `action`, `observation` or `clearance`, spelled in lower case, from [the prevention notes](../../notes/hil/12-prevention.md) ("Operator prompts, by kind"). `None` is a study written before the field. **An `action` prompt carries `confirmed_by`**, the name of a parse anywhere in the same study (an observation's answer is a measurement too, but the person's, so it cannot confirm an action). **An `observation` prompt carries `answer`**: `PromptAnswer {name, answers | number}`, exactly one of the two, `answers` at most `MAX_HOST_PROMPT_ANSWERS` (16, **assumed**) unique choices of at most `MAX_HOST_VALUE_LEN` bytes, `number` an `ObservedNumber {unit, resolution, U, k}` with `unit` in `measures::UNITS`, `resolution` and `U` finite and positive, `k` absent (2) or finite and positive ([02](../../notes/hil/02-study.md), "a `person` measurement"). Either field on any other kind, or on a prompt with no kind, is refused. The observation's shape is the plan's recommendation, which the owner may strike.

**Not here:** that an action's confirming measurement is `by: bench` and feeds a limit that can fail (the width check, at test definition); who may answer which kind (Core, by the token's scope, T.16); the clearance before an energising step (Core).

**`HOST_TYPE_SCHEMA_VERSION` 24 to 25**, wire stays 17. Every new field is `#[serde(default)]` and skipped when `None`, so a v24 study loads, validates and serializes byte for byte as it did (test-pinned); the number moves anyway (decision 12), and the strict gate means Core, the API and the UI deploy together. History in `schema_version.rs`.

*Rejected:* a parse as a step of its own, which would re-send the command or reach into another step's reply; a kind inferred from the prompt's text, which would let a study relabel an observation as a setup.
