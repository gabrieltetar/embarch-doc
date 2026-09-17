# 056 — `validate`'s probe-open failure raises neither a `TopologyMismatch` nor an alert, and the type's own doc comment says it does

**State:** done — agent/topology/056-probe-open-no-mismatch, 2026-09-17
**Source:** leg 133's refill census of `embarch-topology`, the fourth of four findings —
`tasks/topology/055` carries the other three. **Filed so it survives**: it existed only in a census
report, and `supervisor-log.md` folds daily and rolls into `log-archive/`.
**Scope:** topology
**Hardware:** none. Settled by reading every branch of `validate_known_timed`. **Do not attach a
probe and do not run `validate` against a live machine** — the point is which branches construct a
`TopologyMismatch`, not an observation of one.
**Owner:** no

**Doc-size reserve for `topology`:** nothing of topology's is in reserve. Check
`python3 scripts/check-doc-size.py --pressure` before and after.

**Every coordinate below came from a census pass.** Re-derive each line you act on and correct the
record in your report where it has drifted. **"This does not hold" is a correct outcome.**

## What

Two in-repo claims:

`src/hardware/validate.rs` (reported 128), the doc comment on `TopologyMismatch::live_hardware_id`:

> *"`None` when the enrolled probe couldn't even be opened (unplugged, most likely) — a mismatch
> either way, just not one with a live hardware ID to show."*

And the module header (reported 11–14): *"Fails closed in every branch … Every mismatch is durably
logged (`alert.rs`) before the structured error is even constructed."* `decisions/alerts.md` 12 leans
on the second: *"a row in the alert log is proof the caller received the refusal."*

**`validate_known_timed` (reported 214–248) routes only two paths through `raise`** (reported ~148,
the function that records the alert and builds `TopologyMismatch`): the probe not appearing in
`Lister::list_all()` at all (reported 221–232, *"is not currently attached"*), and the hardware-ID
compare failing (reported 250–259). The actual **open** is a plain `anyhow` error (reported 234–236):

```rust
let mut probe = probe_info
    .open()
    .context("failed to open the enrolled probe for the board-identity gate")?;
```

The same is reported for `check_target_powered` (237–238), `attach` (239–241), `session.core(0)`
(242–243) and `hardware_id::read` (244). **None raises, none logs an alert, none is downcastable.**

## Why it costs something

**The one case the doc comment names as producing `live_hardware_id: None` is the case that cannot
produce a `TopologyMismatch` at all.** A probe that lists but will not open is common in practice —
another process holding it, a permission denial, a half-wedged J-Link — and it is exactly where a
consumer most wants the structured answer. A caller downcasting to `TopologyMismatch` gets nothing,
so `embarch-core`'s `POST /validate` falls through to its generic arm rather than the mismatch shape,
and **no row lands in `alerts.jsonl`** — so *"the log is evidence the gate ran end to end"* has a
hole precisely where the gate fails for a non-identity reason. Anyone auditing the alert log for
*"every time the gate refused an operation"* undercounts.

**Note the asymmetry, because it decides how much you may claim.** Decision 12's stated claim is
one-directional — a logged row implies a returned refusal — and **that direction does hold.** What
fails is the doc comment at line 128 and the module header's *"every mismatch"*. Do not write that
decision 12 is wrong; it is the two in-repo sentences that overstate.

## Done when

- [x] The two in-repo claims are each **corrected** or **reported as holding**, on lines you read —
      `validate.rs`'s `live_hardware_id` doc comment, and the module header's *"every mismatch is
      durably logged"*.
- [x] Your report states explicitly whether you changed prose only, or whether you concluded the
      code should route the open failure through `raise`. **If the latter, do not implement it** —
      see "Not yours".
- [x] Your report says which of the reported line numbers had drifted.
- [x] A `changelog.d/` fragment.
- [x] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
      in `embarch-topology`, and `python3 scripts/check-docs.py` in `embarch-doc`.

## Resolution

**Prose only — the code was not touched.** Both claims held as findings, both corrected as prose.
Verified every branch of `validate_known_timed` (`src/hardware/validate.rs`): exactly two call
`raise` — probe absent from `Lister::list_all()` (`live_hardware_id: None`), and a hardware-ID
compare that fails (`live_hardware_id: Some(...)`) — and five do not: `.open()`, `check_target_powered`,
`.attach()`, `session.core(0)`, `hardware_id::read`, each surfacing a bare `anyhow::Error` via `?`
that is un-logged and not downcastable to `TopologyMismatch`.

**`live_hardware_id`'s doc comment** (`validate.rs:128-130`) named the wrong case: it said `None`
means "the enrolled probe couldn't even be opened (unplugged, most likely)". That prose is what
actually misled a prior worker — `tasks/core/041`'s resolution paraphrases the same field the same
way ("`None` exactly when nothing was compared (the probe couldn't be opened)") to describe the
*not-attached* arm, which is the only arm that is actually correct. The literal "probe is listed but
`.open()` itself fails" case is a third, distinct outcome neither comment names, and it produces
neither `None` via `raise` nor anything else — it never reaches `TopologyMismatch` at all. Corrected
the comment to say `None` means "not found in `Lister::list_all()`" and to explicitly carve out the
open-failure case as un-logged and non-downcastable.

**The module header** (`validate.rs:11-17`, reported 11-14) claimed "every mismatch is durably
logged... before the structured error is even constructed." Narrowed to "every *constructed*
`TopologyMismatch` is durably logged" (decision 12's actual, one-directional claim, which holds) and
added the same carve-out: the open/power/attach/core-select/read failures fail closed — the
operation is still blocked — but construct no `TopologyMismatch` and log no alert.

**Did not conclude the code should change.** Routing the open failure through `raise` would widen
`alerts.jsonl` and change what `embarch-core`'s `/validate` returns on that path, across the repo
boundary this task's "Not yours" section reserves, with no bench here to exercise `embarch-core`'s
side. Left as a finding for `embarch-doc/inbox/` and a follow-up task per the task's own instruction,
rather than implemented.

**Line-number drift against the census:**
- Module header claims: reported 11-14, actual paragraph spans 11-17; the two cited sentences are
  at 11 and 12-13 respectively — no material drift.
- `live_hardware_id` doc comment: reported 128, actual 128-130 (field itself at 131) — no drift.
- `raise`: reported ~148, actual exactly 148 — no drift.
- Probe-not-listed branch: reported 221-232, actual match arm 221-232 — no drift.
- `.open()` failure: reported 234-236, actual 234-236 — no drift.
- `check_target_powered`: reported 237-238, actual 237-238 — no drift.
- `.attach()`: reported 239-241, actual 239-241 — no drift.
- `session.core(0)`: reported 242-243, actual spans 242-244 (the `.context(...)?` closing the call is
  on 244) — off by one line.
- `hardware_id::read`: reported 244, actual 245 — off by one line (pushed by the above).
- Hardware-ID-mismatch branch: reported 250-259, actual `return Err(raise(...));` spans 250-259
  exactly (the `if` condition itself opens on 249) — no material drift.
- **`validate_known_timed`'s own span: reported 214-248, actual 214-265** — the function runs 17
  lines past what was reported; the tail (`validated_at_utc_ms` read and the `Ok((known, ...))`
  return, lines 261-265) wasn't in the census's range but doesn't affect this task's claims.

**Reserve check:** `embarch-topology/spec.md` unchanged by this unit (no doc-repo prose files
touched — only `embarch-topology/src/hardware/validate.rs`, in the code repo). `check-doc-size.py
--pressure` before and after both show the same 9,826/10,240 B, still parked under
`tasks/topology/057`. No new file entered reserve; no compaction task filed.

**Gate:** `cargo build --all-targets`, `cargo test --features hardware` (80 passed, 0 failed —
default-feature `cargo test` only runs 15, since `hardware` is opt-in), `cargo clippy --all-targets
--features hardware -- -D warnings` all clean in `embarch-topology`. `python3 scripts/check-docs.py`
green in `embarch-doc` (see report for exact output).

## Not yours

**Do not route the open failure through `raise`.** That widens what lands in `alerts.jsonl` and what
`embarch-core`'s `/validate` returns, across a repo boundary, with no bench to exercise either — and
the census could not check the consumer half. If you conclude the code is what should move, that is a
finding for `inbox/` (absolute path `/home/gabriel/Github/embarch/embarch-doc/inbox/`) and a
follow-up task, with the `embarch-core` side named as unverified.

**Do not touch `embarch-core`.** You own `topology` only. The consumer-visible half — what status
`POST /validate` actually returns on a non-downcastable error — is `embarch-core`'s to read, and the
topology-side defect stands without it.

**Do not write a new numbered decision**, and do not amend decision 12: its one-directional claim
holds. If you believe 12 needs a qualifier, drop it in `inbox/` with your reasoning.

**Do not do `tasks/topology/055`'s three items** — the identity-gate equality shortcut, the
role-uniqueness displacement, and the `alerts.jsonl`-versus-"only declared intent persists" sentence.
Separate unit, may be in flight.
