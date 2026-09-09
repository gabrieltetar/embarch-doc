# Fix the dev-bench README: it names the wrong board and links a deleted doc

**State:** claimed by leg 049, 2026-09-08
**Source:** owner's repo survey, 2026-09-06 — commit `a6d5355` fixed this breakage in `CLAUDE.md` and stopped there
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## What

`README.md:16` calls the nordic workspace "Currently inactive" and `:22` calls the ESP32-C5
"Milestone 2's actual target board" — exactly inverted from `embarch-doc/embarch-dev-bench/spec.md:19`,
"The board, as of 2026-08-31: `nrf54l15dk/nrf54l15/cpuapp` (`workspaces/nordic`)". `README.md:6` and
`:34` point at `embarch-doc/embarch-dev-bench/design.md` and `embarch-core/design.md`, files the
four-file split deleted.

The workspace list should match `spec.md`: nordic is the bench, espressif stays in the tree and
working per decision 43, native_sim is the host build. Doc links resolve to `spec.md`/`decisions.md`
(a decision number addresses the sub-project, not a file, so `decisions.md` is the correct landing
page). The enrolment fact an operator needs and cannot infer — **`link_port_interface = 2`, because
this DK's console is VCOM1** — belongs where the build instructions are.

Doc-only; no build required.

## Why now

This is the first file a new engineer opens, and it currently sends them to build and flash the
board that is *not* on the bench, over links that 404.

## Done when

- [x] No `design.md` reference remains in `README.md`.
- [x] The three workspace bullets agree with `spec.md` §1 and §2 on which board is current.
- [x] The nordic build/flash section is the primary one, and the `link_port_interface = 2` caveat
      appears with it.
- [x] Every markdown link in the file resolves against the current `embarch-doc` tree.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Closed — leg 049

Doc side was a genuine no-op, as the supervisor notes predicted: `spec.md`/
`decisions.md`/`open.md` needed no edits (nothing in them referenced the
README, and none of them were made false by this fix). Dropped a
`changelog.d/` fragment only; no `status.d/` fragment owed.

`README.md` rewritten: workspace bullets now match `spec.md` (nordic current,
citing decision 43; espressif superseded but working, same citation);
`link_port_interface = 2` moved into the nordic build section with its
rationale; all `design.md`/"design doc" references replaced with links to
`spec.md`/`decisions.md` (this repo's and `embarch-core`'s); the espressif
section's citation of "decision 13" (which no longer means what the README
claimed — `embarch-core` decision 13 is now about `core_version`, unrelated)
was dropped rather than left pointing at the wrong topic, keeping only
decision 18 (which does match — `Format::Bin` at the merge address). Also
found and removed a second stale claim in the same espressif section: an
instruction to set `EMBARCH_DEV_BENCH_PORT`, which `embarch-core` decision 23
says was removed with no replacement env knob (confirmed by a repo-wide grep
for the name in `embarch-core`'s own `.rs` sources — zero hits). Did not
invent a replacement instruction, since that would mean inferring an
enrollment fact not actually stated anywhere; filed
`inbox/core-readme-stale-dev-bench-env-overrides.md` instead, since
`embarch-core`'s own README still documents all four removed env vars and
that fix is outside this task's repo.

Every link resolved by hand (existing files/anchors checked directly, not by
filename pattern) — no `decisions/ble.md` edit was made or needed.

## Supervisor notes — leg 049

**A doc-side no-op is the correct result here, and you should expect it.** `spec.md` §1/§2 are
already right — they are the *source* this README is being corrected against. So do not manufacture
doc churn to satisfy the last Done-when box: drop a `changelog.d/` fragment, and touch
`spec.md`/`decisions.md`/`open.md` only if you find something in them that this work actually made
false. Say plainly in your report that the doc side was a no-op if it was. A `status.d/` fragment
is very unlikely to be owed.

**Doc-size reserve for `dev-bench`, and one of these is the tightest file in the suite:**

- `embarch-dev-bench/decisions/ble.md` — 12282/12288 B, **6 bytes left**
- `embarch-dev-bench/open.md` — 4782/5120 B, 338 bytes left
- `embarch-dev-bench/spec.md` — 9460/10240 B, 780 bytes left

All three are already filed against `tasks/dev-bench/012-compact-dev-bench.md`, which is `open` —
so the debt is recorded and you do not need to file it again. **You almost certainly should not be
writing into `decisions/ble.md` at all for a README fix.** If you find yourself about to, stop and
report it instead: six bytes is not headroom, and a decision that does not fit is a decision that
gets filed in the wrong file, which is a failure this suite has already paid for.

**Verify every link by resolving it, not by pattern.** The task's acceptance is "every markdown
link in the file resolves against the current `embarch-doc` tree". `design.md` is not the only
casualty of the four-file split — check each link, including ones that look fine. Note that a
decision number addresses the sub-project rather than a file, so `decisions.md` is the correct
landing page for a decision citation; the previous leg landed two units on exactly this class of
defect, where a citation *resolves* while pointing at the wrong file.

**`link_port_interface = 2` is a stated fact, not a measured one.** It is the owner's; it is in
`embarch-doc/embarch-dev-bench/spec.md` and in the fleet's hardware buffer. Reproduce it, do not
re-derive it, and do not infer anything further about the bench from firmware source.

**Do not touch hardware.** This is a documentation fix; there is nothing here to flash or probe.
