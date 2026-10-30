# embarch-promptu: open

**Status:** active, 2026-10-29.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Step 1 is not fully reviewed and not installed.** Rounds 1 and 2 of three found 3 medium and 7 low findings, all fixed (decision 3); then the binary goes to `~/.local/share/embarch/bin/` and the plugin is installed from the `embarch` marketplace in `embarch-umbrella` (decision 20) once the owner's Claude Code has re-registered it there.
- **Six design forks wait for the owner** in the repo's `docs/forks.md` (F5–F10; F1–F4 became decisions 18–21): writes the hook cannot see, other memory folders, labels on a body-only edit, warnings to the owner too, a `CLAUDE.md`'s granularity in the menu, memory-id collisions. Each runs on a provisional default meanwhile.
- **Block mode is off** until the owner turns it on after relabelling (decision 6). Three projects were not in the relabelling; their files carry 41 errors between them [measured 2026-10-29 on copies], which warn mode reports as each file is next written.
- **Parts of Claude Code's hook contract are unmeasured** (contract §3.9): the PostToolUse orphan warning has not run in a real session; whether Edit and MultiEdit get the same move-and-stamp as Write; whether Claude Code loosens `old_string` matching before an Edit (if so, that edit goes unchecked, never wrongly refused); a subagent's write; `autoMemoryDirectory` read from project and local settings, and the managed-settings path. Each needs one real session or a read of Claude Code's docs.
- **A shell write into a memory folder is unseen** (`>`, `sed -i`, `mv`). `promptu memory check` and the menu's flags show its result afterwards.
- **"Where it's used" is empty** until step 2 writes footers; `promptu memory --json` says so with `used_scanned: false`.
- **No feature-inventory row**: `scripts/build_features.py` has no `promptu` section, so a `features.d/promptu-*` fragment fails its check until one is added.
- **Step 2's first job is a measurement**: the Sonnet pass on 20 real rough prompts for latency, pattern accuracy and fill precision, about $0.50 [assumed]. Its cost and latency today are estimates.
