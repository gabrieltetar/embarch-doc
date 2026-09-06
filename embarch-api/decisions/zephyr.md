# embarch-api decisions: Target discovery and selection

**Status:** active, 2026-09-05.

The one scoped exception where this crate had to learn Zephyr: what a call may name, what that resolves to against the repo as it stands, and what is refused rather than ignored.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). How a build then runs and what it produces: [build.md](build.md).

### 12 — Live target discovery for Zephyr projects; every other build system keeps the static schema
A Zephyr board's buildable surface is a property of the **current** state of `boards/*/board.yml` and `app/*/`, not something safe to snapshot into config once — and not every combination `board.yml` *declares* is real. So a `zephyr-west` project stores only what cannot be derived from the repo, and board, variant, revision, app, chip, build directory and artifact path all resolve live per call, **never cached**: caching would reintroduce the exact staleness this exists to eliminate.

**The one existing principle this scopes an exception into**, stated rather than glossed: decision 5's "no toolchain-specific logic" stays true for *how* a command runs and for every non-Zephyr project unconditionally — but this crate now has to understand Zephyr's board-qualifier grammar and file conventions well enough to assemble an argv. A deliberate, scoped cost, not a reversal.

Shapes, semantics and the narrowing rules: [../interfaces/config.md](../interfaces/config.md).

### 13 — `soc_chip_overrides`, an escape hatch for a SoC Core cannot map (retired unbuilt 2026-09-05, no replacement)
A per-project `{soc, chip}` list consulted *before* `POST /resolve-chip`: a hand-resolved SoC had somewhere to live, and a hit skipped the call. **Never implemented**: no field, an unconditional call, no `deny_unknown_fields`, so the key was silently dropped on *both* discovery kinds — decision 20's shape 1 again, found by `api/016`.

**Retired because the short-circuit was the design and is the defect.** Core validates every mapping against probe-rs's registry (`embarch-core` decision 8), so a hit here skips that check: one typo reaches `/flash` as a plausible chip name and attaches the wrong physical target, which is what decision 8 refused fuzzy matching to avoid. And it is per-project for a per-silicon fact, consulted *first* — restated per project and per repo, and still winning after Core's table is fixed.

***Rejected: build it anyway.*** The dead end is real — a 404 naming the SoC, nowhere to put the answer — but bounded: one row in the repo that owns the table plus a redeploy this suite already runs, and no unmapped SoC in three months. **What reverses this:** a Core the operator cannot rebuild; the hatch then belongs in Core's own config, machine-scoped and still registry-validated, not in a per-project field here.

Declaring the key is now **refused at load naming the retirement**, on both kinds, pointing at Core's table and `chip-list` — decision 53's posture.

### 20 — `default_target`, the narrowing caveat stated, and what a `static` project is refused at load
Decision 12's narrowing means **a call that works today can start erroring the moment a second board lands in the repo** — silently, as the repo grows. Fixed by a per-project base selection applied before a call's own params narrow further. It was config [open.md](../open.md) stated as truth and nothing implemented ([../../embarch-decision-reversals.md](../../embarch-decision-reversals.md) shape 1); **built, not retired**, because the failure it prevents is silent and arrives in somebody else's commit. Three calls:

- **Per field, not all-or-nothing.** A call naming `board` overrides this default's `board` and nothing else. *Rejected: a call-time param discarding the whole default* — that turns "narrow to the other revision" into "restate every axis".
- **A selection error names what the default supplied**, or the surprise returns one layer down: a caller who gave one field reading `no target matches the given board/variant/revision/app` about three it never gave.
- **Refused at config load for a `static` project, and when empty** — decision 51 rejects these on a *call* to one, so failing at load beats failing at every use.

**That refusal covers the class, not `default_target` alone.** It shipped naming one field while `default_snippets`, `default_extra_args`, `west_binary` and `build_dir_root` were **equally unhonourable on a `static` project and loaded silently** — an asymmetry nobody decided, and a trap for whoever adds the sixth field. All five are refused together, one message naming each that is set, mirroring the `zephyr-west` arm's refusal of `build_command`/`chip`/`artifact_path`. `soc_chip_overrides` is *not* in the set — retired unbuilt instead, with its own both-kinds refusal (decision 13).

- ***Rejected: narrow instead*** — let `default_target` go silent too, so the class is consistent the other way. Breaks nothing, and deletes the one member already behaving correctly. A silently dropped setting's cost is decision 44c's measured one: a build reporting success having produced an image whose config says the option was unset.
- ***Rejected: warn rather than refuse***, the only shape that is both consistent and non-breaking. This binary's normal mode is an MCP server whose stderr nobody reads, so the warn lands nowhere for exactly the operator it exists for — and it would make a **third** posture for one class of config mistake, beside this refusal and decision 53's.
- **The breaking config change is accepted, not overlooked.** A config carrying one of the four loads today and stops, with no deprecation window ([../../embarch-dev-workflow.md](../../embarch-dev-workflow.md) §6). Bounded because the break is loud, immediate, at load, and names the field and both remedies — unlike the silence it replaces. Decision 53 took the same cost for `[[projects.targets]]` on the stronger ground that those rows actively advertised a choice; these four are merely inert, **which is the state an author cannot see.**

### 21 — A sentinel forces "no snippets" over a configured default
There was no third state between "use the default" and "use this explicit list". `["none"]` is the reserved literal; [../interfaces/config.md](../interfaces/config.md) carries the rule. Built alongside decision 20 and for its reason — the doc stated this while `["none"]` really resolved as `unknown snippet(s) ["none"]`. Why there was no third state is decision 51's: an empty call-time list is indistinguishable from an omitted one through the plain slice `Selection` carries.

**"Reserved" is checked now, not asserted.** The original reasoning — that the literal *cannot* collide, snippet names being directory-derived identifiers — was wrong: nothing stops a directory under `app/<app>/snippets/` being named `none`. So three refusals rather than one convention: a list **mixing** the literal with real names, `["none"]` against an app that really **declares** a snippet called `none`, and `"none"` inside `default_snippets` — that last a **config-load** error, since as a default it says what omitting the field already says, and a config line reading as meaningful while doing nothing is what this work existed to remove.

**The collision message's remedy is conditional, and now says which case it is in.** It offered "rename that snippet, or omit `snippets` to take the configured `default_snippets`" unconditionally — but omitting yields the empty set the caller asked for only when that default is *empty*, and the config edit it invites next, the literal in `default_snippets`, is the load error the bullet above added. **Half the advice routed the reader into a second refusal.** `resolve_snippets` holds the default, so it branches: none configured, both remedies; one configured, renaming named as the only one and the other two paths named as the dead ends they are. Decision 51's surface-text rule — naming an unreachable remedy is worse than naming one reachable one.

### 22 — The uncached scan's cost bound is written down
Decision 12 never caches, reasoned as "already cheap enough", and **no bound was ever stated for what that assumes**. Stated: single-digit boards, low tens of variant/revision/app combinations, low hundreds of files, comfortably sub-100 ms on ordinary local storage. A repo an order of magnitude larger has not been measured — if the scan ever becomes perceptibly slow, *that* is the signal to revisit caching, not a reason to add it pre-emptively.

### 51 — A static project rejects a selection it cannot honour, rather than ignoring it
`resolve` branches on `discovery`, and the `static` arm took the `ProjectConfig` alone: **every one of `board`, `variant`, `revision`, `app`, `snippets` and `extra_args` was accepted and dropped**, and the build reported success. Decision 44c recorded the observed cost for `snippets` — a build with two of them returned success having produced an image whose config said the option was unset — and left the fork open. **Verified before widening the fix**: nothing upstream honoured the other five either — all four param structs (`TargetSelection`, `TargetParams`, `FlashParams`, `RunStudyParams`) do nothing with them but hand them to `resolve` — so all six were one defect and all six are refused together.

**Reject, not splice**, which was the fork decision 44c named. A `static` project's `build_command` is an opaque hand-authored argv this crate did not assemble: there is no `-S` to add to it and no scan to narrow, so splicing would mean guessing at another build system's flag grammar — the exact thing decision 5 exists to keep out and decision 12 admitted only as a scoped Zephyr exception. Refusing costs a caller one error and a re-run; splicing wrongly costs a flashed board and a wrong answer nobody can see.

**Absent stays absent.** An omitted param and an explicitly empty list are indistinguishable through the plain slices `Selection` carries — and for a `zephyr-west` project empty already means "use the configured default" — so "given" is `Some(_)` or a non-empty slice, and a call passing nothing resolves byte-for-byte as before. That half is asserted over the whole `Resolved`, not just the error path.

**The `[[projects.targets]]` menu is gone too** ([shape.md](shape.md) 53): a `static` project has exactly one target — itself — and a config still declaring the table fails at load. This entry is why there is nothing to lose by it: a menu pays for itself only if something narrows against it, and the arm that would have narrowed accepted the params and dropped them.

The help text already said these were Zephyr-only; this is that sentence made mechanical, and the tool descriptions, CLI help and `config.example.toml` now say *refused* rather than *ignored* — decision 44's lesson that surface text is what a caller reads.
