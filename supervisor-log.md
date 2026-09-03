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

The example below uses placeholders on purpose. It once used a real-looking date
and real-looking SHAs, and phase 0 — which reads the newest entry as its handoff
— picked the *template* up as a batch that had run, complete with a hardware debt
that never existed. Second instance of the same root cause as batch 001's
recovery greps: documentation shaped exactly like the data it documents.

```markdown
## <yyyy-mm-dd> — batch <NNN>

**Decided:** anything the supervisor approved on the owner's behalf, suite-wide
first. If it decided nothing, say "nothing" — an empty line here is ambiguous.
**Merged:** `agent/<scope>/<task>` (code `<sha>`, doc `<sha>`). Always both SHAs —
under `embarch-dev-workflow.md` §6 there is no merge commit and no surviving
branch name, so the SHA is the only handle a revert has.
**Blocked:** `agent/<scope>/<task>` — why, and what state the task was left in.
**Hardware debts:** what needs a board, and what board.
**Budget:** verdict at start and end, and the wave size it produced.
**Least sure about:** one sentence. Not optional.
```

---

## 2026-09-03 — batch 003

**First batch run by a supervisor agent rather than the owner's session, and the
nesting works.** Two `embarch-worker` agents dispatched from inside an
`embarch-supervisor` agent, both ran to completion, both reported honestly. The
role split from [ops](embarch-parallel-agents-ops.md) §8.1 is no longer
theoretical: `check-ownership.py --supervisor` ran on this batch's own 16 changed
paths and came back clean, so nothing here reached into the rules.

**Decided:** nothing suite-wide. **The gate held this time.** Checks and merge
ran as one script — pre-merge ownership, then `--ff-only`, then the full gate on
the *merge result*, with an automatic `git reset --hard` back to the pre-merge
SHA on any red. Nothing merged that had not already passed, and there was no
second command that could run past a failure. That closes the thing batches 001
and 002 both flagged; it is worth keeping the shape rather than the habit.

**Merged:** `agent/core/001-events-route-doc-corrections` (doc `e3cdd4e`, **no
code branch** — doc-only, the code worktree carried no commits) ·
`agent/study-designer/003-alloc-only-test-build` (sd `dcefe37`, doc `c6b3c3b`).
Both fast-forward. On the sd merge result I ran the whole feature matrix myself,
not just the default cell the script runs: `alloc` 109 passed, `std`, and
`--all-features` 212 passed, plus `clippy --all-targets --features alloc`.

**Blocked:** none.

**Opened:** three, all from reading the eight `open.md` files by hand —
`api/003` (`schema_version`/`error_kind` are documented on every `--json` object
and appear nowhere in the source), `umbrella/001` (`doctor` check 11 is a
hardcoded warn whose stated reason is false, on the one check meant to catch a
wire mismatch unasked), `core/002` (`/status` version fields, designed in
decisions 12/13 and never built — `umbrella/001` wants one of them). Inbox was
empty; nothing was taken from it.

**Hardware debts:** none new. Both tasks were `Hardware: none` and both were
fully verified host-side. `api/001`'s debt from batch 002 still stands.

**Budget:** DEGRADED at start and at end — no cache on this machine, which is
the documented normal — no 429 in the window either time. Wave 2, both slots
used.

**Two defects in owner-reserved files, reported not fixed** (both dropped in
`inbox/`, both marked owner-only since a worker cannot touch `scripts/` either):

1. **`collect-open-questions.py` does not read the files phase 1 is told it
   reads.** `supervise.md` says it prints "every sub-project's `open.md` … in one
   pass". It reads `design.md`'s *Open questions* section instead, and today
   printed 10 questions across 3 docs — `atlas`, `promptu`, `embarch-token.md`,
   two of which are sub-projects that have not started. The eight `open.md`
   files, 34 KB, are invisible to it. A supervisor following the instruction
   literally sweeps three dormant docs, finds nothing, and **dreams on an empty
   queue while eight active sub-projects' open questions sit unread.** All three
   tasks this batch filed came from files that script cannot see.
2. **`check-ownership.py`'s `--base` defaults to `origin/main`, so every worker
   gets false positives for the whole batch.** The claim commit is made on local
   `main` and not pushed, so local `main` is always ahead mid-batch, and a
   worker's ownership check reports the supervisor's task files for *other*
   scopes as paths it does not own. The `core` worker saw 3, the `study-designer`
   worker saw 4; both diagnosed it correctly and both spent tokens on it. Second
   batch in three where both workers independently hit the same script.

**Worth noting about worker output, not a defect:** both workers marked their
task file `done` in the body rather than deleting it, and `tasks/README.md` says
a done task's file is deleted in the merge that closes it. I deleted both in the
fold. A worker cannot delete it itself without the deletion racing its own
branch, so this may just be how it works — but the README and the observed
behaviour disagree, and one of them should move.

**Least sure about:** filing `core/002` and `umbrella/001` at all. Both are real
and both are quoted verbatim from their own `open.md`, but each one's honest
answer might be "retire the design, do not build it", and I wrote the task so a
worker can reach that conclusion. A queue that grows from what the fleet noticed
while working is the drift `inbox/README.md` already warns about, and three
tasks filed from a sweep the owner did not ask for is exactly that shape. If he
does not want them, that is the signal — not a failure of the tasks.

---

## 2026-09-03 — batch 002

**Decided:** nothing suite-wide. But **I merged past a red check**: on
`study-designer/002`'s doc branch `check-doc-conventions` FAILED and the merge
ran anyway, because it was a separate command in my script rather than gated on
the result. `main` was never red — the offending file was untracked — but §10
exists to stop exactly that, and batch 001's deliberate red-gate exception is the
precedent that makes walking past the next one easier. Second batch running, and
the gate has now been bypassed in both.

**Merged:** `agent/study-designer/002-test-harness-stack-overflow` (sd `9add296`,
doc `2a5573b`) · `agent/api/001-sse-client` (api `974e8f9`, doc `cda9df9`).
All fast-forward.

**Blocked:** none.

**Opened:** `study-designer/003` (`cargo test --features alloc` has never
compiled) and `core/001` (embarch-core's `interfaces.md` lists three event kinds;
Core emits four, so a client written from that row cannot decode transcripts) —
both worker findings, both handed over through `inbox/` rather than fixed in
place. One inbox drop was **closed rather than filed**: `inbox/` failing
`check-doc-conventions` was real and I had already fixed it hours earlier.

**Hardware debts:** `api/001` owes a six-step rig on the deployed Core + bench +
DUT. The one that matters: **provoking `lagged` for real** — host tests
structurally cannot, and if no realistic study can outrun Core's buffer, that is
itself worth recording. Also a `[assumed]` 45 s idle timeout read off axum's
default rather than measured against the deployed build.

**Budget:** DEGRADED throughout, wave 2, no 429.

**What the batch found that I had to act on as the owner, not as supervisor:**
`embarch-core-client` lives in `embarch-api` but `embarch-ui` path-depends on it,
so §10's read-the-diff carve-out named the wrong set — a worker owning `api` can
change `ui`'s dependency without owning `ui`. The worker flagged it and could not
fix it; I widened the carve-out and built `embarch-ui` against the merge result
(green, 87 tests) before landing. **This is the first case where the
owner/supervisor split earned itself**, one commit after being built.

**Least sure about:** the same thing as batch 001, which is the signal. A gate
that has been bypassed in two consecutive batches — once deliberately, once
carelessly — is not a gate. The deliberate one was defensible; the careless one
means the next supervisor should run the checks and the merge as one gated
command, not two.

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
