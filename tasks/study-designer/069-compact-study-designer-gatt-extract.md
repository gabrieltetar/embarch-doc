# 069 — `embarch-study-designer/decisions/gatt-extract.md` is in reserve

**State:** open
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

- [ ] Out of reserve (under 90% of 12,288 B), or the task says why not.
- [ ] **Three things a squeeze will reach for first, and none may go:** decision
      57's three named failure modes of a wide walk (duplicate service, one name
      with two values, no C found at all); decision 56's *rejected* `name` field
      on the characteristic type, which is the reason names ride beside the
      table; and decision 78's argument for the **union** over a pick or a
      failure, which is the whole entry — the union is only defensible while the
      reasoning for it is readable.
- [ ] `decisions.md`'s index row updated if the file splits.
- [ ] Every inbound reference to 33, 56, 57 and 78 still resolves
      (`check-decision-refs.py`) — `embarch-ui` cites all four.
- [ ] Byte numbers before and after.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.
