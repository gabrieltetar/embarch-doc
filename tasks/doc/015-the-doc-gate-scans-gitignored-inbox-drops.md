# 015 — The doc gate scans gitignored `inbox/` drops, so the owner's gate is red whenever a drop is pending

**State:** open
**Source:** owner's session, 2026-09-06, twice in one sitting while leg 018 was running.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/check-links.py` and
`scripts/check-decision-refs.py`, reserved from workers and supervisors alike
(`../../embarch-fleet/protocol.md` §3).

## What

`check-links.py` and `check-decision-refs.py` walk `inbox/*.md`. Drops are **gitignored**
(`.gitignore:7`, `inbox/*.md`), so they exist only in the owner's main checkout — a leg's
worktree has none. Two consequences, and the second is the problem:

- **A leg's gate is unaffected.** Verified: with three drops pending and the owner's gate
  red, the leg worktree's `check-docs.py` was `rc=0`.
- **The owner's gate is red for as long as any drop is pending**, on findings that are
  correct-by-construction. Observed twice on 2026-09-06:
  - `inbox/api-open-md-versions-is-read-now.md` cites `embarch-umbrella` decision 42 — a
    decision the drop is *proposing*, so it does not resolve yet.
  - the same drop links `decisions/surface.md`, correct from `embarch-api/` and broken
    from `inbox/`, because a drop is written at the depth of the file it will *become*.
    Leg 018 hit the same thing and fixed one by hand (`e795b3f`, "a link the inbox drain
    moved").

**A drop legitimately references things that do not exist yet.** That is what a drop *is*:
`inbox/README.md` calls it a complete task minus its number, written by a thread that found
something. Requiring its references to resolve before it is drained inverts the order.

## Why now

It is the standing-exception failure this suite names in three other places — a gate with a
red nobody should act on teaches its reader to skim the other eight. `install.py`'s own
header says exactly this about the `FLEET_REL` bug that made `check-docs.py` permanently red
in every worktree. Tonight the owner reached "that red is not mine" twice, correctly both
times, which is the habit forming.

## Candidates

- **Exclude `inbox/` from both scanners**, the way `check-doc-size.py` already excludes
  `changelog.d/` and `features.d/` via `EXEMPT`. Cheapest, and it matches the existing
  treatment of the other two staging directories.
- **Scan it but do not fail on it** — report drop findings as warnings, so a malformed drop
  is still visible to whoever drains it. Keeps the one real benefit of scanning.
- **Leave it and drain promptly.** Rejected on the evidence above: the drops arrive faster
  than the drain when the pump is latched, and "self-resolves" is what made this look like
  a non-issue the first time.

Prefer the second if it is not much more work than the first: the drain is exactly when a
malformed drop should be caught, and `queue-status.py` already lists drops as a queue state.

## Done when

- [ ] A pending, well-formed drop does not make the owner's `check-docs.py` red.
- [ ] A malformed drop is still caught before or during the drain, not silently filed.
