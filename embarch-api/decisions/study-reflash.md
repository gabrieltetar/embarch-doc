# embarch-api decisions: What a study flashes first

**Status:** active, 2026-09-11.

Reflash sequencing, and three gaps in `run_study`'s own contract.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The other half
of this split, reads: [study-reads.md](study-reads.md).

### 40 — A reflash selector, and this crate will not move an engineer's tree
`reflash` is `none` (default) / `dev-bench` / `dut` / `both`. Default `none` because flashing is the destructive-ish half and **a study that merely observes a board you just flashed by hand should not silently reflash it**.

**This crate never knowingly runs a tree-mutating `git` subcommand to reach a required version, and that is the load-bearing constraint.** "Reflash" means build and flash the tree **as it stands**, then verify what that produced — and fail, naming both, when it does not match. It does not mean "make my tree be that version". Manipulating an engineer's working tree to satisfy a test harness is a genuinely destructive act on the thing they are actively editing. The failure message says which revision the study wants; moving the tree there stays the engineer's decision. **[../spec.md](../spec.md) §2 carries that first sentence too; the restatement is deliberate** — an agent loading only `spec.md` has to meet the rule there.

**The rule is enforced against the config file too, not just this code.** `version_command` is somewhere `["git", "checkout", "v1.2.3"]` could plausibly be typed as an attempt at exactly that, so a `git` argv naming a tree-mutating subcommand is refused — **matching any argument rather than the one in subcommand position**, because a `-C` flag puts a path where the subcommand looks like it should be, and matching behind a shell/exec wrapper's own argv (`bash -lc "…"`, `env git …`) too, not just a bare `git` program. It over-rejects deliberately: a false positive costs renaming an argument, a false negative costs somebody's uncommitted work. An opaque program of the config's own (`./scripts/version.sh`) stays out of reach — this rule reads argv, not a script's contents.

**The two halves sequence differently, and the difference *is* the verification asymmetry showing up as control flow.** The bench is **flashed and then read back**, because its version is genuinely observable over the handshake, so verification is a measurement and can only follow the flash. The DUT is **verified and then flashed**, because nothing can be read back off it, so the only available check is against the tree about to be built — which means a study asking for a revision this tree is not at fails **without touching the board at all**.

Three smaller things only running it settles. **A bench reflash resets the bench**, and forgetting to would have looked like a link failure: flashing halts the core rather than starting it, so an unreset bench never answers the handshake. **The bench check is skipped when the study says `any`** — opening the link to confirm a vacuous comparison is a hardware touch for nothing. And **`project` appears exactly where it becomes meaningful**: a study is not project-shaped, but rebuilding a DUT's firmware is, so it is required only by a DUT reflash, and passing it where it means nothing is ignored rather than rejected.

**Where the DUT's version string comes from, stated as the limitation it is:** a project-declared command defaulting to the suite's `git describe` convention. **It describes the tree that was built, not the image running.** So "flashed this run" means "this run put the build of this tree on the board" — stronger than a declaration nobody checked, weaker than a measurement.

**Core's gate is live and independent**, so nothing here is the enforcement point: this adds the *choice* about what to do, and the chance to fail before doing something destructive.

### 44 — Three gaps in `run_study`'s own contract, and the tool text was the defect
Not design questions — the surface having been extended past the code that implements it. Recorded because **the tool text still described the old behaviour, which is what a caller reads**. All three are the same shape: **an input accepted, quietly discarded or skipped, and reported as success.**

**(a) A DUT reflash flashed and did not reset** — so a study asking to run against freshly-built firmware ran against **whatever was already on the board**, and reported a successful reflash while doing it. **Failure signature: "I flashed it and nothing changed."** Fixed; the bench half had always reset explicitly.

**(b) Resealing recomputed two of the study's three seals.** The third is a deliberate sibling, checked independently so a mismatch names which third is corrupt, and Core validates all three — but the reseal helper overwrote the first two, and the tool description and CLI help both said "both seals". **Every study to date had an empty protocol list, whose CRC is stable, so nothing noticed**; a study carrying a real protocol is rejected unless its author computed the third seal by hand. Fixed. **The regression test asserts against a non-empty list deliberately:** the empty-list CRC is 0, so a protocol-free study cannot distinguish "recomputed to 0" from "never written" — which is precisely how every existing test passed against a function that never touched the field.

**(c) `snippets` was accepted and silently ignored for a project with an explicit build command**, returning success having produced an image whose config said the corresponding option was not set. The CLI help already says snippets are only meaningful for a Zephyr-discovery project, and **that is documentation rather than a gate**. **Closed by [decision 51](zephyr.md): reject** — and the same check covers `board`/`variant`/`revision`/`app`/`extra_args`, discarded identically.
