# 012 — `embarch-ui/spec.md` says the UI reaches Core over `GET /logs/stream`; it does not

**State:** done, agent/ui/012-spec-names-the-real-log-path, 2026-09-06
**Source:** core/006 worker, 2026-09-06 — found while surveying `/logs/stream`'s consumers
**Scope:** ui
**Hardware:** none
**Owner:** no

**Filed by the supervisor, leg 025**, from an `inbox/` drop the `core/006` worker wrote into
**its own doc worktree** rather than the main checkout. That worktree is deleted at cleanup, so
the drop existed for about twenty minutes and nowhere else. `Hardware:` re-checked: `none` —
this is a doc correction against sources already read.

## What

`embarch-ui/spec.md:32` lists, under "HTTP + Bearer --> embarch-core", the line
`GET /logs/stream (SSE live tail) · GET /logs/recent (backfill)`.

Only the second half is true. `embarch-ui/src/logs.rs`'s `poll_loop` calls
`core.logs_recent(POLL_TAIL)` on a 2 s interval and republishes the diff over a
`watch` channel; `sse_lines` then relays that as the UI's *own* `lines` SSE
event to the browser. `embarch-core-client` (`client.rs:1163`) has `logs_recent`
and no `/logs/stream` method at all — a grep of the whole suite finds no caller
of Core's `/logs/stream` anywhere outside `embarch-core` itself.

So the UI's live tail is a server-side poll of `/logs/recent`, not an SSE
subscription to Core, and the spec line reads as though Core's SSE stream is a
dependency the UI holds. A later reader deciding whether `/logs/stream` may
change (or go) will conclude it has a consumer when it has none.

Not fixed here: this is `embarch-ui`'s doc and a `core` worker may not edit it.
`embarch-core`'s own decision 44 records the same finding from Core's side.

## Reserve (supervisor, leg 026 — measured at dispatch)

`embarch-ui/spec.md` is **7,653 / 10,240 B (74.7%)**, comfortably out of reserve — the file you are
fixing has room. Two `embarch-ui` decisions files are in reserve and **neither is where this work
goes**: `decisions/study-designer.md` 11,164 / 12,288 (90.9%, filed as `tasks/ui/011`, `open`) and
`decisions/trace-view.md` 11,080 / 12,288 (90.2%, filed as `tasks/ui/009`, `blocked`).
`decisions/debug-tab.md` is 4,828 and is the obvious home if this warrants a numbered decision at
all — **and it probably does not**: correcting a spec line to match shipped code records no choice.
Say which you did and why. If your work pushes any file into reserve, file
`tasks/ui/<NNN>-compact-ui.md` in the same commit.

## Scope note from the supervisor — one task, but read the whole block

This is a small edit and the temptation is to change exactly one line. **Do read the entire
architecture block in `embarch-ui/spec.md` before you edit it.** One wrong dependency arrow in a
block that nothing checks is evidence about that block, not just about that line: `check-links.py`
sees a link that resolves, `check-staleness.py` only fires on a row that *disagrees* with a
sub-project doc, and nothing at all compares a stated HTTP dependency against the code that would
make the call. If another arrow in that block is also unsupported, fix it in the same unit and say
so; if they all hold, say that too — a checked "the rest is right" is worth more than silence. This
stays inside `embarch-ui/spec.md`, so it is one task in one sub-project.

**Do not widen into `embarch-core`.** `/logs/stream` still exists and `embarch-core` decision 44
deliberately keeps it; this task is about what the UI's spec *claims*, not about retiring anything.

## Why now

`embarch-core` decision 44 (landed by core/006) turns on `/logs/stream` having
no consumer today. That reasoning and this spec line contradict each other, and
whichever is read first wins.

## Done when

- [x] `embarch-ui/spec.md`'s architecture block describes how the Debug tab
      actually reaches Core (poll of `/logs/recent`), or the code changes to
      match the spec and the spec says which.
- [x] Gate green.

## Done — what was found and changed

Doc-only. `embarch-ui`'s code is right and unchanged (`git diff --stat` against
`origin/main` in the code worktree is empty); the spec was wrong.

**Confirmed in the code first**, as dispatched. `src/logs.rs::poll_loop` calls
`core.logs_recent(POLL_TAIL)` with `POLL_TAIL = 500` every `POLL_INTERVAL = 2 s`,
diffs the window in `diff_new_lines` and publishes only genuinely new lines over a
`tokio::sync::watch`; `main.rs::sse_lines` relays that outward as this UI's own
`lines` SSE event on `/api/logs/events`. A failed poll is `tracing::debug!` and the
next tick retries — it is not surfaced to the browser. `embarch-core-client`'s
`logs_recent` (`client.rs:1163`) builds `{base}/logs/recent` and is the crate's only
`/logs` method; there is no `/logs/stream` client anywhere in this repo's tree.

**The distinction the corrected text keeps:** the UI *serves* SSE to the browser and
does *not* consume Core's. The Debug tab does have a live tail; it is a server-side
poll, not a subscription.

**Not widened into `embarch-core`.** Nothing here says `/logs/stream` is unused or
should go — `embarch-core` decision 44 keeps it deliberately. The recorded fact is
only that *this* repo does not call it.

### The rest of the architecture block, checked

Every other arrow was verified against the code, not assumed.

- **Every endpoint listed is real and reached**, verb included: `POST /probes/enroll`
  (`main.rs:328`), `POST`/`GET`/`DELETE /signals`, `GET /serial-ports`,
  `/probes/enrolled`, `/alerts`, `/status`, `/dev-bench/port`, `/dev-bench/hello`,
  `POST /study`, `GET /study/{id}`, `/steps`, `/streams`, `/stream/{name}`. All
  seventeen `CoreClient` methods the UI calls map onto a listed line — with one gap.
- **One omission fixed:** `core.get_study_gatt_data` (`study_designer.rs:1737`) hits
  `GET /study/{id}/gatt-data`, which the list did not carry although the list claims
  to be "every hardware-adjacent call". Added.
- **One further unsupported claim fixed:** `+-- does NOT link embarch-topology, at
  all, deliberately` is false as written. `cargo tree -e normal -i embarch-topology`
  shows `embarch-topology -> embarch-core-client -> embarch-ui`, features
  `default,software` [measured 2026-09-06]. What is true is what this sub-project's
  own `decisions/wiring.md` already says — never the **`hardware`** feature — and the
  Invariants section's `probe-rs`/`serialport` test is the accurate measurement of it
  (both count 0 in the normal tree, re-measured). The spec had dropped its own
  decision's qualifier; the prose paragraph below the block had the same overstatement
  and was corrected with it.
- **"there is no client-side interval polling anywhere" holds:** no `setInterval` in
  `assets/app.js`; the three `EventSource` consumers all point at this binary's own
  routes. Qualified anyway, so a reader does not read it as "nothing polls" now that
  the block states a server-side poll two paragraphs up.
- The tabs table's **Debug** row was widened to name both mechanisms and say which
  direction the SSE runs.

### No numbered decision

None written, and the Reserve section's guess was right: correcting a spec line to
match shipped code records no choice. The `embarch-topology` half needs one even less
— `decisions/wiring.md` already states the accurate form, so the spec was
contradicting its own decisions file rather than missing an entry. Nothing was added
to `decisions/debug-tab.md`, and neither file in reserve (`study-designer.md`,
`trace-view.md`) was touched.

`embarch-ui/spec.md` 7,653 -> 8,866 B (86.6% of 10,240) — out of reserve, no
compaction task filed. `check-doc-size.py`: 10 in reserve suite-wide, all already
filed.

### Gate

`cargo build`, `cargo test` (99 passed / 2 ignored / 0 failed — identical to base),
`cargo clippy --all-targets -- -D warnings` clean. `embarch-ui` has exactly one
`Cargo.toml`, so there is no unlinted nested crate under the root gate.
`scripts/check-docs.py`: all 10 checks green. `check-client-names.py --repo` clean.
`check-ownership.py` clean on both sides.

### No hardware debt

Nothing here is verifiable only on a board — it is a claim about this repo's own
source, checked against that source.
