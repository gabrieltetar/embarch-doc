# 062 — Two `embarch-core` comments say `embarch-ui`'s text is unchanged, and `ui/052` changed it

**State:** open
**Source:** `ui/052`'s worker, filed mid-task as an `inbox/` drop, 2026-09-13; filed here by leg 114
in `ui/052`'s own fold. `ui/052` fixed `embarch-ui`'s stale retention sentence; this is the other
side its `Done when` list required checking rather than editing (`embarch-core` is not `ui/052`'s
scope). The body below is the worker's own text.
**Scope:** core
**Hardware:** none — comment text only. No board, no probe, no live Core, no deploy.
**Owner:** no

## What

`core/058` edited two `embarch-core` comments that had asserted a correction to `embarch-ui`
decision 7 existed when it did not:

- `src/main.rs`'s `build_log_file_writer` (or its surrounding comment — worker should re-locate by
  the text below, `core/058`'s own diff has the exact lines)
- `src/logs.rs`'s module doc, which after `core/058`'s fix reads: *"Reuses the existing
  daily-rolling logfile (`main.rs`'s `init_tracing`, decision 16) rather than introducing a second,
  size-capped log mechanism — `embarch-ui` decision 7 describes a size-capped rotating logfile,
  written before this session noticed Core already had a real, tested, daily-rotating one (7-file
  retention). This crate builds no second mechanism to match that description (see this crate's own
  decisions for the full account); `embarch-ui`'s own text is unchanged."*

That last clause — **"`embarch-ui`'s own text is unchanged"** — is no longer true. `ui/052` added a
dated blockquote correction directly under decision 7's stale sentence in
`embarch-doc/embarch-ui/decisions/debug-tab.md`, explaining that the size-capped mechanism was a
proposal, never built, and that Core's real logfile (decision 16, daily-rolling, `max_log_files(7)`)
is what `/logs/recent` actually serves. The sentence itself was **not** rewritten to say
"daily-rolling" — it stands as the record of what was proposed — but it is no longer bare and
unqualified.

## Why now

`src/logs.rs`'s comment was written to be accurate as of `core/058`'s landing. `ui/052` changed the
fact it was describing. Whether the comment still reads correctly is a judgement call for whoever
owns `embarch-core`'s source: the substance (Core builds no second, size-capped mechanism) is still
true, but "`embarch-ui`'s own text is unchanged" is now stale in the other direction from what
`core/058` was originally fixing.

## Done when

- [ ] `src/logs.rs`'s module doc and `src/main.rs`'s comment re-read against the corrected
      `embarch-ui/decisions/debug-tab.md` (post-`ui/052`) and updated if the "unchanged" clause (or
      anything else in either comment) no longer holds.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment if anything changes.

## Watch for

- **The substance may well still hold** — Core really does build no second, size-capped mechanism, and
  `ui/052` deliberately left decision 7's sentence standing as the record of an abandoned proposal
  rather than rewriting it. Read the corrected `embarch-ui/decisions/debug-tab.md` first and decide
  whether the clause is stale or merely imprecise; changing nothing is a legitimate outcome, recorded
  in your report.
- **`embarch-ui` is not your scope.** If the right fix turns out to be on that side, it is an `inbox/`
  drop, not an edit.
