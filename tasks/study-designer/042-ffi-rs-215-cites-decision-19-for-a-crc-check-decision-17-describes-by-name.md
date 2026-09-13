# 042 — `ffi.rs:215` cites decision 19 for a decode-time seal check that decision 17 describes by name

**State:** claimed — leg 110, 2026-09-13.
**Doc-size reserve (supervisor, leg 110):** two of your sub-project's docs are in reserve and both are
already filed against a **blocked** compaction task: `embarch-study-designer/spec.md` 9,350/10,240 B
(**890 B left**, `tasks/study-designer/032`) and `embarch-study-designer/open.md` 4,659/5,120 B
(**461 B left**, `tasks/study-designer/026`). Do not compact either as part of this unit; plan around
them. If your work pushes any file into reserve or leaves one there unfiled, file
`tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit
(`scripts/check-task-numbers.py --next study-designer` for the number; never `ls | tail`).
**Source:** found by the worker on `study-designer/040` during that task's sweep and **deliberately
left unfixed as ambiguous** — a different bug shape from the class it was sweeping for, and it said
so in the task file rather than guessing. The `embarch-reviewer` on the same unit then settled it.
Filed by the supervisor (leg 109).
**Scope:** study-designer
**Hardware:** none — one doc comment, no logic change.
**Owner:** no

## What

`embarch-study-designer/src/ffi.rs:215`, on `essd_study_decode_and_verify_full`:

> *"superseding neither `essd_study_decode_and_verify` nor decision 19's existing check"*

The comment sits on the `steps_crc` seal check. **Decision 19 has no decode-time CRC mechanism at
all** — it is the real-time `Outcome` / post-hoc-validation decision, and its post-hoc half was
retired by decision 48.

**The number should be 17.** Decision 17 (`decisions/seals.md`) describes this exact code path
verbatim: *"The FFI decode surface still checks the first seal only… Left as-is with the reason
written at the call site."* Decision 18 — the other candidate the `040` worker named — is Core's
structural pre-flight check, a different call site entirely. **17 is the only decision whose own text
names this function and this check**, which is what settles it.

## Why this was filed rather than fixed in `040`

Worth recording, because the behaviour was right both times. `040`'s worker was sweeping for one
specific class — *a retired mechanism stated as a live fact* — and correctly judged this a different
shape: a **possibly-wrong decision number**, where the cited mechanism is not retired, merely
unrelated. It had no way to settle which number was intended without more certainty than its task
gave it, so it left the site alone and wrote down why. The reviewer, reading with the decisions open,
could settle it in one pass. **A worker declining to guess a decision number is the outcome the
citation rules want**; the cost is one queued task, and that is the right price.

## Done when

- [ ] `src/ffi.rs:215` cites decision 17.
- [ ] **Check the sentence still parses as a claim about the code.** It is a "supersedes neither X nor
      Y" construction, and swapping the referent changes what it is contrasting — read the whole
      comment, not the clause. Say in the task file whether the surrounding wording needed a change
      too, either way.
- [ ] A one-line statement of whether any *other* `decision 19` citation in this crate is the same
      wrong-number shape rather than the retired-mechanism shape `040` closed. `040` swept for the
      second and found three; nobody has swept for the first.
- [ ] `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green.
- [ ] `changelog.d/` fragment only if something reader-visible changed; say which way you judged it.
      `040` judged its equivalent fix reader-visible because it corrected a factually wrong claim —
      a wrong decision number arguably is too. Your call, stated.

## Not in scope

- Any change to the `steps_crc` check itself. Decision 17's *"left as-is with the reason written at
  the call site"* is a standing choice, not a defect; this task fixes the reason's pointer, not the
  choice.
- `tasks/study-designer/041`, the forty dead `§N` section references. Different class, already filed.
