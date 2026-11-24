# embarch-promptu: unmeasured

**Status:** active, 2026-11-23.

Moved verbatim from [open.md](../open.md).

- **Parts of Claude Code's hook contract are unmeasured** (contract §3.9): the PostToolUse orphan warning has not run in a real session; whether Edit and MultiEdit get the same move-and-stamp as Write; whether Claude Code loosens `old_string` matching before an Edit (if so, that edit goes unchecked, never wrongly refused); a subagent's write; `autoMemoryDirectory` read from project and local settings, and the managed-settings path. Each needs one real session or a read of Claude Code's docs.
- **The skill has not run in a real session.** Unverified: that Claude Code lists it as `/promptu` and not only `/embarch-promptu:promptu`; what AskUserQuestion returns on Esc (the skill treats no answers as Esc); that `$ARGUMENTS` keeps line breaks. `prep`, `next` and `render` ran end to end against the real model once [2026-10-29].
