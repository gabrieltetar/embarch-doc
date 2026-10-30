# embarch-promptu decisions: Prompt patterns

**Status:** active, 2026-10-30.

The pass, the guard, the patterns and their questions, paging, the footer. Moved verbatim from `decisions.md` on 2026-10-30, when step 3's fork answers took it past its 25 KB cap ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 9 — Prompt-first, and render, don't rewrite
The owner types a rough prompt, or desk Start work hands Promptu the issue. One stripped Sonnet `claude -p` picks the pattern and fills what the prompt, the work item, memory and last time's answers already say; a dialog asks only what is missing, costliest gap first; the prompt lands in the draft and is never sent. **His words go verbatim under Goal and no model rephrases them**: it keeps his ownership, makes his edits measurable, and lets the chat's form render with no model. The prompt has six headed sections (Goal · Context · Read first · Done when · Constraints · Who does it), only those with content. Esc keeps the answers and turns the rest into assumptions Claude must state. **Rejected:** a rewrite call after the quiz, Haiku for the pass, a UserPromptSubmit hook (it can neither ask nor rewrite), no model (a regex picker scored under half right on hand-labelled asks).

### 22 — The pass runs at effort medium; thinking cannot be turned off
Decided by the owner on 2026-10-29 (fork S1), after the measurement this decision's design asked for. `--model sonnet` is Claude Sonnet 5.5, and through `claude -p` (2.1.287) its thinking cannot be turned off: `--max-thinking-tokens 0`, `MAX_THINKING_TOKENS=0` and `alwaysThinkingEnabled: false` all still return a thinking block [measured 2026-10-29]. `--effort` is the only control, so the design's "thinking off" became a choice of effort, `pass_effort` in `config.toml`, **medium** by default. On 20 of the owner's real task prompts and 3 that fit no pattern [measured 2026-10-29, local data]: right picks 16/20 at low, 18/20 at medium, 16/20 at high; by hand, medium's 16 kept fills were all right and low had 3 wrong of 21; wall time p50 3.6–3.9 s at all three, p95 7.3 s at medium; about $0.02 a run with a new prompt, $0.06 after an hour idle. `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` drops a side call Claude Code makes on every `-p`. **Rejected:** low (3 wrong fills), high (no gain), pinning Sonnet 4.6, where thinking does turn off (p50 8.5 s, dearer, 8 of 11 right).

### 10 — Fill rules
Bench state (board, what is attached, instruments, the gate) is asked on every run, and only the prompt itself may pre-select an answer: what is plugged in changes daily. A fill whose evidence quote is not found in its claimed source is dropped and asked instead. Every question has a recommended option with a one-line why, and one key takes them all; **no recommended option proceeds on a design fork by itself.**

### 11 — A pattern is one Markdown file, in one public, generic set
The frontmatter is the quiz (questions with a header of at most 12 characters, 2–4 options, a recommendation, `required`, `always_ask`, allowed `sources`, `when`, the friction gap it closes, a why); the body is a logic-less Mustache template; `_<id>.md` is a fragment other patterns include. **No local overlay:** anything specific to the owner comes from memory and the desk at run time. The first set is 11 patterns and 2 fragments (implement an issue, review loop, draft a message, relay a colleague's ask, design shaping, address PR comments, research and explain, debug a failure, handoff, bench session, delegate to agents; house rules, bench state); five candidates wait. Every pattern commit passes the client-name and public denylist checks.

### 23 — A reply to a PR comment is `address-pr-comments`
Decided by the owner on 2026-10-29 (fork S2). A reply to a review comment on a pull request, even one comment, goes to `address-pr-comments`; `draft-message` keeps Slack, email and Linear messages. Both patterns' descriptions and pick signals were reworded so they no longer overlap, `draft-message`'s channels became Linear comment, Linear issue, Slack and email, `address-pr-comments` gained a "One comment" choice, and two invented regression examples pin the case. **Why:** the measurement's only misses that recurred at every effort were two such replies, which stream C had labelled as drafts. **Rejected:** keeping both descriptions as approved.

### 24 — A pasted brief is checked for its gaps, not rewritten
Decided by the owner on 2026-10-29 (fork S3). When the prompt is a brief already written for an agent (headed sections, an order of work, a definition of done), the pass runs the pattern of the work it describes, treats the brief as evidence that pre-fills what it answers, and asks only its open required and always-asked questions. **The brief's text stays verbatim**; only the answers to those questions are added after it, under the six headings, and the footer says `mode=brief`. The pass flags a brief, and `prep` also recognises one without the model. **Why:** seven of the owner's sixteen "handoff" asks were such briefs being run, and the measurement's first draw wrapped two of them in a full template. **Rejected:** wrapping a brief in its pattern's template (it rewrites what is written), and sending it as is (its gaps go unasked).

### 25 — A skipped house-rules question adds nothing
Decided by the owner on 2026-10-29 (fork S4). When the pass judges the house rules not relevant, the question is skipped and the prompt gains no constraint: the fragment's `default` is `[]`, where it used to take the including pattern's recommendation ("work in another checkout", "only I open pull requests"). Asked or filled, the rules render as before. **Why:** a constraint nobody chose and the pass saw no reason for should not appear. **Rejected:** the recommendation as the default.

### 26 — The desk work item reaches the terminal through the desk's MCP tool
Decided by the owner on 2026-10-29 (fork S5). The `/promptu` skill calls the desk's `desk_work_item` when the session has the desk, and passes the item to `prep --desk <file>`; **the CLI makes no network calls**. **Rejected:** `prep` calling the desk's `GET /items/{id}/brief` itself.

### 27 — Last answers live in a state file
Decided by the owner on 2026-10-29 (fork S6). `render` keeps each pattern's latest answers per project in `~/.local/state/embarch-promptu/last/<project>.json`, the `last` source of the next run; it holds the answers, not the run (13). **Rejected:** deriving them from the transcripts' newest footer, which holds only `other` for a typed answer and is lost when a draft is edited or the footer deleted.

### 28 — A bare pasted question is a colleague relay
Decided by the owner on 2026-10-29 (fork S7). `colleague-relay` gained an invented example of a question pasted with no speaker named, and its description names the case, since the measurement's pass picked "none" for one at every effort. **Rejected:** leaving it to the chip row.

### 31 — A bench session asks the bench state first
Decided by the owner on 2026-10-29 (fork S8). `bench-session` asks board, what is plugged in, instruments and the green light before its own questions, as one bench check, through a pattern field, `ask_first`, that puts named questions ahead of the usual order (required by gap cost, then always-asked, then relevant optional). That put the required "Pass means" behind the Rest control, so **"take the rest as recommended" applies to optional questions only**: required and always-asked ones are still asked on the next page, and the control's description says so (12). **Rejected:** costliest gap first, which asked "Instruments" after "Pass means" and before "Board".

### 12 — Paging in the terminal
`/promptu` is a skill with `disable-model-invocation: true`. AskUserQuestion takes four questions a call, so a page holds three plus a "Rest" control (keep going, or take the rest of the optional questions as recommended; required ones are still asked, 31), and the last page four; `/promptu --rec` takes every recommendation.

### 13 — The footer is the only record
The footer is the only record of what a run asked and filled; the answers alone are kept per project for next time (27). The rendered prompt ends with one line, `— promptu <pattern>@<version> asked=… filled=… skipped=… assume=…`, about 40–60 tokens; a memory fill names its entry as `memory.<id>`, **the first six hex digits of the SHA-1 of the topic file's name**. Nothing else is stored. **Rejected:** a separate run log, the file stem as the id (up to 40 characters).
