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
