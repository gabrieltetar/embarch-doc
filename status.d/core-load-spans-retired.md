**Target:** suite/features.md — the `GET /study/{id}/stream/{name}/load/spans` row (its `features.d/core-230-load-spans-route.md` fragment is deleted by `tasks/core/105`, so the next assemble drops it; the text here covers a stale hand-edit)
**Was:** "Shipped, `Gap` at full parity with `embarch-ui`'s own ... decisions 65, 66"
**Now:** Route retired by `embarch-core` decision 91 (no caller ever existed; precedent `tasks/core/021`). `/load` is unchanged. Decisions 65 and 66 are tombstones; `embarch-ui` keeps its own decode permanently.

`suite/decisions/placement.md` line 20 cites `embarch-core` decision 64 and describes the route as shipped; it reads as history and may want a pointer to [embarch-core decision 91](../embarch-core/decisions/stream-index.md).
