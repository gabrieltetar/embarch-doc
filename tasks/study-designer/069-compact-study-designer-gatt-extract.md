# 069 — `embarch-study-designer/decisions/gatt-extract.md` is in reserve

**State:** claimed by agent/study-designer/069-compact-gatt-extract, 2026-09-29 21:05
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by decision 78
**Scope:** study-designer
**Hardware:** none — prose only, plus a `grep` over the corpus.
**Owner:** no
**Compacts:** embarch-study-designer/decisions/gatt-extract.md
**Size debt due:** 2026-09-27
**In flux:** no

## What

The GATT-extraction decision group is **12,252 / 12,288 B, 36 B left**, on this
task's clock. Out of reserve when this closes, or the task says why not.

The entry that crossed the floor is **78**, the config-gated properties alias.
It was trimmed three times on the way in to fit, and what went was phrasing —
but 36 B is not enough to correct a sentence in any of the four entries, which
is a worse state than the reserve usually describes.

## Where the seam is

Four decisions, two missions: **33 and 57 are the scan** — what it reads, how
wide it walks, what it refuses — and **56 and 78 are resolution**, turning a
scanned token into a name or a properties byte. 78 is the newer half's second
entry and the one most likely to grow: every firmware convention the scanner
learns to resolve lands there, and it has already met one real `#if`.

A split into `decisions/gatt-scan.md` and `decisions/gatt-resolve.md` is the
candidate, per [../../DOC-BUDGET.md](../../DOC-BUDGET.md) §3. Judge it against a
squeeze first — 57 is the longest entry by a wide margin and carries three
rejected alternatives that may compress.

## Done when

- [x] Out of reserve (under 90% of 12,288 B), or the task says why not.
- [x] **Three things a squeeze will reach for first, and none may go:** decision
      57's three named failure modes of a wide walk (duplicate service, one name
      with two values, no C found at all); decision 56's *rejected* `name` field
      on the characteristic type, which is the reason names ride beside the
      table; and decision 78's argument for the **union** over a pick or a
      failure, which is the whole entry — the union is only defensible while the
      reasoning for it is readable.
- [x] `decisions.md`'s index row updated if the file splits. (N/A — squeezed,
      not split; see below.)
- [x] Every inbound reference to 33, 56, 57 and 78 still resolves
      (`check-decision-refs.py`) — `embarch-ui` cites all four.
- [x] Byte numbers before and after.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.

## Closed: squeezed rather than split, and why

**Before/after:** 12,252 B -> 11,053 B (89.94% of the 12,288 B cap). All three
protected clauses in the "Done when" list above are untouched verbatim: decision
57's three named failure modes, decision 56's rejected-`name`-field paragraph,
and decision 78's union argument (the "union is only defensible because it is
visible" paragraph and its three-candidate-answers reasoning).

**The candidate split (`gatt-scan.md` for 33/57, `gatt-resolve.md` for 56/78)
was rejected, not attempted.** `embarch-ui/decisions/gatt-capture.md` and
`embarch-ui/decisions/designer-panels.md` link decisions 33, 56 and 78 straight
at `embarch-study-designer/decisions/gatt-extract.md` (the topic-file link
shape `check-decision-refs.py`'s `check_topic_links` watches for). A split
moving 33 into a different file would make that link stale the moment 33 no
longer resolves there — the exact `topology/010` failure mode the script's own
docstring names — and the fix is either DOC-CONVENTIONS.md's canonical
`embarch-ui` -> `<sub>/decisions.md` indirection (an edit inside `embarch-ui`,
outside this task's ownership row) or leaving the gate red for a sub-project
this task must not touch. Squeezing needed no cross-repo edit and left every
inbound link, including `embarch-study-designer/interfaces/gatt-types.md`'s own
reference to 57, resolving unchanged. Filed as an inbox drop for whoever owns
`embarch-ui` next, in case the split is revisited later.

**Squeeze quote (verbatim first dozen-ish words of each cut hunk, file-qualified),
per DOC-COMPACTION-PASS.md:**

- `decisions/gatt-extract.md` (33): "so extracting it statically lets a step be
  authored with real UUIDs before dev-bench connects to anything, and" ->
  tightened to "extracting it statically authors a step ... before dev-bench
  connects,"
- `decisions/gatt-extract.md` (33): "confirmed against real source rather than
  guessed against a generic Zephyr layout. It is a `std`-only ... never
  something dev-bench or Core links." — reworded, no clause dropped.
- `decisions/gatt-extract.md` (56): "because that was the only thing this crate
  could tell a UI" -> "the only thing this crate could tell a UI" (compressed,
  not cut).
- `decisions/gatt-extract.md` (56): "An identifier says what the firmware's
  authors *call* a characteristic" paragraph — trimmed connective tissue
  around it, kept the mechanical-shortening rule and the "no expanding an
  abbreviation" prohibition whole.
- `decisions/gatt-extract.md` (57): "What decides the scope now: the firmware
  repo's own ignore files, not a list this crate maintains." -> "Scope is now
  the firmware repo's own ignore files, not a list this crate maintains" —
  same claim, shorter lead-in.
- `decisions/gatt-extract.md` (57): "Printing the handful of contributing files
  out of hundreds read is what makes 'it never opened the file I expected'
  something an engineer can *see* rather than infer from a table that came
  back plausible." — this illustrative sentence was cut; the invariant it
  illustrates ("this kills the failure mode rather than patching this
  instance of it") stays.
- `decisions/gatt-extract.md` (78): "[embarch-ui] decision 41 recorded it as 'a
  real extractor limitation' and nothing tracked it;" -> "recorded it as 'a
  real extractor limitation';" (dropped "and nothing tracked it", a narrative
  aside, not a constraint).
- `decisions/gatt-extract.md` (78): "`chrc_property_bit`'s own rule, one level
  up." — cut; the rule itself ("a half-read expression is refused rather than
  contributing the bits it recognized") stays, only its cross-reference name
  went.

No rejected alternative, failure signature, or constraint reason was removed
from any of the four entries. What went was connective phrasing, one
illustrative sentence (57) and one narrative aside (78) — none of it something
a reader would need to avoid re-proposing a rejected fix.

**Human question (DOC-COMPACTION-PASS.md):** *Can `spec.md` alone answer what
someone needs to work on this component today?* Not assessed as part of this
unit — this task compacted one decision-group file, not `spec.md`, and
`spec.md` was untouched. The question as asked applies to the second-pass
hot/cold split of a sub-project's whole decisions layer, not a reserve-driven
squeeze of one topic file; nothing here changed what `spec.md` can answer.
