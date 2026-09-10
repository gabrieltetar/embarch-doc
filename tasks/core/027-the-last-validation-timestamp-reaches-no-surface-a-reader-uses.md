# 027 — `validated_at_utc_ms` exists only on the one response no reader calls

**State:** done
**Source:** leg 045's reconciliation of `tasks/umbrella/041` and `tasks/ui/020`,
both of which were closed as unsatisfiable. Upstream: `tasks/topology/009`'s
consumer enumeration, `embarch-topology` decision 26, `embarch-core` decision 50.
**Scope:** core
**Hardware:** none
**Owner:** no

## What was found

`topology/009` added `validated_at_utc_ms` — when a board's live identity check
actually ran — because `confirmed_at_utc_ms` names *enrolment* time and can be
days stale on a passing check. It then enumerated the consumers that should show
it, and four tasks were filed down that chain. Three landed
(`core/026`, `api/045`, `api/046`). **The remaining two named readers turn out
not to read that response at all**, checked against the code as it stands:

- **`embarch-umbrella`'s `doctor`** contains no occurrence of
  `confirmed_at_utc_ms`, makes no call to `POST /validate`, and does not depend
  on `embarch-core-client`. It also *must not* call it: `src/doctor.rs`'s own
  header states the property that `doctor` takes no `hw_lock` and waits on no
  board, which is exactly what `POST /validate` does.
- **`embarch-ui`'s Topology tab** renders `EnrolledBoardResponse`
  (`src/snapshot.rs`), never a `ValidateResponse`. Leg 044's reviewer
  independently confirmed `EnrolledBoardResponse` was correctly left without the
  new field, because its upstream body never carries it.

The field lives on exactly one response — `POST /validate`
(`embarch-core/src/api.rs`) — and that endpoint takes the hardware lock and
touches a board. **The enrolled-board shape that every passive reader actually
consumes (`api.rs`'s `EnrolledBoardResponse`, served by `GET /probes/enrolled`
and echoed in `GET /status`) still carries `confirmed_at_utc_ms` alone.** So the
defect `topology/009` set out to fix — a human reading enrolment time as
freshness — is untouched for both of the surfaces where a human actually reads it.

## The question, which is a design call and not a mechanical fix

Should Core **persist** the last successful validation's timestamp with the
enrolled board, so that `EnrolledBoardResponse` can carry it and a passive
reader can answer "how stale is this identity check?" without taking the lock
and touching hardware?

That is a store change, not a response change, and it is the reason this is
filed as a question rather than as an edit. Arguments to weigh, not to assume:

- **For:** it is the only shape in which `doctor` and the Topology tab can ever
  show the thing decision 26 exists for, and both are the readers most likely to
  mislead. `topology/009` observed the concrete failure — two roles, both `ok`,
  timestamps six days apart, read as a freshness ranking that meant nothing.
- **Against:** a persisted "last validated" is a new durable fact with its own
  staleness and its own migration, and `confirmed_at_utc_ms` already has a
  documented meaning that a second timestamp beside it may blur rather than
  clarify. It may be that the honest answer is to **label** the existing field
  as enrolment time everywhere it is rendered, and never claim freshness at all.

**Either answer closes this task.** What must not happen is a third consumer
being filed against a field it cannot reach.

## Why now

Not urgent. Filed so the residue of a four-task chain is visible rather than
lost when the two unsatisfiable tasks were closed.

## Resolution

**Chose "label, do not add."** `embarch-core` decision 54 (`decisions/surfaces.md`)
records why: a persisted last-validation instant needs a store change in
`embarch-topology`'s enrollment file, not this crate's, so it is a cross-repo
half-change the "for" arm can't actually complete from a `core`-scoped unit —
and even done right, every board enrolled before the field existed would have
no honest value to backfill, which is the exact trap the dispatch note named.
Decision 54 says what passive readers render instead: **"Enrolled"**, never
"Validated"/"Last validated", with a cross-reference added to
`interfaces/topology.md` next to `confirmed_at_utc_ms`. No `embarch-api` or
`embarch-ui` code changed.

## Done when

- [x] Either `EnrolledBoardResponse` carries a last-validation timestamp (with
      the store change and the migration behind it, and a decision recording
      why), or a numbered decision records that it deliberately does not and
      says what the passive readers should render instead. — decision 54.
- [x] If the answer is "label, do not add", the follow-up tasks for
      `embarch-umbrella` and `embarch-ui` are filed rather than assumed. —
      dropped to `embarch-doc/inbox/umbrella-relabel-confirmed-at-if-doctor-ever-shows-it.md`
      and `embarch-doc/inbox/ui-relabel-confirmed-at-cell-away-from-freshness-wording.md`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Dispatch note (leg 066, 2026-09-10 15:35)

**This is a design task and the decision is yours to make.** Protocol §5.4: a numbered decision
scoped to one sub-project needs nobody's approval. Both arms above close this task, and I am not
pre-picking between them — but I am naming what would make each one wrong, because the failure
this task exists to prevent is "a third consumer filed against a field it cannot reach".

**If you choose to persist and serve it**, the store change and the migration are the whole cost,
and the decision body must state what a reader sees for a board enrolled *before* the field
existed. A `None` that renders as "never validated" would be a lie about every board on the
bench today. That is the sentence I would look for first in review.

**If you choose to label rather than add** — which the task itself flags as possibly the honest
answer — then the decision has to say what the passive readers should render *instead*, in words
a `doctor` line and a UI cell can both use, and **bullet 2 above becomes binding**: file the
follow-up tasks for `embarch-umbrella` and `embarch-ui` rather than assuming someone will notice.
Those two are `tasks/umbrella/<NNN>` and `tasks/ui/<NNN>`, which is a **cross-scope write and is
NOT yours** — `check-ownership.py --scope core` will refuse both. Write each one as a full task
file into **`/home/gabriel/Github/embarch/embarch-doc/inbox/`** instead, by that absolute path,
per `inbox/README.md`; I file them into the queue in the fold. Do not write them relatively, and
do not put them under `tasks/`.

**Do not change `embarch-api` or `embarch-ui` code either way.** `embarch-core-client`'s response
structs live in `embarch-api`, and one of them (`EnrolledBoardResponse`) is exactly what the
persist arm would need to grow. That makes the *rollout* cross-repo, which §8 reserves to the
supervisor. Land Core's half — the store, the response Core serves, the decision — and file the
client half into `inbox/` as above. `tasks/api/044` is already the standing example of this shape
being mis-filed as a single-worker task; do not repeat it in the other direction.

**Doc-size reserve for this sub-project.** `embarch-core/open.md` is at **4,813 / 5,120 B
(94.0%), 307 B left**, filed against `tasks/core/022-compact-core.md` — which is `open`, not
blocked, so the debt is live and payable and is **not** your unit. Every `decisions/` file has
room (largest `studies.md` at 10,762 / 12,288); `handshake.md` is 5,553 B and is where decision 47
lives, so it is the natural home if your decision belongs beside that one. `spec.md` is
8,212 / 10,240. **Keep `open.md` net-zero or net-negative**: if your answer closes an open
question, strike it and you have paid down 307 B of nothing; if it opens one, you have spent a
reserve that is already 94% gone, and the standing rule then makes you record the debt — amend
`tasks/core/022` rather than filing a duplicate compaction task.

**Read `embarch-topology` decision 26 and `embarch-core` decision 50 before deciding.** The
task's upstream chain rests on both, and decision 26 is the one that says what
`validated_at_utc_ms` is *for*. Read the bodies, not the headings — three legs running have found
a citation that looked wrong because only the body says what a decision covers.
