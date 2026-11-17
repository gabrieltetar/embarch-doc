# embarch-chat spec: the handoff

**Status:** active, 2026-11-17.

Split verbatim from [../spec.md](../spec.md) §2 on 2026-11-17, under [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: `spec.md` was in reserve. The bullet is unchanged. Current truth: [../spec.md](../spec.md). Why: [../decisions.md](../decisions.md).

- **An agent can hand its chat to a fresh session** (103): `handoff(prompt)`, a tool of the panel's own MCP server, shows a card with the prompt editable and Continue or Stay (`embarchChat.handoff`: `card`, `immediate`, `off`). Continue starts a new session on the same work item in the same panel, in the chat's mode, model and effort, the old history above a divider; Stay answers the tool and the agent carries on.
