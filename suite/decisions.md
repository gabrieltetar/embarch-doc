# embarch: suite-wide decisions

**Status:** active, 2026-09-12.

Decisions that span more than one sub-project and therefore belong to none of them — the record every sub-project's own `decisions.md` keeps, at suite level. It exists because there was nowhere for a suite-wide call to go, so one accumulated inside a principle bullet in [embarch.md](../embarch.md) §5 (`tasks/suite/008`, announced and parked 2026-09-06, window closed unanswered; that task file was consumed by its own fold, hence a citation and not a link).

**What belongs here:** a call binding more than one sub-project that is not a rule of the development process. **What does not:** anything in [embarch-dev-workflow.md](../embarch-dev-workflow.md), [DOC-PROTOCOL.md](../DOC-PROTOCOL.md), [DOC-COMPACTION.md](../DOC-COMPACTION.md) or [the protocol](../../embarch-fleet/protocol.md) — the reserved rule set; a decision needing one of them amended is the repo owner's. **And [embarch.md](../embarch.md) §5 stays a list of one-line principles**: a principle that grows a measurement history, a reversal condition and a named trap has become a decision record, so it moves here and §5 keeps the one line plus a pointer.

**This file is an index.** The decision text lives in the topic files below — the shape every sub-project's own `decisions.md` already uses. It became one on 2026-09-12 (`tasks/suite/033`): three decisions in one file put it 1,794 B over its cap **two hours after `suite/031` had compacted it out of reserve**, and a compaction a single new decision undoes is evidence of the wrong shape rather than of a bad compaction. Nothing was re-worded in the move; only relative link paths were re-based for the extra directory level, the same allowance `suite/008` took.

| # | Decision | File |
|---|---|---|
| 1 | `rustfmt` is not enforced, and nobody runs `cargo fmt` | [decisions/tooling.md](decisions/tooling.md) |
| 2 | `embarch-outpost` gets a host-only CI workflow, and a green check there covers strictly less than a local run | [decisions/tooling.md](decisions/tooling.md) |
| 3 | `rx_utc_ms` keeps its name in both homes, and every home says which clock it is | [decisions/naming.md](decisions/naming.md) |

- **[decisions/tooling.md](decisions/tooling.md)** — how the suite's formatting and CI checks are run, and what a green one covers.
- **[decisions/naming.md](decisions/naming.md)** — what a field name shared across two sub-projects is allowed to promise.
