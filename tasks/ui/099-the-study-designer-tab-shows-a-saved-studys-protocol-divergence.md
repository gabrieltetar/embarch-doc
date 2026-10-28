# 099 — The Study Designer tab shows when a saved study's protocol no longer matches its `.eap`

**State:** open
**Source:** `embarch-ui/open.md` — "A saved study is never checked against the `.eap` file it was built from … this repo's half is only where a divergence would be *shown*"; and `embarch-study-designer/open.md` — "What to do with a protocol divergence — the check exists (decision 87, `protocol_divergence`); showing it is `embarch-ui`'s". The check landed as `study-designer/079` on 2026-10-28.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

A saved study carries resolved `ProtocolDef`s, so editing the `.eap` afterwards changes nothing the study runs — correct, and silent. `embarch-study-designer` now answers the question (decision 87): `protocol_divergence(&study.protocols, &repo.defs())` gives, per protocol the study carries, `Unchanged`, `Changed(Vec<Difference>)` or `Gone`. `src/study_designer.rs` already scans the repo's protocols (`eap_repo::scan`, `RepoProtocols`).

When this is done, opening a saved study in the Study Designer tab shows, for each protocol it carries that has diverged, a visible note: which protocol, whether it changed or is gone, and the differences by part and name (added, removed, modified). The note says plainly that the study still runs what it carries (decision 87 is advisory; decision 58), so the reader knows nothing is broken yet and what re-saving would change. An unchanged study shows nothing extra. Where the divergence is computed (backend route vs. the existing listing) and how re-adopting the current definition is offered, if at all, are this repo's design calls; record them as a ui decision.

## Why now

The check has no caller. Until something shows it, the study-designer half is a function nobody reads and the silence `embarch-ui/open.md` names is unchanged.

## Notes for the worker

- `Difference::part` is about to gain correct labels for order-only changes (`tasks/study-designer/080`, dispatched alongside this). Render `part` as text; do not branch on its values, so that change needs nothing here.
- `embarch-ui/open.md` is in reserve (935 B left, filed against the blocked `tasks/ui/088`). This task should **delete** the "A saved study is never checked against the `.eap`" bullet once the display ships, which pays down rather than spends.

## Done when

- [ ] A saved study whose protocol was edited shows the divergence note with its differences; one whose protocol is deleted or renamed shows `Gone`; an unchanged one shows nothing. Tested headless or by a route test against fixture `.eap` files.
- [ ] The note states that the study still runs what it carries.
- [ ] `open.md`'s bullet removed; a ui decision records where the check runs and what the user can do about a divergence.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions/`/`open.md` updated, `changelog.d/` fragment dropped.
