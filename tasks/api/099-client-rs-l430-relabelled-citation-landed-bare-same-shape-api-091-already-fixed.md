# 099 — `client.rs` L430's decision-17 fix landed unlabelled, the same shape `api/091` already fixed once

**State:** open
**Source:** the `api/097` **reviewer**, leg 116, 2026-09-16, reviewing landed unit `api/097` (code
`8f7fc5c`, doc `aa65f1e`). I had independently flagged the same line at merge review and was drafting
a thinner version of this task; the reviewer's drop was the better document, so this **is** that drop,
promoted from `inbox/` with its text kept and an extra item added below.
**Scope:** api
**Hardware:** none — a citation-text finding, confirmed by reading, not by running anything. No
board, no probe, no live Core.
**Owner:** no

**Doc-size reserve for `api`:** `embarch-api/spec.md` 9,102/10,240 B, 1,138 B left, filed as
`tasks/api/083` and **blocked**. This task should not need to write it.

**Take `tasks/api/098` in the same unit.** It is also a one-line `api` citation fix filed this leg
(a stale `decisions/streams.md` mention left by `core/060`'s split). Two one-line fixes in one repo
should not cost two dispatches.

## What

`api/097` (commit `8f7fc5c`) relabelled `crates/embarch-core-client/src/client.rs` L430 from
`` (`link_port_serial` added decision 27) `` to `` (`link_port_serial` added decision 17) ``. The
number is now right — `embarch-topology` decision 17 (`links-port.md`: "the dev-bench link's own
USB serial is a second declared fact, distinct from its JTAG probe's") is where `link_port_serial`
actually originates, and neither `embarch-api`'s own decision 27 nor `embarch-topology`'s own
decision 27 is about it, exactly as the commit message says.

But the new citation is written **bare** — `decision 17`, no repo label — inside `embarch-api`'s
own file. `embarch-api` has its **own, real, unrelated decision 17** (`decisions/core-link.md`:
"Checking Core's contract version where the schema version is already checked"). Under
`DOC-CONVENTIONS.md`'s "Referring to a decision" section (decided 2026-09-04): a bare
`decision N` addresses the citing file's **own** sub-project; a cross-repo referent must carry the
`` `<repo>` `` label. The fixed comment now reads:

```
/// enrollment storage `embarch-topology` decision 14 moved into that crate
/// (`link_port_serial` added decision 17) — every currently
```

The sibling citation eight words earlier, in the same sentence, **is** correctly labelled
(`` `embarch-topology` decision 14 ``) — so the sentence now applies the convention inconsistently
to two citations that are both about the same foreign sub-project.

**This is not a hypothetical ambiguity.** `scripts/check-decision-refs.py`'s own attribution
window (`ATTRIB_WINDOW = 44` chars, `DOC-CONVENTIONS.md`'s canonical-label regex) looks back only
44 characters from a reference for an explicit `` `embarch-<repo>` `` label. The text between
"decision 14" and "decision 17" — `" moved into that crate (`link_port_serial` added "` — is
~48 characters, past the window. (Moot for the script itself, which only walks `*.md` files in
this repo and never reaches `embarch-api`'s Rust source — which is exactly why this class of
defect needs a manual sweep like `api/095`/`097` at all, and exactly why nothing else will ever
catch it.) A human reader applying the same "nearest label wins, else same-repo" rule the sweep
itself uses gets the same wrong answer: `embarch-api`'s own decision 17.

**This exact shape was already found and fixed once in this file**, `api/091` (`f2f1de2`,
2026-09-13): *"Two bare `decision N` citations were foreign referents left unlabelled immediately
after a differently-labelled sibling citation in the same sentence, each colliding with a real,
unrelated same-numbered decision in the other repo... Both labelled."* One of those two was the
very `embarch-topology` decision 14 citation eight words before L430 in this same sentence. The
`api/097` fix reintroduces the pattern `api/091` closed, in the neighbouring clause of the same
sentence.

`api/097`'s own task file (`tasks/api/097-...md`) lists "Cross-repo citations carry the labelled
`<repo> decision N` form; same-repo ones stay bare" as a checked-off `Done when` item. The landed
fix does not meet it.

## Why now

`tasks/doc/055` ("settle the cross-repo citation form for embarch-doc") is still open, and this is
a second, independent instance of the exact citation-form defect the whole `client.rs` sweep
(`api/091`, `095`, `097`) exists to eliminate — landed by the fix itself, invisible to every gate
that ran, and blocking on nothing but a one-label edit.

## Done when

- [ ] `crates/embarch-core-client/src/client.rs` L430 reads
      `` (`link_port_serial` added `embarch-topology` decision 17) `` (or equivalent phrasing that
      puts the `` `embarch-topology` `` label within the attribution window of "decision 17").
- [ ] A pass over the rest of the file (or at minimum, every bare cross-repo citation reintroduced
      or touched by `api/091`/`095`/`097`) confirms no sibling instance of "labelled citation
      immediately followed by an unlabelled one for the same foreign repo" slipped through.
- [ ] **L1774's "2026-08-25 amendment" framing is corrected** — see the note below, which the
      supervisor has promoted from a side remark into a required item. `api/097` left it
      **`unsettled`**, and the reviewer then settled it: `embarch-topology` decision 18 was
      **created** on that date (`e46164b`), so the cited text is its founding content and there is
      no amendment. Either drop the word "amendment" and cite the decision plainly, or say it was
      the decision's origin. **Leaving it as-is is not an option now that it has been settled** — an
      `unsettled` that somebody has since resolved and nobody has written down is worse than the
      original wrong label, because the next sweep will spend the effort again.
- [ ] `changelog.d/` fragment.

## Note from the reviewer — now item 3 of `Done when`, above

L1774 (`declare_signal`'s doc comment, `` `embarch-topology` decision 18's 2026-08-25 amendment ``)
was checked as requested. `embarch-topology`'s decision 18 was **created** 2026-08-25
(`e46164b`, "Add embarch-outpost... New decision 18: the DUT signal link..." — same day, and the
idempotent-declare/migration-path language `client.rs` cites is in that founding text, not added
later). No commit anywhere near that date **amends** decision 18; nothing in `links.md`'s own text
marks a 2026-08-25 amendment the way decision 5's amendment is explicitly marked in-text elsewhere
in this file. So the "amendment" framing looks like a conflation of decision 18's creation date
with an amendment date — settleable (drop "amendment", cite the decision plainly, or state it was
the decision's origin), not genuinely unresolvable. This is a citation-accuracy question the sweep
itself owns, not a decision contradiction, so I'm not filing it as a separate defect — but
`api/097`'s choice to leave it "unsettled" rather than fold it either way was the right call
procedurally; it just wasn't actually unsettleable, if reopened.

L667's relabel to `embarch-core` decision 16 is correct: its body (`decisions/logging.md`) says
verbatim "served as plain text, because reformatting a deployed service's output into JSON for one
client is a bigger change than this needs," and `embarch-ui` decision 7's full git history
(`debug-tab.md`, all four revisions) never discusses formatting at all — only retention, SSE vs.
poll, and logfile-vs-endpoint. No finding there.
