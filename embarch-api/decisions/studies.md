# embarch-api decisions: Submitting and orchestrating studies

**Status:** active, 2026-09-03.

Seals, the MCP schema that read as "anything", reflash sequencing, and three gaps in run_study's own contract.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 27, 28 — Validate capacities and fill the seals before the HTTP call
Capacity validation lived only in Core, but **this crate is the one holding the file** for a `--study-file` submission — so a JSON exceeding a bound failed with a raw deserialize error here, before Core's friendlier field-naming message ever ran. And the seals are computed and overwritten here, so a hand-authored study **no longer needs a human to compute a CRC by hand**, closing the gap between the integrity check and the suite's symmetric-human/agent principle. Recomputation is idempotent, so a caller that already computed a correct value is unaffected. Core's own checks are unchanged and stay the authoritative, un-bypassable gate for any other caller.

**Decision 27 is only partially realised** ([../open.md](../open.md)): oversized submissions *are* rejected before the HTTP call, but by `serde`'s own raw error rather than the friendlier field-naming message this decision described.

### 30 — A named smoke-harness tier, because the real methodology was unnamed
**Every real bug found in this project to date came from a live run** against a real Core or a real repo, not from the still-unwritten unit-test suite. That is a real, working methodology, just an unnamed and unrepeatable one. So it gets a name and a script: a throwaway Core instance plus a synthetic fixture repo, re-running a fixed sequence of calls. Not a substitute for the mocked unit tests, which remain the acceptance criteria below the process boundary.

### 31, 33 — `run_study`'s schema declares an object, and the handler tolerates a stringified one
*(One decision under two numbers: the commit that added decision 32 inserted it in the middle and renumbered the entry below it. Both numbers resolve here; neither is reused. [../decisions.md](../decisions.md) has the shape of that breakage.)*

`serde_json::Value`'s own generated JSON Schema is the literal `true` — "matches anything", with **no `type` key at all** for a client to key off. At least one real client, this suite's own daily driver, read that as "no declared shape" and sent the entire study **JSON-encoded as a string** rather than an inline object, failing deserialization with a confusing "expected struct, got a string".

**A failure mode the CLI path structurally cannot hit**, since `--study-file` parses the file directly with no schema involved — which is why MCP coverage cannot be implied by CLI coverage here. **Fixed two ways:** the schema is overridden to declare an object, for clients that read the type; and the handler unwraps a string by parsing it as JSON first, for those that do not.

### 39 — The manifest rides the build, and one parameterised stream tool replaces three
**The manifest is a build output, so this repo is the only place that can see it.** A DUT firmware repo built with the outpost module emits it next to its artifact; Core needs it to decode a trace and can never produce it. So the flash carries it — no new user-facing step and nothing to remember, **because the failure mode of forgetting is silent mislabelling** and the only reliable fix is for the manifest to travel with the build that produced it. Absent, it is simply not sent; that is the normal case, not an error.

**Derived from the firmware path rather than added as a parameter, and that follows from the reasoning above.** A parameter is a thing a caller can forget, and there are a dozen flash call sites across the two front-ends and the reflash path — every one a place to forget it. A rule applied inside the client cannot be. It also means nothing needs to know which board it is talking to: a dev-bench build leaves no manifest beside its artifact, so none is sent.

**This inherits the artifact-transfer gap in a second place and does not fix it** — a remote Core cannot see a local path, and the manifest rides the same route into the same wall. Named here rather than discovered later.

`study_stream_data` replaces the three fixed per-channel tools, mirroring Core's collapse of three routes into one parameterised one. **The three stay as aliases for one release** rather than breaking an agent's working invocation mid-flight. `list_study_streams` names what a study actually captured, since an agent that must *guess* a tap name to read one has been handed a worse tool than it had. Two rules the implementation settled:

- **`truncated` is what the listing is *for*.** It is set both by a retention rotation deleting a segment and by a close reporting a non-zero drop count — two different losses a reader cares about identically. A listing that dropped the flag would hand back a capture that reads complete and is not, which is worse than no listing.
- **The aliases' descriptions were updated, not frozen.** The don't-move-ground-under-a-live-client posture protects a *working invocation* — same name, same params, same bytes. **It does not protect stale prose**, and one alias's text still described an `Action` retired several schema versions earlier. Leaving a description that is simply false is the mislabelling class this whole area keeps closing.

### 40 — A reflash selector, and this crate will not move an engineer's tree
`reflash` is `none` (default) / `dev-bench` / `dut` / `both`. Default `none` because flashing is the destructive-ish half and **a study that merely observes a board you just flashed by hand should not silently reflash it**.

**This crate never runs `git checkout` to reach a required version, and that is the load-bearing constraint.** "Reflash" means build and flash the tree **as it stands**, then verify what that produced — and fail, naming both, when it does not match. It does not mean "make my tree be that version". Manipulating an engineer's working tree to satisfy a test harness is a genuinely destructive act on the thing they are actively editing. The failure message says which revision the study wants; moving the tree there stays the engineer's decision.

**The rule is enforced against the config file too, not just this code.** `version_command` is somewhere `["git", "checkout", "v1.2.3"]` could plausibly be typed as an attempt at exactly that, so a `git` argv naming a tree-mutating subcommand is refused — **matching any argument rather than the one in subcommand position**, because a `-C` flag puts a path where the subcommand looks like it should be. It over-rejects deliberately: a false positive costs renaming an argument, a false negative costs somebody's uncommitted work.

**The two halves sequence differently, and the difference *is* the verification asymmetry showing up as control flow.** The bench is **flashed and then read back**, because its version is genuinely observable over the handshake, so verification is a measurement and can only follow the flash. The DUT is **verified and then flashed**, because nothing can be read back off it, so the only available check is against the tree about to be built — which means a study asking for a revision this tree is not at fails **without touching the board at all**.

Three smaller things only running it settles. **A bench reflash resets the bench**, and forgetting to would have looked like a link failure: flashing halts the core rather than starting it, so an unreset bench never answers the handshake. **The bench check is skipped when the study says `any`** — opening the link to confirm a vacuous comparison is a hardware touch for nothing. And **`project` appears exactly where it becomes meaningful**: a study is not project-shaped, but rebuilding a DUT's firmware is, so it is required only by a DUT reflash, and passing it where it means nothing is ignored rather than rejected.

**Where the DUT's version string comes from, stated as the limitation it is:** a project-declared command defaulting to the suite's `git describe` convention. **It describes the tree that was built, not the image running.** So "flashed this run" means "this run put the build of this tree on the board" — stronger than a declaration nobody checked, weaker than a measurement.

**Core's gate is live and independent**, so nothing here is the enforcement point: this adds the *choice* about what to do, and the chance to fail before doing something destructive.

### 44 — Three gaps in `run_study`'s own contract, and the tool text was the defect
Not design questions — the surface having been extended past the code that implements it. Recorded because **the tool text still described the old behaviour, which is what a caller reads**. All three are the same shape: **an input accepted, quietly discarded or skipped, and reported as success.**

**(a) A DUT reflash flashed and did not reset** — so a study asking to run against freshly-built firmware ran against **whatever was already on the board**, and reported a successful reflash while doing it. **Failure signature: "I flashed it and nothing changed."** Fixed; the bench half had always reset explicitly.

**(b) Resealing recomputed two of the study's three seals.** The third is a deliberate sibling, checked independently so a mismatch names which third is corrupt, and Core validates all three — but the reseal helper overwrote the first two, and the tool description and CLI help both said "both seals". **Every study to date had an empty protocol list, whose CRC is stable, so nothing noticed**; a study carrying a real protocol is rejected unless its author computed the third seal by hand. Fixed. **The regression test asserts against a non-empty list deliberately:** the empty-list CRC is 0, so a protocol-free study cannot distinguish "recomputed to 0" from "never written" — which is precisely how every existing test passed against a function that never touched the field.

**(c) `snippets` was accepted and silently ignored for a project with an explicit build command**, returning success having produced an image whose config said the corresponding option was not set. The CLI help already says snippets are only meaningful for a Zephyr-discovery project, and **that is documentation rather than a gate**. **Closed by [decision 51](zephyr.md): reject** — and the same check covers `board`/`variant`/`revision`/`app`/`extra_args`, discarded identically.
