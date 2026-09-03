# embarch-api decisions: Build orchestration and target discovery

**Status:** active, 2026-09-03.

A generic build command, and the one scoped exception where this crate had to learn Zephyr.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 5 — A generic configurable command per project, not toolchain-specific logic
Originally motivated by an assumption that the two day-one projects used different toolchains. On inspection **both turned out to be Zephyr/west-based** — one reads as an Arduino board by name and its own `board.yml` confirms otherwise, confirmed by reading the real repo rather than assuming from the name. The generic design is kept regardless: it is the right call on its own merits, even though the two-toolchain premise did not hold.

### 12 — Live target discovery for Zephyr projects; every other build system keeps the static schema
A Zephyr board's buildable surface is a property of the **current** state of `boards/*/board.yml` and `app/*/`, not something safe to snapshot into config once — and not every combination `board.yml` *declares* is real. So a `zephyr-west` project stores only what cannot be derived from the repo, and board, variant, revision, app, chip, build directory and artifact path all resolve live per call, **never cached**: caching would reintroduce the exact staleness this exists to eliminate.

**The one existing principle this scopes an exception into**, stated rather than glossed: decision 5's "no toolchain-specific logic" stays true for *how* a command runs and for every non-Zephyr project unconditionally — but this crate now has to understand Zephyr's board-qualifier grammar and file conventions well enough to assemble an argv. A deliberate, scoped cost, not a reversal.

Shapes, semantics and the narrowing rules: [../interfaces/config.md](../interfaces/config.md).

### 13 — `soc_chip_overrides`, an escape hatch for a SoC Core cannot map
Decision 12 removed the stored chip field entirely for a Zephyr project, and Core's resolver returns a 404 naming the unmapped SoC — but there was **nowhere to write the answer** once `chip-list` found the right string. Consulted *before* the HTTP call, so a hit short-circuits it entirely: no reason to ask Core about a SoC the operator already resolved by hand. Keeps Core's table as the source of truth for the common case while giving the uncommon one a real fix instead of a dead end.

### 19 — A readable build-dir prefix, and a `target.json` beside the output
`extra_args` folds into the directory name via a hash, since an arbitrary flag can contain directory-unsafe characters — but **a bare hash makes a directory listing undebuggable to a human staring at it**. Two additions without touching the hash: every other axis spelled out ahead of it, and a `target.json` recording the full resolved selection, so `cat target.json` recovers exactly what produced that directory.

### 20 — `default_target`, and the narrowing caveat stated rather than left implicit
Decision 12's narrowing means **a call that works today can start erroring the moment a second board lands in the repo** — behaviour changing silently as the repo grows, with nothing warning a reader. Stated here explicitly, and given a fix: a per-project base selection applied before a call's own params narrow further, so a repo's common case stays stable after a second target appears.

### 21 — A sentinel forces "no snippets" over a configured default
There was no third state between "use the default" and "use this explicit list". `["none"]` is the reserved literal — chosen because it cannot collide with a real snippet name, those being directory-derived identifiers. **Any other list containing `"none"` is a call-time error naming the ambiguity**, rather than a silently-wrong interpretation.

### 22 — The uncached scan's cost bound is written down
Decision 12 never caches, reasoned as "already cheap enough", and **no bound was ever stated for what that assumes**. Stated: single-digit boards, low tens of variant/revision/app combinations, low hundreds of files, comfortably sub-100 ms on ordinary local storage. A repo an order of magnitude larger has not been measured — if the scan ever becomes perceptibly slow, *that* is the signal to revisit caching, not a reason to add it pre-emptively.

### 42 — `base_address` is a per-project config field, not a per-call parameter
A `bin` artifact carries no address, so flashing one needs an offset, and this crate had no way to supply it. **The consequence was concrete rather than theoretical:** a validation flashed via a hand-written call straight to Core, bypassing this crate entirely for that step, because there was no config-driven path through it.

It wins the same argument `flash_format` already won: the offset is a fact about how the project builds, not something varying call to call, so **an agent should never have to know a hex number to flash a board**. *Rejected: a per-call parameter, and a config-default-with-override.* The override shape has a real precedent here — `--firmware-path` overrides the configured artifact — but that flag exists to flash *something other than what the project builds*, which is a genuinely per-call intent. An offset is not.

Opaque pass-through, like chip and format: this crate does not validate it against the target's memory map. Two shape details that were not free choices: the field is a **TOML integer** using TOML's own hex literal while Core takes a hex-or-decimal *string*, so the round trip lands a config-driven flash on byte-identical wire form to a dev-bench flash; and **a `bin` project that omits it is not a config-load failure**, despite being wrong in practice, because enforcing it is one step from validating the offset itself.

### 51 — A static project rejects a selection it cannot honour, rather than ignoring it
`resolve` branches on `discovery`, and the `static` arm took the `ProjectConfig` alone: **every one of `board`, `variant`, `revision`, `app`, `snippets` and `extra_args` was accepted and dropped**, and the build reported success. Decision 44c recorded the observed cost for `snippets` — a build with two of them returned success having produced an image whose config said the option was unset — and left the fork open. **Verified before widening the fix**: nothing upstream honoured the other five either, since both front-ends do nothing with these params but hand them to `resolve` (`TargetSelection::selection`, `TargetParams::selection`, `FlashParams::selection`, `RunStudyParams::selection`), so all six were the same defect and all six are now refused together.

**Reject, not splice**, which was the fork decision 44c named. A `static` project's `build_command` is an opaque hand-authored argv this crate did not assemble: there is no `-S` to add to it and no scan to narrow, so splicing would mean guessing at another build system's flag grammar — the exact thing decision 5 exists to keep out and decision 12 admitted only as a scoped Zephyr exception. Refusing costs a caller one error and a re-run; splicing wrongly costs a flashed board and a wrong answer nobody can see.

**Absent stays absent.** An omitted param and an explicitly empty list are indistinguishable through the plain slices `Selection` carries — and for a `zephyr-west` project empty already means "use the configured default" — so "given" is `Some(_)` or a non-empty slice, and a call passing nothing resolves byte-for-byte as before. That half is asserted over the whole `Resolved`, not just the error path.

The help text that already said these were Zephyr-only was documentation rather than a gate; this is that sentence made mechanical, and the tool descriptions, CLI help and `config.example.toml` now say *refused* rather than *ignored* — decision 44's own lesson that the surface text is what a caller reads.
