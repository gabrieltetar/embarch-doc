# embarch-topology decisions: Scope and what got removed

**Status:** active, 2026-09-02.

What this models, what it refuses to model yet, and the override mechanism it deleted.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 7 — Declared facts can be unset, an ordinary state — but there is no general "topology hasn't been resolved yet" failure mode

Because auto-detectable topology is computed live on every call, **there is no file that can be missing or stale for it.** What *can* be unset is a human's declared intent — no board enrolled for a role, or no host declared for a remote Core — and calling a function that needs one returns **a specific error scoped to exactly the missing fact**, not a blanket dependency on having run this first for anything at all.

**Reversed**, same session: the earlier framing had `base_url = "auto"` and umbrella's `setup`/`doctor` **hard-depend on a resolved-state file existing, failing outright if this had not been run first** — a real breaking change to today's zero-config auto-detection, flagged at the time as needing its own onboarding migration. **That cost goes away under the live model:** local and WSL2-host detection need no prior declaration at all, so auto resolution keeps working out of the box, just backed by the shared crate instead of duplicated code.

### 9 — RETIRED: explicit-override detection

Originally a dedicated mismatch class for "an env var or registry override disagrees with what would otherwise resolve" — **precisely what caused the motivating incident.** Superseded by decisions 2 and 3: **every topology-shaped env var and registry override is abandoned outright, not merely checked for disagreement.** The auth token is unaffected — that is authentication, not topology.

**Removing the override mechanism is a stronger fix than detecting when it has gone stale: there is no longer anything that can silently win over reality, so there is nothing left in this category to detect.**

### 10 — Hardware topology scope: one DUT and one dev-bench per machine, today's real shape

Roles are modelled as an **extensible table rather than a hardcoded pair**, so adding a second board later is not a rewrite — but no logic for concurrent multi-DUT or dual-dev-bench scenarios is built, because those do not exist yet. **It did flag the risk that later came true**: a dev-bench sharing a chip family with the DUT. See decisions 20 and 21 for what actually happened when it did — the chip-family half turned out harmless, and **the half nobody anticipated was both boards having the same probe vendor and two serial interfaces each.**

### 11 — Software topology scope: the existing three classes; a LAN Raspberry Pi is an ordinary `remote`

The anticipated Pi move has not happened, and **giving it dedicated modelling ahead of that move would be building for a scenario that is not real** — the same reasoning as decision 10.

### 22 — A remote Core's declared host stays with each consumer; centralizing it here was examined and rejected

Every consumer declares it independently today, at different scopes: **per firmware repo for the API, per machine for umbrella.** **Two things would have to be true for centralizing to be an improvement rather than a migration nobody asked for:** a real disagreement or stale value actually observed causing a wrong connection, and a clear answer for *whose* scope wins when a repo-level override and a machine-level default genuinely differ. Neither is true.

**The reasoning cuts the other way too, and that is what makes this a rejection rather than a deferral:** the API deliberately did *not* centralize address resolution at setup time, precisely because **the value has to be right at the moment a build is flashed, not at the moment setup last ran.** A stored answer read by a third party is exactly that staleness risk — **a literal remote host is no more exempt from it than a dynamic gateway IP was** — so centralizing here would import the failure mode decisions 2 and 3 removed. Revisit only on a real wrong connection.

### 29 — No explicit invalidation signal; a caller re-resolves per operation instead

Considered and rejected, not merely undone yet: giving resolution/validation an explicit "this answer is now stale" push or token. **Every real caller already re-resolves fresh at the top of each operation** (spec.md, "What a caller may assume across calls"), so a signal would answer a question nobody holding an old answer actually asks. Revisit only if a caller shows up that must hold an answer across operations rather than re-calling.

### 30 — `CoreConfig`/`ProjectConfig` were never this crate's question, and it was already answered elsewhere by the time this crate existed to ask it

`open.md` carried a bullet since this crate's own extraction: "the config mirrors of `embarch-api`-internal logic are untouched by this crate's existence." That bullet was correct about the fact and wrong about where the fix belonged. **This crate models topology — role/link/probe facts — not Core's connection config**, so `CoreConfig`/`ProjectConfig` were never candidates for a topology-shaped extraction; the bullet lived here only because it was written the day this crate was cut, as the leftover half of the same "what does extracting topology *not* fix" thought.

**Why decision 15's topology precedent (`embarch-umbrella/decisions/mirrors.md`) does not transfer automatically:** that precedent's trigger for extraction was "a shared crate already had to exist for an unrelated reason, and the mirrored logic turned out to fit inside it" — a third consumer alone was explicitly *not* the trigger. `CoreConfig`/`ProjectConfig` have exactly two consumers (`embarch-api`, `embarch-umbrella`) and no crate that already has to exist for another reason; the "more machinery than the problem justifies" reasoning decision 15 first applied still holds for them on its own terms, unless and until something else forces a crate to exist anyway. Reading topology's extraction as precedent for these two would have been the same mistake decision 15 itself names: treating consumer count as the trigger instead of an incidental crate.

**The question was answered, just not by this crate and not by either of the two routes this bullet named.** `embarch-umbrella/decisions/mirrors.md` (decision 20, amended 2026-09-08 and 2026-09-10) resolved both structurally: `CoreConfig` now re-exports `embarch-core-client::CoreConfig` directly — the third answer, "call the owner," the same route `umbrella/036` took for the token half, not extraction and not a CI diff — and `ProjectConfig` (which lives inside `embarch-api`'s own binary, not a shared crate, so it cannot be re-exported the same way) is guarded by a fixture test in `embarch-umbrella` that parses `embarch-api`'s own `config.example.toml` through a `#[serde(deny_unknown_fields)]` shadow struct, failing the moment upstream adds a field this copy does not know about. `embarch-umbrella/open.md` no longer carries this bullet — it closed there on 2026-09-10, before this task was ever filed. This crate's `open.md` bullet was stale, not unresolved: it was tracking a question against a file that had already stopped asking it.
