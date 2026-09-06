# 016 — Decisions 20/21 left two loose ends: advice that cannot be followed, and an asymmetric load-time refusal

**State:** claimed by agent/api/016-decisions-20-21-loose-ends, 2026-09-05 23:05
**Source:** `embarch-api/open.md`, the bullet beginning "Two loose ends left by decisions 20/21
shipping (found by review, 2026-09-04, neither a contradiction)". Swept by leg 013 when the
queue ran dry; still stated in that file today, so it reconciles.
**Scope:** api
**Hardware:** none

**Reserve for `api` at dispatch** (`scripts/check-doc-size.py --pressure`): **nothing.**
`api/012` paid the whole sub-project's debt on 2026-09-05 and no `api` file has re-entered
reserve. The only file in reserve suite-wide is `embarch-umbrella/spec.md`, which is another
scope's and another unit's. **So you owe no ride-along compaction** — but you are still the
actor who could put a file back in, so run `scripts/check-doc-size.py --pressure` before you
report and file `tasks/api/<NNN>-compact-api.md` if your own edit spends a reserve.

## What

Two independent loose ends, both left behind when decisions 20 and 21 shipped, both found by
review rather than by a failure. **Neither is a contradiction and neither is urgent** — which
is exactly why they have sat. `embarch-api/open.md` states them:

**1. The `none`-snippet collision error gives advice that cannot be followed.** It tells the
caller to omit `snippets` "to take the project's configured `default_snippets`" — but a
`default_snippets` containing `"none"` is itself now a load error, so that half of the advice
routes the reader into a second refusal. Only the other half (rename the snippet) actually
works. **This is the same defect class as `api/015` and `embarch-api` decision 51**: the
surface text is what a reader acts on, so a message that names an unreachable remedy is worse
than a message that names one remedy.

**2. The load-time refusal is asymmetric.** `default_target` fails at load for a `static`
project. `default_snippets`, `default_extra_args` and `soc_chip_overrides` are **equally
unhonourable on a `static` project** and still load silently. Either the refusal covers the
set or it covers none of it, and whichever you choose, the decision entry has to say which
and why — an asymmetry that is deliberate is fine, an asymmetry nobody decided is a trap for
the next person who adds a field.

## What I am not deciding for you

**Item 2 is a genuine either/or and I want your reasoning, not just your verdict.**

- **Extend the refusal** to the other three fields, so a `static` project cannot carry a
  setting it will never honour. Consistent, catches a real authoring mistake at load. Costs:
  it is a **breaking config change** — a config that loads today stops loading — and the suite
  works directly on `main` with no deprecation window (`embarch-dev-workflow.md` §6).
- **Narrow the refusal** so `default_target` behaves like the other three and the whole class
  is a warn or is silent. Consistent the other way, breaks nothing, and gives up a check that
  is already catching something.

There is a third shape, and if you take it say so plainly: **warn rather than refuse, for all
four.** It is the only one that is both consistent and non-breaking, and the reason to be
suspicious of it is that this suite has a stated preference for refusing at load over warning
(a warn nobody reads is the muted-alarm failure the client-name check was built around).

Whatever you pick, **the decision entry says which and why**, and `open.md`'s bullet loses
whichever half you closed. Do not close a half you did not actually close.

## Why now

`api` had **nothing dispatchable at all** at the start of this leg — my predecessor said so
explicitly — and this is the cheapest genuinely-open `api` item in `open.md` that needs no
hardware, no other repo, and no decision the owner reserves. Everything else in that file is
either blocked on Core (`error_kind`, decision 12), blocked on hardware (a real event stream,
a firmware version off a DUT), or another repo's fix.

## Done when

- [ ] The `none`-snippet collision message no longer advises a remedy that is itself a load
      error. Either it names only the workable remedy, or it names both and says what makes
      the other one conditional.
- [ ] Item 2 resolved one of the three ways above, with a test that pins the behaviour you
      chose — including, if you extended the refusal, one per newly-refused field.
- [ ] The relevant `embarch-api` decision entry records the choice and the argument against
      the option you rejected. Amend in place per `DOC-CONVENTIONS.md`; do not append a
      correction below a body that now contradicts it (that defect is `umbrella/015`, landed
      an hour ago, and it is the second time in two days).
- [ ] `embarch-api/open.md`'s "Two loose ends" bullet is corrected to whatever is left of it,
      or deleted if nothing is.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/api-*` fragment dropped.
      A `features.d/` row only if a capability actually changed, which it probably has not.
