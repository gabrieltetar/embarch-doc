# 058 — Route `validate_known_timed`'s probe-open failure through `raise`, or accept it stays silent

**State:** done — agent/topology/058-route-probe-open-failure-through-raise, 2026-09-17
**Filed by:** leg 134, from `inbox/topology-route-probe-open-failure-through-raise.md`, written by
the `topology/056` worker while landing that unit. Filed verbatim except for the two corrections
noted below, both mine. I re-checked the `Hardware: verify-only` claim myself and it holds: the
topology-side change is reachable by a unit test, and the `embarch-core` half is explicitly deferred
to a paired task rather than needed to land this one.
**Source:** `tasks/topology/056` (the fourth of leg 133's census findings). That task fixed the two
in-repo claims that mismatched the code (`TopologyMismatch::live_hardware_id`'s doc comment, and
`validate.rs`'s module header) to describe current behavior accurately. It deliberately did **not**
change behavior — its own "Not yours" section reserved that decision for a follow-up, since the
consumer-visible half crosses into `embarch-core` and no bench was available to exercise either side.
**Scope:** topology
**Hardware:** verify-only — the topology-side code change itself needs no board (same shape as
`tasks/core/041`'s resolution: reachable by unit test, since the two paths differ only in whether
`probe_info.open()` `Ok`s or `Err`s). Confirming `embarch-core`'s `POST /validate` renders the
widened alert/error correctly is free the next time a probe is physically busy/permission-denied,
but nothing here needs a board to land.
**Owner:** no

## What

In `embarch-topology/src/hardware/validate.rs`, `validate_known_timed` only calls `raise` (which
constructs a `TopologyMismatch` and durably logs an `Alert`) for two of its failure points: the
probe missing from `Lister::list_all()` entirely, and a hardware-ID compare that fails. **The other
five** — `probe_info.open()`, `check_target_powered`, `.attach()`, `session.core(0)` and
`hardware_id::read`, all part of the same "open and read the board" sequence —
each return a bare `anyhow::Error` via `?`.

*(Correction, leg 134: the drop as written said "two of its five failure points" and then "the other
three points" before listing five. Two raise and five do not — seven in total. The `topology/056`
worker's own report and the corrected module comment it landed name the same five, so the list is
right and the two counts around it were not. Re-count them yourself before acting on the number.)* None of these is downcastable to `TopologyMismatch`, none
is durably logged to `alerts.jsonl`, and a caller like `embarch-core`'s `POST /validate` falls
through to its generic (non-mismatch) error arm for all of them.

The case most worth naming: **a probe that lists but won't open** — another process holding it, a
permission denial, a half-wedged J-Link. That's common in practice and is exactly where an operator
or an unattended supervisor most wants the structured "this needs a human" answer decision 12
describes, not a generic I/O error indistinguishable from any other failure in the suite.

## Why now

`embarch-topology` decision 20's own incident (a bench that "flashed, booted, ran, and timed out"
under a papered-over mismatch) is the standing reason this suite treats a mismatch as a safety
property, not a nicety. `tasks/core/041` already fixed the adjacent defect — Core was collapsing
"not attached" and "wrong hardware ID" under one lead — on the strength of the same reasoning. This
is the third case that incident didn't cover: not attached, wrong ID, and (unhandled) attached-but-
won't-open.

## Done when

- [x] A decision on whether `validate_known_timed`'s open/power/attach/core-select/read failures
      should route through `raise` (widening what's alertable and what `TopologyMismatch` can
      report), or a documented reason the current silent behavior is correct as-is. If routing
      through `raise`, decide what `reason`/`live_hardware_id` should say for each of the five call
      sites — they are not interchangeable (an unpowered board is a different fact than a busy
      probe).
- [x] If behavior changes: a topology decision recording why (this crate's `decisions/alerts.md`,
      alongside decision 12, or a new one — decision 12 itself is correct as written and needs no
      amendment).
- [x] **Named but explicitly out of this task's reach:** whether `embarch-core`'s `POST /validate`
      (and `flash`/`reset`/`run_study`'s dev-bench gate, all downstream of the same `TopologyMismatch`
      downcast per `tasks/core/041`) handles the widened set of alertable failures correctly, and
      whether its `kind` classification (`"not_attached"` / `"mismatch"`, `embarch-core` decision 59)
      needs a third value for "couldn't open/attach/read, but the probe is physically there." That is
      `embarch-core`'s to verify, and belongs in a paired `embarch-core` task once the topology side
      lands, the same two-repo shape `core/041`'s own resolution used.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) in `embarch-topology`; `changelog.d/`
      fragment; `spec.md`/`decisions.md` updated if behavior or a decision changes.

## Resolution

**Routed through `raise`, all five.** Re-counted `src/hardware/validate.rs`'s `validate_known_timed`
myself before acting: two failure points already called `raise` (probe absent from
`Lister::list_all()`, hardware-ID mismatch), and exactly five did not (`probe_info.open()`,
`check_target_powered`, `.attach()`, `session.core(0)`, `hardware_id::read`) — seven in total, the
corrected count, confirmed against the function body rather than the drop's original miscount.

All five now call `raise` with a distinct `reason` naming which step failed and folding in the
underlying error's own text, so nothing the old plain `anyhow::Error` would have shown an operator is
lost. `live_hardware_id` stays `None` for all five, same as the pre-existing "not attached" branch —
deliberately not widened into a new field or enum to carry more structure, since that would be a
shape change reaching every `TopologyMismatch` consumer (`embarch-core` first), which is a decision
for the consumer that would actually use it, not one to make on its behalf from this crate. That
residual ambiguity (an attached-but-stuck probe reads the same as a genuinely absent one to any
caller that only looks at `live_hardware_id.is_none()`) is the reason this task explicitly deferred
`embarch-core`'s classifier question to a paired task rather than answering it here.

**Decision 34** records this in `embarch-topology/decisions/alerts.md` (room there; decision 12 is
unchanged, per this task's own note that it needs no amendment) and `decisions.md`'s index row for
that file is updated to list it. `spec.md` was **not** touched — its "What validation asserts, and
what it cannot" section never described alerting behavior in the first place (that's
`decisions/alerts.md`'s job), so there was nothing there to correct, and touching it would have
spent the crate's last 414 B of headroom for no reason.

**`tasks/topology/057`'s unpark condition is met and I did not act on it, per this task's own
instruction to leave it alone when the unit doesn't need to write `spec.md`.** `topology/056` landed
2026-09-17 (leg 135), which is 057's own stated unpark trigger; its `**In flux:** yes` rationale
("`topology/056` is open against the same section") is no longer true. This unit did not need
`spec.md`, so per the reserve section below, `057` was left untouched rather than silently unparked.
**Supervisor: please re-state `057`'s block condition** — it should very likely move from `blocked`
back to `open` now, independent of anything this task did.

**`embarch-core`-side verification handed off via `inbox/`, not answered here and not written
directly into `tasks/core/`.** I first drafted this as a direct `tasks/core/076-...md` file, then
caught it against `protocol.md` §3's ownership table (`tasks/` — worker: "claim + close its own" —
and `check-ownership.py --scope topology` correctly flagged it as a real cross-scope write, not a
false positive) and `inbox/README.md`'s explicit instruction that a worker who finds work outside its
own task drops it in `inbox/` rather than filing the task itself. Moved it there instead:
`/home/gabriel/Github/embarch/embarch-doc/inbox/core-validate-kind-classifier-cant-tell-not-attached-from-stuck-mid-attach.md`
(absolute path, full task format minus the number, per `inbox/README.md`). It asks whether
`POST /validate`'s `kind` classifier — and `describe_topology_error`/`describe_gate_error`'s
plain-text paths — need a third value now that the "attached but stuck" case is a live, reachable
`TopologyMismatch` rather than a case that never reached that type at all (which is what let
`core/074`, its immediate predecessor, correctly treat the same gap as accepted-because-moot). The
supervisor assigns the number and files it into `tasks/core/` per that README's own "What happens to
it."

**Doc-size reserve:** `python3 scripts/check-doc-size.py --pressure` run before and after —
same 14 parked files both times. `decisions/alerts.md` moved 6,067 B → 9,151 B (12,288 B cap for a
`decisions/*.md` file, same cap class as `decisions/auth.md`/`decisions/bind.md`), well short of the
reserve band. `spec.md` unchanged at 9,826/10,240 B (still the file `057` parks). `decisions.md`
unchanged in size class, +4 B for the index-row edit.

**Hardware-verification debt:** none new. The topology-side change is exercised by the crate's
existing test suite (80 tests green under `--features hardware`, including the pre-existing
`select_probe`/`Validation` coverage in this same file) — no new test was added that calls `raise`
directly, because doing so would invoke `alert::record`, which on this machine writes to the real,
machine-wide `/var/lib/embarch/topology/alerts.jsonl` (`paths.rs` has no test-time override by
design, per `alert.rs`'s own `record_then_recent_round_trips` test comment, which avoids the same real
path for the same reason). Confirming `POST /validate` actually surfaces the widened alert set
correctly against a real stuck-probe condition is free the next time one occurs against a live Core,
per this task's own `Hardware: verify-only` line — nothing here needed a board to land.

**Gate:** `cargo build --all-targets`, `cargo clippy --all-targets -- -D warnings` and `cargo test`
green with default features and with `--features hardware` (80 tests passed, 0 failed, under
`hardware`) in the code worktree. `python3 scripts/check-docs.py` green in the doc worktree.

## Not yours (for whoever picks this up)

Do not touch `embarch-core` from this task — same boundary `topology/056` respected. If the answer
is "route through raise," file the `embarch-core`-side verification as its own task rather than
reaching across.

## Doc-size reserve for topology — read this before you plan where the decision goes

**`embarch-topology/spec.md` is at 9,826/10,240 B — 414 B left, the tightest reserve in the whole
suite right now.** It is filed against `tasks/topology/057-compact-topology.md`, which is
`blocked`. Nothing else of topology's is in reserve; `decisions/alerts.md` has room, and decision 12
lives there, so **that is where a new or amended decision belongs.** Run
`python3 scripts/check-doc-size.py --pressure` before and after.

**`tasks/topology/057`'s block condition has been met and nobody has acted on it.** Its `**State:**`
line reads *"unparks when `tasks/topology/056` lands, or is closed without touching `spec.md`"* —
and `topology/056` landed on 2026-09-17 (leg 135, doc `b3c5827` / fold `3d384c2`). Its `**In flux:**
yes` rationale is *"`tasks/topology/056` is open against the same section `055` just edited"*, which
is no longer true. So:

- **If your unit does not need to write `spec.md`, do not.** Put the decision in
  `decisions/alerts.md` and leave 057 alone; say in your report that its unpark condition is met so
  the supervisor can re-state it.
- **If your unit does write `spec.md` and would push it past 10,240 B, compact `spec.md` as part of
  this unit** (`.claude/leg.md`: a blocked compaction task parks the pass, not the reserve). Carry
  `057`'s `**Must not delete:**` list verbatim — the three qualifiers `topology/055` added, each of
  which exists to stop a reader relying on a guarantee the code does not provide — and close `057`'s
  single `Compacts:` item if you pay it. Do not shorten any of those three back into the flat claim.
- Either way **do not silently unpark `057` and leave it `open` unpaid**; say what you did.
