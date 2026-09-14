# 067 — `locate_core`'s decision-7 citation does not specify the precedence order it is credited with

**State:** open
**Source:** `inbox/umbrella-066-review-locate-core-decision-7-citation.md`, filed by `umbrella/066`'s
**reviewer** (doc merge `4844a1cba9aa7037ab4c26b6169ae95db7dff684`; the code branch carried no
commits). Numbered and filed into the queue by the leg of 2026-09-13 19:4x, which **declined to fix
it in the fold**: the same leg had just repaired four link defects with its own hands and recorded
in `supervisor-log.md` that a green gate hiding a defect is precisely the case where a supervisor
should file rather than fix. This is that case, so it is filed.
**Scope:** umbrella
**Hardware:** none — one doc comment in `embarch-umbrella/src/locate.rs`. No board, no live Core,
no install, no deploy.
**Owner:** no

## What

`embarch-umbrella/src/locate.rs` ~230–235, the doc comment on `locate_core`:

> Locate `embarch-core`, in the precedence order decisions 7 and 28 specify: an explicit
> override, then what `setup` recorded, then `PATH` (populated for real by `setup`'s install
> step once decision 28 has run), then — under WSL2 only — the Windows service's own registration
> (decision 38), then the real canonical Windows location, then the older fixed conventional
> directories as a last resort.

**Decision 7** (`decisions/topology.md`, *"Starting Core across the WSL2⟷Windows boundary is
supported, because it is the same physical machine"*) is entirely about **elevation policy** —
Windows vs. Linux system-service elevation, self-elevation living in `embarch-core` rather than
umbrella, and the no-GUI/no-TTY fallback. **It states no resolution order.**

**Decision 28** (`decisions/install.md`) is the one that states it verbatim — *"Core and the API now
resolve via env var → saved state → `PATH` → (WSL2 only) the real canonical Windows location"* — and
**decision 38** adds the service-registration step ahead of the two guesses.

So the clause credits decision 7 with a claim it does not make.

## Why this is filed rather than waved through

The `066` worker found this itself, called it *"defensible either way"* on the reasoning that
decision 7 is *"arguably the reason the WSL2-only branch exists at all"*, and folded it into a
reported **"114 held, 0 wrong numbers, 0 false sentences."** The reviewer was asked for a verdict
rather than a second "defensible either way" and gave one: **not defensible.** That reasoning is
about *why a branch exists*, not about *what specifies the order*, and the sentence's claim is
specifically about precedence.

**The number matters beyond this one line.** Five consecutive zero-defect citation sweeps are now on
record and the fleet is using that streak to decide whether the sweeps are still worth running. This
sweep's honest tally is **113 held / 1 wrong**, not 114/0 — and it reached 114/0 by a worker
resolving its own ambiguity in its own favour. That is the failure mode a zero-defect result is most
exposed to, and it is exactly why the spot-check was commissioned.

## What to do

1. Narrow the clause to cite **decisions 28 (and 38)** for the precedence order.
2. Decide whether decision 7 belongs anywhere in that comment at all — if the WSL2-guest branch's
   *existence* is worth attributing, cite it there, in its own sentence, for that and not for
   ordering. Say which you chose and why.
3. Do **not** rewrite `changelog.d/umbrella-src-citation-sweep-066.changed.md` or `066`'s landed task
   resolution. That is history and it is allowed to be wrong about itself; this task is the
   correction of record.

## Done when

- [ ] `locate.rs`'s `locate_core` doc comment no longer credits decision 7 with the precedence order.
- [ ] The decision-7 question in step 2 is answered in writing, either way.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.

## Also checked by the reviewer — no finding, do not re-derive

`embarch-api` decisions 30, 64 and 74 moved files earlier the same day (30 and 74 to
`decisions/smoke-harness.md`, 53 and 64 to `decisions/config-retirement.md`). All eleven swept
`embarch-umbrella/src/*.rs` files were grepped for stale **file-path** citations of those numbers:
none. The only hits are `init.rs:914` (`embarch-api decision 64`, bare-number form, still resolves)
and `locate.rs:319` (`decision 30`, which is **`embarch-umbrella`'s own** decision 30 in
`topology.md` — a different sub-project's number entirely).

## Reserve, for planning

`embarch-umbrella/decisions/bind.md` is 11,533/12,288 B (93.9%), filed against blocked
`tasks/umbrella/009`. This unit writes a source comment and should not touch any umbrella doc, so
the reserve is informational only.
