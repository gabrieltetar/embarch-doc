# 164 — The measurements route serves a host study's file, and its refusal carries a code

**State:** done — host study file served (same run dir); 422 body is JSON with code no_measurements; decision 141; native Windows build is the owner debt
**Source:** EMB-553 — Core's measurements route still refuses a host study that now has measurements (Core's half; `api/202` is `embarch-api`'s)
**Issue:** EMB-553
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Core writes `measurements.json` for a host study whose steps declare a `parse`
(core decision 131), but `GET /study/{id}/measurements` (`src/publish.rs`)
still answers `422` "has no measurements.json: it declared no measurements, did
not complete, or is a host study" for it. When this is done:

- A host study with a `measurements.json` is served from the route exactly as a
  dev-bench study's is.
- A study with no file still gets `422`, and its body carries a stable
  `code: "no_measurements"` beside the message. The message no longer says a
  host study cannot have measurements: it says the study declared none, did not
  complete, or is a host study with no `parse` step.
- The other refusals of the route (`404`, `409`, `410`) are unchanged.

`api/202` makes `embarch-api` read the code rather than the sentence, and
tolerates a Core without it, so this unit may land before or after it.

## Where to look

- `src/publish.rs` — the measurements route and its `422`
- `src/host_study.rs`, `src/host_parse.rs` — where a host study's file is
  written
- `embarch-doc/embarch-core/decisions/host-parse.md` (131),
  `embarch-doc/embarch-core/interfaces/` for the route's row
- `embarch-doc/embarch-core/open/unverified-and-moved.md`, where the worker who
  found this noted it

## Where the doc goes

The route's row in `interfaces/` amended; `open/unverified-and-moved.md`'s note
removed. `check-doc-size.py --pressure` lists signing#110, analog-capture#127,
host-study#95, definitions#133, lease#93 and stopping-a-study#128 over their
entry limits and test-run-go#135, run-log#111 and instruments#104 near them: do
not grow those; a short new decision if the code needs one. If your work pushes
a file into reserve, file `tasks/core/<NNN>-compact-core.md` in the same commit
per `tasks/README.md`.

## Done when

- [x] A host study with a `parse` serves its `measurements.json` from the
      route, with a test.
- [x] A study with no file gets `422` with `code: "no_measurements"` and a
      message that does not say a host study cannot have measurements.
- [x] `interfaces/` gives the code.
- [x] Gate green. The native Windows build is a debt the owner runs.
