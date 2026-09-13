# embarch-dev-bench decisions: Documentation conventions

**Status:** active, 2026-09-13.

How a comment in this repo's C sources cites another repo's decision, and what happens when the
document it used to point at is gone.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 47 — A bare `§N` into a deleted `design.md` resolves to a decision, a live document, or nothing — never a naked section number

`dev-bench/019`, `020` and `022` each repointed citations of the deleted
`embarch-study-designer/design.md §3` and this repo's own `design.md` away from the dead filename.
Where a citation carried a decision **number** alongside the section, the fix was already covered
by [DOC-CONVENTIONS.md](../../DOC-CONVENTIONS.md)'s citation form and resolved cleanly: own-repo,
the bare number (`decision 39`); cross-repo, the repo named (`` `embarch-study-designer` decision
39 ``). Where a citation carried **only** a section number — `design.md §4.8`, `§4.3a`, `§4` — the
three units, independently and without writing anything down, converged on the same wrong move:
strip the dead filename and leave the bare section number standing alone. That is not a fix. It
drops the repo name along with the filename, so a reader who could previously search a named
repo's history for what `§4.8` became now has nothing to search at all — a citation naming neither
a decision nor a document is *strictly worse* than the dead-but-named path it replaced, not an
improvement on it (`dev-bench/022`'s reviewer, 2026-09-13, caught this and it is why this decision
exists).

**The rule, applied per citation rather than by pattern-matching the text around it:**

1. **If the cited material is now owned by a specific decision** — the section described a type,
   a rule, or a behavior that a `decisions/<topic>.md` entry in the owning repo now states —
   resolve to that decision, in the citation form above. Most of the `.eap`-manifest citations
   (`§4.9` beside "decisions 58-62") were already carrying the right decision numbers and only
   needed the redundant dangling section dropped; a few carried the *wrong* decision number
   entirely (content about GATT discovery's flattening convention cited as `§4.3a` with no decision
   attached, when it is `embarch-study-designer` decision 32's rule by content) and were corrected
   by rereading the paragraph, not by trusting the number already there.
2. **If the cited material moved to a live, still-readable document instead of a decision** —
   this repo's own open questions live in `open.md` now, not in a numbered decision — name that
   document directly (`open.md`), the same way `scan_seen_mfg.h` already cites it elsewhere in this
   repo. A live document is always preferable to a decision citation that would misrepresent an
   unresolved question as a settled one.
3. **If neither applies** — the citation was to a general "how the types are shaped" passage with
   no single owning decision, or the repo naming it is already stated in the surrounding sentence
   with nothing left for a section number to add — delete the section pointer outright. **Do not
   invent a section number for a document nobody can read, and do not guess which decision absorbed
   a section when the paragraph does not say.** A missing citation costs a reader nothing they did
   not already not have; a wrong or repo-less one costs a false lead.

**Applied retroactively** (`dev-bench/029`) to every bare `§N` this repo's C sources still carried,
re-deriving the count from `grep` rather than trusting either of two disagreeing prior counts:
`app/src/main.c`, `ble_bridge.h`, `ble_bridge_real.c`, `serial_protocol.c`, `serial_protocol.h`,
`eap.h`, `eap_interp.h`, `eap_interp.c`, and `app/tests/serial_protocol/src/main.c`. One survivor
was deliberately left untouched: `ble_bridge_real.c`'s `§1.3` cites the Bluetooth Core
Specification's own Vol 4 Part E, an external standard with real numbered sections, never this
repo's or `embarch-study-designer`'s `design.md` — the same `§N` shape, a different kind of
reference entirely, and resolving it as if it were one of ours would have been exactly the mistake
this decision exists to stop.
