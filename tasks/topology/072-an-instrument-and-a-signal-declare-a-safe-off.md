# 072 — An instrument and a signal declare a safe-off

**State:** done — safe_off on Instrument and SignalLink, checked and round-tripped; gate green on four feature sets; landed by suite/059 with the consumers' literal fixes
**Source:** HIL implementation plan (`notes/hil/14-implementation-plan.md`, attested phase): Core is to switch off every output a bench declares, with a command built from the declaration, and no declaration holds one
**Issue:** EMB-321
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`Instrument` (`embarch-topology/src/hardware/instrument.rs`) holds a name,
protocol, port, baud, terminators, pacing and acknowledgement strings;
`SignalLink` (`src/hardware/signal.rs`) holds its port and origin. Neither says
how to switch the instrument or the bench board off. The HIL design has Core run
a safe-off at every graceful stop and every start that switches off every output
the bench declares, "with a command it builds from the instrument's or board's
declaration, never a step's text" (`notes/hil/12-prevention.md`, "What Core then
guarantees, in code", item 3, and "The root of trust").

When this is done both declarations carry an optional safe-off, in the plan's
recommended shape (kept by the owner, `14-implementation-plan.md` line 64):

- `Instrument.safe_off: Vec<String>`: lines sent in order with the
  instrument's own terminators and pacing. Each line is checked in `check` like
  an exchange's `line`: not empty, no CR or LF, within the write cap.
- `SignalLink.safe_off: Option<String>`: one shell line Core sends to the bench
  board on that signal, checked the same way.
- Both optional and skipped when empty, so a store written before them loads
  and is rewritten byte for byte (`src/hardware/enrollment.rs`, `Store`).
- A declaration with none is not refused; Core will list it as "no safe-off
  declared". Using the field (Core's safe-off at start and stop) is later Core
  work, not this task.

Docs, in `embarch-doc/embarch-topology/`: amend decision 49
(`decisions/instruments.md`) in place to say what the field is for and who
declares it (a declaration like any other: the person's act on an attested
Core, the agent's and labelled so on an unattested one), and say the
`SignalLink` half where `decisions/links.md` describes the link's fields;
`spec.md` and `interfaces/` where they list either type's fields.

**Core's docs are not yours.** `embarch-doc/embarch-core/interfaces/instruments.md`
carries the route bodies built on these types; if it lists their fields, write
in this file's notes the line it needs, and the supervisor applies it at the
fold.

## Why now

The first of the attested phase's declaration units: Core's safe-off, the call
log's fail-closed rule, and the api and UI declaring surfaces each wait on this
field. EMB-321.

**Burndown leg: no new numbered decision.** Amend decision 49 in place; if the
change seems to need a new decision, stop and say so in this file.

**Doc-size reserve (dispatch note):** no `embarch-topology` file is in reserve.
Decisions near their per-decision limit (`check-doc-size.py --pressure`):
storage#23 already 516 B over (do not touch it), enrollment#35 14 B,
link-declares#20 29 B, validation-classifier#25 95 B. If the `SignalLink` half
belongs in decision 20, keep its growth to a pointer at decision 49.

## Done when

- [x] An instrument and a signal with `safe_off` round-trip through the store.
- [x] A store fixture written before the field loads, and is rewritten byte for
      byte.
- [x] An empty line, a line holding CR or LF, and an over-long line are each
      refused by `check`, for both types.
- [x] Gate green under every feature set the crate's consumers build it with
      (`../../embarch-fleet/gate.md`).
- [x] Decision 49 amended; `spec.md`/`interfaces/` updated; `changelog.d/`
      fragment dropped.

## Notes

- **Core's docs (supervisor applies at the fold):** if `embarch-core/interfaces/instruments.md` lists `Instrument`'s fields, add `safe_off: Vec<String>` (optional, omitted when empty); if it lists `SignalLink`'s, add `safe_off: Option<String>`.
- **Breaking for consumers that build the structs by literal:** both types gained a field, so `embarch-core` (`api.rs`, `study.rs`), `embarch-api` (`tools.rs`, `core-client`, `tests/core_client_http.rs`) and `embarch-ui` (`topology.rs`) need `safe_off: Default::default()` where they construct `Instrument`/`SignalLink`. Not touched here (other repos); expect red there until fixed.
- **Assumed, not measured:** the 4096-byte cap repeats Core's `MAX_WRITE_BYTES`; topology cannot depend on Core. `SignalLink::check` is new and is called by `signal::declare` (hardware feature).
- The `SignalLink` half is a one-line pointer in `decisions/links-origin.md` (decision 48's file) and in decision 49; decision 20 untouched (29 B margin).
