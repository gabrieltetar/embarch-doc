# 062 — A host study step parses a number, and a prompt says its kind

**State:** open — announced in #embarch-fleet 2026-11-25 01:59, ts 1795597152.735759; window closes 02:29; runs as a leg's last unit if that thread holds no objection
**Source:** EMB-352 — a host study step can neither parse a number nor say what kind of prompt it is
**Issue:** EMB-352
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`HostAction::Exchange` and `HostAction::Instrument` in `embarch-study-designer`
record their reply as raw text; nothing declares a number to read out of it.
`HostAction::Prompt` has a `text` and a `bench_config`, and no kind. The HIL
design has Core parse the number at step time from a declared pattern and unit,
recorded beside the raw reply (`embarch-doc/notes/hil/03-test.md`, "The
verdict"), and every prompt declare its kind
(`notes/hil/12-prevention.md`, "Operator prompts, by kind"). When this is done:

- **`parse`, optional on `Exchange` and `Instrument`**: `{name, pattern,
  unit}`. `name` is the measurement's name, unique within the study; `unit` one
  of the reducers' units (`reducers::UNITS`); `pattern` a regex with exactly one
  capture group. The captured text is read by the crate's number grammar
  (`number_grammar.rs`). One parse per step.
- **A pure function** `parse_step_number(reply, parse) -> Result<f64,
  Incomplete>`: no match, or a capture the grammar does not read as one number,
  is `parse_failed`. Core and `verify` will both call it, so they cannot
  disagree.
- **`kind` on `Prompt`**: `setup`, `action`, `observation` or `clearance`. A
  study written before the field reads as having no kind. An `action` prompt
  carries `confirmed_by`, the name of a `parse` in the same study. An
  `observation` prompt declares what its answer is (`notes/hil/02-study.md`,
  "Measurements"): a `name`, and either `answers` (the choices) or
  `number {unit, resolution, U, k}`.
- **`HOST_TYPE_SCHEMA_VERSION` 24 to 25** (the issue says 22 to 23; two bumps
  have landed since), with the reason in `schema_version.rs`'s history.
  `DEV_BENCH_WIRE_SCHEMA_VERSION` does not move: nothing here reaches dev-bench.
- `embarch-study-designer/interfaces/hil-shapes.md`'s
  `method {kind: "parse", pattern}` and `source.step` already name the
  step-time measurement; point them at the new field.

## Why it is a suite pass and not a study-designer task

The issue scopes it to `embarch-study-designer`, but new fields on the
`HostAction` variants break two consumers' `main` the moment the crate lands:
`embarch-core/src/host_study.rs` destructures `Exchange`, `Instrument` and
`Prompt` without `..` (about lines 539, 574, 600) and constructs all three in
its tests, and `embarch-ui/src/bench/files.rs` (about line 636) constructs a
`Prompt`. So the crate change and the two consumers' mechanical updates land as
one sequenced pass, shared crate first (`protocol.md` §8), each repo's `main`
compiling on its own. The consumers change only what the new fields force (a
`..` in a pattern, `None` or the default in a constructor); Core's step-time
parse and prompt rules are later units (T.8, T.16), not this one. Check
`embarch-api` too (`src/host_study.rs` matches `Prompt { bench_config, .. }`,
which survives) and `embarch-umbrella`, by building every consumer.

It also bumps a wire schema version, which is announced and parked on its own
account (`ops.md` §4).

## Why now

EMB-352, unit T.1 of the HIL Test phase
(`embarch-doc/notes/hil/14-implementation-plan.md`). Core's step-time parse,
its prompt rules, `verify`'s re-parse and the test definitions all read these
fields. One parse per step and the observation prompt's shape are the plan's
recommendations; the owner may strike them later.

A new numbered `embarch-study-designer` decision, amending 88 and 99 with
dated pointers. Study-designer decision files within 256 B of their limit,
left alone: `streams` (39), `versioning` (12), `seals` (17), `protocols` (58),
`authoring` (73), `declares` (40), `protocol-exec` (60), `ble` (44). Decision 12
has 67 B left: the bump is recorded in `schema_version.rs`'s history, not in
decision 12.

## Done when

- [ ] A fixture reply and pattern with one capture group give the expected
      number.
- [ ] No match, and a capture that is not one number, each give
      `parse_failed`.
- [ ] A pattern that does not compile, has no capture group or two, an unknown
      unit, a repeated name, an action prompt whose `confirmed_by` names no
      parse, or an observation prompt declaring neither answers nor a number is
      refused at validation.
- [ ] A study without the new fields deserializes and validates as before; the
      host schema version is 25.
- [ ] `embarch-study-designer` gated under every feature set its consumers
      build it with; `embarch-core`, `embarch-ui`, `embarch-api` and
      `embarch-umbrella` each build, test and clippy green against it.
- [ ] `hil-shapes.md` and a new decision say it; `changelog.d/` fragments for
      each repo changed.
