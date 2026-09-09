# 019 — the per-caller-identity feature row carries as owed work a capability the suite principle forbids

**The filename still reads `features-md-...-embarch-md-5-forbids` and stays that way.** The title
was rewritten 2026-09-09 because it named two paths a `core` worker may not write, which is
`tasks/doc/029`'s defect; the filename could not follow, because a task number's identity is the
number *and* its slug and `check-task-numbers.py` reads a rename as reissuing the number
(`tasks/README.md`). `check-task-state.py`'s rule 6 reads the title, not the filename, for exactly
this reason.

**State:** open
**Source:** suite review pass 2026-09-06, dimension 3 (one philosophy).
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`features.d/core-200-per-caller-identity-beyond-one.md` assembles into `suite/features.md:34` as:

    | Per-caller identity beyond one shared token | Todo | n/a | §6 |

A **bare** `Todo`, where three of that file's five `Todo` rows carry a qualifying clause.

Against `embarch.md:65` — *"**Single-engineer scope.** No multi-tenancy, **no user or permission
model, anywhere.**"* — and `embarch-token.md:59-62`, which records this specific item as one of
those *"**deliberately kept open rather than answered — the repo owner's explicit call**"*, with
the reason (*"per-caller identity distinguishes one caller from itself"*) and a named revisit
trigger.

So the ledger renders a deliberate refusal as owed work. The `Status` vocabulary has `Shipped` and
`Todo` and no third state for *"declined, with a trigger"*, and `build_features.py --check`
validates fragment *shapes* — nothing reads a `Todo` against a principle or against its own owning
doc.

Candidate direction: make it hold that a `Todo` row in the ledger names owed work and nothing else.
This row states the refusal and its trigger, or goes. The fix is the `features.d/` fragment,
**never `suite/features.md` itself**, which is assembled.

## Why now

`embarch.md` §6 sends the newcomer to `suite/features.md` as *"Every feature and how far it is
actually verified"*, and there they learn the suite plans a permission model that the principle two
sections earlier forbids. The row has been safe only by luck: the fleet's refill sweep reads
`suite/roadmap.md` and the eight `open.md` files, and per-caller identity is in neither — so
nothing has yet picked it up as work to do.

## Done when

- [ ] The per-caller-identity row does not read as owed work. **The edit is
      `features.d/core-200-per-caller-identity-beyond-one.md` and nothing else** — the assembled
      file and the principle it contradicts are both outside a `core` worker's row
      (`../../embarch-fleet/protocol.md` §3), so *"or the principle no longer forbids it"* is
      **not** an arm of this task: if that is the answer, drop a `status.d/core-*` fragment saying
      so and leave the row alone. Rewritten 2026-09-09 (`tasks/doc/029`) — the earlier wording
      offered a `core` worker an out it may not take, which is the defect that task exists to stop.
- [ ] The assembled row stays within the **per-row 600 B cap** (`build_features.py`), which is the
      only cap that applies: the assembled file lost its byte cap outright on 2026-09-07, so the
      *"~14 bytes of headroom"* this box used to cite no longer exists.
- [ ] Whether the `Status` vocabulary should gain a "declined, with a trigger" value is
      **`features.d/README.md`'s question and not this worker's** — that file is outside every
      worker's row too. Express the refusal in this row's own prose, and if the vocabulary really
      needs a third value, say so in the `status.d/core-*` fragment.
- [ ] Gate green; `changelog.d/core-*` fragment.
