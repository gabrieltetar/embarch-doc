# 044 — `suite/decisions/placement.md` §4's "exactly one implementation" property is permanently false, not transitionally false

**State:** done — leg 139, 2026-09-17. **The 30-minute window opened at `1789684951` and closed
unanswered**; the thread was polled at every unit boundary of this leg (three times) and carried no
reply but the supervisor's own detail post. Executed by the supervisor as its fourth and last unit.
Originally drained from
`inbox/suite-placement-decision-4s-exactly-one-implementation-property-is-permanently-false.md` by
leg 139, 2026-09-17. Body unchanged apart from this line, the number, and the supervisor note below.

**Announcement `ts`: `1789684951.085879`** in `#embarch-fleet` (`ops.md` §4). The window opened at
that timestamp and closes 30 minutes later. **If it is still open when you read this, do not restart
the clock — read the thread with `scripts/fleet-read.py --thread 1789684951.085879` and execute
once the 30 minutes have elapsed with no objection.** A reply saying go runs it now; a reply saying
cancel drops this back to plain `open` with the reply quoted here.

**This is a `suite` task, so the supervisor executes it — never a worker** (`protocol.md` §8).
**Source:** `embarch-core` decision 66 (`embarch-core/decisions/stream-index.md`), from
`tasks/core/085`. Filed here rather than edited directly: `tasks/core/085`'s dispatch note bars a
`core`-scoped worker from touching `suite/decisions/placement.md`, and a suite-scope task is one the
supervisor executes itself, never dispatches to a worker (`tasks/README.md`).
**Scope:** suite
**Hardware:** none.

## What

Suite decision 4 (`suite/decisions/placement.md` §4) bought *"an agent can obtain [the outpost's
per-subject load shares and coverage line] without re-implementing the timeline, and **exactly one
implementation of that timeline exists in the suite**."* `embarch-core` decision 64 believed shipping
`GET .../load/spans` would close that property. `tasks/ui/065` checked the served payload against
`embarch-ui/src/trace.rs` field-for-field and found it does not, and `embarch-core` decision 66
(`tasks/core/085`) established why not permanently rather than provisionally: axis-health
diagnostics (`frames`, `resolution_ms`, `dual_clock`, and nine more — all fields of `trace.rs`'s own
`TraceView`) and point events are excluded from `embarch-core`'s route by decision 62's own scoping
and stay excluded, because serving them would not let `embarch-ui` retire its row decode either —
point events are built in the same row-iteration pass, so the loop stays regardless.

**Net: the *reduced* answer (`LoadSummary`, per-subject shares and the coverage line) does have
exactly one implementation — `embarch-core`'s. The full timeline underneath it (row
decode/clock-health/stale-prefix/`Lane`/`Span`/`Gap` construction) does not, and per decision 66,
never will while `trace.rs` needs point events and axis-health notes it alone computes.** §4's text
does not distinguish these two properties; as written it reads as bought in full.

`embarch-core` decision 64's own closing sentence (which claimed the gap was closed) has already
been corrected in `embarch-core/decisions/stream-index.md`, citing decision 66. This drop is only
about `suite/decisions/placement.md` §4's text, which `tasks/core/085` was not permitted to touch.

## Why now

A suite-level doc asserting a property as bought when it is now established as *not* bought, by two
sub-projects' own decision records, is exactly the kind of drift `check-decision-refs.py` cannot
catch (it checks citations resolve, not that what they say is still true).

## Done when

- [x] `suite/decisions/placement.md` §4 narrows its stated property to the **reduced** answer, and
      **also** adds the paragraph naming the permanent exception, citing `embarch-core` decision 66.
      Both, not either — the one-word narrowing fixes the falsehood but leaves a reader with no way
      to know which of the two properties they are holding, and the drop's own framing (reduced
      answer vs. full timeline) is the thing worth not re-deriving.
- [x] Gate green — `check-docs.py` 11/11.
- [x] `changelog.d/suite-placement-decision-4-scoped-to-what-it-actually-bought.decided.md`.

## What was actually written, and one thing deliberately left alone

The edit does three things. It changes *"exactly one implementation of that **timeline**"* to
*"of that **reduced answer**"*. It adds a paragraph immediately after, stating both properties
separately — the reduced answer genuinely has one implementation and it is `embarch-core`'s; the
full timeline has two, `outpost_load.rs` and `trace.rs`, permanently per decision 66 — with that
decision's two reasons in one sentence each. And it records the **history**, because the drift is
more instructive than the correction: decision 64 wrote a tombstone for a gap that was still open,
`tasks/ui/065` found it by comparing payloads field by field, and **`check-decision-refs.py` cannot
catch this class at all** — it verifies a citation resolves, not that what it says is still true.

**Left alone deliberately: the "honest limit" paragraph further down §4**, which already says that
*being Core* is not what makes an implementation correct — being **one** implementation, pinned to
the vocabulary it decodes, is. That paragraph was written against reversals row 86 and it reads
*more* sharply now that the timeline is known to be permanently double-implemented, so the new
paragraph points at it rather than restating it. The home argument and the reversal condition are
untouched: **this task changed the scope of the property §4 says it bought, not the decision.**
