# A successful request with an unreadable body is reported as `request-failed`

**State:** done
**Scope:** umbrella
**Hardware:** none
**Source:** `inbox/umbrella-status-probe-report-malformed-body-collapses-to-zero.md` (embarch-reviewer, at `umbrella/028`'s fold), filed by the supervisor of leg 034.

## What

`embarch status`'s `probe_report` handles a Core that answers `200` with a body carrying no
parseable `probes` array by returning
`ProbeReport::RequestFailed("Core answered HTTP 200 but its body carried no \`probes\` array")`
(`embarch-umbrella` `5c92ea0`, `src/main.rs`).

**Do not re-litigate the collapse.** The original defect — that case silently becoming
`Count(0)`, indistinguishable from a real zero, contradicting decision 46's own stated success
condition that *"a real zero and 'wasn't allowed to look' never share a value"* — **is already
fixed** and landed on `main` as `5c92ea0`. That half is closed.

**What is left is the state's name.** The request did not fail: it succeeded, and the Core said
something unexpected. A `--json` consumer that switches on `state: "request-failed"` will
reasonably retry, which is exactly the wrong move against a Core that is up and answering. The
retry will also succeed, and produce the same unreadable body, indefinitely.

## What to do

Give that case a sixth `ProbeReport` state of its own — `bad-response`, or a better name you can
argue for — and thread it through every place the five existing states appear:

- `ProbeReport` itself and `state_str` (`embarch-umbrella/src/main.rs`)
- `probes_json` — this is the part that changes the `--json` contract, so be deliberate about it
- decision 46's enumerated list of states in `embarch-umbrella/decisions/reporting.md`
- the `status` row in `embarch-umbrella/spec.md`, if it enumerates states
- a test covering a `200` with a body that has no `probes` array

## Why this was not done at the fold

The supervisor of leg 033 fixed the value and deliberately left the label, recording the reason:
this changes the `--json` contract that `embarch-umbrella` decision 11 protects, and a supervisor
hand-writing a new wire state inside a fold, unattended, with no worker's gate behind it, is a
wider change than the defect warrants. It wanted a worker and a gate. That is this task.

Its own `Least sure about` line is worth reading before you start: it names the current state as
*"a wrong value traded for a wrong label, and the wrong label is the one a machine consumer acts
on"* — so treat the present behaviour as a known-temporary shape, not as a precedent to preserve.

## Decision record

Decision 46 exists and enumerates five states; adding a sixth is an **amendment to 46**, not a new
decision, unless the `--json` shape change turns out to need its own argument against decision 11 —
in which case file a new numbered decision and say why 46 alone could not carry it.

## Doc-size reserve for this scope

`embarch-umbrella/spec.md` is at **90.4%** (9,257/10,240 B, 983 B left) and
`decisions/bind.md` at **92.8%**, `decisions/doctor.md` at **92.3%** — all three filed against
`tasks/umbrella/038-compact-umbrella.md` and `tasks/umbrella/009-compact-docs.md`.
`decisions/reporting.md` is not in reserve. If your work pushes a file into reserve or leaves one
there that nothing has filed, file `tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit.

## Done when

- [x] A `200` with an unreadable body reports a state that does not read as a transport failure.
      `ProbeReport::BadResponse`, `state_str() == "bad-response"`.
- [x] `state_str`, `probes_json`, decision 46's list and `spec.md` all agree on the set of states.
      `spec.md`'s `status` row lists only three of the five prior states as illustrative examples
      (never all five/six) and is unchanged — adding a sixth name there would not make it a
      complete enumeration, since `request-failed` itself was never named in that row either.
- [x] A test constructs that response and asserts the new state.
      `interpret_probe_response(200, "{}")` (the response-handling logic split out of
      `probe_report` so it's testable without a socket or a resolved token) asserts
      `state_str() == "bad-response"`.
- [x] `cargo build`, `cargo test`, `clippy --all-targets -- -D warnings` clean.

## Notes

Landed as an amendment to decision 46 (`embarch-umbrella/decisions/reporting.md`) rather than a
new decision — the `--json` shape change (a new `state` value inside the existing
`{state, count, reason}` envelope) does not need its own argument against decision 11; the envelope
itself is unchanged, only one more value it can take.

This amendment pushed `decisions/reporting.md` into reserve (94.3%, 699 B left); filed as
`tasks/umbrella/040-compact-umbrella.md` in the same commit.
