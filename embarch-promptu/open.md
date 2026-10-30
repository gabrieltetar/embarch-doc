# embarch-promptu: open

**Status:** active, 2026-10-29.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Block mode is not on yet.** Step 1 is installed in warn mode (2026-10-29), after three review rounds that found 3 medium and 7 low findings, all fixed, and a clean round 3. The owner's call when to switch it to block.
- **Six design forks wait for the owner** in the repo's `docs/forks.md` (F5–F10; F1–F4 became decisions 18–21): writes the hook cannot see, other memory folders, labels on a body-only edit, warnings to the owner too, a `CLAUDE.md`'s granularity in the menu, memory-id collisions. Each runs on a provisional default meanwhile.
- **Block mode is off** until the owner turns it on after relabelling (decision 6). Three projects were not in the relabelling; their files carry 41 errors between them [measured 2026-10-29 on copies], which warn mode reports as each file is next written.
- **Parts of Claude Code's hook contract are unmeasured** (contract §3.9): the PostToolUse orphan warning has not run in a real session; whether Edit and MultiEdit get the same move-and-stamp as Write; whether Claude Code loosens `old_string` matching before an Edit (if so, that edit goes unchecked, never wrongly refused); a subagent's write; `autoMemoryDirectory` read from project and local settings, and the managed-settings path. Each needs one real session or a read of Claude Code's docs.
- **A shell write into a memory folder is unseen** (`>`, `sed -i`, `mv`). `promptu memory check` and the menu's flags show its result afterwards.
- **No feature-inventory row**: `scripts/build_features.py` has no `promptu` section, so a `features.d/promptu-*` fragment fails its check until one is added.
- **Step 2 is committed, not installed.** Review round 1 found 17 (1 high, 9 medium, 7 low), round 2 found 2 (1 medium, 1 low) and round 3, the last, found 3 low; all are fixed, and step 2 passed review. Until then the installed plugin is still 0.1.0 and has no `/promptu`.
- **No step 2 fork is open**: S1–S8 became decisions 22–28 and 31.
- **The weekly sheet without the Desk** (decision 30) is decided, not built: build step 4.
- **The skill has not run in a real session.** Unverified: that Claude Code lists it as `/promptu` and not only `/embarch-promptu:promptu`; what AskUserQuestion returns on Esc (the skill treats no answers as Esc); that `$ARGUMENTS` keeps line breaks. `prep`, `next` and `render` ran end to end against the real model once [2026-10-29].
- **Where a memory is used is untested on real transcripts**: built and tested on invented ones (decision 33); a run in the terminal that was cancelled at "send as is" counts, and a removed worktree's runs are lost. A cold-cache scan time is not measured.
- **`promptu week --pack` is not stubbed**: SYNTHESIS put a stub in step 2; it belongs with step 4's loop.
