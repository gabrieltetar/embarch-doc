# 044 — `manifest.rs` cites decision 14 for a claim decision 14 itself assigns to decision 24

**State:** done — worker umbrella/044, 2026-09-10 (`d06bb64`) — cited both 14 and 24, per the
leg-063 supervisor's note, not the title's proposed revert. See "Resolution" below.

## Dispatch note, leg 065

**Doc reserve in your scope is the tightest in the suite, and three of the four files are parked.**
`embarch-umbrella/spec.md` 10,104 / 10,240 B (**136 B left**), `embarch-umbrella/open.md`
4,870 / 5,120 B (**250 B left**), `embarch-umbrella/decisions/bind.md` 11,409 / 12,288 B (879 B
left) — all three already have compaction tasks filed (`umbrella/038`, `umbrella/009`) and both are
`blocked` on `In flux: yes`, so **you owe no new compaction task for them**. Plan to write **no new
prose** into `spec.md` or `open.md`: at 136 B you cannot say anything true about this. This unit is
a source-comment repair; keep the doc side to a `changelog.d/` fragment and, if anything, a
one-clause edit inside an existing sentence.

**Closing this as "no change needed" is a legitimate and possibly correct outcome.** Re-derive the
argument yourself from the two decision **bodies** (`decisions/install.md` #14 and
`decisions/schema-skew.md` #24) before touching the comment. **Do not replace 14 with 24** on the
strength of this task's title — that is the specific outcome the note below argues against, and
the "real but wrong decision" failure mode the suite has already paid for. The cheap improvement,
if you take one, is citing **both** with the split named (14 for the manifest being read at all, 24
for why a mismatch warns).

**Done-when item 2 is a real second pass and is in scope**: check whether any other production
comment in `umbrella/043`'s sweep pairs a decision-14 citation with 24's specific claim. If it
does, fix it here; if you cannot audit it fully, say exactly how far you got.
**Source:** reviewer pass on umbrella/043 (`ea9b72a`), `src/manifest.rs` lines 1-5

## Supervisor's note, leg 063, 2026-09-10 — I checked this and I do not agree with the revert

I read both decision bodies before accepting or applying anything, and the conclusion is that
**`decision 14` is the better citation of the two, not the wrong one.**

- **Decision 14's own body states the cited fact literally:** *"A version mismatch against the suite
  manifest is a warning (decision 24)."* The clause the comment quotes is therefore **in decision
  14**, and decision 14's third paragraph is also the only place that says `doctor` reads the manifest
  at all — *"which `doctor` reads only when one happens to sit next to the running binary — absent
  for a per-repo release or a debug build, reported as skipped rather than failed."* That is exactly
  `manifest.rs`'s subject.
- **Decision 24 is about a different thing.** `decisions/schema-skew.md`'s decision 24 is *"Version
  skew between Core and the API stays a warning, not a refusal"* — the Core/API pair, not the suite
  manifest. Decision 14 cites 24 for the **warn-not-refuse posture**, applying it by analogy; it does
  not hand the manifest behaviour over to it. Re-pointing `manifest.rs` at 24 would send a reader
  about the suite manifest to a decision about Core-versus-API skew, which is the *real but wrong
  decision* failure mode `api/031` is the recorded case of.
- So the reviewer read decision 14's parenthetical `(decision 24)` as a handover and it is a
  cross-reference. **This is the mirror of the mistake the same leg caught in `core/008`**, where a
  correct citation looked wrong because only the decision's body — not its heading or its
  parentheticals — says what it covers.

**What is left that is genuinely worth doing, and it is small.** Decision 14 is a *distribution*
decision whose body happens to carry two `doctor` facts, so any citation of it for a `doctor`
behaviour is ambiguous-looking even when correct — which is why both the worker and the reviewer
stopped on this line independently. The cheap improvement is to cite **both**, e.g. *"decision 14, and
decision 24 for why it is a warning rather than a refusal"*, or to move nothing and accept it. What
must **not** happen is a worker replacing 14 with 24 on the strength of this drop's title. Whoever
takes it re-derives the argument above from the two decision bodies first, and closing this as
"no change needed" is a legitimate outcome.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`src/manifest.rs`'s module doc, as rewritten by umbrella/043, reads:

```
//! shipped (decision 14: "`doctor` warns when the installed
//! component versions don't match the suite manifest").
```

`embarch-umbrella/decisions/install.md`'s own decision 14 entry ends: **"A
version mismatch against the suite manifest is a warning (decision 24)."**
Decision 24 lives in `decisions/schema-skew.md` and reads: "Version skew
between Core and the API stays a warning, not a refusal." The quoted clause in
`manifest.rs` — "doctor warns when the installed component versions don't
match the suite manifest" — is decision 14's own paraphrase of decision 24's
subject, not decision 14's. Decision 14 itself is about *what gets
distributed* (the suite archive, its four targets, the manifest file's
existence); it explicitly hands the warn-vs-fail behavior off to 24.

This is not a case the task's own item 2 (the `decision 14` in this same file
the worker deliberately left alone reasoning about check-1/manifest-reading
being decision 14's subject) resolves — that reasoning covers *why check 1
reads the manifest at all*, which is fair to leave at 14. But the sentence as
written puts a quoted, specific behavioral claim ("warns when versions don't
match") under 14's number when 14's own text sends that exact claim to 24.

## Why now

umbrella/043 (`ea9b72a`) touched this exact line — stripping `design.md §3`
down to bare `decision 14` — while leaving the citation number unresolved
against `decisions/install.md`'s explicit forwarding text. The commit message
claims every number was "resolved... against the naming repo's decisions/
index," so this one slipped through that check rather than being a
deliberate, noted boundary like the manifest/decision-14 call the task
flagged separately (that one attributes the *check exists* framing to 14,
correctly).

## Done when

- [x] `src/manifest.rs`'s doc comment either cites decision 24 for the
      quoted warn-behavior clause, or cites both (14 for "the manifest is
      read at all," 24 for "and a mismatch warns").
- [x] No other production comment in this sweep repeats the same pattern
      (a decision-14 citation paired with 24's specific claim) — not
      independently re-audited by this reviewer, worth a second pass by
      whoever picks this up.

## Resolution, worker (umbrella/044), 2026-09-10

Agreed with the leg-063 supervisor's note, not the task title. Re-read both
decision bodies before touching anything:

- `decisions/install.md` #14's own text: *"A version mismatch against the
  suite manifest is a warning (decision 24)."* — 14 is also the only place
  that says `doctor` reads the manifest at all.
- `decisions/schema-skew.md` #24: *"Version skew between Core and the API
  stays a warning, not a refusal"* — Core/API skew, not the suite manifest.
  Nothing in 24's body mentions the suite manifest.

Re-pointing `manifest.rs` at 24 alone would send a reader about the suite
manifest to a decision about a different pair of binaries — the *real but
wrong decision* failure mode `api/031` already paid for. Took the cheap
improvement instead: `src/manifest.rs`'s doc comment now cites **both** —
14 for the manifest being read at all, 24 for why a mismatch warns rather
than refuses. Commit `d06bb64`, branch `agent/umbrella/044-manifest-decision-14`.

**Done-when item 2, full audit, not partial:** `grep -rn "decision 14" src/`
across the whole `embarch-umbrella` tree returns exactly one hit — the
`manifest.rs` line just fixed. `decision 24` appears twice elsewhere
(`src/doctor.rs:2348`, `src/doctor.rs:4634`), both citing 24 alone for the
warn-never-fail posture, correctly, with no 14 alongside. No other
production comment in the `umbrella/043` sweep pairs a 14 citation with 24's
claim.

Doc reserve: wrote no prose into `spec.md` or `open.md` (both parked, both
below reserve). Only new file is `changelog.d/umbrella-manifest-decision-14-and-24.fixed.md`.

## Contradiction

Decision `embarch-umbrella/decisions/install.md` #14's own clause "A version
mismatch against the suite manifest is a warning (decision 24)" versus
`src/manifest.rs`'s doc comment attributing that same claim to decision 14
instead.

**Hunk:** `src/manifest.rs`, lines 1-5 (module doc), diff hunk starting
`@@ -1,7 +1,7 @@` in merge SHA `ea9b72a` (`embarch-umbrella`).

**Why contradiction, not refinement:** decision 14's text is the standing
record of which decision governs the warn-on-mismatch behavior, and it names
24, not itself — the comment now asserts the opposite attribution in quotes,
as if quoting 14 directly.

**To undo:** revert is clean — this is a comment-only line in a
comment-only commit (`ea9b72a`, embarch-umbrella). `git show ea9b72a --
src/manifest.rs` isolates the one hunk; no code or test depends on the
comment text.
