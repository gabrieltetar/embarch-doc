**Target:** `embarch-ui/decisions/debug-tab.md` decision 7 — "Core gains a live-tail SSE route
**and** a recent-lines route" (out of scope for this unit to edit directly: `embarch-ui`'s
decisions are that sub-project's own doc, and this worker's scope is `core`)
**Was:** decision 7 describes Core as having built a live-tail SSE route (`GET /logs/stream`)
alongside the recent-lines route.
**Now:** `GET /logs/stream` is retired (`tasks/core/021`) — no caller anywhere in the suite ever
used it, and the same file's own decision 13 structurally excludes an SSE source for this data by
sharing one poll/diff loop across both log sources. Only the recent-lines route (`/logs/recent`)
remains. Decision 7's historical account of what was built stands as history; whoever next reads
it should know the SSE half no longer exists.

Not a suite-level doc per `status.d/README.md`'s literal five-file list, but the sub-project doc
this fact makes stale sits in a repo this worker may not edit (scope: core only) — filed here per
the task's own dispatch note rather than left only in this worker's final report.
