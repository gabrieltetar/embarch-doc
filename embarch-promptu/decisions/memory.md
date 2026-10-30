# embarch-promptu decisions: Memory

**Status:** active, 2026-10-30.

The labels, the hook and its checks, the inventory the memory menu draws. Moved verbatim from `decisions.md` on 2026-10-30, when step 3's fork answers took it past its 25 KB cap ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

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
