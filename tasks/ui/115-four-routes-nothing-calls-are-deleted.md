# 115 — Four routes nothing calls are deleted

**State:** open
**Source:** suite review audit, 2026-11-23: four `embarch-ui` routes have no caller in any page or sibling repo
**Issue:** EMB-311
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`embarch-ui/src/main.rs` still routes four endpoints that no page and no other
repo calls, since phase 4 moved the bench page off them:

- `POST /api/topology/roles/{role}/board` (`topology::api_set_role_board`)
- `POST /api/topology/link` (`topology::api_link`)
- `POST /api/topology/profiles/{slug}/apply` (`topology::api_apply_profile`)
- `GET /api/study-designer/gatt/{study_id}` (`study_designer::api_gatt_data`)

When this is done the four routes, their handlers and the tests that exercise
only them are gone, and they answer 404. `apply_role` and `apply_link` stay:
`src/bench/live.rs` uses them. The page's own profile routes stay.

Before deleting, finish the caller search the audit left open: grep
`embarch-ui`'s own tests, Python tests and `scripts/`, and the suite's other
repos (api, umbrella, core, chat, desk, topology, outpost, atlas, dev-bench
scripts) for each path. **If any caller exists, keep that route**, name the
caller in this file, and delete the rest.

Docs, in `embarch-doc/embarch-ui/`:

- drop the four routes' rows from `interfaces/topology.md` (and any other
  interface file that names one);
- amend decisions 90 and 94 in place (`decisions/bench-canvas.md`,
  `decisions/bench-live.md`), which keep these routes "for API callers": say
  they were removed and why, in the decision's own body. If that retires part
  of a decision, follow `DOC-CONVENTIONS.md` for a reversal, with a
  `status.d/ui-*` fragment for `embarch-decision-reversals.md`, which you do
  not edit;
- close the slugify bullet in `open/bench.md`, which queues a fix on the apply
  route being deleted here.

## Why now

Dead routes are surface to keep correct for no caller, and one of them
(`api_link`) carries a doc comment that has been false since phase 4. EMB-311.

**Burndown leg: no new numbered decision.** Amend 90 and 94 in place; if the
change seems to need a new decision, stop and say so in this file.

**Doc-size reserve (dispatch note):** no `embarch-ui` file is in reserve.
Decisions near their per-decision limit (`check-doc-size.py --pressure`):
launcher#28 22 B, tab-folders#100 113 B, topology-tab#10 141 B,
topology-tab#43 207 B, plus several pinned ones. Do not grow those.

## Done when

- [ ] The four routes return 404 (or the ones with a found caller are kept and
      named here), and their handlers are gone.
- [ ] No `embarch-ui` doc names a deleted route; decisions 90 and 94 say what
      happened; the `open/bench.md` slugify bullet is closed.
- [ ] `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
      green in `embarch-ui`.
- [ ] `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
