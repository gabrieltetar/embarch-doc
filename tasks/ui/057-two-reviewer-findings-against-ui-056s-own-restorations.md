# 057 — Both of `ui/056`'s restorations are wrong: decision 13's universal claim is false, decision 25's vertex count is on the wrong trace

**State:** done — agent/ui/057-two-reviewer-findings, 2026-09-16
**Source:** two `embarch-reviewer` drops against `ui/056` (merge `b67da91`), drained from `inbox/` by
leg 121 on 2026-09-16: `ui-debug-tab-13-by-construction-claim-wrong.md` and
`ui-decision-25-restored-count-wrong-trace-mode.md`. Filed as one task because they are one unit's
two corrections in one repo, and a scope gets one slot.
**Scope:** ui
**Hardware:** none — decision prose in `embarch-doc/embarch-ui/decisions/`, plus reading one Rust
function. Nothing is built for a board, no probe, no live Core, no UI launched.
**Owner:** no

**Doc-size reserve for `ui`: nothing in reserve.** No `embarch-ui` file appears in
`check-doc-size.py --pressure`. **But both parts of this task are bounded by the *per-decision* cap
of 4,096 B, which is a different ledger** — decision 13 is reported at 4,080 B, so it has roughly
**16 B of margin** and part A almost certainly needs a trim elsewhere inside that same entry to fit.
Report the byte count of each decision you touch, before and after. If this unit pushes a `ui` file
into reserve, file `tasks/ui/<next free NNN>-compact-ui.md` in the same commit per `tasks/README.md`.

## Part A — `decisions/debug-tab.md`#13 asserts a guarantee the code does not give

`b67da91` added:

> **The diff tolerates a growing trailing line too** — Core's tail can end mid-line.
> `diff_new_lines` (`src/logs.rs:126`) needs exact overlap; a mutating last line never matches, so
> the same no-overlap fallback fires as for volume aging the window out.

The function (`embarch-ui/src/logs.rs:126`, unchanged by that doc-only unit):

```rust
fn diff_new_lines(previous: &[String], new: &[String]) -> Vec<String> {
    if previous == new { return Vec::new(); }
    let max_overlap = previous.len().min(new.len());
    for k in (1..=max_overlap).rev() {
        if previous[previous.len() - k..] == new[..k] { return new[k..].to_vec(); }
    }
    new.to_vec()
}
```

For `k < n`, `new[..k]` **excludes** the freshly-grown trailing line while `previous[n-k..]`
**includes** the pre-growth one — so a match at `k < n` never compares the grown line at all. The
reviewer's counter-example: `previous = ["A","B","A"]` grows to `["A","B","A2"]`; `k=1` matches
(`["A"] == ["A"]`) and the function returns `["B","A2"]` through the *overlap* branch, republishing
`"B"` — a duplicate, and never reaching the fallback the decision calls universal.

**Verify that counter-example yourself against the current function before you rewrite anything.**
If the code has moved since the drop was written, the drop is what is stale, not the decision.

**This is not a contrived case by the decision's own standard.** Three bullets above, the same entry
rests on *"log lines repeat verbatim all the time (a retry, a heartbeat, a stack frame)"* to explain
why a different anchor bug was real. The same property defeats "never matches".

## Part B — `decisions/shell.md`#25's restored vertex count is attached to the wrong trace

`b67da91` restored *"22 vertices for the E (plus its 4-vertex counter) and 15 for the A (plus its
own 4-vertex counter), 657 B inline"* into the **standalone-SVG / `layers`-mode** paragraph. The
pre-`ui/055` text (`f6418f5`) carried those exact numbers in the **preceding** paragraph — the
**header glyph**, which the same decision's still-standing text says is drawn in **union** mode and
lives **inline** at `assets/index.html:34`. The standalone `embarch-mark.svg` (`layers` mode, served
at `/favicon.svg`) had its own different numbers: **693 B, 53 vertices**.

So as landed, decision 25 says a served file is "657 B inline", two sentences from its own
inline/served distinction. `history/ui.md:38` — *"Decision 25's E vertex count was 16 (a non-union
trace); corrected to 22"* — confirms the 16→22 correction was about the **union** trace.

## Watch for

- **You cannot write `history/ui.md`.** It is `build_changelog.py` output and outside §3's allowed
  paths for a `ui` worker; `ui/056` tried, got a real red from `check-ownership.py --scope ui`, and
  reverted. If part B leaves `history/ui.md:38` needing a wording change, **say so in your report**
  and do not edit it. Re-checking that line against wherever the number lands is in scope; changing
  it is not.
- **Confirm `f6418f5`'s wording rather than reconstructing it.** `git show f6418f5` in the doc repo
  has the pre-compaction paragraph; both drops quote it, and a paraphrase of a paraphrase is how the
  original residue was introduced.
- **Do not fix the algorithm.** Part A is about the doc's accuracy. Whether the spurious-match
  behaviour is itself worth a code change is a separate question — if you form a view, put it in
  `embarch-ui/open.md` or an `inbox/` drop (absolute path
  `/home/gabriel/Github/embarch/embarch-doc/inbox/`), not in `src/`.
- **Report counts.** Bytes per decision before and after, and say explicitly whether part A's rewrite
  needed a trim elsewhere in entry 13 and what you trimmed.

## Done when

- [x] Decision 13's sentence states the actual guarantee: a growing trailing line falls into the
      no-overlap replay-the-window branch **unless** the window holds a line elsewhere identical to
      the pre-growth trailing line's content, in which case the overlap search can match spuriously
      and republish an already-sent line.
- [x] Decision 25's restored count is either moved back to the header-glyph (union-mode) paragraph as
      it read pre-`ui/055`, or rewritten in place with the layers-mode file's own numbers (693 B, 53
      vertices). Took the second shape: `assets/brand/embarch-mark.svg`'s own mention now reads
      `(693 B, 53 vertices)` and the wrong 22/15-vertex/657 B sentence (the header-glyph/union trace's
      numbers, misattributed) is removed from the layers-mode paragraph.
- [x] Both decisions at or under 4,096 B, bytes reported before and after: debug-tab.md#13
      4,080 B -> 4,079 B (rewrite plus trims elsewhere in the same entry — see commit message);
      shell.md#25 3,906 B -> 3,778 B.
- [x] `history/ui.md:38` re-checked against wherever the number ends up — reported, not edited. The
      cited line has drifted to line 41 as newer fragments were folded in ahead of it ("Decision 25's E
      vertex count was 16 (a non-union trace); corrected to 22...") and remains an accurate historical
      record of `ui/030`'s union-trace fix — it does not describe present doc content either way, so it
      needs no wording change. A second, `ui/056`-authored line (now at line 30 — "restoring what
      history/ui.md:38 cites") records an action that is now known to have restored the number to the
      wrong paragraph with the wrong file's figures; that stays as an accurate record of what `ui/056`
      did, not a live claim, so it is also left alone. `history/ui.md` is `build_changelog.py` output
      and out of a `ui`-scoped worker's reach either way (protocol.md §3); this unit's own fragment
      (`changelog.d/ui-057-reviewer-corrections.fixed.md`) will fold into a further, newer line next
      assembly.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) for everything this unit touched. One
      pre-existing, unrelated red found in the full `check-docs.py` run:
      `check-task-state.py` flags `tasks/topology/049-decision-21-no-longer-backs-history-topologys-three-times-count.md`
      (topology scope, not touched by this unit, not in this branch's diff — confirmed via
      `git diff --stat` against this branch's own two file changes).
