# doc: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB — older windows roll into [archive/](archive/).

## 2026-09

### Added
- A doc's last 10% of cap is now a writable reserve whose debt must be filed as a task; check-duplication.py reports a claim held in two files.
## 2026-09

### Changed
- Both protocol docs off their caps; §2's budget table now lists the three roles the checker enforced and it never named.
## 2026-09

### Changed
- Client-identifying names are gone from every repo: the extractor type, the `static_extractor` config value, board ids and prose all use generic names now.
## 2026-09

### Changed
- The fleet's standing rules, log and scripts move to the embarch-fleet repo; `.claude/` and the protocol READMEs here are now generated from it.

### Fixed
- A leg no longer emits shell no permission rule can match (`for` loops, heredoc writes); a `PermissionRequest` hook alerts Slack if one blocks anyway.
## 2026-09

### Added
- Blocking conditions alert via `scripts/fleet-alert.py` and a Slack webhook: a fleet `@` notifies nobody, since the connector posts as the owner.
## 2026-09

### Added
- `check-ownership.py --supervisor` now fails on a top-level doc classified by neither list, so a compaction split cannot silently drop a file's protection again.

### Fixed
- A status line *is* configured; DEGRADED is a missing `rate_limits` payload, not a missing status line — and the two look identical on disk.
- A unit's log entry goes in its fold commit, so landing unlogged is impossible; a dream post now carries `crystal_ball`, which the 6-hour gate can actually read.
- An `inbox/` drop no longer starves itself: the leg drains `inbox/` every leg and counts with `--tasks-only`, so a drop cannot suppress the refill that files it.
- Six rule-bearing files a leg could write are now owner-reserved, and §3's table no longer grants it `scripts/` when the check always refused.
- The dispatchable count is `scripts/queue-status.py`, not four prose copies of "State is open"; a claim held by a dead worker now counts as recoverable.
- The listener's cron fires only while it is idle, so a tick now makes one spawn attempt and ends; an in-turn retry suppressed its own recovery.
## 2026-09

### Changed
- The fleet is now a zero-context listener window, a `fleet start` pump latch, and a relay of four-unit supervisor legs — see [embarch-fleet/protocol.md](../../embarch-fleet/protocol.md) §6.
- The fleet's risk register moved out of embarch-fleet/protocol.md §12 into [embarch-fleet/risks.md](../../embarch-fleet/risks.md), which hit its size cap.
- The four-surfaces comparison and the cloud-session rules moved out of the ops doc into [embarch-remote-surfaces.md](../embarch-remote-surfaces.md).

### Fixed
- check-ownership defaulted to origin/main, so an unpushed claim commit gave workers phantom violations.
- collect-open-questions read design.md only and missed 88 questions in eight open.md files.
## 2026-09

### Fixed
- The documented tick prompt had drifted from the live one and lost the dream step.
## 2026-09

### Added
- An empty queue makes the supervisor propose three real options and stop, rather than inventing work.
- An idle tick with an empty queue dreams too, rate-limited to once per 6 hours.
- The batch boundary is the only safe clear point; the digest is the handoff and phase 0 now reads it.
- inbox/ lets any thread or worker hand the fleet a task without touching git or the queue.

### Changed
- The supervisor is a disposable agent; check-ownership --supervisor rejects owner-reserved paths mechanically.
- fleet start spawns a supervisor agent rather than running the batch in the listener session.

### Fixed
- Phase 0 refreshes from origin and re-reads docs; session memory is a cache with no invalidation.
- The fleet marks its own Slack posts robot_face; without it a tick reads its own batch report as a command.
- check-ownership --code-repo died in every code repo; recovery greps matched documentation.
- embarch-core-client is a shared crate too: api owns it, ui path-depends on it.
- inbox/ was missing from check-doc-conventions SKIP_DIRS, so a queue entry failed a doc rule.
## 2026-09

### Fixed
- DOC-COMPACTION s10 projection corrected: deletable cold is ~18 percent corpus-wide, not 54.
- The usage gate degrades to a capped wave when percentages are unavailable, and HOLDs on a real 429 instead.
## 2026-09

### Added
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
