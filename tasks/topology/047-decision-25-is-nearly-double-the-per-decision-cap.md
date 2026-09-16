# 047 — `embarch-topology` decision 25 is 7,818 B — nearly double the per-decision cap, and nothing tracks it

**State:** done — decision 25 compacted from 7,818 B to 4,001 B (95 B margin under the 4,096 B cap);
compacted rather than split (see `## Split vs. compaction` below); no citation broken; gate green.
**Reserve (leg 118):** no `embarch-topology` file is in the last 10% of its cap —
`decisions/validation-classifier.md` is at 68.4% of its *file* cap, which is exactly why this is a
per-decision problem and not a file-size one. If your work pushes a file into reserve, file
`tasks/topology/<NNN>-compact-topology.md` in the same commit.
**Source:** leg 117, 2026-09-16. `core/063` closed the same gap for `embarch-core` decision 30 and
its own framing was *"nothing is watching it, and that is the actual finding."* I ran the full
census that task implied and it turned out to be true four more times: **five** decisions across the
suite are over [`DOC-BUDGET.md`](../../DOC-BUDGET.md)'s **4,096 B per-decision cap** with no pin in
`scripts/decision-size-baseline.json`, so nothing reports them and no ledger has a clock for them.
`core/063` fixed one and `core/064` files another. **This is the largest of the remaining four, and
the largest in the suite.**
**Scope:** topology
**Hardware:** none — doc prose only. No board, no probe, no live Core, no deploy.
**Owner:** no
**Compacts:** `embarch-topology/decisions/validation-classifier.md`
**In flux:** no — decision 25 is a *closed* classifier defect: two functions that had to agree on
which chips carry the `FICR.INFO.DEVICEID` pair, and did not. The fix landed. What is still open in
[`open.md`](../../embarch-topology/open.md) is a **hardware** gap, not doc flux — `nRF54L10`,
`nRF54L05` and `nRF54LM20A` take the same arm with no silicon ever attached — and no board is
coming to change this entry's text.

## What

`embarch-topology/decisions/validation-classifier.md#25` is **7,818 B** against a 4,096 B cap:
**3,722 B over, 191% of the limit**, and the single largest decision entry in the suite. Every other
over-cap decision is within ~3 KB of the line; this one is nearly a second decision's worth of prose
on its own.

The task is the same fork `core/063` faced, and it is much more likely to fall the other way here:

- **One decision that has accreted several arguments** → split it into two numbered decisions and
  update `embarch-topology/decisions.md`'s index — number list **and** size column, same commit.
- **One decision stated at length** → compact the entry under 4,096 B without losing the "why not",
  [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md) in full, including quoting every cut hunk
  verbatim rather than naming categories.

**Read it before choosing.** At 191% of cap the split branch is genuinely on the table in a way it
was not for decision 30 (152 B over, compacted). But **a new decision number is the most expensive
thing in this suite to reverse**, so the burden of proof is on splitting: you have to be able to
name two claims that a citation could want to point at *separately*. If every inbound citation lands
on the same claim, it is one decision stated at length and you compact it.

## Split vs. compaction

**Compacted, did not split.** Read the whole entry first, per the instruction above, before making
any edit. It is eleven paragraphs, added over three dates (2026-09-09 landing, amended 2026-09-10,
amended 2026-09-11), covering four chip families (nRF54L, nRF54H, ESP32-C5, STM32G0) — on the surface
exactly the "several accreted arguments" shape the task calls out as split-worthy. It is not, for one
reason that outweighs the surface shape: **every paragraph answers the same single question** —
`classify_chip`'s design rule that a chip name resolves to a register pair (or eFuse) only on positive
evidence, never a guess, with the narrowest verified prefix winning. The Nordic bug is that rule being
violated by accident; the nRF54H refusal, the `esp32c5` case-sensitivity carve-out, and the STM32G0
family-not-vendor narrowing are all *instances* of that same rule being applied on purpose to a new
name. None of them is a second, independent claim — each is the same claim's evidence trail. The
group's own one-line description in `decisions.md` already reads this way: "Which register pair a
chip name resolves to, and the classifier both the gate and the flash path share" covers the STM32
material exactly as well as the Nordic material; nothing needed rewording after the compaction.

**The citation grep confirms it rather than just failing to contradict it.** Every inbound `decision
25` citation to this file (`embarch-core/decisions/flash-backend.md` x2, `history/topology.md` x3,
`embarch-topology/decisions/validation.md`) lands on the shared-classifier / refuse-don't-guess claim.
**None cites the STM32 material at all** — not `embarch-topology/spec.md`, not any other repo. Under
the task's own test ("if every inbound citation lands on the same claim, it is one decision stated at
length and you compact it"), that is exactly the signal for compaction: there is no second claim
anyone has ever needed to point at separately, so there is nothing a split would buy that citation
stability doesn't already have, and a split would cost a new decision number — "the most expensive
thing in this suite to reverse" — for zero citation benefit.

## Why now

**Because the per-decision cap has no ledger and no clock.** The file-level ledger has both — a leg
spends its first unit on the oldest overdue entry. A decision that was never pinned is invisible to
everything: `check-doc-size.py --decisions` prints only its top 20 by size, which is how
`embarch-core` decision 30 sat over cap unnoticed until a reviewer opened the baseline file while
checking something unrelated. Whether that gap should be closed mechanically is the owner's call
under `scripts/` ([`tasks/doc/052`](../doc/052-a-verbatim-split-silently-drops-the-decision-size-pin-of-every-decision-it-moves.md)
records the adjacent defect). **This task is only about the one decision.**

## Watch for

- **Do not add a pin to `scripts/decision-size-baseline.json` to make the number go away.**
  `scripts/` is owner-reserved, and pinning an over-cap decision is the papering-over move, not the
  fix. `core/063` was told the same thing and did not.
- **Grep the whole doc repo for inbound `decision 25` citations before renumbering anything**, and
  remember a bare `decision 25` in another repo's file means *that* repo's 25, not this one. If you
  split, every existing citation still has to resolve to whichever half carries the claim it was
  citing, and `check-decision-refs.py` must stay green.
- **This entry's subject matter is a silent-failure story** — `"nRF54"` starts with `"nRF5"`, so
  unlisted nRF54L spellings matched the classic arm's guard first and never reached the newer pair,
  in both functions at once. That kind of reasoning is exactly what a compaction must **keep**: it
  is the "why not" that stops someone re-introducing the fall-through. Cut narrative and
  measurements, not the mechanism.
- **Report the before and after byte counts and the margin left**, the way `core/063` did.

## Compaction taken

7,818 B → 4,001 B, 3,817 B cut, **95 B of margin left under the 4,096 B cap.** File total
(`embarch-topology/decisions/validation-classifier.md`, header + decision 25, the file's only
content): 8,402 B → 4,585 B — no file-cap issue either way (12 KB `decision-group` cap), so no
`tasks/topology/<NNN>-compact-topology.md` debt is owed.

**What survived, load-bearing, unchanged or near-unchanged:** the failure signature (`"nRF54"` starts
with `"nRF5"`, so an unlisted nRF54L/nRF54H spelling used to fall through to the classic arm) — kept
in full in paragraph 1; the nRF54H refusal and its evidence limit (decision 21 is nRF54L-only, nothing
says anything about Haltium) — kept; the `esp32c5` case-sensitive-on-purpose inconsistency — kept
near-verbatim, it is the one paragraph DOC-COMPACTION-PASS's hot/cold test calls a pure "watch for" and
it was already short; the STM32G0 family-not-vendor narrowing and its `UID_BASE`-moves-per-family
rationale — kept; the `read_words` widening and its enrollment-compatibility invariant — kept. **The
"What this does not change" paragraph — the pointer to decision 21's confirmed-on-one-board,
nRF54L10/L05/LM20A-untested hardware gap — was left completely unedited**, byte for byte, since the
task named it as the one thing that must survive.

**What was cut**, per `DOC-COMPACTION-PASS.md`'s hot/cold test — provenance, incident narrative, and
duplicated restatement, quoted in full rather than by category. Grouped by which original paragraph
each hunk came from (paragraph order as it stood in the file before this edit):

**Paragraph 1 (the bug).**
- `— that is the whole basis for deriving the self-report relation rather than guessing it` (a
  connective clause back to decision 21; the relation itself is still named)
- `, `nRF54LM10`, a lowercase `nrf54l15_cpuapp`` (two of three illustrative examples; one, `nRF54L47`,
  was kept — the fact "case and suffix vary" no longer has three illustrations, only one)

**Paragraph 2 (the fix).**
- `(so case and suffix don't matter) ` (states *why* lowercasing also fixes the suffixed/lowercase
  spellings, not just the case-varied ones — a real fact, cut for space)
- ` because there is only one decision left to make` (the stated reason the two functions cannot
  disagree; the claim that they cannot disagree is kept, the reason is not)

**Paragraph 3 (why lowercase).**
- `chip.to_ascii_lowercase().starts_with("nrf54l")` (the literal `flash_backend.rs` expression;
  replaced with a paraphrase, "a lowercased `starts_with("nrf54l")`")
- `the flash path already accepts `nrf54l15_cpuapp` and unlisted parts like ` (a second worked example,
  redundant with the one kept)
- `(`requires_vendor_tool`, and its own `an_unknown_nrf54l_part_is_still_refused` test)` (names the
  specific test backing the flash-path claim — evidence citation, cut)
- `Hardware-id readback classifying a narrower set than the flash path already accepts was the actual
  defect; matching flash_backend's rule closes the gap on this side without proposing this crate
  depend on that one.` (restates paragraph 1's failure story from a different angle; the failure story
  itself is not lost, this second telling of it is)
- `**The two matchers are not unified across repos** — that would touch `embarch-core`, which this
  task does not own — so an `inbox/` drop records the option for whoever owns that boundary.` (this
  sentence described the *open* state, before `embarch-core` decision 49 closed it by declining — it
  is superseded by, not merely redundant with, the amendment content kept below)

**Paragraph 4 (nRF54H refusal) — the largest single cut, all incident narrative:**
- `and that arm was corrected by the supervisor before this decision landed` (from the heading
  sentence)
- `The worker's first version routed any `nrf54h` spelling to the `INFO.DEVICEID` pair alongside
  nRF54L, and this entry described it as if that were part of the same fix. It is not:` (the full
  incident: what the first draft got wrong)
- `which is exactly how the original defect worked` (a connective clause; the load-bearing "checked
  first" claim is kept, this restatement of *why* is not)
- `**The old code's behaviour was also a guess** — nRF54H fell through to the classic pair — so this
  is not a regression being avoided but a guess being retired, and it was available to retire because
  this task's own text authorised either the `INFO.DEVICEID` arm *or* the named error.` (a
  self-referential note about the worker/supervisor edit itself, not about the classifier's design)

This is the paragraph `embarch-core/decisions/flash-backend.md:24` loosely cites ("exactly the kind
of unevidenced guess topology decision 25's reviewer caught and reverted"). That citation names the
*pattern* (an nRF54H guess gets caught and refused), not this specific wording, and the pattern is
still true and still stated here — "nRF54H is checked first and returns `None`... nothing establishes
the Haltium family's FICR layout... An unrecognized chip is a named error, never a guess." Checked
against the citing sentence directly: it still resolves.

**Paragraph 6 (Amended 2026-09-10, first count) — entirely provenance about the entry's own edit
history, cut in full except the one fact folded into the merged paragraph below:**
- `**Amended 2026-09-10 (`tasks/suite/024`), on two counts.** First, this entry used to say that
  `embarch-core`'s `flash_backend.rs` "stops at `nrf54l` too", offered as corroboration for refusing
  nRF54H here. **That is no longer true and the sentence is removed rather than softened:**` (narrates
  a previous edit to this same entry — pure edit-history provenance)
- `` `embarch-core` decision 49 extended `requires_vendor_tool` to match `nrf54h` as well, because an
  nRF54H name was silently falling through to `false` and reaching probe-rs with no message at all. ``
  (the story of *why* core decision 49 changed — that decision is the right place for its own story;
  this file only needs the fact that it now also refuses nRF54H, which is kept)
- `Both repos still refuse nRF54H — but they refuse it *in opposite directions*, and that is the point
  the deleted sentence obscured.` (restates the abstention-vs-positive-refusal point a second time;
  that point is kept once, in the merged paragraph)

**Paragraph 7 (Amended 2026-09-10, second count) — merged into one paragraph with the requires_vendor_tool
material, most of the meta-commentary cut:**
- `Second, and following from it:` (transition, no content)
- `The option was left open above and filed to `inbox/`, becoming `tasks/suite/024`; `embarch-core`
  decision 49 settled it on its own side by declining.` (the *history* of how it was settled — the
  *fact* that it is settled, and by which decision, is kept)
- `` `classify_chip` is a three-way judgment over which register pair (or eFuse) holds a factory
  device ID, with `None` for "unrecognised"; `requires_vendor_tool` is a boolean over whether probe-rs's
  flat-NVM erase/write model is safe. `` (a fuller restatement of the codomain difference; the shorter
  form — "a different codomain (bool vs. three-way)" — is kept)
- `There is no shared return type that serves both without one caller re-deriving its own answer from
  the other's, which is two matchers again with an indirection in front.` (the specific technical
  reason a shared type doesn't work — real rationale, genuinely cut for space rather than redundancy;
  flagged here rather than silently dropped)
- `**They agree on the nRF54L prefix by shared evidence, not by shared code, and that is the intended
  arrangement** — so a future reader finding the duplication should read this paragraph rather than
  file it as a fresh finding for a third time.` (the anti-rediscovery instruction to a future reader —
  genuinely cut for space; flagged rather than silently dropped, same as the return-type sentence
  above)

**Paragraph 8 (esp32c5 inconsistency) — minimal cut, wording only:**
- `, so nobody has to rediscover it` (from the heading sentence)
- `That is ` / `it is now ` (filler removed around "the safe direction" / "the one arm")
- `the rule the paragraph above spends its length justifying` → reworded to `the narrowest-verified-
  match rule above` (same referent, shorter; no fact lost)

**Paragraph 9 (STM32 arm) — narrative and one evidence detail cut:**
- `Amended 2026-09-11: an ST arm, and the first prefix that stops at a *family* rather than a vendor.`
  (heading framing; the "family not vendor" point is kept in full in the next paragraph, which is why
  this restatement of it here was redundant)
- `Enrolling a NUCLEO-G0B1RE hit `read`'s named error, so the gate refused every flash to it — the
  first time this classifier's *coverage*, not its correctness, was in the way.` (the discovery story;
  the fact "a real NUCLEO-G0B1RE hit the named error until this arm was added" is kept, compressed
  into the same sentence as the fix)
- `Evidence, unusually, both documented and observed: ` (framing)
- `reads three `LL_GetUID_Word*` from that base` → reworded to `agree` (drops the specific detail that
  Zephyr's driver does three named reads; the fact that Zephyr's driver corroborates the address is
  kept)

**Paragraph 10 (stm32g0 not stm32) — one sentence of analogy cut:**
- `Same shape as the nRF54H refusal above, inverted: there a family was carved *out* of a prefix that
  would have swallowed it; here a prefix is not widened to the vendor it could cover.` (a symmetry
  observation connecting this paragraph to the nRF54H one; not a distinct fact, the narrowing rule
  itself is kept in full both before and after this cut)

**Paragraph 11 (read_words widening) — two small cuts:**
- `— one definition of what an ID string is` (states the design rationale for widening rather than
  adding a parallel three-word function; genuinely a rationale, cut for space)
- `at their next gate check. Tested.` → `next gate check` dropped the qualifier, and the standalone
  `Tested.` verification note was cut

**Heading.** Reworded from `an unlisted nRF54L name no longer falls through to the classic address` to
`unlisted nRF54L/nRF54H and STM32 names are refused, not guessed`, to cover the STM32 material the old
heading predated. No fact lost — the STM32G0 addition postdates the old heading and was never named in
it.

**Citation check, done before cutting anything (not after):** grepped the whole doc repo for `decision
25` and hand-checked every hit that could plausibly mean this file's decision 25 (a bare `decision 25`
in `embarch-ui/*`, `suite/user-guide.md`, `embarch-core/*`, `tasks/topology/011`, and
`tasks/doc/044:39` all belong to a *different* repo's decision 25, per the task's own warning, and are
unrelated). The real inbound set:

- `embarch-core/decisions/flash-backend.md:22` — cites `classify_chip` vs. `requires_vendor_tool` as
  two matchers answering different questions. Still true, still stated (merged paragraph).
- `embarch-core/decisions/flash-backend.md:24` — the "unevidenced guess... reviewer caught and
  reverted" line, addressed above under paragraph 4's cuts. Still resolves.
- `history/topology.md:20` — records the file split that created `validation-classifier.md`. A
  historical fact about a past event, unaffected by today's compaction.
- `history/topology.md:22` — "Topology decision 25... no longer claim `embarch-core` stops at nRF54L;
  core decision 49 matches `nrf54h` too. The two matchers stay separate on purpose." Still true — the
  merged paragraph keeps "stays unrelated to this classifier, on purpose... declined independently by
  `embarch-core` decision 49."
- `history/topology.md:42` — "one `classify_chip` fn picks the register pair; unlisted nRF54L names no
  longer fall through to the classic address." Kept verbatim in substance (paragraphs 1–2).
- `embarch-topology/decisions/validation.md:23` — "coverage... moved to `validation-classifier.md`
  decision 25, once a second consumer (the flash path's vendor-tool refusal) needed the same answer."
  Still true — the classifier/flash-path relationship is still the subject of the merged paragraph.

No renumbering happened (compaction, not split), so `check-decision-refs.py`'s number-resolution check
was never at risk — every citation above already resolved mechanically before this edit and still
does. The check above is the stronger one this task asked for: that the *passage* each citation is
actually pointing at still holds, not just that the number still exists.

## Done when

- [x] `embarch-topology` decision 25 is at or under 4,096 B, or split into two decisions each under
      it, with the branch taken justified in the task body. (4,001 B; compacted, not split — see
      `## Split vs. compaction`.)
- [x] `embarch-topology/decisions.md`'s index table matches — numbers and size column. (No
      renumbering; the table has no size column and its one-line description of the
      `validation-classifier.md` group already covered the STM32 material without editing.)
- [x] Every inbound `decision 25` citation still resolves to the claim it was citing. (Checked in
      `## Compaction taken`, before cutting.)
- [x] If compacted: every cut hunk quoted verbatim in the task file, per `DOC-COMPACTION-PASS.md`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
