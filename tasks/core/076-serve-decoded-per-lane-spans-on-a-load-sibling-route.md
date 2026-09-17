# 076 — Serve decoded per-lane spans on a sibling route to `/load`

**State:** open
**Source:** `tasks/core/075` (`embarch-core` decision 64, `embarch-core/decisions/stream-index.md`)
decided this should ship, and filed the building as this task rather than doing it itself
(decision 64 is a decision, not an implementation).
**Scope:** core
**Hardware:** none.
**Owner:** no

## What

`GET /study/{id}/stream/{name}/load` (decision 62) serves only the reduced `LoadSummary`.
`outpost_load.rs` already builds the full timeline underneath it — `Lane`/`Span`/`Gap`, after row
decode, `dut_clock_health`, `stale_prefix_end` and the axis-tier choice — and then discards it once
`summarize` reduces it. `embarch-ui/src/trace.rs` rebuilds the identical timeline itself, because
nothing serves it. Add a sibling route (name and exact response shape are this task's call, e.g.
`/study/{id}/stream/{name}/load/spans`) that serves the decoded per-lane spans directly: make
`Lane`, `Span` and `Gap` (or a purpose-built wire type built from them) `Serialize`, wire a handler
in `study.rs` beside `stream_load_handler`, and document it in `embarch-core/interfaces/studies.md`
and `spec.md`.

**This is a wire-schema bump.** Per `../../embarch-fleet/ops.md` §4, the supervisor announces it
before it lands — do not skip that because the shape feels additive.

**Announced by leg 137, 2026-09-17 13:29 — `ts` `1789673384.645649`** in `#embarch-fleet`. The
window opened at that post and closes 30 minutes later; this task may be dispatched after it closes
if no objection arrived. **If leg 137 ends before the window closes, this task goes back to `open`
with this `ts` in place and the next leg completes the window rather than restarting the clock**
(`ops.md` §4: the relay must not restart it every twenty minutes). A reply saying go runs it
immediately; a reply saying cancel drops it to `open` with the reply quoted here.

## Why now

`embarch-core` decision 64 decided to serve this rather than decline, reasoning that suite decision
4's own bought property — "exactly one implementation of that timeline exists in the suite" — is not
actually true while only the aggregate is shared. `embarch-ui` decision 27 records the split staying
open until this lands.

## Done when

- [ ] The new route serves decoded per-lane spans over HTTP, reusing `outpost_load.rs`'s existing
      decode rather than writing a second one.
- [ ] `embarch-core/interfaces/studies.md` and `spec.md` document the new route.
- [ ] `embarch-core/decisions/stream-index.md` gets the implementation decision (numbered), citing
      decision 64.
- [ ] A follow-up `embarch-ui` task (filed via `inbox/`, since it is outside this task's own repo)
      retires `trace.rs`'s row-decode/clock-health/stale-prefix/lane-building in favor of consuming
      this route. Not this task to file from scratch if `tasks/core/075` already dropped it —
      check `inbox/` and the `embarch-ui` queue first.
- [ ] Gate green per `../../embarch-fleet/protocol.md` §10.
- [ ] `changelog.d/` fragment. `status.d/` fragment if this makes any suite-level doc's description
      of `/load` stale.

## Measure the CSV before you quote decision 64's size argument — leg 136, from `core/075`'s reviewer

Decision 64 argues this route is **not a new category of transfer** because decision 18 measured a
reference capture's decoded spans at **12.6 MB serialized**, *"the same order of magnitude as the CSV
that already crosses this same call today."* The 12.6 MB half is quoted correctly from decision 18
(225,627 rows / 112,804 spans / 26 lanes, measured 2026-09-04). **The other half is not sourced.**
`core/075`'s reviewer grepped `embarch-core`, `embarch-ui` and the `suite/` tree at the merge SHA and
found **no document anywhere stating the rendered CSV's byte size** — so "same order of magnitude" is
an assumption, not a comparison anyone has made.

It is not a contradiction of anything locked, which is why no finding was filed and decision 64 was
not amended. But it is **the one number this task's whole cost argument rests on**, so: measure the
rendered CSV for that same reference capture, state it with its provenance, and **either cite it in
the implementation decision or say plainly that the comparison did not hold.** If the CSV turns out
to be materially smaller than 12.6 MB, that is a reason to revisit the response shape — streaming,
per-lane paging, or a narrower payload — before shipping, not after.

## Not yours

- Do not change `embarch-ui` — file its retirement task, do not do the retirement here.
