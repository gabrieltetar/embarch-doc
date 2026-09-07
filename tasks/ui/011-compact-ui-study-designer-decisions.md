# 011 — `embarch-ui/decisions/study-designer.md` crossed into reserve

**State:** open
**Source:** `ui/010` added decision 20; its reviewer then found a wrong number inside it, and the
supervisor's correction at the fold spent the last of the headroom. `DOC-COMPACTION.md` §2
**Scope:** ui
**Hardware:** none
**Owner:** no

**Compacts:** embarch-ui/decisions/study-designer.md
**In flux:** **No.** Every decision in this file describes a shipped, rendered surface — the step
editor, the run card, the saved library. Nothing here is a design mid-rewrite. This is **not** the
file [`009`](009-compact-ui.md) is blocked on; that one is `decisions/trace-view.md` and it stays
blocked.

## What

**11,164 of 12,288 B; the reserve line is 11,059.** The history is worth two lines because it is the
whole reason this task exists rather than being avoided:

- `ui/010`'s first draft of decision 20 landed the file at **11,535** — inside reserve. The worker
  trimmed its own entry **three times**, to **11,050**, specifically so no compaction task was owed.
  That is ~9 bytes of clearance.
- Its reviewer then found that decision 20 quoted the clamp window as **5 s**. It is **~1 s**:
  `study_designer.rs`'s `POLL_INTERVAL` is `from_secs(1)`, and the 5 s constant is `main.rs`'s
  dashboard poll, a different loop. The supervisor corrected it at the fold and said *why* 5 s is
  wrong, so the next reader does not restore it. **That correction is what crossed the line**, and
  filing this is cheaper than a decision doc carrying a number that is 5× off.

**Do not resolve this by shortening the correction back out.** The whole sequence — trim to duck the
line, then discover the entry was wrong — is the argument for treating the reserve as a ledger rather
than a wall.

**Must not delete:**

- **Decision 20's stated cost**: that the clamp makes a run's last moment read `N/N` with nothing
  running, and that the window is ~1 s and which constant that is. A version keeping the choice
  without its cost turns a weighed trade into a preference.
- **Decision 20's premise**, that during a run the badge is the only thing on the run card saying
  where the study is, because per-step rows do not render until `completed`. Verified twice against
  `renderRunState` at `fa3b7b6`. It is the entire argument for *step now running* over *steps
  finished*, and without it the entry reads as taste.
- **The zero-step case** — `total_steps` of `0` gets no counter rather than `1/0`.

## Note on the likely shape

Check whether a **mission split** fits before prose surgery (`DOC-COMPACTION.md` §2 prefers it, and
two units this same day took it successfully). This file plausibly holds more than one mission: the
authoring surface (the step editor and the saved library) versus the run surface (the run card, its
badge, its rows). If it splits, `decisions.md` gains the index row, nothing is renumbered, and
`scripts/check-decision-refs.py` is the check.

**And check the inbound links by hand.** `check-links.py` passes a `decision N` link whose target
file no longer defines N, and `check-decision-refs.py` resolves numbers against the sub-project
rather than the file — so a split silently strands them. That defect is `tasks/doc/022`, found the
same day by a split in `embarch-topology`.

## Done when

- [ ] `decisions/study-designer.md` is clear of its reserve line (under 11,059 B), by shortening or
      by a mission split.
- [ ] Every `Must not delete:` item above survives, verified against the pre-image rather than from
      memory.
- [ ] If it splits, every inbound link to a moved decision is repointed **and checked by hand**.
- [ ] `DOC-COMPACTION-PASS.md`'s question answered in the commit message, in the compactor's own
      words: *what does someone about to change the study-designer tab lose if this paragraph is
      gone?*
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
