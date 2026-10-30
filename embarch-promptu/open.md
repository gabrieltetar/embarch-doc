# embarch-promptu: open

**Status:** active, 2026-10-29.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Block mode is not on yet.** Step 1 is installed in warn mode (2026-10-29), after three review rounds that found 3 medium and 7 low findings, all fixed, and a clean round 3. The owner's call when to switch it to block.
- **Six design forks wait for the owner** in the repo's `docs/forks.md` (F5–F10; F1–F4 became decisions 18–21): writes the hook cannot see, other memory folders, labels on a body-only edit, warnings to the owner too, a `CLAUDE.md`'s granularity in the menu, memory-id collisions. Each runs on a provisional default meanwhile.
- **Block mode is off** until the owner turns it on after relabelling (decision 6). Three projects were not in the relabelling; their files carry 41 errors between them [measured 2026-10-29 on copies], which warn mode reports as each file is next written.
- **Parts of Claude Code's hook contract are unmeasured** (contract §3.9): the PostToolUse orphan warning has not run in a real session; whether Edit and MultiEdit get the same move-and-stamp as Write; whether Claude Code loosens `old_string` matching before an Edit (if so, that edit goes unchecked, never wrongly refused); a subagent's write; `autoMemoryDirectory` read from project and local settings, and the managed-settings path. Each needs one real session or a read of Claude Code's docs.
- **A shell write into a memory folder is unseen** (`>`, `sed -i`, `mv`). `promptu memory check` and the menu's flags show its result afterwards.
- **No feature-inventory row**: `scripts/build_features.py` has no `promptu` section, so a `features.d/promptu-*` fragment fails its check until one is added.
- **Step 2 is committed, not reviewed or installed.** Its three review rounds come next; until then the installed plugin is still 0.1.0 and has no `/promptu`.
- **Five step 2 forks wait for the owner** in the repo's `docs/forks.md` (S4–S8; S1–S3 became decisions 22–24): a skipped house-rules question rendering its recommendation, the desk work item in the terminal, where last answers live (a state file today, against decision 13's "nothing else is stored"), an untagged pasted colleague message, and the order of the always-asked questions.
- **The skill has not run in a real session.** Unverified: that Claude Code lists it as `/promptu` and not only `/embarch-promptu:promptu`; what AskUserQuestion returns on Esc (the skill treats no answers as Esc); that `$ARGUMENTS` keeps line breaks. `prep`, `next` and `render` ran end to end against the real model once [2026-10-29].
- **"Where it's used" is still empty**: footers are written now, but `promptu memory` does not scan transcripts for them yet (contract §5 `used`).
- **`promptu week --pack` is not stubbed**: SYNTHESIS put a stub in step 2; it belongs with step 4's loop.
