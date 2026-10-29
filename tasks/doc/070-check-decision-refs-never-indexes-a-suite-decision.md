# 070 — `check-decision-refs.py` never indexes a `suite/decisions/*.md` entry, so every suite decision number is invisible to the checker

**State:** done — owner session, 2026-10-29, branch `owner/decision-refs`: fixed by `tasks/doc/060`'s change (the regex side, not a reheading); the literal citation above is restored and is a self-test fixture; see `## Closed`
**Source:** `inbox/doc-check-decision-refs-suite-headers-not-indexed.md`, found incidentally by
`ui/060`'s worker (citation sweep of `embarch-ui/src/main.rs` and `src/trace.rs`) while writing that
task file's own `## Result` section and hitting the red first-hand. Drained by leg 125 in the same
leg it was filed.
**Scope:** doc
**Hardware:** none — a `scripts/` bug and a `.md` heading-level convention question. No board,
no build, no live Core. Re-checked at drain.
**Owner:** required — both candidate fixes are owner-reserved: `scripts/check-decision-refs.py`
itself, or a reheading of the four `suite/decisions/*.md` files, whose convention
`DOC-PROTOCOL.md`/`DOC-CONVENTIONS.md` settle. **This drop deliberately takes no position on which
side is wrong, and neither do I.**

## What

`scripts/check-decision-refs.py`'s `build_index()` only recognizes a decision entry heading of
the form `^#{3,4}\s+(\d+...)\s+[-—]\s` — three or four `#`s. Every sub-project's own
`decisions/<topic>.md` file uses `### N — ...` (three), which matches. But all four files under
`suite/decisions/` — `tooling.md`, `naming.md`, `placement.md` (checked directly; `DOC-CONVENTIONS.md`
does not appear to carve out a different rule for `suite/`) — write their entries as `## N — ...`
(two `#`s):

    suite/decisions/tooling.md:9:## 1 — `rustfmt` is not enforced...
    suite/decisions/tooling.md:15:## 2 — `embarch-outpost` gets a host-only CI workflow...
    suite/decisions/naming.md:9:## 3 — `rx_utc_ms` keeps its name in both homes...
    suite/decisions/placement.md:9:## 4 — The outpost's own answer is computed once...

So `index['suite']` is always the empty set — **every one of the suite's four decisions is
invisible to the checker**, regardless of citation form.

**Consequence, reproduced:** most citations of a suite decision are bare prose ("suite decision
4") with no doc-path in the preceding 44-char attribution window, so they fall into the
*warning* bucket (`explicit is None` branch) rather than erroring — silently absorbed into the
script's existing "1005 ambiguous (--warnings to list)" count, indistinguishable from a real
unresolvable citation. But a citation that spells out the actual defining path —
`suite/decisions/placement.md` decision 4 — matches `DOC_PATH`, sets `explicit = 'suite'`, and
then **hard-fails** with `not defined by suite`, even though the decision plainly exists and the sentence citing it is
true. `ui/060`'s own task file hit this red and had to reword around it (drop the literal path,
cite the decision bare instead) rather than fix the indexer, since `scripts/` is owner-reserved
and outside every worker's ownership row.

**This file had to do the same thing, and that is the third instance of a pattern this queue has
now hit three times: documentation shaped exactly like the data it documents.** The sentence above
originally wrote the path-plus-number form out literally, to show the reader exactly what fails —
and the checker failed it, turning the gate red on `main` inside the fold that filed this task
(leg 125, 2026-09-16). It was reworded so the gate would pass. **Whoever fixes the indexer should
restore the literal form in this paragraph as the fix's own regression case**, because a task
describing a citation defect that cannot spell the defective citation is a poor bug report.
*(Restored 2026-10-29: the paragraph above carries the literal form again and the gate passes on
it; the same shape is a fixture in the script's self-test.)*

**Two failure modes from one root cause:** real suite-decision drift would currently pass silently
(never checked), and a *correct*, precisely-attributed citation of one is the one form the checker
actively rejects — backwards from what the tool is for.

## Why now

Nobody appears to have written a doc-path-form citation of a suite decision before `ui/060` did,
so this has presumably been sitting latent since `suite/decisions.md` was split into topic files
(`tasks/suite/033`, 2026-09-12) without anyone hitting the red. It will recur for any future
citation that names a `suite/decisions/*.md` path directly, and — more importantly — it means the
suite's four decisions currently get zero mechanical drift protection at all.

## Done when

- [x] `check-decision-refs.py`'s `build_index()` (or `DEF_HEAD`) recognizes `suite/decisions/*.md`'s
      `## N —` heading level, OR those four files are reheaded to `### N —` to match every other
      sub-project's convention — whichever the repo owner judges is the intended rule; this drop
      takes no position on which side is "wrong."
- [x] Re-running `check-decision-refs.py` after the fix shows `suite` decisions 1-4 as indexed
      (`--verbose`, if it has one, or a deliberately-introduced bad suite citation should now be
      caught).
- [x] The now-fixed indexing doesn't turn any currently-passing bare suite-decision citation red
      (there are several across `embarch-core`, `embarch-ui`, `embarch-outpost` — e.g.
      `embarch-core/decisions/stream-index.md`'s `[Suite decision 4](../../suite/decisions.md)`,
      `embarch-ui/decisions/trace-view.md`'s two "suite decision 4" mentions).

## Closed

**Same root cause as `tasks/doc/060`, closed by that change**: `DEF_HEAD` reads `##` to `####`, so
the suite tree stays as written; `DOC-CONVENTIONS.md` says which tree uses which level.
`--verbose` now prints `suite 4 entries (1..4)`.

**Both failure modes verified against the real index**, with a scratch doc dropped into
`embarch-ui/` and removed: the path-plus-number form passes; a suite citation of 7 fails
`not defined by suite`; and so does a suite citation of 5 written there, which `embarch-ui`'s own
decision 5 used to absorb. Run against the script as it stood before the fix, the restored line
above is red with exactly the message this task quotes, and the scratch doc's two bad citations
pass. **Nothing went red:** all 40 suite citations in the repo name 1–4, including
the three this file lists, and the whole check was green before and after.
