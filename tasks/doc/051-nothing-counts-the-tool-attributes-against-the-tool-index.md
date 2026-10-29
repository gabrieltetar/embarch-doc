# 051 — Nothing counts `#[tool(...)]` against the tool index, and the index is the file agents read first

**State:** done — owner session, 2026-10-29, branch `owner/decision-refs`: new `scripts/check-tool-index.py`, run by `check-docs.py`; 54 tools, index green; see `## Closed`
**Source:** `api/080`, leg 107, 2026-09-13. Found by a worker and a reviewer independently counting
the same attributes, which is the only evidence available for this file today.
**Scope:** doc
**Hardware:** none — a check in `scripts/`.
**Owner:** required — `scripts/` is owner-reserved (`protocol.md` §3), so no agent may add this
check. Filed here so it is visible in the queue rather than only in a log entry that folds daily.

## What

`embarch-doc/embarch-api/interfaces/tools.md` is the tool index: five sections whose lists name
every MCP tool `embarch-api` exposes. Nothing compares it to the `#[tool(...)]`-annotated functions
in `embarch-api/src/tools.rs`.

`api/080` re-derived the census by hand: **26 annotated functions, and the five section lists sum
to 3+6+5+6+6 = 26** once a stale phrase naming three retired aliases was removed. That is correct
as of `embarch-doc` `76e75af` / `embarch-api` `cd1bc2f` and nothing can keep it correct.

## Why now

The defect this would have caught is not cosmetic. `suite/015` retired `study_power_data`,
`study_waveform_data` and `study_gatt_data` on 2026-09-11. `interfaces/studies.md:15` was updated
to say *"the three **retired** fixed-channel aliases"*. `interfaces/tools.md:15` still said
*"the three data aliases"* — **two interface docs in one directory, disagreeing for two days, and
the wrong one is the index a reader meets first.** An agent reads that file to decide what to call,
so the failure mode is a call that 404s rather than a sentence that reads oddly.

`check-decision-refs.py` and `check-links.py` resolve links and decision numbers. Neither can see a
prose enumeration, and `tasks/doc/033` and `tasks/doc/044` are the general-purpose halves of that
gap — this is the narrow, cheap, mechanical case inside it.

## Done when

- [x] A check enumerates `#[tool(...)]` attributes in `embarch-api/src` and compares both the
      **total** and the **set of names** against `embarch-doc/embarch-api/interfaces/tools.md`.
      The set matters more than the total: two compensating errors pass a count.
- [x] It runs inside `check-docs.py` so a worker and a leg both meet it.
- [x] It tolerates prose. `tools.md` legitimately mentions non-tool identifiers — `versions`,
      `doctor`, JSON field names, crate names, and retired alias names inside an explanatory
      parenthetical. A check that flags those is a check that gets disabled. `api/080`'s reviewer
      distinguished them by hand; whatever rule it used is the one to encode.
- [x] Run against `main` as it stands: it should report green, because `api/080` left the index
      true. A red result means the census was wrong and that is worth knowing immediately.

## Do not

Do not widen this into a general prose-enumeration checker — that is `tasks/doc/044`'s problem and
it is much harder. This one has a machine-readable source of truth on both sides.

## Closed

**Green on `main`: 54 `#[tool]` fns, all 54 listed, nothing else** (`versions` is listed and
declared CLI-only). The index has grown from five sections to eleven since this was filed, and
the census is still exact.

**The rule the reviewer applied, encoded:** only the *leading run* of each `## Sections` bullet
counts — the comma-separated backticked names right after its dash. Everything after the run is
prose and is never read: the retired aliases in the Studies parenthetical, `test` in the Ledger
bullet, `status` in the Lease bullet, and the whole rest of the file. A listed name that is not a
tool must appear in the file's own "The CLI is a **superset**" sentence, so the doc declares its
exceptions and the script hardcodes none.

**Tested against the real files, mutated in memory:** dropping `reset_dev_bench` (the `api/080`
history case) fails as missing; adding a retired alias to the Studies run fails as unknown;
dropping one tool and adding another fails both by name, where a count would pass; removing
`versions` from the superset sentence fails it; a retired alias added to the prose after a run
passes. With no `../embarch-api` beside the repo it prints `SKIP` and exits 0, the same rule
`check-docs.py` applies to the framework checks — CI has no sibling checkout, so CI does not run it.

**Shape chosen:** a separate 97-line script rather than a function inside an existing check,
because it is the one doc check that reads a code repo and so the one that must skip on its own.
It does not widen into general prose enumeration, as asked.