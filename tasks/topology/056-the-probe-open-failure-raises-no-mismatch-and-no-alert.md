# 056 — `validate`'s probe-open failure raises neither a `TopologyMismatch` nor an alert, and the type's own doc comment says it does

**State:** claimed by agent/topology/056-probe-open-no-mismatch, 2026-09-17 01:50
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

- [ ] The two in-repo claims are each **corrected** or **reported as holding**, on lines you read —
      `validate.rs`'s `live_hardware_id` doc comment, and the module header's *"every mismatch is
      durably logged"*.
- [ ] Your report states explicitly whether you changed prose only, or whether you concluded the
      code should route the open failure through `raise`. **If the latter, do not implement it** —
      see "Not yours".
- [ ] Your report says which of the reported line numbers had drifted.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
      in `embarch-topology`, and `python3 scripts/check-docs.py` in `embarch-doc`.

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
