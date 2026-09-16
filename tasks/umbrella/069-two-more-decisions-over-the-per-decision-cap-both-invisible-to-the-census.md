# 069 — two more `embarch-umbrella` decisions are over the per-decision cap, both invisible to the census that missed them

**State:** done — agent/umbrella/069-two-decisions-over-cap, 2026-09-16
**Source:** `agent/umbrella/068-two-decisions-over-cap` found `mirrors.md#16` while closing
`tasks/umbrella/068` and filed it to `inbox/` rather than reaching past its own task — the right
call. Leg 118 drained that drop, re-ran the census through `decision_state()` directly instead of
through the printer, and found `sticky-host.md#48` as well. **Why both were missed is
`tasks/doc/064`:** `check-doc-size.py --decisions` prints the twenty largest decisions in the suite
and marks which are over cap, so an unpinned breach below that line is printed nowhere. Neither of
these is a regression — `mirrors.md#16` was already 4,330 B at `91e75f5^` on 2026-09-13, before
`umbrella/064` touched it.
**Scope:** umbrella
**Hardware:** none — doc prose only. No board, no probe, no live Core, no `doctor` run.
**Owner:** no
**Compacts:** `embarch-umbrella/decisions/mirrors.md`, `embarch-umbrella/decisions/sticky-host.md`
**In flux:** no, both, and each was checked separately rather than answered once for the line.
Decision 16 is the `doctor`-mirrors-`embarch-api` rule; `mirrors.md`'s last two commits are
`umbrella/064` (a citation repoint) and a `suite/038` fold, neither rewriting the argument.
Decision 48 said what a sticky `saved.host` means and **left the clearing open** — that opening was
closed by **decision 51** (`umbrella/056`, then `umbrella/058` correcting the claims about it), and
`embarch-umbrella/open.md` line 15 now records the clearing as settled with a hardware debt against
it. A hardware debt is not doc flux: no board is coming to rewrite decision 48's text.

## What

Two entries, both over the 4,096 B per-decision cap, neither pinned in
`scripts/decision-size-baseline.json`:

```
4,347 B  embarch-umbrella/decisions/mirrors.md#16      (+251 B, 106% of cap)
4,193 B  embarch-umbrella/decisions/sticky-host.md#48  (+ 97 B, 102% of cap)
```

Both are small breaches. For each, the same fork the four units of leg 118 faced:

- **One decision stated at length** → compact under 4,096 B without losing the "why not",
  [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md) in full.
- **One decision that has accreted several arguments** → split into two numbered decisions and update
  `embarch-umbrella/decisions.md`'s index, same commit. **A new decision number is the most
  expensive thing in this suite to reverse**, so the burden of proof is on this branch, and at 102%
  and 106% of cap it is a hard case to make for either.

Decision 16's heading is a warning sign worth reading before choosing: *"`doctor`'s token check
needed the same treatment, **and so did its config reading**"* — a heading with an "and so did" in
it is the shape that sometimes really is two decisions. Read it and say which you found.

## Watch for

- **Do not add pins to `scripts/decision-size-baseline.json`.** `scripts/` is owner-reserved, and
  pinning an over-cap decision is the papering-over move rather than the fix.
- **Quote every cut hunk verbatim and completely** in this task file. Leg 117 landed a compaction
  whose quote list had an unmarked gap; leg 118 made the rule explicit in every dispatch and a
  reviewer still found three single words cut without being itemized. Err toward over-inclusion.
- **The `core/064` failure mode, which cost this class a real claim.** That unit compacted a
  *retired* decision and cut a sentence about `read_recent`/`tail_lines` — functions backing a
  **live** route — as if the whole entry were retired-route provenance. The fact then existed nowhere
  (`tasks/core/065`). Before cutting anything, ask of it: *is this provenance about something already
  settled, or a statement about behaviour that is still true and documented nowhere else?*
- **Two live claims that must survive in readable form.** Decision 16's reason for the mirror — that
  a `doctor` resolving the token differently from the `embarch-api` it diagnoses is **worse than no
  check** — is the entry's reason for existing. Decision 48's meaning-of-the-field claim is what
  decision 51 builds on; `open.md` line 15's **hardware debt** ("confirm on a real machine") must not
  end up reading as confirmed.
- **Grep the whole doc repo for inbound `decision 16` and `decision 48` citations first**, and
  remember a bare `decision 16` in another sub-project's file means *that* sub-project's 16. That
  collision is what `api/099` spent a whole unit fixing.
- **If only one fits in a sane unit, do that one properly and file the remainder** as
  `tasks/umbrella/<NNN>-...` in the same commit.
- **Report before/after byte counts and the margin left** for each entry you touch. Three of leg
  118's four compactions finished inside 150 B of the cap; if yours does too, say so plainly, because
  nothing mechanical distinguishes "paid" from "paid, barely".

## Dispatch note (leg 120, 2026-09-16)

**Doc-size reserve for `umbrella`:** one file, and it is not one of yours —
`embarch-umbrella/decisions/bind.md` at 11,533/12,288 B, **755 B left**, PARKED under
`tasks/umbrella/009` which is `blocked`. Both files this task compacts are *out* of reserve
(`mirrors.md` 86.7%, `sticky-host.md` 60.1%) and `check-doc-size.py` lists both as **PAID — close
its item** once you are under. If your work pushes any `embarch-umbrella` doc into the last 10% of
its cap and nothing has filed it, file `tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit.

**Do not touch `decisions/locate-api.md`#42.** A separate live task, `tasks/umbrella/071`, owns it —
decision 42 cites decision 35 for a `list-targets` shape decision 35 does not record, and it has 77 B
of margin. Leave it alone entirely so the two units do not collide.

**The justification test, stated as this leg is stating it to every worker.** Five units in two legs
have now cut a hunk on a justification that was true of the hunk's *topic* and false of one clause
inside it. When you justify a cut with "this is already recorded in X", open X and read it **against
the hunk sentence by sentence**, not against the hunk's subject. If X is a paraphrase, the cut is not
covered. Quote the evidence, not the conclusion.

## Done when

- [x] `embarch-umbrella` decision 16 is at or under 4,096 B, or split, with the branch justified.
- [x] `embarch-umbrella` decision 48 likewise, **or** left untouched with a follow-up task filed.
- [x] `embarch-umbrella/decisions.md`'s index matches, if anything was split. (N/A — neither was
  split; both compacted in place, so the index is untouched.)
- [x] Every inbound citation to a touched decision still resolves to the claim it was citing.
- [x] Every cut hunk quoted verbatim in this task file.
- [x] No pin added to `scripts/decision-size-baseline.json`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Closed 2026-09-16

**Both compacted, not split.** Neither entry's "and so did" heading (decision 16) or two-numbered
shape (decision 48/51, already two decisions) turned out to be an argument for a *new* split — see
below.

### Decision 16 — `embarch-umbrella/decisions/mirrors.md#16`

**4,347 B -> 3,803 B, 293 B margin under the 4,096 B cap.**

**Why compact, not split.** The heading's "and so did its config reading" reads as a two-decision
shape, but both halves (token mirror, config mirror) share the one argument the entry exists for —
*"a `doctor` resolving [something] differently than the `embarch-api` it is diagnosing... is worse
than no check"* — applied to two fields of the same mirror, not two arguments. Splitting would
duplicate that sentence rather than separate two reasons. Compacted instead.

**What was cut, both hunks verbatim and complete:**

Hunk 1 (from the "Two implementation details" paragraph — the UNC-comparison mechanics, which the
entry's own 2026-09-13 amendment already marks as retired: *"the UNC half below is retired, and the
scaffolding that fed it with it"* / *"The paragraph below is kept as the record of how the
comparison worked, not as a description of code that exists."* Verified against `src/doctor.rs`:
`artifact_path_for_core`/the UNC-translation code is gone; only `declared_base_url` /
`probe_topology`'s address-probing behaviour, kept below, is still live):

> Comparing a WSL2 path against its Windows-visible form means **reverse-translating the UNC form
> back to a `/`-rooted path and comparing canonicalized paths** — not literally stat-ing the UNC
> string, **which is not a path WSL2's own filesystem namespace resolves.** It verifies anything
> only when the UNC's embedded distro name matches this one's; otherwise it reports "cannot verify
> from here" **rather than guessing.**

The heading of that paragraph was reworded from "**Two implementation details worth recording
because they were not obvious going in.**" to "**One implementation detail worth recording because
it was not obvious going in.**" (one detail remains: the still-live "config declares an explicit
address -> `doctor` probes exactly that address" claim, kept verbatim — it is the only place in the
doc repo this fact is recorded, confirmed by `grep -rn` across `embarch-umbrella/` and matched
against `src/doctor.rs`'s live `declared_base_url`/`probe_topology`.)

Hunk 2 (the 2026-09-13 amendment's own forward-reference to hunk 1's paragraph, left dangling once
hunk 1 was gone — cutting it removes a pointer to text that no longer exists, not a fact; it made no
claim beyond "the paragraph below is provenance, not live code," which is already true of what
remains of that paragraph):

> The paragraph below is kept as the record of how the comparison worked, not as a description of
> code that exists.

**Citations checked.** `embarch-api/decisions/config-retirement.md#42`'s citation of
`embarch-umbrella decision 16` (about `init.rs` emitting `artifact_path_for_core` for a static/WSL2
project) cites a different clause, untouched. `embarch-umbrella/interfaces/doctor-chain.md` rows 6
and 9 cite decision 16 for check 6's shell-out and check 9's re-scoping, both untouched. No citation
anywhere quoted or depended on the cut UNC-mechanics text.

### Decision 48 — `embarch-umbrella/decisions/sticky-host.md#48`

**4,193 B -> 3,910 B, 186 B margin under the 4,096 B cap.**

**Why compact, not split.** Nothing in decision 48 is two arguments — it is one claim ("what a
found `saved.host` is evidence of") plus its "may/may not infer" consequences for check 2. Decision
51 is already the separate decision this file's own accreted-argument shape produced (the clearing
rule), landed earlier as its own number. No further split is justified.

**What was cut, hunk verbatim and complete** (provenance about which commits rewrote a *code
comment* in `src/state.rs` — not a statement about current behaviour; the substantive claim it
followed, "at some past run, some `--host` was typed... [not] whether that run's conclusion still
held", is kept verbatim and unabridged):

> **That quote is gone now, not dead**: this decision's own fix (`umbrella/050`) rewrote the comment
> to state this point directly, and decision 51 rewrote it again to add the clearing rule — read
> `src/state.rs`'s current comment on `host`, not this sentence, for what it says today.

**Justification test applied.** The candidate justification was "this is already recorded in
`decision 51`" — checked against decision 51's actual text sentence by sentence: decision 51 records
the *clearing rule* (what `apply_plan` writes), not that a code comment was rewritten twice. That
narrower claim about comment provenance is genuinely not restated anywhere, which is why it is cut
as provenance (cold: "how a doc comment evolved") rather than justified-elsewhere — it carries no
live behavioural fact `src/state.rs`'s current comment and this decision's own retained sentences
do not already carry.

**Two live claims verified intact, not touched by either cut:** decision 16's mirror-rationale
sentence (*"worse than no check"*) is unabridged in the kept text above. Decision 48's
meaning-of-the-field claim (what a found `saved.host` attests to, and the full "may/may not infer"
lists) is untouched; `open.md` line 15's hardware debt ("confirm on a real machine") is unedited and
still reads as unconfirmed.

**Citations checked.** Every other `decision 48` hit in the doc repo belongs to
`embarch-study-designer`'s own decision 48 (post-hoc validation removal) — a different sub-project's
numbering, per this task's own warning. The one real `embarch-umbrella` citation,
`embarch-umbrella/open.md:15` ("settling what decision 48 left open"), cites the still-open clearing
question (lines 66-69, "Deliberately does not change when `saved.host` is cleared"), which is
untouched by this compaction.

**`decisions/locate-api.md`#42 not touched**, per the dispatch note — left entirely alone for
`tasks/umbrella/071`.

**Gate:** `cargo build`/`test`/`clippy` N/A (no code repo changes — this is a pure doc-repo task;
`embarch-umbrella`'s code worktree has no `decisions/` directory, decisions live only in
`embarch-doc`). `scripts/check-docs.py`: all 11 checks green. `check-client-names.py --repo
<umbrella code worktree>`: clean. `check-ownership.py --scope umbrella` (doc worktree) and
`--code-repo` (umbrella worktree): both OK, 0 unowned paths.
