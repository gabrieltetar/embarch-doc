# 043 — The desk sets the weekly sheet's feel line through a route that runs `promptu week mark --feel`

**State:** open
**Source:** decision 65 (`decisions/cockpit.md`, the Desk tab's Promptu section and its four routes, `desk/042`); `embarch-promptu` `docs/contract.md` §10 (`feel`) and §14.4 (`week mark --feel`, which takes no id)
**Issue:** EMB-283
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

The Desk tab's Promptu section (EMB-283, `ui/113`) shows the sheet's feel
line, *better · same · worse*, and the owner sets it there. `desk/042` gave
the tab four routes; none sets the feel, because `week mark --feel` takes no
line id and the mark route is per line. When this is done:

- **`POST /promptu/feel/{week}`** with `{"feel": "better" | "same" | "worse"}`
  runs `promptu week mark --feel <feel> --week <week> --json` and passes its
  JSON on, exactly as the mark route does: the same week check (`YYYY-Www`),
  the same status mapping (no binary a 503 naming it, Promptu's exit 2 a 400
  in Promptu's words, anything else a 502), and it clears the `GET /promptu`
  cache. Any other `feel` value is refused before the binary runs.
- That path and body are fixed here because `ui/113` is built against them
  in the same wave; if the router cannot take them as written, stop and say
  so in this file rather than choosing another shape.
- **No MCP tool reaches it**, like the other four, and the existing test that
  says so covers it.

Where to start: `src/server.rs`, the four `/promptu` routes `desk/042` added,
and `src/promptu.rs`. Read the `promptu` repo; do not edit it.

## Why now

EMB-283's Desk tab section has to set the feel line, and nothing on the desk
can. `ui/113` draws the section against this route.

**Burndown leg: no new numbered decision.** Record the route by amending
decision 65 in place and adding it to the existing `/promptu` row in
`interfaces.md`. If the work needs a new decision, stop and say so in this
file and in your report.

**Doc size, a dispatch note (supervisor):** `embarch-desk/spec.md` is in
reserve (9,186 of 10,240 B), filed under `tasks/desk/038`, blocked. This unit
should not need `spec.md`; if it does, compact it in this unit into `spec/`
verbatim to at or below 9,039 B, carrying `desk/038`'s `Must not delete:`
list, and do not edit `tasks/desk/038`. `interfaces.md` is 12,723 B, out of
reserve; keep it there.

## Done when

- [ ] The route is tested against a fake `promptu` on a scratch `PATH`: a good feel runs `week mark --feel` once with the week, a bad feel and a bad week are refused without running it, and no binary is a 503.
- [ ] No MCP tool reaches the route, and a test says so.
- [ ] `interfaces.md`'s `/promptu` row and decision 65 name the route.
- [ ] Gate green (`../../embarch-fleet/gate.md`), with `cargo test` and `cargo clippy --all-targets -- -D warnings`.
- [ ] `changelog.d/` fragment dropped.
