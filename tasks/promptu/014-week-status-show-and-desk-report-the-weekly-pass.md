# 014 — `promptu week status`, `week show` and `promptu desk` report the weekly pass

**State:** open
**Source:** `embarch-promptu` `docs/contract.md` §9, §10 and §14 (written by `promptu/011`); decisions 14, 30 and 46 (`decisions/learning.md`)
**Issue:** EMB-275
**Scope:** promptu
**Hardware:** none
**Owner:** no

**Dispatch note (reserve):** `embarch-promptu/spec.md` (9,186 of 10,240 B)
and `open.md` (4,055 of 5,120 B) are in reserve, filed as `promptu/015`
(blocked, in flux). For each of the two you write, move reference text into
`spec/` (or `open/`) **verbatim** in this unit, keeping `promptu/015`'s Must
not delete, so the file ends at or under 9,039 B (`spec.md`) or 3,919 B
(`open.md`). A verbatim move restates nothing, so the flux does not forbid it.
Do not edit `promptu/015`; say in your report which files left reserve and the
supervisor strikes them off it at the fold.

## What

The chat's Promptu card and the desk's `GET /promptu` need to ask Promptu what
the weekly pass has done and what is waiting for review. No command answers
yet. When this is done, three read-only commands print the JSON the contract
fixes, each carrying `"promptu": 1`:

- **`promptu week status --json`**: the last run (start, end, result), the next
  run, whether a run was missed, whether one is running now, and the waiting
  sheet's week and open count. The next run and a missed run come from the
  schedule config key and the run records, as the contract fixes it (decision
  45). The chat never reads the timer itself.
- **`promptu week show --json`**: one week's sheet, for the Desk's panel and the
  review skill.
- **`promptu desk --json`**: contract §9's shape, `{"promptu": 1, "open": 0}`
  when nothing is open, **including when the state folder does not exist**.

Without `--json`, each prints the same facts as text for a user with no Desk
(decision 30). Where to start: `src/main.rs` (`Cmd`), `src/config.rs` (the
schedule keys the contract adds), `src/state.rs` (`dir`, the state folder the
week folder sits in).

No other unit has written a sheet yet, so build the test fixtures by hand in
the contract's shapes.

## Why now

The chat's card (EMB-85), the desk's routes (EMB-282), the terminal review skill
(EMB-280) and `week run` (EMB-277) all read these commands.

**Burndown leg: no new numbered decision.** Where the contract turns out to be
wrong once it meets real code, fix the contract in this unit and say so. A new
choice goes to `docs/forks.md` as an open fork with a provisional default.

## Done when

- [ ] Each command's JSON matches the contract, tested on scratch state folders: no week yet, a waiting sheet, an applied sheet, a missed run, and a run in progress.
- [ ] None of them calls a model or the network.
- [ ] `promptu desk --json` prints `{"promptu": 1, "open": 0}` when the state folder does not exist.
- [ ] `cargo test --all-targets` and `cargo clippy --all-targets -- -D warnings` pass. On a machine with a crowded `/tmp`, a failure of `claude::tests::a_folder_name_decodes_back_to_the_checkout_on_disk` is `promptu/012`'s (EMB-286), not this unit's: say so if it appears.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`open.md`/`interfaces.md` updated, and a `changelog.d/` fragment dropped.
