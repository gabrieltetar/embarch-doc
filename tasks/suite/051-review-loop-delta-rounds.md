# 051 — Run independent reviewer loops on the delta, with a findings ledger and a stop rule

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 177 fresh reviewer agents in 10 sessions were 54 % of all review-loop cost (3.7 B context tokens) and 30 of 76 active hours; mean peak context per reviewer was 400 k; 16 spend-limit stops; rounds 4–11 of one loop cost 59 M units for 0 high, 3 medium and 30 low findings
**Scope:** suite
**Hardware:** none
**Owner:** required — its command and reviewer template ship in `embarch-fleet/templates/.claude/`, which is owner-reserved. Set on filing by the 2026-10-25 leg; the drop said `no`. A non-template half (the ledger format in a sub-project `spec.md`) can be split out by the owner if he wants the fleet to take it.

## What

Make the fleet's "independent reviewer loop" a defined procedure with a shipped command and reviewer template, so a session does not have to rebuild it by hand. In the field, each session improvised the loop: a detached snapshot per reviewer per round, a brief, and a free-text "already handled" list that every reviewer reread in full. Three changes cut the cost. **(1) Delta rounds.** Round 1 and an optional final round read the whole branch. From round 2 on, a reviewer gets `git diff <last reviewed SHA>..<tip>`, the functions that diff touches, and their direct callers, and reads beyond that only to confirm a finding. **(2) One context pack per loop.** It is built once and read by every reviewer instead of each one re-deriving it: the file map, the spec sections in scope as extracted text with page cites, and the project's rules. **(3) A findings ledger instead of the handled list.** It has one row per finding (id, round, reviewer, severity, file:line, status fixed/rejected/decision, fix SHA) and is kept under the project's untracked `embarch/` folder, not `/tmp`. Reviewers report in a fixed format that the loop parses, so it dedupes the same finding from parallel reviewers and counts severities mechanically. The ledger also carries a **stop rule**: after two consecutive rounds with no high or medium finding, the loop stops, or it hands over to one verifier that reads only the last round's fix diff. A round cap stays as the backstop. Protocol §10's merge-time `embarch-reviewer` is unchanged. This adds a separate mode for pre-PR loops that a session or a leg can run.

## Why now

Reviewer rounds were the most expensive step of every review loop measured: 54 % of cost and 40 % of active wall time, against 6.7 % for all history folding combined. In the 2026-10-13 loop, 60 % of the reviewer spend went to rounds that found only lows. The engineer had to ask "are the review rounds converging?", and the loop's state in `/tmp` was lost twice to a WSL restart.

## Done when

- [ ] A review-loop command and a reviewer agent template ship in `embarch-fleet/templates/.claude/`. They create per-round snapshots outside every repo tree and write the ledger to the project's `embarch/` folder, in the format `spec.md` documents.
- [ ] Briefs for round 2 and later carry the diff since the last reviewed SHA plus the list of touched functions. Only round 1 and the final round read the whole branch.
- [ ] The context pack is built once per loop and every reviewer in that loop reads it. A replay on a suite repo's own branch reports reviewer peak context and cost per round against the field baseline (400 k peak, about 2.5 M units per reviewer).
- [ ] The ledger dedupes one finding reported by two reviewers in the same round (fixture test), and a fix SHA closes the row.
- [ ] The stop rule is implemented and its decision is logged in the ledger: two clean-of-high/medium rounds end the loop or switch to one fix-only verifier, and the round cap is the backstop.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Evidence

### Review-loop costs, field project, 2026-09-09 to 2026-10-20

**Method.** 32 of 89 sessions whose main work was review feedback: 14 human-PR-review, 8 agent-reviewer loops, 7 stack/merge upkeep, 3 manifest patch review/regroup. Main thread and all subagents were counted.
Each tool call was given a step by regex on the tool name and input, and every subagent whose description says review, round, audit or verify went wholly to "reviewer rounds". Each API message's tokens were split evenly over its calls' steps. Cost units = input + 1.25 × cache-write + 0.1 × cache-read + 5 × output, in tokens.
Active wall time comes from one timeline per session (main thread and subagents). Gaps over 15 min count as idle. A slice goes to the main thread's step when the main thread's own gap is 2 min or less, otherwise to the subagent step that ends it. The classing is a heuristic, checked by reading about 40 sampled commands per step; "fix" also holds the code reading done for a fix.

#### Per step, all 32 sessions (845.5 M cost units, 76.0 active h, 544 idle h)

| Step | Cost % | Context tokens (M) | Output (k) | Turns | Calls main / sub | Active h | Wall % | Compactions | Auto-mode denials |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Reviewer rounds (fresh reviewer agents) | **54.4** | 3721 | 1087 | 14207 | 252 / 14838 | **30.1** | 39.6 | 0 | 0 |
| Making the fixes (incl. reading code) | 22.5 | 1536 | 3738 | 4440 | 3355 / 1515 | 15.5 | 20.4 | 4 | 3 |
| Re-verification (builds, per-commit, bench) | 6.4 | 455 | 797 | 909 | 1076 / 15 | 7.2 | 9.5 | 0 | 1 |
| Plans, memory, handoff notes | 2.9 | 148 | 475 | 392 | 441 / 13 | 1.5 | 1.9 | 0 | 2 |
| Patch-series regeneration (manifest) | 2.3 | 148 | 384 | 366 | 339 / 35 | 1.6 | 2.1 | 0 | 0 |
| Commit-message curation at fold | 1.8 | 121 | 265 | 262 | 266 / 1 | 1.0 | 1.3 | 0 | 0 |
| History rewriting (rebase, fixup fold, cherry-pick, force-push, backups) | 1.6 | 121 | 263 | 284 | 285 / 0 | 1.2 | 1.5 | 2 | **11** |
| Replies to reviewers (drafts) | 0.9 | 64 | 232 | 124 | 123 / 1 | 0.8 | 1.0 | 0 | 0 |
| Fold mapping (fold-map, curation notes, blame) | 0.8 | 55 | 133 | 106 | 106 / 2 | 0.4 | 0.5 | 0 | 0 |
| Reading human review comments | 0.2 | 14 | 41 | 66 | 83 / 1 | 0.1 | 0.2 | 0 | 0 |
| Stack rebase after a lower PR moved | 0.2 | 12 | 34 | 43 | 43 / 0 | 0.2 | 0.2 | 0 | 0 |
| Waiting on the engineer (questions, plan approval) | 0.6 | 35 | 118 | 88 | 89 / 0 | 12.8 | 16.8 | 0 | 0 |
| Orientation, text-only turns, other | 5.4 | 357 | 802 | 1098 | 435 / 275 | 3.6 | 4.9 | 0 | 1 |

All fold mechanics together (mapping, curation, history, stack, patch regeneration): **6.7 % of cost and 4.4 active h**.

#### By session group (cost % / active h)

| Step | Human PR review (14 sessions, 50 M, 9.8 h) | Agent reviewer loops (8, 725 M, 59.5 h) | Stack/merge upkeep (7, 3 M, 1.4 h) | Manifest patches (3, 67 M, 5.3 h) |
|---|---|---|---|---|
| Reviewer rounds | 0 / 0 | **58.6 / 28.7** | 0 / 0 | 52.5 / 1.4 |
| Fixes | **46.2 / 2.4** | 20.9 / 11.5 | 43.1 / 0.3 | 20.7 / 1.2 |
| Re-verification | 10.2 / 0.8 | 6.1 / 6.0 | 5.4 / 0.1 | 6.2 / 0.4 |
| History + curation + mapping + stack | 8.0 / 0.5 | 4.1 / 1.8 | 13.0 / 0.1 | 4.6 / 0.3 |
| Patch regeneration | 0.9 / 0.1 | 2.0 / 1.0 | 1.3 / 0 | 6.0 / 0.5 |
| Replies | 2.1 / 0.1 | 0.9 / 0.6 | 0.8 / 0 | 0.8 / 0 |
| Waiting on the engineer | 2.7 / **4.3** | 0.5 / 6.9 | 0 / 0.6 | 0.5 / 0.9 |

#### Ranking and the step that hurt most

1. **Reviewer rounds: 54 % of cost, 30 of 76 active hours.** 177 fresh reviewer agents across 10 sessions. Each had a median run of 23 min and a peak context of 400 k tokens on average (647 k at most), and together they used 72 agent-hours. Spend limits stopped the loops 16 times in 4 sessions, and a WSL restart wiped the loop state in `/tmp` twice. Every reviewer re-read the whole branch. In one loop, 35 reviewers read the same 130 KB app source for a total of 3.9 MB, and all 37 reread the growing list of findings already handled. Returns fell off: in the 2026-10-13 loop, rounds 1–3 cost 41 M units for 1 high and 18 low findings, while rounds 4–11 cost 59 M for 0 high, 3 medium and 30 low. A spec-only loop on 2026-10-08 hit its 10-round cap with 2 mediums still turning up each round.
2. **Making the fixes: 22.5 %, 15.5 h.** This is inherent work, and it is the largest step in human-review sessions (46 %).
3. **Re-verification: 6.4 %, 7.2 h.** 74 per-commit build runs in 15 sessions, through about 12 hand-written build scripts (`percommit.sh` was written in 4 separate sessions). Two "byte-identical" checks were invalid because a worktree build used the main checkout's module.
4. **Fold mechanics: 6.7 %, 4.4 h, and 20 of the 25 auto-mode denials over six weeks.** Those 20 denials, in 14 sessions, hit rebase, cherry-pick, amend or force-push, or a note describing one. Once allowed, each fold was short. Five measured events took 14–32 min and 0.9–3.0 M units each: 43→7 commits in 14 min with per-commit builds, the 79-commit re-slice to 6 in 32 min, the 22→6 patch regroup in 31 min, a PR squash of 20→6 in 16 min, and a 4-branch restack plus atomic push in 27 min. The cost came from deferral. After the 2026-10-08 denials, a 229-line fold map took 76 calls and 46 writes, and it was discarded when the history was re-sliced from the final tree. Along the way the sessions made 97 `fixup!`/`amend!` commits and 46 commits that name a fold target in their message, and wrote 17 one-off sequence-editor, message-fix and conflict scripts.
5. **Patch regeneration: 2.3 %, 1.6 h.** 32 scratch Zephyr worktrees (18 in one session) and 8 hand-written regen or renumber scripts. About 20 manifest "Fix:" commits each had to be split across 2–6 patch commits at curation.

Reading human comments (0.2 %), stack rebases (0.2 %) and reply drafting (0.9 %) are cheap.

#### Part B: workflow pieces

| Piece | Use (excluding this analysis) | What broke without it | Belongs in |
|---|---|---|---|
| Hardware test log + pending-by-hardware | log 55 calls / 30 writes, pending 38 / 20, plan file 80 / 42; 5–6 sessions, 2026-10-08..19 | Before 2026-10-12, results were scattered over plan-file sections and memory notes. The engineer asked for both files that day, and on 2026-10-14 asked "did we run all tests that need me at the office?" Reruns after every fold were tracked by hand. | `api` (ledger plus a pending view computed from topology roles) |
| Bench handoff (bench-state header, live-tools note, handoff plans) | bench-state section in the log; live-tools note 4 calls in 2 sessions; handoff plans 17 calls in 4 sessions; plan files 176 calls in 24 sessions | A 10 h night session restarted from a handoff file and survived 3 compactions. A dead port and the probe wiring had to be restated in every session. | bench state: `api` ledger header; session handoff: a skill (not drafted, little use) |
| Bench lock directory | 70 takes, 67 releases, 82 owner checks; 8 sessions, 10 days | Two sessions shared one board on 2026-10-08. One contention was solved by a 5 s `mkdir` busy-loop. The rule has to be restated in every session's prompt or memory, and a stale lock older than 2 h needs the engineer. | `core`: a lease (Core has only a per-call lock and a per-study port reservation); already drafted as `core-bench-lease.md` by a sibling analysis, so not duplicated here |
| Fold map | 76 calls / 46 writes, 4 sessions, 3 days | Created because auto mode refused the rewrites, then discarded at the re-slice | generated by an `api` stack tool |
| Curation notes (message corrections owed at fold) | 28 calls / 23 writes, 2 sessions | Without them, `fixup!` bodies are lost at the fold. They fed the 14-min fold on 2026-10-19. | the same stack tool (`amend!` commits or a curation file it applies) |
| Reviewer briefs + handled list | 197 calls / 42 writes in 2 sessions' main threads, reread by every reviewer | lost twice to `/tmp` wipes; it grows each round and is reread in full | `suite`: a findings ledger in the review-loop protocol |
