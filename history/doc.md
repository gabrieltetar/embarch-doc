# doc: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-10

### Added
- A `blocked` task names what unparks it in an `**Unparks when:**` field; `check-task-state.py` requires it and fails a queue path in it that does not exist (`tasks/doc/032`).
- New check-tool-index.py: every MCP tool in embarch-api/src/tools.rs is listed in interfaces/tools.md, and nothing else is.
- `check-doc-size.py --pressure` lists every decision over or within 256 B of its limit, by sub-project, for dispatch notes; printed only, no debt and no failure.
- `check-task-state.py` refuses a second `**State:**` line and a compaction task whose `In flux:` answer is a heading rather than a field (`tasks/doc/077`).
- check-decision-refs.py fails a decision number defined on two live headings in one sub-project; a pointer says "moved", a deliberate split says "half".

### Changed
- A compaction task paid as a ride-along closes `done` with its `In flux: yes` left as written: `check-task-state.py` exempts `done` as it does `Owner: required` (`tasks/doc/083`).
- DOC-BUDGET.md compacted 12,279 -> 9,571 B, out of reserve: provenance, a status claim and twice-told incidents cut; every measured number behind a rule kept.

### Fixed
- A decision pin a split orphans is a NOTE in every gate run naming where the decision went; one moved pin re-keyed (umbrella 26), three retired pins dropped.
- A history roll re-bases the moved window's relative links, so it no longer breaks them; history/*.md has no size reserve, since its assembler rolls it at the cap.
- A task title naming another repo's `README.md` no longer trips the scope-claim check: `check-task-state.py` matches a path whole, not as a substring (`tasks/doc/053`).
- `check-doc-size.py --decisions` lists every over-cap and pinned decision instead of the 20 largest, so all 14 unpinned breaches show, not 6.
- `check-task-numbers.py --next` reads every registered worktree and every ref, so a refill and a worker filing mid-unit no longer get the same number (`tasks/doc/079`).
- check-decision-refs.py checks the number beside a topic-file link, not only inside it; 12 stale cross-repo citations repointed at their index.
- check-decision-refs.py indexes the suite's four decisions, checks `suite decision N` against the suite alone, and resolves task and history files against their scope.
- check-decision-refs.py no longer reads a per-decision byte cap or a thousands-separated size as a decision citation.
- check-decision-refs.py reads a number beside a topic path in inline code and any relative href, and refuses a decisions-file :line citation outside tasks/.
- check-links.py looks a link into a sibling code repo up again where the main checkout lives, so a fresh doc worktree is no longer red on links nobody wrote.
- collect-open-questions.py prints a wrapped open.md bullet whole instead of its first physical line.

### Decided
- A compaction task states the gate verdict, never a byte target; `check-doc-size.py --pressure` prints each file's exact out-of-reserve size, since the 1.2 KB floor governs below 12 KB.
- A compaction task's Must not delete: list names a finding's receipt (symbol, path, confirmed-by sentence) with it; the hot/cold test otherwise drops it as cold.
- A full open.md of live questions is paid by a split into open/<topic>.md, never by striking a live one; a decision is filed by subject, never by room.
- A leg has no number: `.claude/leg.md` says to point at a unit, a log heading's timestamp or a SHA instead, since nothing assigned one and two legs were both 108 (`tasks/doc/054`).
- A spec.md split by mission, spec/<topic>.md, is capped at 10 KB per part like spec.md itself, not 25 KB as legacy; seven existing parts reclassified, all clear.
- A task cites a shared method (the citation census in DOC-CONVENTIONS.md) instead of copying it, so a fix lands once; whoever finds it wrong drops it in inbox/.
- DOC-CONVENTIONS.md: outside embarch-doc, a shipped string names the sub-project (embarch-ui decision 11); a cited file is embarch-doc/<path> from the suite root; no :line.
- DOC-PROTOCOL.md names suite/decisions.md as a suite-level doc: a call binding several sub-projects that none owns; process rules stay in the reserved docs.
- DOC-PROTOCOL.md's link-don't-restate exception covers any guide written for a reader outside the project, not suite/user-guide.md by name; suite/030's split is unparked.
- Decided: no recurring completeness sweep for uncited implementations; `SUITE-REVIEW-PASS.md` records why, the report-where-tripped rule and the reversal condition.
- The citation census has one copy, in DOC-CONVENTIONS.md: case-insensitive, plural, wrap- and anchor-aware, a floor not a coverage claim. No mechanical check, by decision.
- open.md splits by mission into open/<topic>.md at 5 KB each, its own cap; the open-questions collector reads the split files too.
## 2026-09

### Added
- - A `[decision N]` link is now checked against what the topic file it names defines, and `history/`'s 17 are repointed at their indexes — [DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md).
- - A task file can no longer grant a worker a path the ownership map reserves: its title is checked against `check-ownership.py` — [tasks/README.md](../tasks/README.md).
- A task number is checked: `check-task-numbers.py` fails on two files sharing an `NNN` under one scope, or on one reissued after a fold deleted it.
- `/suite-review`: a seven-dimension sweep for design flaws across every sub-project at once, landing as `inbox/` drops. Method: SUITE-REVIEW-PASS.md.
- `check-task-state.py` enforces the four task states at token zero; two tasks that said `partially` were undispatchable and five that said `closed` were never retired. See `tasks/README.md`.
- `fold-commit.py` refuses a fold whose own unit's task file still says `open` or `claimed` — the shape that makes recovery re-dispatch work that already landed (`tasks/doc/028`).
- A doc's last 10% of cap is now a writable reserve whose debt must be filed as a task; check-duplication.py reports a claim held in two files.
- Blocking conditions alert via `scripts/fleet-alert.py` and a Slack webhook: a fleet `@` notifies nobody, since the connector posts as the owner.
- `check-ownership.py --supervisor` now fails on a top-level doc classified by neither list, so a compaction split cannot silently drop a file's protection again.
- An empty queue makes the supervisor propose three real options and stop, rather than inventing work.
- An idle tick with an empty queue dreams too, rate-limited to once per 6 hours.
- The batch boundary is the only safe clear point; the digest is the handoff and phase 0 now reads it.
- inbox/ lets any thread or worker hand the fleet a task without touching git or the queue.
- A decisions entry may own several numbers (`### 20, 21, 25, 27 — …`) so merging entries under a byte budget keeps all 2,354 prose `decision N` references resolvable.
- A suite-scope task is announced by Slack DM and parked, not blocked; the owner can cancel it until the batch ends.
- Background agent threads: one supervisor, 4-6 workers, one repo each, on branches. See embarch-fleet/protocol.md.
- Closing VS Code is the fleet kill switch by design; a killed batch is recovered by phase 0, not prevented.
- Four outside surfaces distinguished: Remote Control steers, the fleet channel logs, cloud sessions investigate, channels are blocked.
- Recorded the git add -A race: workers are safe in worktrees, the supervisor folding in the main checkout is not.
- Slack #embarch-fleet starts, steers and questions the fleet; reactions are the watermark and cron dies with the session.
- The supervisor sizes each wave from the real 5h/7d rate-limit percentages, and stops rather than guessing when they are missing.
- `scripts/check-doc-size.py` enforces per-file size caps by role as a ratchet: a file may shrink freely, but never grow past `min(cap, baseline)`.
- check-decision-refs now fails on a cited reversal row no range file defines.
- check-ownership.py enforces the worker ownership map that was previously prose nothing read.
- status.d/ fragments and a tasks/ queue: a worker never edits a shared suite-level doc or the queue it pulls from.

### Changed
- - `DOC-COMPACTION.md` stops calling itself the budget: it is the invariant, [DOC-BUDGET.md](../DOC-BUDGET.md) the weights, [DOC-COMPACTION-PASS.md](../DOC-COMPACTION-PASS.md) the procedure.
- The doc gate warns instead of failing on findings in gitignored `inbox/` drops, and `check-docs.py` now surfaces a passing check's `NOTE:` lines.
- - Both suite guides now say `embarch-ui` is not in the release archive and where to get it, and its README no longer claims three environment variables when there are four.
- - `embarch.md` §4 draws `embarch-ui` as Core's peer over the shared `embarch-core-client`, and the funnel invariant now names `embarch-topology`'s `hardware` feature, not a process.
- The doc gate's check list is no longer restated in protocol.md, supervise.md or DOC-COMPACTION-PASS.md; they had said six and eight while check-docs.py ran nine. Run the wrapper, read its output.
- A compaction debt is filed at tasks/<scope>/<NNN>-compact-<scope>.md — the scope of the doc, a path its worker owns — not tasks/doc/, which check-ownership.py refuses them.
- DOC-COMPACTION.md splits: §1–§5 stay as the budget, §6–§9 become DOC-COMPACTION-PASS.md, how to run a pass.
- DOC-PROTOCOL.md §7 becomes DOC-CONVENTIONS.md: the shapes scripts parse, loaded when you need one.
- Both protocol docs off their caps; §2's budget table now lists the three roles the checker enforced and it never named.
- Client-identifying names are gone from every repo: the extractor type, the `static_extractor` config value, board ids and prose all use generic names now.
- The fleet's standing rules, log and scripts move to the embarch-fleet repo; `.claude/` and the protocol READMEs here are now generated from it.
- The fleet is now a zero-context listener window, a `fleet start` pump latch, and a relay of four-unit supervisor legs — see [embarch-fleet/protocol.md](../../embarch-fleet/protocol.md) §6.
- The fleet's risk register moved out of embarch-fleet/protocol.md §12 into [embarch-fleet/risks.md](../../embarch-fleet/risks.md), which hit its size cap.
- The four-surfaces comparison and the cloud-session rules moved out of the ops doc into [embarch-remote-surfaces.md](../embarch-remote-surfaces.md).
- The supervisor is a disposable agent; check-ownership --supervisor rejects owner-reserved paths mechanically.
- fleet start spawns a supervisor agent rather than running the batch in the listener session.
- Compaction is lossy by design: efficiency and modularity over losslessness. Every file capped by role, a sub-project is four small files, and git holds what is dropped.
- Dev-workflow compacted, 27 KB to 18 KB; the manual deploy steps are a fallback now that a command does them.
- Every doc is within its cap and the size baseline holds no exceptions.
- Feature inventory moved to suite/features.md and compacted, 45 KB to 13 KB.
- Glossary compacted, 14 KB to 8 KB; it names three study seals now, and no version numbers.
- Reversals split to an index plus stable numeric ranges; 109 rows, none over 17 KB.
- Roadmap moved to suite/roadmap.md and compacted, 40 KB to 13 KB.
- Stream-pipeline proposal reduced to its still-proposed half, 47 KB to 12 KB.
- Token doc compacted, 14 KB to 8 KB.
- User guide moved to suite/, split at the studies chapter, 45 KB to 32 KB across two files.
- embarch.md compacted, 20 KB to 11 KB; the index is grouped tables.

### Fixed
- `check-links.py` ignores link syntax inside fenced blocks and code spans, so a doc can show an example reference; heading anchors are read the same way.
- The changelog assembler merges into the current window instead of opening one per fold; 111 duplicate headings collapsed to 11, all entries intact, and a duplicate now fails the gate.
- build_changelog.py --only lets a fold consume just its unit's fragments, and fold-commit.py refuses one that swept another's — the legs 004/005 failure reached without `git add -A`.
- check-dispatch.py refuses a second worker into a worktree another holds; check-doc-size.py stops citing DOC-COMPACTION.md §8/§9, which moved to DOC-COMPACTION-PASS.md two days ago.
- A code worktree links every sibling in the dependency closure, not the ones its own Cargo.toml names; embarch-ui needs embarch-topology transitively via embarch-core-client.
- A spawned leg does get the Slack connector: it arrives deferred, so ToolSearch must pull it before any tool list shows it. ops.md §5.2a is a contingency, not the state legs 007-009 logged.
- All eight sub-project CLAUDE.md files pointed at design.md, deleted by the four-file split; DOC-PROTOCOL.md §6 now carries the current template and says why check-links.py cannot guard it.
- The PermissionRequest alert hook moved from the gitignored settings.local.json into .claude/settings.json, rendered by install.py and guarded by --check; it no longer fires for AskUserQuestion.
- build_features.py --check validates fragments only; the suite/features.md equality assertion moved to --check-assembled, run on main. A worker shipping a feature can now pass every gate.
- collect-open-questions.py reads a whole open.md, not just an "open question" heading: 100 questions across 11 docs, was 78 across 8. DOC-CONVENTIONS.md records the shape.
- A leg no longer emits shell no permission rule can match (`for` loops, heredoc writes); a `PermissionRequest` hook alerts Slack if one blocks anyway.
- A status line *is* configured; DEGRADED is a missing `rate_limits` payload, not a missing status line — and the two look identical on disk.
- A unit's log entry goes in its fold commit, so landing unlogged is impossible; a dream post now carries `crystal_ball`, which the 6-hour gate can actually read.
- An `inbox/` drop no longer starves itself: the leg drains `inbox/` every leg and counts with `--tasks-only`, so a drop cannot suppress the refill that files it.
- Six rule-bearing files a leg could write are now owner-reserved, and §3's table no longer grants it `scripts/` when the check always refused.
- The dispatchable count is `scripts/queue-status.py`, not four prose copies of "State is open"; a claim held by a dead worker now counts as recoverable.
- The listener's cron fires only while it is idle, so a tick now makes one spawn attempt and ends; an in-turn retry suppressed its own recovery.
- check-ownership defaulted to origin/main, so an unpushed claim commit gave workers phantom violations.
- collect-open-questions read design.md only and missed 88 questions in eight open.md files.
- The documented tick prompt had drifted from the live one and lost the dream step.
- Phase 0 refreshes from origin and re-reads docs; session memory is a cache with no invalidation.
- The fleet marks its own Slack posts robot_face; without it a tick reads its own batch report as a command.
- check-ownership --code-repo died in every code repo; recovery greps matched documentation.
- embarch-core-client is a shared crate too: api owns it, ui path-depends on it.
- inbox/ was missing from check-doc-conventions SKIP_DIRS, so a queue entry failed a doc rule.
- DOC-COMPACTION s10 projection corrected: deletable cold is ~18 percent corpus-wide, not 54.
- The usage gate degrades to a capped wave when percentages are unavailable, and HOLDs on a real 429 instead.
- A worker branches both its code repo and embarch-doc; the two land together, and worktrees live outside every repo tree.
- Reversal rows 59-105 restored: the changelog-stripping pass deleted 47 rows appended below that heading.
- Roadmap said Milestone 7 Phase E was not started; it closed on 2026-08-27.
- Stale section refs into a migrated sub-project decisions.md index dropped corpus-wide.
- User guide said no outpost byte had crossed a real UART, and blamed a diagnosis that was withdrawn.
- `check-doc-size.py --update` may raise a still-over-cap baseline by up to 1 KB for cross-cutting renames, refuses to pin a newly-over-cap file, and needs `--adopt` to bootstrap one.
- check-doc-size prunes a baseline entry for a file that no longer exists.
- check-ownership.py accepts a scope written as embarch-core, not only core.
- check-staleness half A survives embarch.md changing its table shape.
- check-staleness half B was a silent no-op: it read a design.md changelog no doc has.

### Removed
- Every doc's `## Changelog` section, plus the `*.changelog-archive.md` files and `archive-changelog.py` — 643 KB, 25% of the corpus. History now lives in `changelog.d/` fragments.

### Decided
- - A compaction squeeze quotes every deleted hunk verbatim and the reviewer counts them: [DOC-COMPACTION-PASS.md](../DOC-COMPACTION-PASS.md). A squeeze cannot classify its own cuts.
- - `In flux:` is answered per file, `blocked` needs a due date, and `Owner: required` is exempt — [tasks/README.md](../tasks/README.md). Both rules were right; the field was wrong.
- A `history/` entry links a sub-project's `decisions.md` index, not a `decisions/<topic>.md` a mission split can empty; hand edits there survive reassembly.
- A cap overrun lands once on a 7-day clock, the ratchet steps in 1 KB, and a decision has its own 4 KB cap: [DOC-BUDGET.md](../DOC-BUDGET.md).
- A split is the default remedy for a file in reserve; reserve is `max(1.2 KB, 10%)`, and an assembled file has no byte cap.
- Decision 11's reflash half reversed: the build machinery moved to a shared crate instead (reversals rows 113-114).
- A blocked compaction task parks the pass, not the reserve: the compaction rides in the unit that next writes the file.
- `tasks/doc/007` closed: the daily fold gets a script and a subagent, and the 25 KB roll line — which one folded day already exceeded — becomes 40 KB.
