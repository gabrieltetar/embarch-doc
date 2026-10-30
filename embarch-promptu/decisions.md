# embarch-promptu: decisions

**Status:** active, 2026-10-29.

Why Promptu is shaped this way. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). Reference: [interfaces.md](interfaces.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). 1–17 are the design the owner approved on 2026-10-29, after a research pass over published prompting practice, prior tools and his own sessions; they hold from build step 1 on, and the step that builds each one may refine it here. 18–21 are his answers the same evening to four forks step 1 raised. Cite them as `embarch-promptu decision N`. 22–24 are his answers to build step 2's measurement and its first forks, 25–28 and 31 his answers to its later forks, and 29–30 his requirement that Promptu work without the rest of EmbArch. 32–33 were built in step 3 where the design left the mechanics open; their open details wait in `docs/forks.md`. Choices the design leaves open are in the repo's `docs/forks.md` until the owner picks: F1–F4 (18–21) and S1–S8 (22–28, 31) are decided; F5–F10 are open.

## What Promptu is

### 1 — Its own sub-project again, as a plugin plus a CLI
Decided by the owner on 2026-10-29, so Promptu can be used without `embarch-chat`. **This reverses `embarch-chat` decision 6**, where `embarch-promptu` became `embarch-chat`. It ships as one Claude Code plugin, `embarch-promptu@embarch`, and a `promptu` CLI that prints its data as JSON; it works in the terminal and in Claude Code's panel, and `embarch-chat` finds it installed and draws its menus. Promptu owns two things: memory organisation and prompt patterns. `embarch-chat` keeps the 📚 library and the 💡 assistant. **Rejected:** staying inside `embarch-chat`, which tied both to one UI.

### 29 — Promptu works with or without the rest of EmbArch
Decided by the owner on 2026-10-29. Promptu stands alone: the binary and the plugin need nothing else from the suite, and the README and spec describe standalone use first, EmbArch as the optional integration. **Detection is automatic with a config override**: the `/promptu` skill checks which EmbArch parts its session has, the desk (`desk_work_item`) and the bench tools (`embarch-api`), and passes them as `prep --have`; an `[embarch]` table in Promptu's `config.toml` forces each to `on` or `off`, `auto` by default. **What needs a missing part is hidden and a generic fallback stays**: a pattern marks such a question or option `requires: desk`, `requires: embarch-api`, or `requires: item` (the desk **and** a work item passed to the run, for anything that reads or writes the item); without it, it is not shown, filled or rendered, the model's catalogue leaves it out, and no text fill may equal a hidden label; a hidden recommendation gives way to the first option that shows (bench-session's "flash through EmbArch" gives way to "the project's own tooling"), and lint checks every `requires` and that each question keeps 2–4 options without EmbArch. **Install alone** with `cargo install --git …` or a release binary in `~/.local/bin`; inside the suite the binary stays in `~/.local/share/embarch/bin`. **Rejected:** requiring the desk for `/promptu`, and per-user pattern variants.

### 2 — Rust, one binary
Like `embarch-desk`: the hook runs on every file write in every session, and a Rust hook call costs about a millisecond [measured 2026-10-29]. **Rejected:** TypeScript (shares code with the chat, pays Node's start on every write), Python (fastest to write, tens of milliseconds a call [assumed]).

### 3 — Five build steps, each usable alone; built by agents under a contract
1 memory · 2 `/promptu` in the terminal · 3 Start work, the chat's dialog and rail · 4 the weekly loop and the Desk section · 5 the 💡 linker's new kinds. Background agents build each step in their own worktree, the contract (`docs/contract.md`) first, then three independent review rounds; nothing is installed before review passes. **A design fork goes to the owner's ranked list (`docs/forks.md`) and runs on its most reversible default; an agent never decides one.**

### 20 — The `embarch` marketplace moves to `embarch-umbrella`
Decided by the owner on 2026-10-29 (fork F3): the suite's `embarch` marketplace, until then a file in `embarch-desk`'s repo, moves to `embarch-umbrella` and lists every suite plugin, so this plugin keeps the id `embarch-promptu@embarch`. **Moved and re-registered 2026-10-29:** `embarch-umbrella/.claude-plugin/marketplace.json` lists `embarch-desk`, `embarch-promptu` and `embarch-chat`, each a `git-subdir` source (`url` + `path: plugin`). A `github` source with `path`, tried first, installed the whole repo as the plugin, so the plugin's manifest, hooks and MCP config were not found [measured on Claude Code 2.1.287]. `embarch-desk`'s file is gone. **Rejected:** a second entry in `embarch-desk`'s file (a suite list in one plugin's repo), a marketplace in this repo named `embarch` (clashes with the desk's) or named after it (changes the decided id).

## Memory

### 4 — Two labels: a kind beside Claude Code's `type`, and a domain
`kind` is one of `preference` · `rule` · `trap` · `reference` · `status`, and must match Claude Code's `type` (user · feedback · feedback · reference · project). A `status` carries `review-by` at most 90 days ahead: stale status is the memory most likely to mislead. A `reference` carries `source` (a repo path, an absolute path, a URL or a commit), a `trap` when there is one. The domain is the `## ` header the index line sits under; the headers are the domain list, and the owner adds them, never a tool write. Index lines stay within 150 characters and state the fact, because a later pass reads only the index. **Read at either level**, top or `metadata:`, since Claude Code moves the keys (18). **Rejected:** replacing `type` (fights Claude Code's own instructions), mapping `type` alone (cannot tell a trap from a rule or status from a reference), a domain field per file.

### 5 — A hook checks every memory write, with no model
A PreToolUse hook on Write, Edit and MultiEdit into an auto-memory folder runs T1–T7 on a topic file and I1–I5 on the index, **on what the write touches**, and fails open; a PostToolUse warning names orphaned topic files. Claude keeps writing memories freely. **Why a hook:** in a four-run test, one model dropped a field it had not written when it rewrote a memory, and no model added `kind` unprompted; a rule that must hold goes in a hook. What T7 counts as a dropped field: 18. When a new domain header is allowed: 21. **Rejected:** a model judging each write (cost and latency on every write), checking whole files on every write (old long lines would block unrelated writes).

### 6 — Warn first; block after relabelling
`memory_hook = "warn" | "block" | "off"` in `~/.config/embarch-promptu/config.toml`, warn by default. Warn lets the write through and tells Claude what to fix (`additionalContext`); block refuses a write with an error (exit 2, the reason on stderr). Existing memories are relabelled first, from a ✓/✕ sheet applied with backups, then the owner turns block on. **Neither mode answers with a permission decision**: an `allow` would skip the user's own prompt. **Rejected:** blocking from the first day, when most index lines were over 150 characters.

### 18 — T7 ignores the level, and Claude Code's three stamped fields
Decided by the owner on 2026-10-29 (fork F1). On a Write into a memory folder, Claude Code moves every frontmatter key but `name` and `description` under `metadata:` and stamps `node_type`, `originSessionId` and `modified` afresh [measured 2026-10-29, 2.1.287]. So T7 treats `kind` and `metadata.kind` as one field and does not count those three as dropped; losing `type`, `source`, `review-by` or any other field is still refused, and every other check reads a field at either level. **Rejected:** T7 literal, every key at every level, which refuses rewrites that lose nothing.

### 21 — Domain headers are free until the index has one
Decided by the owner on 2026-10-29 (fork F4), extended by this build to the same case in an older file. I3 refuses a `## ` header the index did not have **only once the index has at least one**: a new `MEMORY.md`, or one written before domains existed, may add its headers in the write that creates or repairs it. **A write that removes every header of an index that had some is refused too**, or the rule could be dodged in two writes: empty the list, then add any headers. **Why:** I2 wants every touched index line under a header, so with I3 strict from the start, block mode could never create or repair a header-less index. **Rejected:** refusing and having Claude ask the owner for the domains (it stalls a background agent on its first memory), a default domain list per machine.

### 7 — The hook lives in the Promptu plugin
The owner's split puts memory organisation in Promptu. **Rejected:** `embarch-desk`'s hook binary, which already sees every tool call but owns time and work items, not memory.

### 8 — The memory menu, v1
`promptu memory --json` feeds it; the terminal prints the same view. Entries grouped by scope (user, each project's auto memory, its `CLAUDE.md` files), then domain, then kind; **stale** flags for a past `review-by`, a `source` path that is gone, and a missing label; **where an entry is used**, from the footers that name it (decision 13). The only action is open to edit. **Rejected:** showing each memory's startup cost.

## Prompt patterns

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

## Learning

### 14 — A weekly ✓/✕ sheet, drafted locally
A systemd user timer runs a stripped Opus `claude -p` every Wednesday at 08:00 (`Persistent=true`), about $1.5–3 a week [assumed]. Its inputs: friction in sessions, his edits, skipped and overridden questions, prompts no pattern matched, outcomes, and a quarterly or new-model refresh of published practice. **Every event becomes a proposal**; a specific fact becomes a memory entry, so patterns stay generic. He approves the sheet in a Promptu section of the Desk tab, the spot `embarch-desk` decision 65 kept, hidden while it has nothing open. **The ping is the Desk section alone**: no Slack message, since the desk's Slack connector is gone (`embarch-desk` decision 66). **Rejected:** 👍/👎 clicks and memory corrections as inputs, cloud routines (the data stays local), the fleet, a session cron (it skips while the session is busy).

### 30 — The weekly sheet works without the Desk
Decided by the owner on 2026-10-29; **not built** (build step 4). Without the Desk, the weekly ✓/✕ sheet is a Markdown file applied with `promptu week apply`, and a `/promptu:review` skill walks it in the terminal. With the Desk present, its Promptu section shows the same sheet (14). **Rejected:** a sheet only the Desk can show.

### 15 — Success after four weeks
Reported on each sheet: corrections per prompt at or below 0.10 against non-Promptu sessions as a control, redirected messages per task start down about 30%, at least 90% of pre-filled answers kept, at least 85% of picked patterns kept, questions per run falling, and a one-key "better · same · worse" line.

## The chat and the desk

### 16 — Start work runs the pass on the issue; the rail; the linker
From step 3, desk Start work runs the pass on the issue itself and leaves the improved start prompt in the draft, replacing today's read-and-summarize starter. `embarch-chat` gains a left rail, folded like VS Code's activity bar, holding Memory, Promptu, 📚 and 💡. The 💡 becomes the reference linker, gaining datasheet and spec sections through the atlas, instruments, captures and traces, Linear projects and docs, branches and worktrees, Kconfig symbols and devicetree nodes; Promptu owns missing context and improvement. **A reply inside a running task is never touched.**

### 17 — The owner's `CLAUDE.md` carries the rules
The memory rule went live on 2026-10-29, worded as 19 says. With step 2 come rules on design forks (interactive work waits for his pick), asking, web research in his own wording, and ignoring the footer. **Rejected:** "take the recommendation and proceed" as a standing rule.

### 19 — The memory rule says "in its frontmatter", not "at the top level"
Decided by the owner on 2026-10-29 (fork F2): the global `CLAUDE.md` rule tells Claude to add `kind:` "in its frontmatter (Claude Code may move it under `metadata:`)", since Claude Code moves it there on the next Write (18). The hook's T2 message says the same. **Rejected:** keeping "at the top level", which a file Claude wrote by the rule stops matching after one write.

### 32 — Start work takes the desk's default pattern, never a `never` one
Built in step 3 from 16 and the pattern field `signals.desk` (11): `promptu prep --start` marks a desk Start work run, which the chat sends for its own Start work and the skill's `--item` for the panel's. A pick that is missing, unknown or a `signals.desk: never` pattern becomes the `default` one, `implement-issue`; offline, so does the keyword pick; a `possible` pick (a bug, a bench validation, a review) stands. A replaced pick opens the chip row with the default recommended, so one Enter confirms it — **provisional**, an open choice in the repo's `docs/forks.md` (step 3). **Rejected:** forcing `--pattern implement-issue`, which would turn every bug into an implementation.

### 33 — Where a memory is used: the footers sent, and the ones the terminal shows
Built in step 3 for the memory menu (8), from the footer as the only record (13). A use is a fill from the entry in a footer of the last 30 days in this project's transcripts, found in **the owner's own sent message** (the chat's route) or in **`promptu render`'s JSON as a tool result** (the terminal skill's route, where the prompt is shown and not sent), once per transcript; never in Claude's own text. A `memory.claude-md` fill names the global `CLAUDE.md` as a file. **Provisional** in its details (a cancelled terminal run counts; a removed worktree's runs are lost), listed in `docs/forks.md` (step 3). **Rejected:** a run log of Promptu's own (13).
