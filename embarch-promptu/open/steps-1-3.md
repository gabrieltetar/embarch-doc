# embarch-promptu: steps 1 to 3

**Status:** active, 2026-11-25.

Moved verbatim from [open.md](../open.md).

- **Block mode is not on yet.** Step 1 is installed in warn mode (2026-10-29) after three review rounds, all findings fixed. The owner's call when to switch it to block.
- **Six design forks wait for the owner** in the repo's `docs/forks.md` (F5–F10; F1–F4 became decisions 18–21): writes the hook cannot see, other memory folders, labels on a body-only edit, warnings to the owner too, a `CLAUDE.md`'s granularity in the menu, memory-id collisions. Each runs on a provisional default meanwhile.
- **Block mode is off** until the owner turns it on after relabelling (decision 6). Three projects were not in the relabelling; their files carry 41 errors between them [measured 2026-10-29 on copies], which warn mode reports as each file is next written.
- **A shell write into a memory folder is unseen** (`>`, `sed -i`, `mv`). `promptu memory check` and the menu's flags show its result afterwards.
- **Step 2 is committed, not installed.** Review round 1 found 17 (1 high, 9 medium, 7 low), round 2 found 2 (1 medium, 1 low) and round 3, the last, found 3 low; all are fixed, and step 2 passed review. Until then the installed plugin is still 0.1.0 and has no `/promptu`.
- **Where a memory is used is untested on real transcripts**: built and tested on invented ones (decision 33); a run in the terminal that was cancelled at "send as is" counts, and a removed worktree's runs are lost. A cold-cache scan time is not measured.
- **Step 3 waits for install.** Review rounds 1 (1 medium, 9 low), 2 (3 medium, 5 low) and 3 (1 low) are fixed; the owner answered P1–P11, P13 and P14 (decisions 33–40), and P16–P19 (`embarch-chat` 94, 96, 99). **Open in `docs/forks.md`:** P12 and P15. Nothing of it has run in the owner's VS Code, against the real Sonnet pass from the chat, or from a real Start work; Claude Code taking `/promptu --item …` from the desk's `vscode://` link is untested.
- **The rewrite's model and wait are unsettled** (decision 42): which model rewrites (`rewrite_model`, default `sonnet`, is a setting) and how long a wait after the last question is acceptable. The build (EMB-196) logs both per run; **owed, owner-side: run ten real `/promptu` prompts, then `promptu stats` for p50 and p95** and pick. EMB-197 (the chat's card) calls `promptu original <run>`.
