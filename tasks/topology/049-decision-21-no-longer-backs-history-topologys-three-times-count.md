# 049 — Decision 21 records two observations now; the topology changelog's line still says three

**State:** done 2026-09-16 — decision 21's timestamp hunk restored; the changelog line matches again.
**Source:** `embarch-reviewer` on `suite/039` (doc merge `2f5da8f`), drained from `inbox/` by leg 121
on 2026-09-16 as `topology-decision-21-three-times-count-now-two.md`. It settles a side question
leg 119 raised as low-confidence and nobody had checked.
**Scope:** topology
**Hardware:** none — doc prose only. No board, no probe, no live Core. **But see "Watch for": the
facts involved are measured hardware results and must stay marked as measured.**
**Owner:** no

**Doc-size reserve for `topology`: nothing in reserve.** No `embarch-topology` file appears in
`check-doc-size.py --pressure`. The per-decision cap still applies to entry 21 — report its bytes
before and after. If this unit pushes a `topology` file into reserve, file
`tasks/topology/<next free NNN>-compact-topology.md` in the same commit per `tasks/README.md`.

## What

`topology/048` (merge `d3f2f81`) compacted `embarch-topology/decisions/validation.md`#21. One listed
cut was "dropped reproduction timestamps":

```
-… relation *match*** [measured 2026-08-31, reproduced 2026-09-06 22:07:51Z and 22:15:45Z from Core's own handshake log]. …
+… relation *match*** [measured 2026-08-31, reproduced 2026-09-06]. …
```

The original names **three** recorded observations of the JTAG-vs-self-report match: one measurement
and two separately timestamped reproductions. The compacted form names two, and nothing in it says
two reproductions happened on that date — "measured X, reproduced Y" parses as two events, which is
exactly the measured/reproduced pairing used elsewhere in the same paragraph.

`history/topology.md:61`, untouched by either unit, still reads: *"the identity gate's mismatch
refusal is on record three times — decision 21."* Three matched the original 1 + 2 exactly. It no
longer matches what decision 21 documents.

## Why now

**Because the count is a claim, and the compaction's commit message asserted no claim was touched.**
It listed the timestamp drop as a phrasing cut, not as a cut with a cross-file consequence — the
residue class `DOC-COMPACTION-PASS.md` asks a squeeze to enumerate. This is the second finding in two
legs where the answer came from running the check rather than from reading the entry's own prose.

## Watch for

- **Restoring is cheaper than it looks and re-cutting is not free.** A revert of that one-line hunk in
  `d3f2f81` is clean — no other line depends on it — but decision 21 was compacted for a reason. Check
  entry 21's current byte count against the 4,096 B per-decision cap before choosing: if restoring both
  timestamps fits, restoring is the honest fix, because the two reproductions are **measured** results
  and a count is cheaper to keep than to re-derive.
- **If you instead correct the count, you may not edit `history/topology.md`.** It is
  `build_changelog.py` output and outside §3's allowed paths for a worker. That constrains the choice:
  fixing the *history* side is not available to you, so if decision 21 cannot carry three, **say so in
  your report and leave the mismatch named** rather than half-fixing it. `ui/056` burned a cycle
  discovering this ownership edge the hard way.
- **Never promote a stated fact to a measured one.** Both reproduction times came from Core's own
  handshake log on real silicon. Whatever wording you land, the bracket must still read as measured,
  with its dates, not as an assertion.
- **Check the rest of the corpus for the same number.** The drop's second checkbox asks whether any
  other doc cites "three times" for this fact. Grep the whole doc repo for it; report the count you
  checked, not just what you changed.

## Done when

- [x] Either decision 21 documents three recorded matches again (both reproduction timestamps
      restored), or the mismatch with `history/topology.md:61` is named explicitly in your report as
      unfixable from this scope, with the reason. **Restored**: it fit under cap (4,046 of 4,096 B),
      so the honest fix was taken. The changelog line no longer disagrees.
- [x] Every other citation of "three times" for this fact found and reported — including "none found",
      with the search you ran. `grep -rn "three times" . --include="*.md"` across the whole doc repo:
      every other hit is a different fact (SRAM overflow count, decision-uniqueness examples, a
      different decision's mismatch-trip count in `embarch-topology/spec.md:119` citing decision 12,
      dev-bench mirrored constants, EAP dropped-chunk anecdote, reviewer/supervisor process notes).
      None besides `history/topology.md` cite this fact.
- [x] Decision 21 at or under 4,096 B, bytes reported before and after. Before (as left by `topology/048`):
      3,992 B. After (this unit): 4,046 B — 50 B margin.
- [x] Measured facts still presented as measured, with dates. The restored bracket reads
      `[measured 2026-08-31, reproduced 2026-09-06 22:07:51Z and 22:15:45Z from Core's own handshake
      log]` — same wording `topology/048` compacted from, unchanged in kind.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `cargo build`/`test`/`clippy --all-targets
      -- -D warnings` clean in `embarch-topology` (no code change; empty diff on that side except this
      task file's own state). `check-docs.py` green in `embarch-doc` after also rewording this task
      file's own title, which `check-task-state.py` flagged for embedding the literal path
      `history/topology.md` — a filing defect from when leg 121 drained the inbox drop, unrelated to
      the decision-21 fix itself. `check-ownership.py --scope topology` clean on both worktrees.
      `check-client-names.py` clean.
