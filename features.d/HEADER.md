# embarch: feature inventory

**Status:** active, 2026-09-02.

**What is built, how far it has been verified, and who owns it.** One row per capability, grouped by sub-project. **Assembled from [features.d/](../features.d/README.md), never edited here** — a hand-edit is reverted by the next `scripts/build_features.py`. Deliberately a *pointer*: the reasoning is in the owning decision, never restated here.

**Verified** is the column that matters, and it is not a synonym for Status. **unit** — mocked or synthetic tests only, no live process. **local** — a real running Core, repo or CI on this machine, but no physical probe or board. **hw** — validated against an actual probe, board, or a genuine OS service install. **n/a** — not shipped.

A `Status` of `Shipped` with a caveat spells the caveat out; a bare `Shipped` has none worth stating. Decision numbers cite the sub-project's own `decisions.md`.
