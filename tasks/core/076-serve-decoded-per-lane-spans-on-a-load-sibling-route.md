# 076 — Serve decoded per-lane spans on a sibling route to `/load`

**State:** done — built by agent/core/076-load-spans-route, 2026-09-17. **Announcement window
closed with no objection.** Announced in `#embarch-fleet` at 13:29 (`ts` `1789673384.645649`), polled
at every unit boundary of leg 137, nothing in the thread and nothing in the channel; 30 minutes
elapsed, so `ops.md` §4's condition to execute is met and this runs as the leg's last unit.
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

- [x] The new route serves decoded per-lane spans over HTTP, reusing `outpost_load.rs`'s existing
      decode rather than writing a second one. `GET /study/{id}/stream/{name}/load/spans`,
      `study::stream_load_spans_handler`, `outpost_load::spans_answer` — reuses the same
      `decode_with_cap` that `load_answer` reduces to `LoadSummary`; `spans_answer` reduces the
      identical `Decoded` to `SpansAnswer` with no second decode.
- [x] `embarch-core/interfaces/studies.md` and `spec.md` document the new route.
- [x] `embarch-core/decisions/stream-index.md` gets the implementation decision (numbered), citing
      decision 64. Filed as decision 65.
- [x] A follow-up `embarch-ui` task (filed via `inbox/`, since it is outside this task's own repo)
      retires `trace.rs`'s row-decode/clock-health/stale-prefix/lane-building in favor of consuming
      this route. Not this task to file from scratch if `tasks/core/075` already dropped it —
      check `inbox/` and the `embarch-ui` queue first. Already filed and `blocked` as
      `tasks/ui/065`; left untouched per the supervisor notes below.
- [x] Gate green per `../../embarch-fleet/protocol.md` §10.
- [x] `changelog.d/` fragment. `status.d/` fragment if this makes any suite-level doc's description
      of `/load` stale. `/load` itself is unchanged and no suite-level doc's description of it went
      stale, so no `status.d/` fragment was needed.

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

**Resolved (this task, 2026-09-17).** The exact reference capture no longer exists to re-measure
(confirmed again: not checked in anywhere, and `embarch-ui`'s `EMBARCH_VIEW_CSV` scratch test reads an
arbitrary local path). Measured instead against `embarch-core`'s own checked-in real-firmware fixture
— 43,573 B / 831 rows, 52.367 B/row — and extrapolated linearly to the reference shape's 225,627 rows:
**≈ 11.8 MB, a likely-low estimate** (this fixture's `rx_utc_ms` column is empty throughout, which
understates a populated capture's row width). **The comparison holds**: same order of magnitude as
12.6 MB, not materially smaller. No response-shape change follows. Full writeup: decision 65,
`embarch-core/decisions/stream-index.md`.

## Not yours

- Do not change `embarch-ui` — file its retirement task, do not do the retirement here.
- **Do not change `embarch-topology`.**
- **Do not bump any existing route's response shape.** This is additive: `GET
  /study/{id}/stream/{name}/load` keeps serving exactly the `LoadSummary` it serves today. If you
  find yourself needing to change `LoadSummary`, stop and say so — that is a different announcement.

## Supervisor notes (leg 137, 2026-09-17)

1. **The announcement is done and the window is closed.** Announced 13:29, `ts`
   `1789673384.645649`, no reply in 30 minutes. You do not announce anything and you do not wait.
2. **Reserve, read at dispatch, and it moved twice today — check it fresh, do not trust this line.**
   `embarch-core/decisions/auth.md` **11,356/12,288 B**, blocked under `tasks/core/046`; and
   **`decisions/surfaces.md` went into the band an hour ago at 11,253/12,288 B (91.6%, 1,035 B
   left)**, filed as `tasks/core/079-compact-core.md`, `blocked`, `In flux: yes`. **Write into
   neither.** `decisions/stream-index.md` is where this task's decision belongs and it has room.
   Run `python3 scripts/check-doc-size.py --pressure` before and after; if your edits push a third
   file into the band, file `tasks/core/<NNN>-compact-core.md` in the same commit — **and check the
   next free number against `main` right before you write it**, because this leg already had one
   number collision between a worker and the supervisor's own refill.
3. **Measure the CSV before you quote decision 64's size argument.** The task's own section on this
   is the most important thing in it. Decision 64's cost argument rests on the decoded spans being
   *"the same order of magnitude as the CSV that already crosses this same call"*, and the 12.6 MB
   half is sourced while **the CSV half is not** — `core/075`'s reviewer grepped the whole suite and
   found no document stating the rendered CSV's byte size. Measure it, state it with its provenance,
   and **if the CSV turns out materially smaller than 12.6 MB, say so and reconsider the response
   shape before shipping** — streaming, per-lane paging, or a narrower payload. That is a legitimate
   outcome of this task, not a failure of it.
4. **Reuse `outpost_load.rs`'s decode; do not write a second one.** Building a parallel timeline is
   the exact duplication this whole chain exists to end.
5. **`tasks/ui/065` is already filed and `blocked` on this task landing** — do not file it again and
   do not unpark it; that is the supervisor's call at the fold.
6. You own exactly one sub-project: `embarch-core`.
