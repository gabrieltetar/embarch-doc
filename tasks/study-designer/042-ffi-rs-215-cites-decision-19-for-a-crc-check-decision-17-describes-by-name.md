# 042 — `ffi.rs:215` cites decision 19 for a decode-time seal check that decision 17 describes by name

**State:** done — agent/study-designer/042-ffi-decision-citation, 2026-09-13.
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

- [x] `src/ffi.rs:215` cites decision 17.
- [x] **Check the sentence still parses as a claim about the code.** It is a "supersedes neither X nor
      Y" construction, and swapping the referent changes what it is contrasting — read the whole
      comment, not the clause. Say in the task file whether the surrounding wording needed a change
      too, either way.

      Re-derived independently (not taken on the reviewer's word): read decision 17, 18 and 19 in full
      (`decisions/seals.md`, `decisions/removed.md`) against the code at `src/ffi.rs:170-286`. Decision
      19 is the real-time `Outcome`/post-hoc-validation decision (`removed.md` #19, #48) — no
      decode-time CRC mechanism, ever. Decision 18 is Core's structural pre-flight check — a different
      call site (Core, not the FFI decode surface). Decision 17 is the only one whose own text names
      this function and this check verbatim: its implementation-findings bullet says "The FFI decode
      surface still checks the first seal only... Left as-is with the reason written at the call
      site" — and the reason at line 253 (`essd_study_decode_full`'s inline comment, "the reason
      `essd_study_decode_and_verify`'s doc comment gives") is that exact reason. 17 is correct.

      The sentence still parses with no further wording change. "Superseding neither X nor Y": X =
      `essd_study_decode_and_verify`, the sibling FFI entry point one function up, which performs the
      identical `steps_crc`-only check via its own bool output. Y, now "decision 17's existing check",
      reads as the narrow single-seal-check design decision 17 established for this FFI surface (the
      same design X embodies and that `essd_study_decode_and_verify`'s own doc comment explains at
      length, lines 176-185). Read this way the sentence is not circular: X names the sibling function
      this one doesn't replace, Y names the standing decision (not to widen the FFI check to cover
      `streams_crc`) that this new, additive function also doesn't override — it just does the same
      established narrow check for a second purpose (dev-bench's real per-`Study` dispatch). True
      before and after the number swap; only the digit needed to change.
- [x] A one-line statement of whether any *other* `decision 19` citation in this crate is the same
      wrong-number shape rather than the retired-mechanism shape `040` closed. `040` swept for the
      second and found three; nobody has swept for the first.

      Swept (`grep -rn "decision 19" --include="*.rs"`): 6 other citations, in `src/result.rs:260`,
      `src/study.rs:381`, and `src/schema_version.rs:59,127,247,260`. Read each in context — all six
      are genuinely about decision 19 (the real-time `Outcome` half that survived, or the retired
      post-hoc half, or its 2026-08-25 amendment) and none share this task's wrong-number shape.
      `ffi.rs:215` was the only wrong-number citation of decision 19 in the crate.
- [x] `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green.
- [x] `changelog.d/` fragment only if something reader-visible changed; say which way you judged it.
      `040` judged its equivalent fix reader-visible because it corrected a factually wrong claim —
      a wrong decision number arguably is too. Your call, stated.

      Judged reader-visible, same reasoning as `040`: filed
      `changelog.d/study-designer-ffi-decode-full-decision-cite.fixed.md`. This is rendered rustdoc
      any reader of the FFI surface sees, and it pointed at the wrong decision's rationale — a
      factually wrong citation, not a style nit.

## Gate note

`check-decision-refs.py` resolves decision numbers only inside `*.md` files. A
wrong number in a `.rs` doc comment that happens to resolve to a real decision
(19 exists, it was just the wrong one) fails no automated check — the gate
staying green here proves nothing about this class of bug; only reading the
source against the decisions it cites does.

## Not in scope

- Any change to the `steps_crc` check itself. Decision 17's *"left as-is with the reason written at
  the call site"* is a standing choice, not a defect; this task fixes the reason's pointer, not the
  choice.
- `tasks/study-designer/041`, the forty dead `§N` section references. Different class, already filed.
