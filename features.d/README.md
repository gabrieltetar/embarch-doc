# features.d

One file per **row** of the suite feature inventory. Nothing edits
[suite/features.md](../suite/features.md) directly — it is assembled by
`scripts/build_features.py` and a hand-edit there is reverted by the next
assemble, silently.

    features.d/<scope>-<NNN>-<slug>.md

- **scope** — a sub-project without the `embarch-` prefix (`core`, `api`,
  `dev-bench`, `study-designer`, `outpost`, `topology`, `umbrella`, `ui`), or
  `not-yet` for a capability whose sub-project has no repo. The scope picks the
  section the row lands in.
- **NNN** — three digits, ordering the row **within its section**. Migrated rows
  went in at 010, 020, 030…, so there is room to insert without renumbering.
  Two fragments in one scope may not share a number.
- **slug** — short, hyphenated, and only an identifier; nothing reads it.

## The file

**One markdown table row, one line, 600 bytes maximum, four cells:**

    | Feature | Status | Verified | Decision |

```markdown
| `embarch deploy-core` — one-command deploy onto the live Windows service | Shipped — **the verification compared a byte count and reported `landed` through a cancelled elevation** | hw | 32 |
```

600 rather than `changelog.d/`'s 200, because a `Status` caveat is the row's
whole value: *what is built* is cheap, *how far it is actually verified* is what
this inventory exists to say.

**Relative links are written as if from `suite/`** — `../embarch-token.md`,
`../embarch-api/spec.md`. That happens to be identical from `features.d/`,
since both directories sit one level below the repo root, so `check-links.py`
resolves a fragment's links and the assembled file's links to the same targets.
It is a coincidence worth knowing about rather than a rule to rely on: a
fragment directory at a different depth would need the links rewritten at
assembly.

## What goes in a cell

The header of [suite/features.md](../suite/features.md) is the contract and it
is generated from [HEADER.md](HEADER.md). In short: **Verified** is the column
that matters and is not a synonym for Status — `unit`, `local`, `hw`, `n/a`. A
`Shipped` with a caveat spells the caveat out; a bare `Shipped` has none worth
stating. The row is **a pointer**: the reasoning lives in the owning decision
and is never restated here.

## Why this exists

`suite/features.md` is an inventory of a suite under active development, so a
row lands about as often as a task does — it is the one doc in this repo with no
quiet state. [DOC-COMPACTION.md](../DOC-COMPACTION.md) §8 says not to compact a
subsystem in flux, and §2 gives this file the interfaces cap for the interfaces
reason: **every row must be present, so the budget is spent on rows and no
compaction pass can help.** Measured 2026-09-04 it was gaining ~200 B per
four-unit leg with 939 B of headroom — about four legs from a wall that nothing
could move.

Assembling it removes the wall, and pays a second dividend that turned out to
matter more. `suite/features.md` is outside every worker's ownership row
([the protocol](../../embarch-fleet/protocol.md) §3), so a worker that shipped a
feature could not record it: it dropped a `status.d/` fragment and the
supervisor hand-folded the row in later, or forgot. **`features.d/<its own
scope>-*` is the worker's to write**, so the row lands in the same commit as the
work that earned it, and `check-ownership.py` enforces that a worker touches
only its own.

`HEADER.md` carries the title, the `**Status:**` line and the prose above the
first section. It is the only fragment here that is not a row.
