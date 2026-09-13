# embarch-study-designer decisions: The GATT table a study declares

**Status:** active, 2026-09-02.

Designed, never built. Split out of [declares.md](declares.md) 2026-09-13 —
verbatim, under `DOC-BUDGET.md`'s split-first rule — because it shares nothing
with that file's other two decisions beyond the word "declares": no code, no
citation from 40 or 74, and no shared reasoning.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 45 — A study declares the GATT table it was authored against, and live discovery is what checks it

**Designed, never built.** No `gatt` field exists on `Study`, no `DeclaredGatt` type exists in `src/`, reconciliation is not implemented, and no `MAX_DECLARED_SERVICES` bound was ever needed. The reasoning below is why it was designed this way, kept for whoever builds it — not a description of code that exists today ([interfaces/types.md](../interfaces/types.md), [../open.md](../open.md)).

Three sources of GATT knowledge existed here, built at three different times, and **nothing ever joined them**: vendor identities, static extraction, and the engineer-authored registry. A study could reference any and declared none, **so nothing could answer the question this milestone actually got stuck on — *is the service this study writes to even present on the build under test?* A whole session ran without that being answerable, because the DUT's GATT table had never once been seen.**

An optional declaration carrying a source and the services, **reusing the same types a live discovery fills in rather than a parallel shape, so comparing the two is a comparison and not a translation.** The source is one of: resolved vendor identities, an extraction against a real checkout **recording *which* checkout**, or hand-authored. Host-side only, **and dev-bench continues to interpret nothing.**

**Live discovery wins, and the difference is reported rather than tolerated.** When a discovery step runs in a study that declared a table, Core reconciles the two and records **what was declared-but-absent, present-but-undeclared, or present with different properties.** A declared service missing from the DUT is **not a study failure by default — it is the single most useful line in the result**, and exactly the fact nobody could produce for a whole session: the config symbol was set, **but was the service actually registered?**

**This is the durable form of decision 35's rule.** That decision said engineer-supplied knowledge must come from the engineer; **this one says where in the study it goes, so an agent authoring one has a field to put it in rather than a temptation to infer it.**

**What building it would take:** a `DeclaredGatt` enum (`Vendor` / `Extracted { repo, revision }` / `Authored`) reusing `GattServiceInfo`/`GattCharacteristicInfo` from [interfaces/gatt-types.md](../interfaces/gatt-types.md), a `gatt: Option<DeclaredGatt>` field on `Study`, and the reconciliation pass in Core this paragraph describes. **Deferred on a named trigger: the first study that needs to say which GATT table it was authored against.** Until one exists, building this would be designing against imagined authoring, the same restraint decision 45's own reasoning argues for.
