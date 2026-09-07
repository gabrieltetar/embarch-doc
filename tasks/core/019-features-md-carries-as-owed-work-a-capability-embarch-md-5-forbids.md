# 019 — `suite/features.md` carries as owed work a capability `embarch.md` §5 forbids

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

- [ ] `suite/features.md`'s per-caller-identity row does not read as owed work, or `embarch.md` §5
      no longer forbids it.
- [ ] The assembled row is no larger than it is now (`suite/features.md` has ~14 bytes of
      headroom, `tasks/suite/004`).
- [ ] `features.d/README.md`'s status vocabulary can express "declined, with a trigger", or this
      row expresses it in prose.
- [ ] Gate green; `changelog.d/core-*` fragment.
