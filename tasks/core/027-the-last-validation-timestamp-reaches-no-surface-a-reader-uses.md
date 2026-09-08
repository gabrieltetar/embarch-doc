# 027 — `validated_at_utc_ms` exists only on the one response no reader calls

**State:** open
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

## Done when

- [ ] Either `EnrolledBoardResponse` carries a last-validation timestamp (with
      the store change and the migration behind it, and a decision recording
      why), or a numbered decision records that it deliberately does not and
      says what the passive readers should render instead.
- [ ] If the answer is "label, do not add", the follow-up tasks for
      `embarch-umbrella` and `embarch-ui` are filed rather than assumed.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
