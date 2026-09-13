# 063 — The bare decision citations in `locate.rs`, `init.rs` and `config.rs` have never been checked against their bodies

**State:** claimed by agent/umbrella/063-bare-decision-citations-locate-init-config, 2026-09-13 17:20
**Source:** the leg of 2026-09-13 17:0x, refill sweep. `supervisor-log.md`'s 2026-09-12
carry-forward says **no sweep has been filed yet for `embarch-umbrella`'s own source**, and that
`check-decision-refs.py` resolves numbers only inside `*.md` — a wrong number in a `.rs` comment
that happens to resolve fails nothing.
**Scope:** umbrella
**Hardware:** none — comments and, where a claim has gone false, the prose around them.
**Owner:** no

## What

Three files carry **~37 bare `decision N` citations** between them — `locate.rs` (~20), `init.rs`
(~10), `config.rs` (~7) — with no repo qualifier, so each resolves by convention to
`embarch-umbrella`'s own decision N. `embarch-umbrella` has 52 decisions and every one of these
numbers is in range, **which is what makes this worth a unit**: all of them resolve, so nothing
fails, and the only way to know whether they are right is to read the bodies.

`doctor.rs` carries roughly another 100 and is deliberately out of scope — it is a separate unit,
and one file that size is not a twenty-minute pass.

## The method, which is the whole task

For each bare citation: resolve it in `embarch-doc/embarch-umbrella/decisions/*.md`, **read the
body**, and ask whether the comment's claim is what that decision actually says.

- **Right number, claim holds** → leave it. Most will be this.
- **Wrong repo** → prefix the owning repo, and **re-derive the number in that repo** rather than
  assuming it is the same number. `ui/040`'s reviewer caught two citations prefixed without being
  re-derived; that is this fix's own characteristic failure.
- **Right number, claim has gone false** → the finding that matters. Four consecutive units have
  hit exactly this, twice in this repo: `umbrella/062` corrected a link's depth while its target
  `spec.md` section had been dead four days, and `core/053` corrected a filename while the sentence
  around it had also gone false. **A citation repair that leaves a false claim intact is the defect
  this suite keeps paying for.** Reword to what is true and say so in the commit message.
- **Number resolves nowhere** → say so; do not guess a replacement.

Note two citations already carry a qualifier of a different kind — `config.rs:94` says *"this
repo's decision 16"* — and those are fine as they are; the task is the unqualified ones.

## Constraints

- **Comments and prose only.** No behavioural change, no refactor. A real code defect is a drop in
  `/home/gabriel/Github/embarch/embarch-doc/inbox/` (absolute path), not a change here.
- **Do not renumber or edit any decision body.**
- **Do not touch citation *form*.** Whether a cross-repo `embarch-doc` path is written
  `../../embarch-doc/...` or `embarch-doc/...` is an open, owner-reserved question
  (`tasks/doc/055`). Leave every path exactly as long as you found it.
- **In reserve for `umbrella`:** `embarch-umbrella/decisions/bind.md` at 11533/12288 B (755 B
  left), filed against blocked `tasks/umbrella/009`. If your work spends that reserve, file
  `tasks/umbrella/<NNN>-compact-docs.md` in the same commit.

## Done when

- [x] Every bare `decision N` in `locate.rs`, `init.rs` and `config.rs` has been resolved against
      its body and either left, attributed, or corrected — and the commit message says how many of
      each.
- [x] Gate green (`../../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/umbrella-*` fragment.

## Result

All ~37 bare citations checked against their `embarch-umbrella` decision bodies. Breakdown by file
(commit `551e33c` in `embarch-umbrella`):

- **`init.rs`: 10 of 10 held.** Every bare citation (10, 12, 13, 17×2, 41×5) matched its body.
- **`locate.rs`: 18 of 20 held, 2 fixed.** Both fixes are the same underlying gap: decision 38
  (2026-09-13, adding the Windows service registration read to `locate_core`) landed after these two
  doc comments were written, and neither was updated.
  - `locate_core`'s precedence-order doc cited decisions 7/28 for the whole chain but never mentioned
    the registration read, which now runs first in the WSL2 branch, ahead of the canonical-location
    guess — added `(decision 38)`.
  - `windows_core_service_binary_path`'s doc said `locate_core` "deliberately guesses"; true before
    decision 38, false since — reworded to say it reads the registration first too and only falls
    back to guessing.
- **`config.rs`: 2 of 4 bare citations held, 2 wrong numbers fixed.** (The other ~3 mentions in this
  file already carry the `` `embarch-api` `` qualifier and were out of scope.)
  - The module doc's "(decisions 51/53)" for the two upstream retired-key refusals — decision 51 is
    embarch-api's `zephyr.md` entry (static-project target rejection, unrelated); the real pair is
    embarch-api decisions 53/13 (`shape.md` / `zephyr-scan.md`), confirmed against `mirrors.md`
    decision 16's own "upstream decisions 53/13" phrasing and against this file's own two
    `Config::validate` call sites, which already cite 53 and 13 correctly.
  - `ProjectConfig`'s "minus the fields nothing here reads (decision 20)" — that exact phrase is
    decision 16's own wording (the config-mirror amendment that retired `artifact_path_for_core`),
    not decision 20 (the CI-diff-vs-extract-a-crate question); corrected to decision 16.

No decision bodies were edited; no behavioural change. `doctor.rs` (~100 more citations) is
deliberately untouched, per the task's own scope note.

Gate: `cargo build`/`test`/`clippy --all-targets -- -D warnings` clean (225 tests) in
`embarch-umbrella`. `check-docs.py` in `embarch-doc` is green except a pre-existing
`check-links.py` red on `tasks/doc/054` → `../../embarch-fleet/protocol.md` (that repo isn't
checked out here; unrelated to this task, confirmed present before this unit's changes).
`check-ownership.py` and `check-client-names.py` clean in both worktrees.
