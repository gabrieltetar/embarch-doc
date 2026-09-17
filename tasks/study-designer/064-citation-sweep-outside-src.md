# 064 — Citation sweep: outside `src/` (`tools/`, `tests/`, `.cargo/config.toml`)

**State:** open
**Source:** `tasks/study-designer/063`, which closed out `src/` (all twenty
files swept, `044` through `063`) and, per its own instruction to note what
else in the repo needs a citation check, found four files outside `src/`
that this chain has never swept.
**Scope:** study-designer
**Hardware:** none — source/config comments only.
**Owner:** no

## What

`grep -rlIE '[Dd]ecisions? [0-9]+' --include='*.rs' --include='*.toml' .`
(excluding `target/`) turns up, besides the twenty now-swept `src/` files and
`Cargo.toml` (re-confirmed correct by every unit from `061` on), four files
never checked by this chain:

```
8  tests/firmware_test_vectors.rs
7  tools/extract_gatt_config.rs
6  .cargo/config.toml
3  tests/eap_worked_protocols.rs
```

(Grep-matching *lines*, same caveat as every prior unit in this chain: not a
citation-instance count, and per `060`'s finding, not a complete count
either — the case-sensitive, singular-only, no-line-wrap grep undercounts. Read
every file, do not only grep it.)

**`.cargo/config.toml` is very likely the same dated-test-count comment
`053`/`059`–`063` tracked in `src/`'s sweep** ("Also worth doing" section of
those task files) — check whether it duplicates or is independent of
whatever `Cargo.toml`'s own hits say, and whether it still reads 125/125
(116 lib + 9 `firmware_test_vectors`) or has drifted again.

Take these four in the same order the size list suggests, or in whatever
order groups naturally (e.g. `tests/firmware_test_vectors.rs` and
`tests/eap_worked_protocols.rs` together, since both are integration tests).

## Method (carried over unchanged from `044`–`063`)

Read the cited decision's body, then the sentence around the citation, in
that order. Check every number and every implementation-status claim in the
cited sentence, not just the decision number. Count wrong numbers and false
sentences separately, report both honestly even if zero. Check cross-repo
labelling first (a bare `decision N` is same-repo by convention); for every
cross-repo citation, also ask whether a same-repo decision already says the
same thing. Read a cited section to its end before judging it off-topic or
correct.

**`063`'s find, carried forward: a wrong number does not require a dramatic
shape to hide in — it can just be a plain wrong number, repeated.** Four
citations across `src/gatt_names.rs` and `src/vendor.rs` cited "decision 57"
(`decisions/gatt-extract.md`, "The extraction scans the repo, not two files
it was told about" — about repo-walk scope, ignore files, and failure
modes) for claims about **service naming and vendor-wins precedence**,
content that is actually decision 56's ("A characteristic gets a name..." —
whose own body states "Services get names by the same mechanism... Two maps
rather than one, because a merged map would have to guess which lookup a
UUID wanted", nearly verbatim against the citing sentences). All four fixed
to decision 56. Unlike `062`'s same-repo-near-duplicate shape (two different
real sentences citing two different real decisions), this was one number,
wrong everywhere it appeared for this specific claim, in two different
files — worth checking whether the same pattern recurs in these four
un-swept files.

Also still carried forward: `056`'s find (a wrong number that's real,
on-topic, cross-repo, and correctly labelled, shadowed by a nearer
same-repo decision saying the same thing), `058`'s find (a citation number
to a real, existing decision that still never said what the comment
claims), `059`'s find (a citation correctly labelled cross-repo, naming the
wrong decision within that repo/file), `055`'s find (a false sentence
misattributing *where* a feature runs, not just which decision covers it).
See `tasks/study-designer/056`–`062`'s copies of these paragraphs for full
accounts.

**Run the continuation-grep fresh, whole-repo, singular-inclusive:**
`grep -rlIE '[Dd]ecisions?[[:space:]]*$'`. As of `063` it hits the same nine
files it has hit since `062` (`Cargo.toml` plus eight `src/` files), all
fully checked — a fresh run for this unit is expected to add nothing unless
one of these four new files gains a hit.

## Done when

- [ ] `tools/extract_gatt_config.rs`, `tests/firmware_test_vectors.rs`,
      `tests/eap_worked_protocols.rs`, `.cargo/config.toml` all fully swept,
      wrong numbers and false sentences counted separately per file.
- [ ] Cross-repo citations carry their repo name and are checked per the
      method above.
- [ ] Continuation-grep run fresh, any hit reported.
- [ ] Say plainly whether any citation-bearing file remains unswept anywhere
      in the repo after this unit (a fresh whole-repo grep, not this task's
      list, is the source of truth).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment with the same three numbers
      (citation instances checked, wrong numbers, false sentences).

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` are both in the last 10% of
their caps, filed as `tasks/study-designer/032`/`026`, both blocked. As of
`063` neither needed touching for a comment sweep; check fresh
(`scripts/check-doc-size.py --pressure`) rather than trusting this note.
