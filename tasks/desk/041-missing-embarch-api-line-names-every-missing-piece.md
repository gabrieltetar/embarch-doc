# 041 — The missing-embarch-api session line names every missing piece

**State:** claimed by agent/desk/041-missing-embarch-api-line-names-every-missing-piece, 2026-11-23 13:08
**Source:** Fleet Ready issue, a session that planned to flash a board by hand after reading the line
**Issue:** EMB-230
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

When a folder's login lacks `embarch-api`, the desk's session line tells the
session everything it is missing and that it must not route around EmbArch.
Today `src/mcpreg.rs` `session_text` says only "this session has no build,
flash or bootload tools. Tell the user." plus `register_command`, and:

- `register_command` / `existing_entry` copy the first `embarch-api` entry found
  in any login, so its `--config` can be another firmware project's
  `embarch/embarch.toml`. That is fine, because `embarch-api`'s
  `src/session_desk.rs` `resolve` falls back to the desk repo's own
  `embarch/embarch.toml`, but nothing says so, and a session read it as
  "EmbArch cannot drive this board".
- The line never checks whether the desk's firmware repo (or, from a worktree,
  its main clone) has an `embarch/embarch.toml`. Without one, registering the
  server alone still fails with `resolve`'s "run `embarch init` there" error.
- Nothing in it says not to flash by hand, and the session planned `usbipd` and
  `nrfutil` instead.

Wanted: the line lists every missing piece in order (the register command;
then `embarch init` in the repo's main clone when no `embarch/embarch.toml`
exists there and no project in the server's config has that repo as
`source_path`); says, when the copied `--config` belongs to another project,
that the server still resolves this desk's repo through the repo's own config;
and says bench work (build, flash, bootload, console) goes through EmbArch
only, so a session missing these pieces stops and asks the user to run them
rather than using `west flash`, `nrfutil`, `JLinkExe` or `usbipd` itself.
`folder_json` carries the same missing pieces.

## Why now

The line as written led a session to plan bench work outside EmbArch.

## Where

- `embarch-desk/src/mcpreg.rs`: `session_text`, `folder_json`,
  `register_command`, `existing_entry`.
- Read only: `embarch-api/src/session_desk.rs` `repo_config` / `resolve`, for
  how a desk repo's own config is found. Do not edit `embarch-api`.

## Dispatch note

**`embarch-desk/spec.md` is in reserve: 9,186 of 10,240 B, 1,054 B left, out
of reserve at 9,039 B or less.** Its compaction, `tasks/desk/038`, is parked on
`In flux: yes` and unparks when the next desk unit writing `spec.md` runs out of
room. If this unit writes `spec.md`, compact it out of reserve in this unit by
moving reference text into `spec/` verbatim and leaving links, honouring 038's
`Must not delete:` list (the invariants that no agent tool sends a draft and
prose is never sent unseen, and every decision/EMB citation). Say in your report
whether you did; the leg closes 038 at the fold. If you do not touch `spec.md`,
leave 038 alone.

## Done when

- [ ] For a folder whose repo has no `embarch/embarch.toml` and no matching
      project, the session line names `embarch init` and where to run it, as
      well as the register command.
- [ ] A session line whose register command carries another project's
      `--config` says the desk repo's own config is used.
- [ ] The session line says not to flash or build outside EmbArch, and to ask
      the user instead.
- [ ] `mcpreg.rs` tests cover the repo-without-config case.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
