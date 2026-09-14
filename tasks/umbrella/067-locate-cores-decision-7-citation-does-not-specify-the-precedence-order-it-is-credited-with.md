# 067 — `locate_core`'s decision-7 citation does not specify the precedence order it is credited with

**State:** claimed by agent/umbrella/067-locate-core-decision-7-citation, 2026-09-13 20:33
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

**Reserve (told at dispatch, 2026-09-13 20:33):** one `embarch-umbrella` doc file is in reserve —
`decisions/bind.md`, **93.9%**, 755 B left, filed against `tasks/umbrella/009` which is
**`blocked` on `In flux: yes`**. Nothing else in this sub-project is in reserve. If the fix here
means amending a decision body, check first whether that body lives in `bind.md`: if it does and
your edit spends that reserve, `DOC-COMPACTION.md` §2 applies — compact it in this same unit,
carrying `tasks/umbrella/009`'s `Must not delete:` list and closing only that file's item. If you
push any *other* `embarch-umbrella` doc file into its last 10%, file
`tasks/umbrella/<next>-compact-docs.md` in the same commit (`check-task-numbers.py --next
umbrella` for the number — never `ls | tail`).

**One caution carried from yesterday's sweeps.** The failure mode here is not "the number does not
resolve" — it does. It is that the sentence credits decision 7 with a *precedence order* its body
may not state. When you correct it, **do not replace one unverifiable claim with another**:
`core/056` did exactly that, and its replacement asserted a new false thing about a different
repo's decision. State only what the decision bodies you have actually read support; if the real
precedence order is not written down in any decision, say so in the task rather than inventing a
citation for it.

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

- [x] `locate.rs`'s `locate_core` doc comment no longer credits decision 7 with the precedence order.
- [x] The decision-7 question in step 2 is answered in writing, either way.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment.

## Resolution

Read both decision bodies in full (`decisions/topology.md` decision 7, `decisions/install.md`
decision 28, and `decisions/topology.md` decision 38 — confirmed to be **`embarch-umbrella`'s own**
decision 38, not a cross-repo number: `topology.md`'s own index line lists `6, 7, 8, 9, 30, 38`).

**Decision 7 states no resolution order and does not belong in this comment at all.** It is
entirely about *elevation policy* for controlling/starting the Core service (Windows vs. Linux
system-service elevation, self-elevation moving into `embarch-core`, the no-GUI/no-TTY fallback).
`locate_core` does not start or elevate anything — it is a read-only search for a binary that may
already be running. The WSL2-only branch inside `locate_core` traces to decision 6 (topology is
auto-detected) and decision 30/38 (what `up`/`doctor` do with a WSL2-guest's topology), never to
decision 7. So step 2's question is answered **no** — decision 7 does not belong anywhere in this
comment, not even in a separate sentence for "why the WSL2 branch exists": that reasoning describes
a different mechanism (starting a service) than the one this function performs (finding a binary),
and citing it for existence-of-the-branch would be exactly the same category of error the reviewer
flagged, just moved to a different sentence.

**Decisions 28 and 38 cover five of the six steps, not all six.** Decision 28's own text is close to
verbatim: "Core and the API now resolve via env var → saved state → `PATH` → (WSL2 only) the real
canonical Windows location" — that is steps 1, 2, 3 and 5. Decision 38 explicitly inserts step 4
(the Windows service's own registration) "after `PATH`... and ahead of both guesses, because a
reading beats a guess" — matching the code's own inline comment at the call site (`locate.rs:263`,
unedited, already correct).

**The sixth step — the older fixed conventional directories, tried last — is not specified by any
decision**, in either file, or in `spec.md` (grepped, no hits). The function `windows_conventional_core_paths`
carries its own doc comment calling itself "a fallback for a copy installed some other way than
decision 28's canonical per-user location" — descriptive, not decision-backed. It most likely
predates decision 28 (from before there was a "real canonical" location to guess past), but nothing
in `decisions/install.md`, `decisions/topology.md`, `decisions.md`'s index, or `spec.md` ever
elevated it to a numbered decision. Per the caution against replacing one unverifiable claim with
another, the fixed doc comment says this plainly rather than inventing a citation for it.

**No new `embarch-umbrella` decision filed.** This last step is a short, already-reasoned
implementation default (the function's own doc comment states the trade-off: "guessing at a
developer's source checkout would find a stale debug build as often as the real thing"), not a
suite-level policy anyone outside this function depends on, and the Reserve note at dispatch flagged
this unit as source-comment-only. If this fallback's shape or order ever needs to be stable across a
larger surface, it is a good candidate for a future decision — for now it stays exactly where it
already lived, correctly described.

**Net for the citation-sweep tally:** this task's own finding is the same defect `066`'s reviewer
already called — decision 7 does not specify the precedence order. Fixed here, once, at the source.
`066`'s landed changelog and task resolution are untouched, per instruction.

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
