# 066 — Citation sweep: the nine `embarch-core` citations that live outside `src/`

**State:** done — leg 122, `agent/core/066-citation-sweep-outside-src`, 2026-09-16.
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

## Results

**9 checked, 1 wrong number, 2 false sentences, 6 confirmed clean.**

- **`Cargo.toml:15`** (`embarch-study-designer` decision 19, `core-validation`) — **false sentence.**
  Decision 19 exists and is correctly labelled, but it is filed under `decisions/removed.md` and its
  own text is *"Retired 2026-08-25 ... the `core-validation` feature that evaluated them — is gone."*
  The Cargo.toml prose said the opposite: `core-validation` was described as a live, not-yet-enabled
  feature, *"costs nothing to turn on now and this is the intended place"* — a claim a retired feature
  cannot support, and contradicted four lines later by the same comment's own *"that feature is gone"*.
  Reworded to state only what decision 19 actually says; the still-correct `heapless`/decision 46
  citation and the `std`/`alloc` reasoning were left untouched.
- **`Cargo.toml:21`** (`embarch-study-designer` decision 46, heap `Vec`) — confirmed correct verbatim
  against `decisions/limits.md`.
- **`Cargo.toml:29`** (`embarch-topology` decisions 2, 4, 8) — confirmed correct against
  `decisions/crate.md` and `decisions/consumer-boundary.md`.
- **`Cargo.toml:54`** (`embarch-dev-bench` decision 12) — **wrong number.** Decision 12 exists but is
  the SEGGER-VID-match rule; it says nothing about telling two VCOM interfaces apart. The
  interface-2/VCOM1 fact this comment actually needs is `embarch-dev-bench` decision 43
  (`decisions/boards.md`, the nRF54L15DK's own onboarding). Repointed to 43, and the comment's
  `dev_bench.rs` referent (deleted from this crate in `b8da8191`, moved wholesale into
  `embarch-topology`) corrected to name `embarch-topology`'s port detection instead.
- **`Cargo.toml:70`** (`` `decision 22` ``, `toml` crate) — **false sentence, the one this task was
  filed to check.** Decision 22 exists, is correctly same-repo-form, and is real (the probe/board
  identity gate) — but its own text says that whole mechanism, table and `toml` serialization
  included, *"moved wholesale into `embarch-topology`."* No decision anywhere in `embarch-core`
  records a same-version-as-`embarch-api` pinning rule; that half of the sentence cited nothing real.
  Searched exhaustively (every `decisions/*.md` file, plus `embarch-api`'s own `toml`-mentioning
  decisions) and found no candidate to repoint to, so corrected the sentence to say what is actually
  true rather than inventing a citation. Also found, not fixed: `grep -rn "toml::" src/` returns
  nothing in this crate — the direct `toml` dependency looks vestigial now that `embarch-topology`'s
  own `hardware` feature (which this crate already enables) pulls in the same `toml = "1.1"` itself.
  Left the dependency line in place per this task's own instruction not to delete it; noted in the
  comment as a candidate for a future dependency-hygiene pass, not resolved here.
  **For `embarch-api`'s own open `decision 22` citations** (`inbox/api-stale-decision-22-citations-remaining.md`):
  `embarch-core` decision 22 is *only* the probe/board identity gate (live hardware-ID readback vs. a
  stale-able label), now implemented as `embarch-topology`'s `validate()`/enrollment mechanism — it is
  not about `known_boards.toml`'s file format, its `toml` crate version, or any HTTP route. Any
  `embarch-api` citation pairing decision 22 with an HTTP route, or with `known_boards`, is citing the
  wrong fact for that number.
- **`README.md:60`** (decision 23, env overrides removed) — confirmed correct against
  `decisions/probes.md`.
- **`README.md:108`** (`embarch-study-designer` decision 8, `embarch-topology` decision 13, path
  deps) — confirmed correct against both crates' `decisions/crate.md`.
- **`README.md:134`** (decision 6, bind default) — confirmed correct against `decisions/auth.md`
  **and** against the code: `src/main.rs` — `DEFAULT_PORT: u16 = 4884`, `DEFAULT_BIND: &str =
  "127.0.0.1"` — matches the README's stated default exactly.
- **`Cross.toml:3`** (`embarch-umbrella` decision 14) — confirmed correct against
  `decisions/install.md`.

No new bare cross-repo citation was introduced; the two repointed citations (`decision 43`,
`decision 19`) both keep their repo label.

## Done when

- [x] All nine citations in `Cargo.toml`, `README.md` and `Cross.toml` checked for existence, repo
      label, and whether the surrounding sentence is true.
- [x] `Cargo.toml:70`'s `decision 22` checked — real decision, wrong for this sentence, and no
      replacement decision exists to repoint to (see Results above); corrected the sentence instead
      of inventing a citation.
- [x] `README.md:134`'s bind address and port checked against the code, not only against decision 6.
- [x] Wrong numbers and false sentences reported as separate counts, with the total checked.
- [x] No new bare cross-repo citation introduced anywhere in the diff.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build`/`test`/`clippy -D warnings`
      clean in `embarch-core`; `scripts/check-docs.py` in `embarch-doc` is green except one pre-existing,
      out-of-scope red (`check-decision-refs.py` on `tasks/ui/058`'s own reference to an undefined
      decision number — already on `main` at this branch's base, a different sub-project, not
      touched by this unit).
