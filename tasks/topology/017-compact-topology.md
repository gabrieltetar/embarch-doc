# 017 — `spec.md` and `decisions/validation.md` are in reserve

**State:** claimed by agent/topology/017-compact-topology, 2026-09-08 23:07
**Source:** `scripts/check-doc-size.py`'s reserve floor, hit by `tasks/topology/009`'s edits, 2026-09-07
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/spec.md, embarch-topology/decisions/validation.md
**Size debt due:** 2026-10-08

## What

`tasks/topology/009` (the additive `validate` timestamp) pushed two files into
reserve at once: `spec.md` is **9,602/10,240 B (93.8%), 638 B left**;
`decisions/validation.md` is **11,178/12,288 B (91.0%), 1,110 B left**. Neither
had a debt filed before this edit — `tasks/topology/014` covers `open.md` only.

## Why now

The debt is real once a file is within one amendment of its cap, and recording
it is the whole mechanism (`tasks/topology/014`'s own wording, same rule).

## In flux: no

**Corrected by the supervisor at `009`'s fold, leg 041, 2026-09-07.** The filer
wrote `yes` on two grounds and both had already expired when it wrote them:

- It said `tasks/topology/013` is *open* against `decisions.md`'s index and this
  sub-project's validation group. **`013` is `done`** — it landed in leg 035
  earlier today, on branch `agent/topology/013-decision-23-acl-rationale`. The
  filer was reading a task file it had not opened.
- It said `009` "just added decision 26 to the same `validation.md`". `009` is
  the unit that filed this task, and it has now landed. Its own edit is not
  future flux.

Nothing else is queued against `embarch-topology/spec.md` or
`decisions/validation.md`. Whoever compacts should still read decisions 20, 21,
25 and 26 as a group — they are four passes over the same chip-identity and
validate surface within two days, which is where a compaction most easily drops
a fact — but that is care, not flux.

**Left `open` rather than `blocked`** on purpose: a `blocked` compaction task is
the state nothing revisits, and `check-doc-size.py --pressure` calls that out as
its own problem. This one is dispatchable.

## Done when

- [x] `spec.md` is out of reserve, or the task says why it cannot be and what
      was deleted instead.
- [x] `decisions/validation.md` is out of reserve, same terms — prefer a split
      per [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 if a seam exists
      (e.g. splitting the Nordic-identity decisions 21/25 from the
      timestamp decision 26 into their own file).
- [x] Whichever it was for each file — split or delete — is stated, with the
      byte numbers before and after.

## Outcome

**`decisions/validation.md` — split, no reasoning cut.** Decisions 21 and 25 (the
Nordic chip-identity arm and its classifier fix) stayed in `validation.md`,
byte-identical; decision 26 (the `validate` freshness timestamp — a different
mission, added-field API surface rather than chip identity) moved verbatim to
a new `decisions/validate-timing.md`. `decisions.md`'s routing table gained a
row; `decisions/validation.md`'s own header now points at the new file, and
`decisions/enrollment.md`'s existing `[validation.md](validation.md)` link
still resolves correctly since chip-identity assertion is still what that file
holds. Before: 11,178 B (91.0%, 1,110 B left). After: `validation.md`
8,771 B (71.4%), `validate-timing.md` 2,843 B (23.1%) — both well clear of
reserve, no debt to re-file.

**`spec.md` — squeezed, since `spec.md` does not split by mission (`DOC-COMPACTION.md`
§3).** Cut only cold content per the hot/cold test: the "Where it stands"
mismatch-path paragraph lost its probe serial number, exact `GET /alerts`
citation, date and the count/proportion caveat, keeping the one fact another
file depends on (`decision 12` cites "three" refusals as recorded here) and
the invariant that the path is exercised on real hardware, not just designed.
The `validate` timestamp paragraph dropped its "why added not renamed"
rationale (already decision 26's job, not spec's) down to the current API
shape plus a pointer. Three smaller cold asides went too (an unset-tag date
citation with no constants-table role, an unobserved-so-far note, a "this
crate's own CLi is one caller" aside, and one incident-citation compressed to
a bare decision pointer). No invariant, constraint, rejected alternative, or
failure signature was touched. Before: 9,961 B (97.3%, 279 B left). After:
8,995 B (87.8%, 1,245 B left).

Gate: `cargo build`/`test`/`clippy --all-targets --all-features -- -D warnings`
green in the code repo (no code changes — this is a pure doc pass);
`check-docs.py` all 10 checks green; `check-ownership.py --scope topology`
(doc repo) and `--code-repo` (code repo) both green, 3 doc paths changed, 0
code paths changed. `check-duplication.py embarch-topology` shows only the
pre-existing spec-restates-invariant overlaps DOC-PROTOCOL.md's four-file
split expects (advisory, not acted on). Changelog fragment:
`changelog.d/topology-compact-017.changed.md`.

**Human question, answered honestly:** yes. `spec.md` alone states topology's
purpose, what it explicitly is not, the crate/CLI shape and who calls it, the
four facts detection cannot produce, storage and role-uniqueness rules with
their failure signatures, what `validate` does and does not assert (including
the current two-timestamp surface), what each consumer owns, and where real
hardware currently stands — with `decisions.md`/`open.md` one hop away for
why or what's unresolved. Nothing cut in this pass removed anything a reader
changing this code would need without opening a decision file too.
