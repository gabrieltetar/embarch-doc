# 029 — Compact `embarch-core/decisions/platform.md`

**State:** done
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

- [x] `embarch-core/decisions/platform.md` is out of reserve (`scripts/check-doc-size.py` clean).
- [x] If split: every moved decision is byte-identical to its original, the index row is updated,
      and each resulting file has a topic line a reader can act on.
- [x] Nothing on the `Must not delete:` list above is shortened or paraphrased.
- [x] Gate green.

## Resolution

Split along the file's own two existing `##` sections rather than the task's candidate seam
(1/2/7/17+3 vs. 42/46): the real tension, once the index and full text were read, was **"how Core
runs as a program" (language/runtime, service install, locking)** vs. **"the request surface"
(auth, binding, config, and the two mechanisms — 42, 46 — that keep the documented surface in sync
with the router)**. That maps exactly onto the original `## Platform and process` + `## Locking`
headers on one side and `## Auth, binding, configuration` on the other, so no decision text needed
rewriting — a pure verbatim block move, confirmed byte-identical against `HEAD:embarch-core/decisions/platform.md`
(only end-of-file trailing blank lines differ, not decision content).

- `embarch-core/decisions/platform.md` (5,820 B) keeps decisions 1, 2, 3, 4, 7, 14, 15, 17 —
  "Platform, process, and locking".
- `embarch-core/decisions/auth.md` (6,627 B, new) takes decisions 5, 6, 11, 42, 46 — "Auth,
  binding, and surface consistency".
- `embarch-core/decisions.md`'s index table updated: the old single row replaced with one row per
  file, decision numbers and sizes corrected; each new file's own header cross-links to its
  sibling.
- Nothing on the `Must not delete:` list was touched beyond relocation: decision 1/2/7/17's
  **Corrected 2026-09-08** paragraph and its measurement are intact and unmoved (they stay in
  `platform.md`); decision 3's Windows SCM 30-second handshake / foreground-fallback detail is
  intact and unmoved (`platform.md`); decision 46's rejected `include_str!` arm and the
  worker-worktree-pair reason are intact, moved verbatim to `auth.md`.
- Gate: `python3 scripts/check-docs.py` — all 10 checks green. `scripts/check-ownership.py --scope
  core` — all 3 changed paths owned. No `--code-repo` run: this task has no code worktree, only
  `embarch-doc`.
- No suite-level doc touched; no `status.d/` fragment needed (no suite-level fact changed — this
  is an internal reorganization of one sub-project's decision files, not a capability/maturity
  change, so no `features.d/` fragment either).
- `changelog.d/core-split-platform-decisions.changed.md` dropped.
- **`DOC-COMPACTION-PASS.md`'s question, answered:** yes — `embarch-core/spec.md` alone still
  answers what someone needs to work on this component today. This split touched no `spec.md`
  content at all; it only reorganized *why*-history across two files instead of one, and both are
  reachable from `spec.md` via `decisions.md`'s index exactly as before.
