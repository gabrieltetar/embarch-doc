# 017 — `tr-cross` now carries two unrelated meanings and decision 10 states only one

**State:** done — leg 2026-09-07, branch `agent/ui/017-tr-cross-two-meanings` (both repos).

**Resolution: same category.** Decision 10's chart half (`trace-chart.md`) now states `tr-cross`'s
complete, exactly-two-cause scope in its own text: an aggregated run whose flags include a gap (the
capture-side cause this half already existed to describe), and, per decision 23, a step outcome
`app.js` could not parse (the client-side cause `ui/015` introduced). Argument for treating them as
one category rather than forking a second token: both already carry the same reader-facing promise —
*this is not vouched for as drawn* — and each already names its own specific reason in the hover
text, so a reader is never actually confused about which of the two is in play; the ambiguity the
prior two rounds kept tripping over was never in the rendering, only in decision 10's text not
saying so. A second token would buy nothing a hover title doesn't already buy, at a real cost this
sitting: `trace-chart.md` had 590 B of file-level reserve left and a new-token paragraph plus an
`app.js` change would not have fit without also running `tasks/ui/019` in this same commit. The fix
instead nets +135 B in the file — a new sentence in decision 10, offset by trimming decision 23's
now-redundant restatement of the same claim down to a pointer at decision 10 — leaving
`trace-chart.md` at 11,833/12,288 B (455 B left), still in reserve but not over cap.

**Decision 10 also has its own, separate, per-decision pinned baseline (`scripts/decision-size-baseline.json`,
8,192 B) that the file-level reserve number does not show.** The first draft of the new sentence was
under the file's 590 B but pushed decision 10's own section to 8,336 B — `check-doc-size.py` caught it
as a pinned decision growing past its baseline, which a merely-under-cap file total does not surface.
Cut to fit the 173 B of headroom that baseline actually had (8,192 − 8,019); the section is now
8,179 B. `tasks/ui/019` (already open, `In flux: no`) carries the updated byte counts and this
reserve-spend note rather than a second filing.
**Scope:** ui
**Hardware:** none — two decision files and one JS file; confirming it needs reading, not a board.
**Source:** `embarch-reviewer` on `ui/015` (code `7468a0e` in `embarch-ui`, doc `fb0a05c` in
`embarch-doc`), 2026-09-07, leg 035. Filed by the supervisor rather than fixed in the fold — see
*Why this was filed and not fixed*, and read it, because the same question was answered the other
way one leg ago.

## Read this first: you are the third unit in a row on one visual token

`ui/014` → `ui/015` → this. **Each was filed by the reviewer of the one before it, about the same
handful of lines in `assets/app.js`.** The history matters because it tells you what a fourth round
would look like and why you should not produce one:

1. **`ui/014`** fixed a real bug — a failed step could render as a neutral dash — and, in the fix,
   drew an unrecognised `Outcome`'s trace band with the **`tr-gap`** hatch. Its reviewer caught
   that `tr-gap` is decision 10's token for *an interval the firmware reported losing records in*,
   so the view asserted a hardware fault that never happened.
2. **`ui/015`** swapped that fill to **`tr-cross`** and amended decision 23 to record why. The swap
   itself is right and is **not** in question here. What its reviewer caught is the justification:
   the amendment paraphrases `tr-cross` as already meaning *"this view cannot vouch for this
   span"* — broad enough to cover a client-side parse failure — and decision 10 does not define it
   that broadly.
3. **This task.** Decision 10's chart half scopes `tr-cross` to exactly **three flags on a merged
   aggregation run**: gap-crossing, below-resolution, open-edge. All three are facts about the
   **capture data**. The pre-existing code use agrees — `app.js` ~line 4277,
   `var fill = crosses ? "url(#tr-cross)" : "var(--accent)"`, with `crosses` set from
   `TRACE_F_GAP`. `ui/015`'s new use at ~line 4432 fills the same pattern for **an `Outcome` this
   JS could not parse**, which is a fact about the client. Decision 10's own text was not touched
   and still describes only the original three.

**So the same hatch now promises two things that share nothing except "something is off", and the
only place the second meaning is written down is decision 23's amendment, in a paragraph decision
10 does not point at.** That is the ambiguity `ui/015` was filed to remove from `tr-gap`, moved
rather than removed.

## Why this was filed and not fixed

One leg ago (leg 034) the supervisor hand-fixed a reviewer finding inside a fold for `dev-bench/011`
and *filed* the one for `ui/014`, and its own log entry said it was unsure the line it drew —
"that one was a measurement I took, this one is a visual vocabulary" — was anything more than
convenient. **This unit resolves that doubt in the same direction, and there is now a concrete
reason rather than a taste:**

**The state left on `main` is not equivalent in the two cases.** After `ui/014`, `main` shipped a
view that *asserted a hardware fault that had not occurred* — a false statement about the DUT, in
the one view whose entire job is telling an engineer which parts of a capture to trust. After
`ui/015`, `main` ships a view that is **correct in what it draws** and **under-documented in why**:
`tr-cross` is the honest token for an unparseable value, and the gap is that decision 10 has not
said so. A reader who trusts the view is not misled today; a reader who trusts decision 10's
enumeration of `tr-cross` is missing a case.

**Answering it properly is a design call with a real fork**, which is what a worker with a full
gate is for and a fold is not (see the `umbrella/039` entry: the same shape of change, done by a
worker, came to 63 lines with two new tests where a fold would have produced a sentence). The fork:

- **Same category** — an aggregation run whose continuity is uncertain and a value this view could
  not read are both "this view cannot vouch for what it is drawing here." Then decision 10 gets the
  sentence that currently lives only in decision 23, and the enumeration becomes four causes, not
  three. Cheapest, and defensible.
- **Different category** — the three original causes are all about the *capture*, and a client
  parse failure is about the *client*, so conflating them is what got us here twice. Then the
  parse-failure case needs its own token or label, and `trace-chart.md`'s byte cap is a cost to
  pay rather than a reason to decide (`tasks/ui/019-compact-ui-trace-chart.md` is already open for that budget
  and may be where the room comes from).

**Pick one and argue it.** Do not add a third amendment that widens a token in a file the token's
defining decision does not reference — that is precisely what rounds 2 and 3 each did.

## Done when

- [x] **One place** states the complete list of what `tr-cross` covers, and whether a client-side
      "cannot parse this value" is the same category as "an aggregated run's continuity is
      uncertain (gap / below-resolution / open edge)". That place is decision 10 if the answer is
      "same category"; if the answer is "different", decision 10 still gains the sentence saying
      what `tr-cross` does *not* cover and where the other case lives. — Decision 10 (`trace-chart.md`
      §10) now states it directly: exactly two causes, gap-crossing and the decision-23 parse
      failure; below-resolution and open-edge alone never trigger the hatch (checked against
      `app.js` ~4274-4277, where `crosses` is set from `TRACE_F_GAP` alone).
- [x] If the two meanings are judged the same category, **decision 10's own text** carries the
      sentence — not decision 23 alone. A reader of decision 10 must not be missing the update. —
      Done; decision 23's amendment is trimmed to a pointer at decision 10 rather than restating it.
- [ ] If they are judged different, the parse-failure case has its own token or label, `app.js`
      uses it, and both decisions name it. — N/A, same category was judged.
- [x] The `tr-gap` → `tr-cross` swap itself is **not** reverted. Reverting `7468a0e` would restore
      the false hardware-fault claim `ui/015` was filed to remove; the remedy here is forward only.
      — `app.js` untouched entirely this task.
- [x] The step table's `badge-danger "?"` for an unrecognised outcome is untouched. It was right in
      `ui/014` and is right now. — `app.js` untouched entirely this task.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment only if a
      user-visible rendering actually changes — if the whole answer is "decision 10 gains a
      sentence", say so and write no fragment. — No rendering changed (doc-only fix); no
      `changelog.d/` fragment written. Gate results below.

## Doc-size

`embarch-ui/decisions/trace-chart.md` went into reserve in `ui/015` — **11,698 / 12,288 B, 95.2%,
590 B left** — and `tasks/ui/019-compact-ui-trace-chart.md` is the filed debt for it (`In flux:
no`). **That task was filed as `016` by `ui/015`'s worker and renumbered by the owner in `161d7b0`**,
because a second thread had issued `016` in the same hour; `018-compact-ui-spec.md` is the other
half of that collision and is not this file's debt.
`decisions/trace-view.md` is **10,989 / 12,288 B (89.4%)**, just under the line, and decision 10's
view half lives there. **Both candidate homes for this fix are tight**, which is why `019` may need
to run first or in the same sitting. If your work pushes another file into reserve, file
`tasks/ui/<NNN>-compact-ui.md` in the same commit.

## There is no automated coverage for any of this

No `node` on this machine, and `src/trace.rs`'s browser harness is `#[ignore]`d and drives Firefox
by hand — so nothing automated has ever exercised `app.js`, and **nobody has seen either the
`tr-gap` or the `tr-cross` rendering of an unknown outcome.** Three rounds of reasoning about a
visual token, none of it observed. Seeing it is `tasks/ui/007`'s territory and that task is gated on
the DUT-naming question. Do not claim a rendering was observed unless you observed it.
