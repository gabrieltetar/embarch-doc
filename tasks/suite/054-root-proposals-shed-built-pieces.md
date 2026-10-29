# 054 — Delete the built pieces from the four root proposals

**State:** open — drained from `inbox/` and announced 2026-10-29 14:28:59 (`ts` `1793305739.311079`); the 30-minute window closes 14:58:59. A later leg reads the thread and runs it.
**Source:** owner's session, 2026-10-29 — cleanup pass; DOC-PROTOCOL.md "A proposal" (an accepted piece is deleted from it, not restated)
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

Each of the four root proposals keeps only what is still proposed. Every piece
that has been built and recorded as a numbered decision in its owning
sub-project is **deleted from the proposal, not restated** — at most a one-line
pointer to the decision — and a proposal with nothing left is deleted outright,
its inbound links repointed at the decisions that absorbed it. `Status:` stays
`proposal` on anything that survives, never `accepted` or `partly built`
(DOC-PROTOCOL.md §"A proposal").

- `bootload-proposal.md` (09-30) — software path built: smp, topology 36,
  core 77–78, api 80–81. Left: the first-DUT hardware run and the UI button.
- `embarch-host-study-proposal.md` (10-09) — phase 2 built (topology 49, core
  104, api 97), phase 3's prompt built (core 105, api 99), the UI modal is
  `ui/100`/`ui/101`; `doc/088` updated its PD bench section 2026-10-29.
- `embarch-desk-sessions-proposal.md` (10-22) — check against `embarch-desk`
  decisions; the desk shipped suite-wide 2026-10-23.
- `embarch-stream-pipeline-proposal.md` (09-02, untouched since) — inbound half
  folded, outbound half still proposed. Shed nothing that is not recorded as a
  decision; if the outbound half has no task, `open.md` entry or roadmap line,
  say so in the digest — whether it is still wanted is the owner's call.

Verify each "built" claim against the decision text before deleting the piece.
These lists come from memory notes and Status lines, not from a read of the
decisions.

## Why now

The owner's cleanup pass, 2026-10-29. Two of the four now restate decisions the
code repos record, which is the second-source-of-truth failure DOC-PROTOCOL.md
names.

## Done when

- [ ] Each surviving proposal carries only unbuilt design, with `Status:
      proposal` and pointers to the decisions that absorbed the rest.
- [ ] Any proposal fully absorbed is deleted and `check-links.py` is green.
- [ ] `check-ownership.py --supervisor` green. **If it reports
      `bootload-proposal.md` or `embarch-desk-sessions-proposal.md`
      unclassified, stop**: their `fleet_writable` entry in `fleet.toml` is
      the owner's to land, and editing them before it has is outside the map.
      A deleted proposal leaves a stale entry there; name it in an `inbox/`
      note for the owner.
- [ ] Leg digest: per proposal, bytes before → after and what was shed.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/`
      fragment `doc-root-proposals-shed.removed.md`.
