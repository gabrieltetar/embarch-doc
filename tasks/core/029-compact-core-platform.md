# 029 — Compact `embarch-core/decisions/platform.md`

**State:** claimed
**Source:** `scripts/check-doc-size.py` — entered reserve on the `suite/021` fold (leg 051,
2026-09-08), which appended a **Corrected 2026-09-08** paragraph to decision 1/2/7/17 retiring its
"CI everywhere" clause.
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/decisions/platform.md
**Size debt due:** 2026-09-22
**In flux:** no
**Must not delete:** decision 1/2/7/17's **Corrected 2026-09-08** paragraph and the measurement
behind it — that `embarch-core` has `release.yml` and no test workflow, and that the only per-push
Rust test workflows in the suite are `embarch-study-designer`'s and `embarch-topology`'s. That is a
measured fact with a date, and shortening it to its conclusion ("CI was never built") loses the
evidence and invites the claim being re-asserted. Decision 3's Windows SCM 30-second handshake
detail and the reason `run` falls back to foreground only when SCM did not launch it — that is a
platform constraint nobody re-derives. Decision 46's *rejected* arm (a relative
`include_str!("../../embarch-doc/...")`, and why a worker's worktree pair breaks it), which this
very leg reintroduced by accident and a reviewer caught: a decision reduced to its conclusion stops
being able to catch that.

## What

`embarch-core/decisions/platform.md` is 11,701 bytes against a 12,288 B `decision-group` cap —
inside the last 10%, with about 590 bytes of runway. **Prefer a split over a squeeze**
(`DOC-COMPACTION.md` §2/§3): a verbatim split restates nothing, so it costs no argument, and this
file has a plausible seam. It carries the language/runtime/service-installation decisions
(1/2/7/17, 3) alongside the documentation-and-surface-enforcement ones (42's auth sweep, 46's
pinned route count) — **"what this process is built out of" and "what checks that the docs match
the router" are two missions sharing one file.** Read the real index before cutting; those are
candidate groupings, not the answer.

## Why now

Nothing is urgent — 590 bytes is runway, not a wall — but the failure mode of a full decisions file
is not a clean refusal: it is a decision filed into the wrong topic file because the right one was
full, gate-green and silent, which `embarch-api` did on 2026-09-05 with 96 bytes left in
`decisions/zephyr.md`.

## Done when

- [ ] `embarch-core/decisions/platform.md` is out of reserve (`scripts/check-doc-size.py` clean).
- [ ] If split: every moved decision is byte-identical to its original, the index row is updated,
      and each resulting file has a topic line a reader can act on.
- [ ] Nothing on the `Must not delete:` list above is shortened or paraphrased.
- [ ] Gate green.
