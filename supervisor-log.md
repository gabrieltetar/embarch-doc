# Supervisor log

**Status:** active, 2026-09-02. Empty — no batch has run yet.

One entry per supervisor batch, **newest first**. Written by the supervisor at
the end of phase 5 ([embarch-parallel-agents.md](embarch-parallel-agents.md) §6),
and read by the owner as the review surface for work that landed without
approval (§11).

What *shipped* is not restated here — the workers' own `changelog.d` fragments
carry that into `history/<scope>.md`. This file carries what was **decided**,
what did not land, and what still needs a board.

When this file passes 25 KB the oldest entries roll into `history/archive/`,
matching what `scripts/build_changelog.py` already does for a history file.

## Entry shape

```markdown
## 2026-09-02 — batch 001

**Decided:** anything the supervisor approved on the owner's behalf, suite-wide
first. If it decided nothing, say "nothing" — an empty line here is ambiguous.
**Merged:** `agent/core/007-sse-drain`, `agent/ui/012-trace-legend`.
**Blocked:** `agent/api/004-…` — clippy red on a pre-existing warning, task
reopened.
**Hardware debts:** core 007 needs a real study to confirm the SSE drain.
**Least sure about:** one sentence. Not optional.
```

---
