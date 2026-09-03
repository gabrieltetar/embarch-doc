**Target:** suite/user-guide.md §5.2 — the `--snippet`/`--extra-arg` bullet
**Was:** "`--snippet none` forces zero regardless of the project default."
**Now:** No such sentinel exists in embarch-api. `resolve.rs` has no handling for a `"none"` snippet literal and its own `Selection::snippets` comment says there is currently no way to force zero snippets over a configured default.

Found while doing `tasks/api/004`, **not caused by it** — the claim mirrors `embarch-api` decision 21, which was recorded and never built. `embarch-api/open.md` now carries the gap ("Decisions 20 and 21 describe config that does not exist"); the fix is either building the sentinel or retiring the decision, and until one happens this line tells a reader to run a flag that will be passed straight through as a snippet name and rejected as unknown.

Worth adding to §5.1 in the same pass, though nothing there is false today: a `discovery = "static"` project now **refuses** any of the six selection params rather than ignoring them (`embarch-api` decision 51), so a reader who carries the §5.2 flags back to a single-board project gets an error naming the fields.
