# 042 — The desk serves Promptu's weekly sheet and takes its ✓/✕ through routes that run the `promptu` CLI

**State:** done — four routes run the promptu CLI, tested on a fake binary; no MCP tool reaches them; interfaces.md compacted to 12,723 B; decision 65 amended
**Source:** decision 65 (`decisions/cockpit.md`, the Desk tab's spot for a Promptu section); decision 67 (finding the `promptu` binary); `embarch-promptu` decisions 14 and 30; `embarch-promptu` `docs/contract.md` §9 and §10, and `week show`, `week mark` and `week apply` (`promptu/014`, `promptu/019`)
**Issue:** EMB-282
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

Promptu's weekly sheet is approved in a Promptu section of the Desk tab. The
tab needs routes to read the sheet and act on it, and the desk must hold no
Promptu logic: each route runs the `promptu` CLI and passes its answer on.
When this is done:

- **`GET /promptu`** runs `promptu desk --json`, cached 60 s. It answers
  `{"promptu": 1, "open": 0}` when Promptu is not installed or the command
  fails.
- **`GET /promptu/sheet`** runs `promptu week show --json`.
- **`POST /promptu/sheet/{week}/{line}`** with `{verdict, note}` runs
  `promptu week mark`.
- **`POST /promptu/apply/{week}`** runs `promptu week apply` and returns each
  line's result.
- These are HTTP routes the tab calls, like ✓ on a tile. **No MCP tool
  reaches them**: an agent never marks or applies a sheet.

Where to start: `src/server.rs` (the router; `approve_tile` is the model of
an action only the tab can take), `src/promptu.rs` `find` (decision 67), and
the promptu contract's §9 and §10 for what each command prints. Read the
`promptu` repo; do not edit it.

## Why now

`week mark` and `week apply` landed as `promptu/019`. EMB-283 (the Desk tab's
Promptu section in `embarch-ui`) waits on these routes.

**Burndown leg: no new numbered decision.** Record the routes by amending
decision 65 in place. If the work needs a new decision, stop and say so in
this file and in your report.

**Doc size, a dispatch note (supervisor):** `embarch-desk/interfaces.md` is in
reserve (14,073 of 15,360 B, 1,287 B left) and `embarch-desk/spec.md` too
(9,186 of 10,240 B, 1,054 B left), both filed under `tasks/desk/038`, blocked
on `In flux: yes`. The route table goes in `interfaces.md`, so **compact
`interfaces.md` in this unit**: move reference detail into `interfaces/`
verbatim, leaving links, until it is at or below 13,823 B, and carry
`desk/038`'s `Must not delete:` list (the invariants that no agent tool sends
a draft and prose is never sent unseen, and the decision and EMB citations).
If you also write `spec.md`, compact it the same way (to at or below 9,039 B
into `spec/`). Do not edit `tasks/desk/038`; I update it at the fold.

## Done when

- [x] Each route is tested against a fake `promptu` on a scratch `PATH`.
- [x] With no `promptu`, `GET /promptu` answers `{"promptu": 1, "open": 0}`, and the other routes answer an error that names the missing binary.
- [x] No MCP tool reaches these routes, and a test says so.
- [x] `interfaces.md` lists the routes and is out of reserve; decision 65 is amended to record them.
- [x] Gate green (`../../embarch-fleet/gate.md`), with `cargo test` and `cargo clippy --all-targets -- -D warnings`.
- [x] `spec.md`/`decisions.md`/`interfaces.md` updated where they change, `changelog.d/` fragment dropped.
