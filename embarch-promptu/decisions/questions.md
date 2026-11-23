# embarch-promptu decisions: The pass's and the patterns' questions

**Status:** active, 2026-11-23.

The pass's effort, the PR-comment reply, and the owner's answers to build step 2's forks S1, S2 and S4 to S7: decisions 22, 23 and 25 to 28. Moved verbatim from `decisions/patterns.md` on 2026-11-23, when it stood in reserve ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 22 — The pass runs at effort medium; thinking cannot be turned off
Decided by the owner on 2026-10-29 (fork S1), after the measurement this decision's design asked for. `--model sonnet` is Claude Sonnet 5.5, and through `claude -p` (2.1.287) its thinking cannot be turned off: `--max-thinking-tokens 0`, `MAX_THINKING_TOKENS=0` and `alwaysThinkingEnabled: false` all still return a thinking block [measured 2026-10-29]. `--effort` is the only control, so the design's "thinking off" became a choice of effort, `pass_effort` in `config.toml`, **medium** by default. On 20 of the owner's real task prompts and 3 that fit no pattern [measured 2026-10-29, local data]: right picks 16/20 at low, 18/20 at medium, 16/20 at high; by hand, medium's 16 kept fills were all right and low had 3 wrong of 21; wall time p50 3.6–3.9 s at all three, p95 7.3 s at medium; about $0.02 a run with a new prompt, $0.06 after an hour idle. `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` drops a side call Claude Code makes on every `-p`. **Rejected:** low (3 wrong fills), high (no gain), pinning Sonnet 4.6, where thinking does turn off (p50 8.5 s, dearer, 8 of 11 right).

### 23 — A reply to a PR comment is `address-pr-comments`
Decided by the owner on 2026-10-29 (fork S2). A reply to a review comment on a pull request, even one comment, goes to `address-pr-comments`; `draft-message` keeps Slack, email and Linear messages. Both patterns' descriptions and pick signals were reworded so they no longer overlap, `draft-message`'s channels became Linear comment, Linear issue, Slack and email, `address-pr-comments` gained a "One comment" choice, and two invented regression examples pin the case. **Why:** the measurement's only misses that recurred at every effort were two such replies, which stream C had labelled as drafts. **Rejected:** keeping both descriptions as approved.

### 25 — A skipped house-rules question adds nothing
Decided by the owner on 2026-10-29 (fork S4). When the pass judges the house rules not relevant, the question is skipped and the prompt gains no constraint: the fragment's `default` is `[]`, where it used to take the including pattern's recommendation ("work in another checkout", "only I open pull requests"). Asked or filled, the rules render as before. **Why:** a constraint nobody chose and the pass saw no reason for should not appear. **Rejected:** the recommendation as the default.

### 26 — The desk work item reaches the terminal through the desk's MCP tool
Decided by the owner on 2026-10-29 (fork S5). The `/promptu` skill calls the desk's `desk_work_item` when the session has the desk, and passes the item to `prep --desk <file>`; **the CLI makes no network calls**. **Rejected:** `prep` calling the desk's `GET /items/{id}/brief` itself.

### 27 — Last answers live in a state file
Decided by the owner on 2026-10-29 (fork S6). `render` keeps each pattern's latest answers per project in `~/.local/state/embarch-promptu/last/<project>.json`, the `last` source of the next run; it holds the answers, not the run (13). **Rejected:** deriving them from the transcripts' newest footer, which holds only `other` for a typed answer and is lost when a draft is edited or the footer deleted.

### 28 — A bare pasted question is a colleague relay
Decided by the owner on 2026-10-29 (fork S7). `colleague-relay` gained an invented example of a question pasted with no speaker named, and its description names the case, since the measurement's pass picked "none" for one at every effort. **Rejected:** leaving it to the chip row.
