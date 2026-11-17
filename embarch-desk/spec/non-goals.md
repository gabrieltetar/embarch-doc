# embarch-desk: what it deliberately does not do

**Status:** active, 2026-11-17. Split out of [../spec.md](../spec.md) §5 on 2026-11-17, verbatim, when that file reached its reserve line.

## 5. What it deliberately does not do

- **No OAuth but Linear's MCP sign-in (68)** — tokens otherwise ([decision 16](../decisions.md)); EmbArch owns no app registration.
- **No time source but Claude Code sessions and the manual timer** — not VS Code focus, git, Slack or the bench.
- **No in-desk Linear comments, issue creation, PR review or merge** (v2), **no Claude chat panel**: that is `embarch-chat`, a VS Code extension running its own `claude` processes (`embarch-chat` decision 5).
- **No second machine**: one desk service and state file per instance, on the bench's machine. A second instance (69) is a personal desk beside the work one, not a second machine.
- **No archive or approve for agents.**
