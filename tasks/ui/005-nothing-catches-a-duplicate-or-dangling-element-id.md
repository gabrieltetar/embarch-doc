# Add a static guard that every `getElementById` target exists and no element id is defined twice

**State:** done — branch `agent/ui/005-element-id-guard`, 2026-09-07.
**Source:** `embarch-ui/decisions/trace-chart.md` decision 10 — the defect this would have caught, which shipped
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

A Rust test over the two `include_str!`-embedded assets asserts that **no id is declared twice**
across `assets/index.html` and the markup `assets/app.js` emits, and that **every id `app.js` looks
up is declared somewhere**. The surface is 142 ids in `index.html` and 42 `getElementById` sites
plus the `sdEl`/`trEl` wrappers.

This finds no live defect today — it is a regression guard, and it should be filed as one. What
earns it is the defect it would have caught: decision 10 records that "The Load button and the load
table's body carried **the same element id**, so every summary row had been rendering into the
button: the table had never once displayed, and its Rust tests all passed."

## Why now

`spec.md`'s Verification technique section says "tested in Rust, never looked at" is how this UI's
worst defects hid, and decisions 10, 17 and 18 each record one found only by rendering. This is the
one shape of that class a Rust test *can* catch.

## Done when

- [x] The test parses both assets and fails on a duplicate id and on a dangling lookup.
- [x] It is shown to fail when a duplicate id is introduced deliberately (revert, confirm, restore).
      Renamed `stat-enrolled-count`'s `id` to the already-used `stat-probes-count` in
      `assets/index.html`; both new tests failed:
      `no_element_id_is_declared_twice`: `` duplicate element id(s) across index.html and the
      markup app.js emits:\n`stat-probes-count` declared 2 times ``.
      `every_looked_up_element_id_is_declared_somewhere`: `` dangling element id lookup(s):\n
      `stat-enrolled-count` looked up via getElementById("stat-enrolled-count") but declared
      nowhere in index.html or app.js's own emitted markup ``.
      Reverted; `git diff --stat assets/index.html` empty and both tests pass again.
- [x] It passes on the tree as it stands.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10): `cargo build`, `cargo test` (103 passed,
      2 ignored, pre-existing/unrelated), `cargo clippy --all-targets -- -D warnings`,
      `check-ownership.py --scope ui` (both worktrees), `check-docs.py` (10/10) all green.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
      `spec.md`'s Verification technique section gained a third bullet naming the guard.
      `decisions.md`'s index row for `decisions/wiring.md` now lists decision 24.
      `decisions/wiring.md` gained decision 24 (the guard itself), citing
      `decisions/trace-chart.md` decision 10 by link rather than editing that file (590 B
      left, compaction filed under `tasks/ui/019-...`).
      `open.md`: nothing there was about this; no change needed.
      `changelog.d/ui-element-id-guard.added.md` dropped (138 B).
      `status.d/`: nothing suite-level changed — this is a `ui`-internal test, so no fragment.
      `features.d/`: not a user-facing capability row (a regression test, not a shipped tab/
      feature), so none written — consistent with this scope's existing rows, which are all
      user-facing.

## Doc-size reserve for `ui` — supervisor, leg 036, 2026-09-07

**`ui` is the most doc-pressured scope in the suite right now — three files in reserve, all filed,
and one of them is the file this task's own source decision lives in.** Plan around this rather
than discovering it:

- `embarch-ui/decisions/study-designer.md` — 12,064 / 12,288 B, **224 B left.** Filed under
  `tasks/ui/011-compact-ui-study-designer-decisions.md` (`open`). **Effectively full.**
- `embarch-ui/decisions/trace-chart.md` — 11,698 / 12,288 B, **590 B left.** Filed under
  `tasks/ui/019-compact-ui-trace-chart.md` (`open`). **This is where decision 10 lives** — the
  defect that earns this guard.
- `embarch-ui/spec.md` — 9,213 / 10,240 B, **1,027 B left**, filed under
  `tasks/ui/018-compact-ui-spec.md` (`open`). Just outside the floor.

**Do not put this unit's decision in `trace-chart.md`.** It is 590 bytes from its cap, its
compaction task is already filed, and a regression guard over *all* of `index.html` and `app.js`
is not a trace-chart concern anyway — it is a whole-asset verification concern. The roomy homes are
`decisions/shape.md` (3,839 B) and `decisions/wiring.md` (3,329 B); `wiring.md` is the better fit
if it is about how markup and lookups are kept in agreement. **Cite decision 10 from wherever you
land rather than moving or extending it** — this is exactly the case
`tasks/doc/022-a-decision-link-survives-a-mission-split-pointing-at-the-wrong-file.md` is about, so
write the citation as a link that will survive `ui/019` compacting that file underneath it.

`embarch-ui/decisions/trace-view.md` is 10,989 B and `gatt-capture.md` 9,952 B — neither is in
reserve, but neither is roomy. **If your work pushes any `ui` file into reserve, file
`tasks/ui/<next NNN>-compact-ui-<file>.md` in the same commit** (`tasks/README.md` has the shape).
Given three `ui` compaction tasks are already open and unpaid, a fourth is a real signal and should
say so in its `## Why now`.
