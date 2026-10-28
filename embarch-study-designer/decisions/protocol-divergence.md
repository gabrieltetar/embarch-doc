# embarch-study-designer decisions: Protocol divergence

**Status:** active, 2026-10-28.

Whether a saved study's protocols still match the `.eap` files; additive to decisions 58 and 75 (in [protocols.md](protocols.md)).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 87 — A saved study's protocols are checked against the manifests by comparing definitions, never a digest

A study carries a resolved `ProtocolDef` and a protocol name (decisions 58, 75), so editing the `.eap` afterwards changes nothing it runs — correct, and silent. `eap_repo::divergence(carried, current)` (exported `protocol_divergence`; `eap-parse` feature) answers, per protocol the study carries and in the study's order: **`Unchanged`**, **`Changed`** (one `Difference` per source, frame, session variable or state that was added, removed or modified, by name), or **`Gone`** (the name does not resolve: deleted, renamed, unparseable, or declared by two files). `carried` is `&study.protocols`; `current` is `RepoProtocols::defs()`. A study with no protocol gets an empty list.

**Structural, not a pinned CRC**, for decision 58's reason: a CRC stored in the study goes stale on the author's next edit, and would need a field on `Study` that every consumer builds by literal. `ProtocolDef` already derived `PartialEq`, so nothing in the wire or the stored shape changes. **Advisory only:** the study is neither modified nor refused, and a diverged study still runs what it carries. What to *show* is `embarch-ui`'s. Detail stops at the state/frame level; two definitions equal part by part but not overall differ only in order, reported as a `(order)` modification because every cross-reference is an index.
