# promptu: history

**Status:** active, 2026-11-09. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-11

### Added
- Promptu's week status, week show and desk read the week folder, offline (contract §9, §14.4); status gains running.
- Added: promptu week pack writes the week's run events (footer facts, the owner's edit as a diff, chat or terminal) to week/<week>/pack.json; no model.
- Promptu weekly pass: the contract now specifies promptu week (pack, draft, run, status, show, mark, apply, timer) and desk, the sheet and the week folder; nine forks open (EMB-272).
- A Bash command that writes a memory MEMORY.md now gets a warning naming the Edit tool, since a shell write skips the index checks; reads get nothing (promptu hook).
- promptu prior lists the questions an earlier run of a prompt asked and the answers, read-only, from a transcript folder (EMB-185).
- Promptu rewrites a rough prompt after the questions and logs the original; `promptu original <run>` prints it, `promptu stats` gives p50/p95 of the wait (decision 42).
- promptu calls <session> counts a session's tool calls and result characters per subagent and activity class, and lists one class's calls with sizes.
- Promptu's pass accepts the chat's context usage (prep --context-usage) and names a way in Who does it for high-context work, footer way=; see contract §7.10.

### Changed
- Promptu's decisions 22, 23 and 25 to 28 moved verbatim from decisions/patterns.md to decisions/questions.md, bringing patterns.md out of reserve.
- Split promptu spec.md: build steps 2 and 3 moved verbatim to spec/build-steps.md, 9,563 to 6,949 B ([spec](../embarch-promptu/spec.md)).
- Promptu decision 39 retired: the chat's handoff card and chip are gone (embarch-chat 36, 97).
- Promptu decision 40 amended: the rail's icons are one-colour SVGs, not emoji, following chat 94 (EMB-56).
- promptu I2 on a header-less MEMORY.md now says the first `## <domain>` header may be added in the same write (decision 21).
