# embarch-promptu: open

**Status:** active, 2026-10-29.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **Step 1 is not reviewed and not installed.** Three independent review rounds come first (decision 3); then the binary goes to `~/.local/share/embarch/bin/` and the plugin is installed, which waits on where it is listed.
- **Ten design forks wait for the owner** in the repo's `docs/forks.md`, five of them before block mode: T7's level-blind comparison, the `CLAUDE.md` rule's "at the top level" wording, where the plugin is listed, a new index's first headers, and writes the hook cannot see. Each runs on a provisional default meanwhile.
- **Block mode is off** until the owner turns it on after relabelling (decision 6). Three projects were not in the relabelling; their files carry 41 errors between them [measured 2026-10-29 on copies], which warn mode reports as each file is next written.
- **Parts of Claude Code's hook contract are unmeasured** (contract §3.9): the PostToolUse orphan warning has not run in a real session; whether Edit and MultiEdit get the same move-and-stamp as Write; whether Claude Code loosens `old_string` matching before an Edit (if so, that edit goes unchecked, never wrongly refused); a subagent's write; `autoMemoryDirectory` read from project and local settings, and the managed-settings path. Each needs one real session or a read of Claude Code's docs.
- **A shell write into a memory folder is unseen** (`>`, `sed -i`, `mv`). `promptu memory check` and the menu's flags show its result afterwards.
- **"Where it's used" is empty** until step 2 writes footers; `promptu memory --json` says so with `used_scanned: false`.
- **No feature-inventory row**: `scripts/build_features.py` has no `promptu` section, so a `features.d/promptu-*` fragment fails its check until one is added.
- **Step 2's first job is a measurement**: the Sonnet pass on 20 real rough prompts for latency, pattern accuracy and fill precision, about $0.50 [assumed]. Its cost and latency today are estimates.
