# embarch-umbrella decisions: The liftable-copy pattern

**Status:** active, 2026-09-02.

Two consumers, one algorithm, and what happened when a shared crate had to exist anyway.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 15 — Topology detection is written once here in a deliberately liftable shape, not extracted into a shared crate

`embarch-api` needs the identical candidate-ordering and probe logic, so there were exactly two consumers and one algorithm. **A fourth Rust crate in the suite, versioned and released, to hold one function that takes a candidate list and returns which one answered, is more machinery than the problem justifies at this scale.**

The alternative accepted instead: one self-contained module, written under a constraint — **no umbrella-specific types cross its boundary.** No CLI structs, no config types, no error context strings that only make sense in a `doctor` run; just pure functions over plain inputs returning plain outputs. **That constraint is what makes it copyable verbatim, and what makes extracting it later a move rather than a rewrite.**

**The honest cost is drift: two copies that must agree, with nothing mechanical enforcing it.** Three things kept that visible rather than silent — the module carried a comment naming its mirror, its unit tests were copied alongside it (pure-function tests port with no adaptation), and **`doctor` reported *which candidate won* rather than just pass/fail, so a divergence surfaced as two different answers on the same machine instead of as a mystery.**

**Reversed.** The "more machinery than the problem justifies" reasoning held for exactly this one function with two consumers; **it stopped holding once `embarch-topology` had to exist anyway for an unrelated reason** — hardware topology — and software topology turned out to fit the same crate. **A third consumer was not the trigger; the trigger was that a shared crate already had to exist**, at which point copying this logic a second time inside it had no remaining justification. This decision's own boundary constraint is exactly what made the move trivial: **the pure functions moved across completely unchanged, tests included.**

### 16 — `doctor`'s token check needed the same treatment, and so did its config reading

**A `doctor` that resolved the token differently than the `embarch-api` it is diagnosing would produce checks that pass or fail for reasons unrelated to the real thing, which is worse than no check.** So the token logic is a liftable copy of `embarch-api`'s own.

The config-shape checks needed the same, applied to config rather than tokens: a mirror of `embarch-api`'s tables **minus the fields nothing here reads** (TOML tolerates the extras since neither struct denies unknown keys), but **skipping `embarch-api`'s own validation, since `doctor`'s entire job is reporting what is wrong rather than failing fast on the first bad field.**

**Two implementation details worth recording because they were not obvious going in.** Comparing a WSL2 path against its Windows-visible form means **reverse-translating the UNC form back to a `/`-rooted path and comparing canonicalized paths** — not literally stat-ing the UNC string, **which is not a path WSL2's own filesystem namespace resolves.** It verifies anything only when the UNC's embedded distro name matches this one's; otherwise it reports "cannot verify from here" **rather than guessing.** And a config that still declares an explicit address rather than auto-detection **makes `doctor` probe exactly that address**, or `doctor` could end up diagnosing a *different* Core than the one `embarch-api` would actually talk to.

### 20 — The pattern gets a CI job diffing the mirrors against their source, instead of extracting a fourth crate

Three modules lived in this pattern, and **the original one-function/two-consumers rationale is stretched thinner with each addition** — while unpublished-git-dependency distribution had already been established as cheap in this suite, **which weakens the "a fourth crate is too much machinery" argument that justified copying in the first place.** Resolved without reversing course: rather than extract a common crate now, a CI job fetches the source file from the other repo at the commit the local copy's own header names, diffs it, and fails the build on any difference — **replacing "a comment and hope" with an actual mechanical check.** A fourth module joining the pattern is the trigger to reconsider the crate, not before.

**Never actually implemented — the workflow does not exist in this repo — and now permanently moot for one of the three modules but not the other two.** Decision 15's reversal means there is **no topology-detection copy left for a diff job to guard.** That narrows "three modules" to two: the token and config mirrors, still hand-mirroring `embarch-api`'s internals, **so the crate-versus-CI-diff question stays open for those two specifically rather than closed outright.** Extracting `embarch-topology` did not extend to them because **they mirror `embarch-api`-internal logic, not a shared concern the way topology turned out to be.**
