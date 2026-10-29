# chat: history

**Status:** active, 2026-10-25. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-10

### Added
- A Read, Edit, Write or NotebookEdit step names its file as a link, opening it beside the chat at the line read or the first change (93).
- Decisions 50-85: Claude Code panel parity - folded runs, rewind and fork, reload with Continue, background tasks, per-change diffs, Keep. Built, not yet installed.
- Decisions 86-88: a 💡 preview never moves the menu, menus by keyboard; a step names what it touched as a link; cards and prose use the desk's reference index. Installed 2026-10-25.
- embarch-chat folded into its own docs: spec, decisions 1-85 by topic, open, interfaces; what embarch-promptu became. [spec](../embarch-chat/spec.md)

### Changed
- /embarch-permissions now carries the agent guide's full 54-tool allow/ask split (dated 2026-10-29) and cites suite/agent-guide.md §1.1.
- A chat opens as an editor tab, not in the secondary sidebar, and what it opens goes into the chat's group as a tab beside it; `chatLocation: sidebar` restores the old layout (92).
- The chat sits in a centred column, 80 % of a wide pane and never under 56rem, prose at 64rem; the gutter grows from 8 to 16 px; steps and thinking indent (91).
- embarch-chat decisions 15, 16, 67, 68, 69, 74, 85 moved verbatim from decisions/timeline.md to decisions/readouts.md; timeline.md back under its cap.
- Chat: a background agent's card shows the subagent's report (hand-back, else its last reply) instead of the launch reply; stylesheet cites decision 89 (embarch-chat decision 90).

### Fixed
- /embarch-claude-md now cites suite/agent-guide.md §1.1 (where the block moved from user-guide §7.1); block text unchanged.
- Decision 41's idle close no longer rests on a 5-minute prompt cache: replies write the 1-hour cache (69); reversal row 115.
- File links in replies open: bare names, `~/`, paths from a folder above, `#L42-L51`; a choice when several match, a message when none does (93).
- A background task's notification shows as one line that opens its card, not as a message the owner sent; another session's message folds to its sender (embarch-chat 89).
