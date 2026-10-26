# 061 — The topology CLI's Core guard probes the port Core really listens on, and the CLI agrees with Core about bench boards

**State:** done 2026-10-26 — decision 45 (`decisions/cli.md`); `--core-port` guard, bench-board enroll, `unenroll --probe-serial`, help text
**Dispatch note:** decisions 28 and 41 both live in `decisions/enrollment.md`, which is at 12,045/12,288 B (243 B left, 98%) and parked under `tasks/topology/060` (blocked, `In flux: yes` for that file only). Do not grow it past the cap. Either record the guard-port and role-set outcomes as a new decision in a file with headroom (`decisions/scope.md` 7,301 B, or a new topic file listed in `decisions.md`) and leave at most a one-line pointer under 28/41, or, if you must amend 28 or 41 in place, first split `enrollment.md` verbatim per `DOC-COMPACTION.md` §2 (a verbatim split restates nothing, so the flux park does not forbid it) and close `topology/060`'s `enrollment.md` item in the same commit. `decisions/link-declares.md` (1,133 B left) is filed under `topology/064`; you should not need it. `spec.md` is 8,365/10,240 B. No change to any public type that `embarch-core`, `embarch-api` or `embarch-umbrella` build against: they path-depend on this crate's main checkout, so a shape change breaks them the moment this lands.
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-topology findings 5, 6 and 11), verified by Opus against embarch-topology@93a83d9c
**Scope:** topology
**Hardware:** none — These are argument handling, the reachability guard and help text, all testable before any probe is opened. If the CLI gains a bench-board `enroll`, its role check runs before the attach, and the attach path is unchanged.
**Owner:** no

## What

Three gaps in `bin/main.rs`.

**1. The guard checks only Core's default port.**
- `refuse_if_core_reachable` (`bin/main.rs:205-222`) probes `resolve_software_topology(DEFAULT_CORE_PORT, None, None)`, and no mutating subcommand takes `--port`.
- Core's own `run --port` (`embarch-core/src/main.rs:64`) can listen elsewhere. With Core on another port the guard finds nothing, and `enroll`, `unenroll`, `set-board`, `validate` and `set-dev-bench-link` run in-process beside a live Core. That is the second writer decision 28 exists to refuse.

**2. The CLI and Core disagree about bench boards.**
- `check_canonical_role` (`main.rs:177-185`) refuses the empty role, and no subcommand calls `hardware::unenroll_probe` (`src/hardware/mod.rs:213`).
- So on the local-bootstrap machine where this CLI is allowed to write, a bench board (decision 41) can be neither enrolled nor retracted.
- Core accepts role `""` when a name is given (`embarch-core/src/api.rs:961-985`) and retracts by probe at `DELETE /probes/by-serial/{serial}` (`api.rs:152`).

**3. `status --host`'s help text is wrong.**
- It says a declared host "skips auto-detection's WSL2/loopback candidates and probes only this one" (`main.rs:31-32`).
- `software::candidates` always probes loopback first and the WSL2 gateway second, and its doc comment says that order is deliberate (`src/software.rs:96-135`). A Core on loopback therefore wins over the named host.

One possible direction:
- Let the guard probe the port the operator names, and say which port it probed.
- Either give the CLI the bench-board path, or record that it has none. Decision 18 already records that cost for signals.
- Correct the help text to the order `candidates` implements.

## Why now

The guard's hard-coded port is at `main.rs:209`. spec/storage-and-roles.md says `is_canonical_role` is applied "by `embarch-core`'s `POST /probes/enroll` and by this crate's own CLI", but the two now accept different role sets. Decision 35 states the check twice so that a local-bootstrap bench is not left unchecked, which makes the divergence a contract gap rather than a style point.

## Done when

- [x] With a Core answering on a non-default port the operator names, every mutating subcommand refuses and names that Core, shown by a test against a local listener or the pure resolution.
- [x] The CLI and Core accept the same set of roles on enroll, or a numbered decision records the difference. If the CLI gains bench boards, an empty role without a name is refused the way Core refuses it, and retracting by probe serial works.
- [x] `embarch-topology status --help` describes the probe order `candidates` uses.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated (decision 28 for the guard's port; decision 41 or spec/storage-and-roles.md for the CLI's role set), `changelog.d/` fragment dropped.
