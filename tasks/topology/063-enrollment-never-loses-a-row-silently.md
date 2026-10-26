# 063 — Re-enrolling a probe under another role, or an interrupted store write, never loses an enrolled row without saying so

**State:** done
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-topology findings 2 and 3, with 13 folded into 3), verified by Opus against embarch-topology@93a83d9c
**Scope:** topology
**Hardware:** none — Both halves are store logic over a file, testable against temp paths through the `*_at` split that `upsert_at`'s tests already use. No probe is opened.
**Owner:** no

## Dispatch note, 2026-10-26 leg — doc reserve in your scope, read before you write a decision

- **`decisions/enrollment.md` is 12,045 / 12,288 B — 243 B left**, filed against
  `tasks/topology/060` (blocked, due 2026-11-01). Decision 35 lives there; decision 20 is in
  `decisions/link-declares.md` (9,537 B, room). **If your decision or amendment lands in
  `enrollment.md`, pay that file first, in your own commit:** move decision 41 (a bench board
  enrolled with no role) **verbatim** into a new `decisions/<name>.md` named for what it settles,
  route it from `decisions.md`, and repoint every link inside `embarch-topology/` that means 41
  (`scripts/check-decision-refs.py`; a link from another sub-project goes to `inbox/` by absolute
  path, not fixed). That is `060`'s own "The move". Then delete `enrollment.md` from `060`'s
  `**Compacts:**` line and say so in its body; leave `060` blocked for `spec.md`. Do not put your
  decision in a different topic file to dodge the cap — that is the silent failure the reserve rule
  exists to stop.
- **`spec.md` is 9,550 / 10,240 B — 690 B left, and stays parked** (in flux for `topology/059` and
  `suite/046`). Keep your `spec.md` edit tight; do not compact it. If it would cross the cap, stop
  and say so here rather than squeezing other prose.
- Shared crate: Core and api consume it. Prefer additive API; if a public signature or a serialized
  type changes, say so plainly in your Result.

## What

**A probe moving between roles deletes the role it leaves, and says nothing.**
- `upsert_at` reports a displaced row only when it shares the new row's *role* (`src/hardware/enrollment.rs:294-298`). Its `retain` also removes the row that shares the new row's *probe* (`enrollment.rs:305-308`), and returns nothing for it.
- Re-enrolling the dev-bench's probe as `dut` therefore deletes the dev-bench row. The same happens when that probe is enrolled as a bench board (`NO_ROLE`, where `holds_role` is false). The deleted row includes its board-type half (`name`/`chip`, written by `set_role_board`), which decision 35's 2026-09-20 amendment makes a binding independent of the probe.
- `validate::enroll` warns only on the role-keyed return (`validate.rs:631-643`), so nothing is logged. The role surfaces next as `NotEnrolled` on a later flash or reset.
- The probe's new row also inherits the old role's `link_port_serial`/`link_port_interface` (`validate.rs:608-610`). Those facts describe the old role's link.

**Every store write can leave a partial or empty file.**
- `save_at` writes with `std::fs::write` (`enrollment.rs:188-196`): truncate, then write, with no temp file, no rename and no `sync`. Every mutation of boards, signals and bootload ports goes through it (`signal.rs:206/219`, `bootload.rs:190/201`).
- A write cut part-way leaves a file every later `load_at` refuses to parse. Every mutator loads before it writes, so no Core route can repair it. Recovery means hand-editing a file under `%ProgramData%`, which decision 35 calls the path nobody should need.
- A write cut right after the truncate leaves an empty file. That parses as an empty store, because every field is `#[serde(default)]`, so every enrollment, signal and bootload declaration disappears with no error, and the next write makes it permanent.

One possible direction:
- Report the row a probe vacates the way a role displacement is already reported.
- Consider keeping the vacated role's board-type half with its probe half cleared. `NoProbeBound` already names that state.
- Write the store to a sibling temp file and rename it over the original. Decision 23 says the file has no per-file ACL, so a renamed file keeps the directory's access.

## Why now

The two faults contradict these docs:
- Decision 20: the displaced row is returned "rather than dropping it silently, so enrolling can say out loud that one board just replaced another".
- `validate.rs:625-630`: moving a role "is never a thing to do *quietly*".
- Decision 35: a role holds two independent bindings, and a probe "is moved between boards".

The probe-keyed path breaks all three at `enrollment.rs:305-308`. The empty-file case loses the one thing this crate persists, the human's declared intent (spec.md), with no error at all.

## Done when

- [x] Re-enrolling a probe that holds a role under a different role, or as a bench board, tells its caller which role it vacated, by return value and not only a log line. Fixture tests cover the role→role and role→bench-board moves.
- [x] After such a move the vacated role's board-type binding is either still on record or its removal is the reported outcome. Which one is a recorded decision.
- [x] Whether the moved row keeps the old role's declared link facts is decided, recorded, and pinned by a test.
- [x] A store write that fails at any point leaves the previous `enrollment.toml` loadable and unchanged, never partial or empty. A test that fails the write before replacement shows it.
- [x] An existing `enrollment.toml` (boards, signals, bootload ports) round-trips byte for byte as it does today.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated (decision 20 or 35 amended for the probe-keyed case), `changelog.d/` fragment dropped. If Core's `POST /probes/enroll` response should carry the displaced or vacated row (today it carries neither, `embarch-core/src/api.rs:944-1008`), a follow-up `core` drop is filed.

## Result

- `enrollment::upsert_reporting` returns `Upserted { displaced, vacated, vacated_kept }`; `validate::enroll_reporting` returns it beside the board. `enroll` unchanged. Public API: **`enrollment::upsert` (module-private, no outside caller) was replaced by `upsert_reporting`; `Upserted` and `enroll_reporting` are additive; no serialized type changed.**
- Decision **42** (`decisions/link-declares.md`): vacated role is reported, keeps board type and link facts with probe half cleared; the moved row inherits no link facts (`enroll` now carries them only for the same role). Decision **43** (`decisions/storage.md`): temp file, `sync_all`, rename. Nothing landed in `enrollment.md`, so `060`'s split was not triggered and `060` is untouched. `spec/storage-and-roles.md` carries the spec lines; `spec.md` itself untouched.
- Tests: role->role, role->bench board, bare vacated row, bench->role, failed write (temp name squatted by a directory); `save_at` output bytes unchanged.
- **Debts:** rename atomicity on NTFS `%ProgramData%` and a power cut mid-sync are untested (no Windows run). Core follow-up filed: `inbox/core-enroll-response-reports-vacated-row.md`.
