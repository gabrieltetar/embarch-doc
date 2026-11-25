# 193 — A confined writer for the person's `embarch/` folder

**State:** claimed by agent/api/193-a-confined-writer-for-the-persons-embarch-folder, 2026-11-25 02:47
**Source:** EMB-457 — nothing writes the person's `embarch/` under a confinement rule
**Issue:** EMB-457
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api` writes `embarch/ledger/`, `embarch/live/` and the build folder
with plain path joins (`src/ledger.rs`, about line 100; `src/live_log.rs`, about
line 268). The HIL design has the person's `embarch/` written from Core's copies
by a tool in the person's account, and that writer confined: only under
`embarch/`, names from a fixed set, no link followed, only known data files,
nothing run (`embarch-doc/notes/hil/12-prevention.md`, "The repo is the
boundary's one door", and item 9, the same rule for Core's staging folder).
When this is done the confined writer exists as a module, ahead of any command
that uses it; this unit does **not** move `ledger.rs` or `live_log.rs` onto it.

- **A module** `src/person_writer.rs`: `ConfinedWriter::open(repo_root)`
  refuses when `<repo>/embarch` is a link or not a folder; `write(kind, name,
  bytes)`.
- **Kinds, each with one folder and one extension:** `study` and `host_study`
  (`studies/`); `test`, `suite` and `plan` (`tests/`); `saved_bench`
  (`topologies/`); `atlas_measured` (`atlas/`); `test_results` (`tests/`);
  `live_log` (`live/`); `report_typ` and `prose` (the study's own folder).
  Anything else is refused.
- **Names:** `[a-z0-9][a-z0-9._-]{0,99}`, no `..`, the kind's extension
  appended by the writer.
- **No link at any step:** each path component opened relative to the last
  without following links (`openat` with `O_NOFOLLOW` on Unix; on Windows,
  `symlink_metadata` refusing any reparse point before each step); an existing
  target with more than one hard link is refused.
- **Atomic:** written to a temp file in the same folder, then renamed over the
  target.
- **Runs nothing:** no `Command` and no spawn in the module; a test reads the
  module's own source and fails on either.

The extensions per kind, the study's-own-folder layout for `report_typ` and
`prose`, and how a caller names the study for those two are the worker's to
settle from the HIL notes and today's ledger layout; record each choice in the
decision.

## Why now

EMB-457, from the HIL standalone container pass
(`embarch-doc/notes/hil/14-implementation-plan.md`). The person's mirror (C.17)
is the only caller in that pass, and any later writer into the person's
`embarch/` goes through it. The kinds and the name set are the plan's
recommendation (plan choice 3), which the owner may strike: say so in the
decision.

## Where the doc goes

A **new decision in a new file**, `embarch-doc/embarch-api/decisions/person-mirror.md`,
listed in the decisions index. Decision files near their limit, to be left
alone: `lease.md` (decision 90, already 504 B over), `ledger.md` (98, 15 B
left), `bench-exchange.md` (89, 122 B left), `failure-reporting.md` (67, 192 B
left). If the new decision should point at the ledger's, point from the new
file, not into `ledger.md`.

## Done when

- [ ] A clean write of each kind lands at its path.
- [ ] Each of these is refused, one fixture each: `embarch` a symlink, a
      symlinked subfolder, a `..` name, a name outside the set, an unknown
      kind, a target with two hard links.
- [ ] A crash between the temp write and the rename leaves the old file whole
      (simulated: the temp file written, no rename).
- [ ] The module holds no `Command` and no spawn, checked by a test.
- [ ] The decision states the rule and the kinds.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `spec.md`/`decisions`/`open.md` updated, `changelog.d/` fragment dropped,
      `status.d/` fragment for anything suite-level it made false.
- [ ] The Windows `cfg` branch is a hardware-verification debt in this file
      if it cannot be built here (`gate.md`'s native-Windows note).
