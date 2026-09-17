# ui: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- Measured the trace handler's in-process request cost (decode + JSON encode) at 250k/500k/1M rows; Core-fetch portion still unmeasured — `embarch-ui/open.md`.
- `tests/element_ids.rs` fails on a duplicate or dangling element id in index.html/app.js — `embarch-ui/decisions/wiring.md` decision 24.
- The Trace view drops a stale pre-reset leading prefix and keeps the DUT clock for the rest, in place of refusing that clock for the whole capture. embarch-ui decision 19.
- The Trace view asks for the window it draws, binned server-side, not a 13 MB capture: [decision 18](../embarch-ui/decisions.md).

### Changed
- Decision 25 (shell.md) compacted from 4,307 B to 3,758 B, under the 4,096 B per-decision cap; the 1.12:1 measurement survives.
- `embarch-ui/open.md` squeezed back out of reserve, 4,033 → 3,879 B; every trigger and citation kept.
- embarch-ui now fetches the Trace tab load repartition from embarch-core (GET .../load) instead of recomputing it locally (suite decision 4).
- `embarch-ui/open.md` compacted (squeeze, not split): 4,341 -> 3,841 B, out of reserve.
- Decisions 19, 21 split verbatim off decisions/trace-view.md into decisions/trace-rows.md; decision 10 stays put.
- The run dialog's "no reflashing here" wording is now verified against the shipped string, not assumed: [open.md](../embarch-ui/open.md).
- `open.md` reshaped: the 250,000-row bullet is now a measurement table, out of size reserve.
- `topology-tab.md` decision 10 compacted 4430→4034 B, cutting cold provenance/investigation prose; under the 4,096 B cap.
- Enrolled-boards tables label `confirmed_at_utc_ms` "Enrolled", never "Confirmed"/"Validated" — that field can't answer freshness.
- ui: spec.md split its trace-chart reference into interfaces.md, out of reserve.
- decisions/study-designer.md trimmed clear of reserve (12,064→10,961 B); decisions.md index row now lists decision 22.
- Decision 23 (outcome decoder) split verbatim from `decisions/trace-chart.md` into `decisions/outcome-decode.md`, clearing its reserve.
- embarch-ui compacted to spec/decisions/open, 92 KB to 68 KB across 12 files; design.md deleted.

### Fixed
- Decision 13 bullet 3's 'append-only' and bullet 4's 'only' restored (4,079 B -> 4,096 B); the interleaving phrase still does not fit.
- Decision 13's growing-trailing-line claim is now conditional, not universal; decision 25's restored vertex count now matches its own file (693 B, 53 vertices).
- embarch-ui/decisions/debug-tab.md#13 documents diff_new_lines's fallback for a trailing log line that mutates between polls.
- embarch-ui/decisions/shell.md#25 states its E/A vertex counts again, restoring what history/ui.md:38 cites.
- Decision 7's retention line described a size-capped logfile that was never built; Core's is daily-rolling.
- `study_designer.rs`'s 74 decision citations checked; two bare decision-40 citations given the `embarch-study-designer` prefix.
- `trace.rs`'s `Lane::unnamed` comment cited a nonexistent decision 35; now a plain, verified statement.
- `assets/app.js`'s `delay_before_ms` comments cite decision 42, not 40; `decisions/surfaces.md` pointer fixed to `enrollment.md`.
- Four stale pointers fixed: trace-view.md's marker count now names the fixture it measured; shell.md's three style.css line citations re-derived.
- Twenty-two source comments now cite `embarch-study-designer`/`embarch-core` decisions by repo, not bare numbers.
- `Cargo.toml` comments repointed off nonexistent `design.md` files to real spec/decisions.
- Fixed: `embarch-ui` comments citing the nonexistent `milestone-1.md` repointed at real decisions or dropped.
- `embarch-ui` source comments repointed off a pre-split `design.md` to `decisions.md`/topic files.
- Run dialog and trace-tab notes now cite `decisions.md`, not the pre-split `design.md` that never existed here.
- Decision 25's E vertex count was 16 (a non-union trace); corrected to 22, and a dead `.sd-param-value` opt-out removed.
- Fixed: decision 25's `--brand` count (two declarations, two call sites, not three); see `decisions/shell.md`.
- The Enroll tab's assign modal now uses `.dialog`/`.dialog-backdrop` like the other four, not an inline reimplementation.
- `snapshot.rs`/`app.js`'s "decision 54" cites now say 57, matching `core/039`'s renumbering; `study_designer.rs`'s own decision 54 is unrelated and untouched.
- Fixed stale `embarch-ui` src comments: `study_designer` config doc names decision 14's real behaviour, `logs.rs` says `GET`, dead `milestone-*.md` pointers replaced with live docs.
- embarch-ui/Cargo.toml's comment overstated decision 5: it never links embarch-topology's `hardware` feature, but the crate is in the tree transitively.
- An unrecognised trace-band outcome now fills with `tr-cross`, not `tr-gap` — it no longer claims the firmware lost records.
- One outcome decoder in app.js handles both wire shapes; an unrecognised one now renders visibly wrong, not a pass or neutral.
- `app.js` no longer restates the row cap or the stream-name cap; both are now served fields.
- embarch-ui/spec.md: the Debug tab polls Core's /logs/recent (it never subscribes to /logs/stream), and embarch-topology is linked transitively, software-only.
- The study run badge names the step now running, not the count finished — Core's `current_step` is the index of the last step that finished (ui decision 20).
- The Trace view counts the rows its decoder refused — truncated or malformed — instead of claiming "every row in the capture": embarch-ui/decisions/trace-view.md, decision 10.

### Decided
- New decision 26: Core down is an expected, renderable state, not a crash; both stale citations repointed.
- 250,000-row view cap kept, measured at 250k/500k/1M in-memory: `open.md`.
