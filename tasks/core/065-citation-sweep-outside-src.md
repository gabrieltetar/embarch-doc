# 065 — Citation sweep: the nine `embarch-core` citations that live outside `src/`

**State:** open
**Source:** leg 121's refill sweep, 2026-09-16. `core/058` (merge `fd90452`) reported
*"embarch-core/src swept end to end"* — its scope was the directory, and three citation-bearing files
sit outside it and have never been read. Same shape as the still-open `tasks/topology/046`, which was
filed for the same reason in the same repo layer.
**Scope:** core
**Hardware:** none — comments in a manifest, a cross-build config, and a README. Nothing is built for
a board, no probe, no live Core, no deploy.
**Owner:** no

**Doc-size reserve for `core`:** one file, `embarch-core/decisions/auth.md` at **11,356/12,288 B
(932 B left)**, filed as `tasks/core/046` and blocked. Nothing else in the scope is in reserve. A
citation sweep should not need to write `auth.md` at all; if it does, say why. If your work leaves any
`embarch-core` doc inside the last 10% of its cap and nothing has filed it, file
`tasks/core/<next free NNN>-compact-core.md` in the same commit per `tasks/README.md`.

## What

Nine citations, in three files, censused at this task's filing:

```
Cargo.toml   5   lines 15, 21, 29, 54, 70
README.md    3   lines 60, 108, 134
Cross.toml   1   line 3
```

Sweep them by the method the seven `study-designer` sweeps, `core/056`/`058` and `umbrella/065`–`066`
used: for each, does the cited decision exist, is its form right for the repo it means, and does the
sentence around it state something the decision actually says. `tests/` has zero citations and needs
no sweep — listed so the count above is exhaustive.

## Why now — and start with `Cargo.toml:70`

**There is a concrete suspected defect already, and it is the same one two other repos are chasing.**
Line 70 reads:

```
# known_boards.toml (`decision 22`) — same version embarch-api
```

`embarch-core` decision 22 (`decisions/probes.md:15`) is *"A probe/board identity gate, because a
label can go stale with nothing to notice"* — an identity gate that decision 22 itself moved into
`embarch-topology`. Nothing in it is about `known_boards.toml` or about version pinning. **Verify
that yourself before acting** — read decision 22's body, then find which decision actually records
the `known_boards.toml` version claim, and repoint or correct the sentence rather than deleting it.

**This number is already known to be stale elsewhere.** `inbox/api-stale-decision-22-citations-remaining.md`
(filed against `api/084`, and referenced in the 2026-09-12 handoff) names four `embarch-core`
decision 22 citations in `embarch-api`'s `client.rs` that cite HTTP routes rather than pairing the
number with `known_boards`. **That drop is another scope's and you must not fix it** — but it is
strong evidence the number is wrong here too, and it means whatever you find should be reported in
terms another scope can reuse.

**And `Cargo.toml` is four-fifths cross-repo, which is where these sweeps actually yield.** Lines 15,
21, 29 and 54 cite `embarch-study-designer` (19, and "that crate's" 46), `embarch-topology` (2, 4, 8)
and `embarch-dev-bench` (12) — manifest prose explaining why the crate is shaped as it is. That is
exactly the class `topology/040` found wrong three times: sentences true when written, made false by a
later decision. `README.md:108` carries the same shape (`embarch-study-designer` decision 8 and
`embarch-topology` decision 13, in one sentence about an oversight).

## Watch for

- **`check-decision-refs.py` walks `*.md` only, and only in the doc repo.** It never reads
  `Cargo.toml` or `Cross.toml`, and this code repo is outside its scope entirely — so nothing fails
  today and nothing will. Treat all nine as unchecked, `README.md` included.
- **`Cargo.toml` mixes citation forms in five lines** — labelled (`` `embarch-study-designer`
  decision 19 ``), referential (`that crate's decision 46`), bare-plural (`embarch-topology decisions
  2, 4, 8`), and bare-in-backticks (`` `decision 22` ``). All of these mean something; **the general
  rule about form is owner-reserved and open at `tasks/doc/055`, so do not settle it here.** Fix a
  wrong number or a false sentence. If the only problem with a line is its form, say so in your
  report and leave it.
- **`README.md:134` names a bound address.** *"Binds to `127.0.0.1:4884` by default — loopback-only
  (decision 6's ...)"*. Decision 6 is cited by `embarch-umbrella` decision 42's neighbourhood too, and
  a README that states a default wrong is user-facing. Check the port and the address against the
  code as well as against decision 6.
- **Do not introduce a bare cross-repo citation.** A bare `decision N` is same-repo by convention; if
  you touch a line that means another repo, it keeps its repo label.
- **Report counts, not just changes.** Wrong numbers and false sentences as two separate numbers, plus
  the total checked. "Checked 9, found none" is a legitimate and useful result — the 2026-09-12
  handoff flags that consecutive zero-defect sweeps may mean refill has converged on always-clean
  files rather than that the corpus is clean, and nothing tracks the hit rate.

## Done when

- [ ] All nine citations in `Cargo.toml`, `README.md` and `Cross.toml` checked for existence, repo
      label, and whether the surrounding sentence is true.
- [ ] `Cargo.toml:70`'s `decision 22` either confirmed correct with the reason, or repointed to
      whichever decision actually records the `known_boards.toml` version claim.
- [ ] `README.md:134`'s bind address and port checked against the code, not only against decision 6.
- [ ] Wrong numbers and false sentences reported as separate counts, with the total checked.
- [ ] No new bare cross-repo citation introduced anywhere in the diff.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
