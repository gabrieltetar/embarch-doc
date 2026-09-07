**Target:** suite/studies-guide.md §3b — the "Where that is written down is a smaller set than you would expect" sentence
**Was:** "**`BleAddress`'s own doc comment in `src/ids.rs` does not**, though `Uuid`'s states its order right above — so an author who goes to the type for the answer finds nothing, and a wrong guess fails *silently*: the step simply never matches. `tasks/study-designer/014`."
**Now:** `src/ids.rs` states it on `BleAddress` as of 2026-09-06 — display order, most-significant first, the same for both `BleAddressKind`s, with a note that nothing in the crate reverses it. The set of places it is written down is now three, not two, and the type is one of them; the `tasks/study-designer/014` pointer and the "an author finds nothing" clause are both spent.

The paired `embarch-dev-bench` half is `tasks/dev-bench/009` and is **not** folded by this fragment: decision 23 there still records a change that had not landed when it was written, and only that task may amend it.
