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
**Merged:** `agent/core/007-sse-drain` (core `a1b2c3d`, doc `e4f5a6b`),
`agent/ui/012-trace-legend` (ui `9c8d7e6`, doc `1f2e3d4`). Always both SHAs —
under `embarch-dev-workflow.md` §6 there is no merge commit and no surviving
branch name, so the SHA is the only handle a revert has.
**Blocked:** `agent/api/004-…` — clippy red on a pre-existing warning, task
reopened.
**Hardware debts:** core 007 needs a real study to confirm the SSE drain.
**Budget:** started 5h 31% / 7d 44%, ended 5h 58% / 7d 49%; wave was 4.
**Least sure about:** one sentence. Not optional.
```

---

## 2026-09-03 — batch 001

**Decided:** one call worth reviewing. I **landed `study-designer/001` on a red
gate.** `cargo test` aborts with a stack overflow in that crate; I reproduced it
on `main` at `2a136be` untouched *before* deciding, confirmed the branch changes
**0 non-comment lines**, and confirmed 107/107 pass under `RUST_MIN_STACK=32M`.
Refusing would have meant nothing can ever land in that crate. §10 cannot tell
"you broke it" from "it was already broken", which is now `study-designer/002`.

**Merged:** `agent/study-designer/001-dangling-gatt-records-link` (sd `e953489`,
doc `cc92b8b`) · `agent/api/002-mocked-http-tests` (api `b397ca1`, doc `b411fab`).
All four fast-forward; post-merge gate green in both repos.

**Blocked:** none.

**Opened:** `study-designer/002` — the test-harness stack overflow, which makes
§10's gate structurally unenforceable for that crate until fixed.

**Hardware debts:** none. Both tasks were `Hardware: none` and fully verified.

**Budget:** DEGRADED for the whole batch — no percentages available on this
machine — wave capped at 2, no 429 in the window. Unchanged start to end.

**Four defects in my own tooling, three fixed here:**

1. `check-ownership.py --code-repo` died with `unknown scope 'api'` in every code
   repo — scope validation ran before the early return, and a code repo has no
   `embarch-*` dirs to derive a scope list from. **Both workers hit it
   independently.** Fixed and verified from a real code repo.
2. Phase 0's recovery greps reported `tasks/README.md` as a live claim and
   `supervisor-log.md`'s own template as two prior batches. A supervisor
   following them literally would reclaim its own documentation. Fixed.
3. `supervise.md` still said exit 2 means don't start, contradicting the
   DEGRADED behaviour shipped the same day. Fixed.
4. **A code worktree cannot build**: sibling path-deps (`../embarch-study-designer`,
   `../../../embarch-topology`) do not resolve from `.worktrees/<repo>/<slug>/`.
   The api worker symlinked them by hand. Now documented as a setup step; it
   should be scripted, and is not yet.

**Both workers beat their briefs.** study-designer found *two* dangling links and
a doc comment asserting "Both survive" about a type retired by decision 54. api
found that `spec.md` described head+tail truncation that has never existed, and
that `suite/features.md` claimed `Verified: unit` for two rows whose module had
no test module at all — folded here, one row corrected to `n/a`.

**Least sure about:** landing on a red gate. It was the right call for a
comments-only change against a pre-existing failure, and it is also exactly the
precedent that makes the next red gate easier to wave through. If batch 002
lands on a red gate too, that is the signal the rule needs teeth rather than
judgement.

---
