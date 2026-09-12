# 033 — `CoreConfig`/`ProjectConfig` still mirror `embarch-api` internals, and the extract-or-CI-diff question is unanswered

**State:** done by agent/topology/033-config-mirrors, 2026-09-12
**Source:** `embarch-topology/open.md` — "**The config mirrors of `embarch-api`-internal logic are
untouched by this crate's existence** and still raise the extract-or-CI-diff question
independently. … **`CoreConfig`/`ProjectConfig` mirror internals, not a shared concern the way
topology turned out to be.**"
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

Two config types duplicate logic that lives inside `embarch-api`. `embarch-topology`'s own
existence did **not** answer this, and the open bullet says so explicitly and correctly: topology
turned out to be a genuinely shared concern, and these two are not — so "extract them into this
crate too" is the answer that looks obvious and probably is not.

Three answers are already known in this suite, and one of them has been taken before:

1. **Extract** into a shared crate — the topology route, and the one the bullet doubts.
2. **A CI diff** that fails when the two copies disagree — cheap, and honest about being a mirror.
3. **Call the owner directly**, which is what `umbrella/036` did for its own instance of this.

Pick one, implement it, and record which and why. **Answering "leave the duplication, here is the
trigger that would change that" is also a real answer** if it is written down with the trigger.

## Why now

The bullet has survived the one event that might have resolved it — this crate being created — and
is now the clearest unanswered structural question in `embarch-topology/open.md`. It is entirely
host-side: two type definitions and whatever check is chosen.

## Done when

- [x] One of the answers above is implemented, or the duplication is kept with a **named trigger**.
      **Finding: already implemented, and not by this crate.** `CoreConfig`/`ProjectConfig` are
      `embarch-umbrella`'s types mirroring `embarch-api`, never `embarch-topology`'s own code — this
      bullet lived in `embarch-topology/open.md` only as leftover phrasing from the day this crate
      was cut. `embarch-umbrella/decisions/mirrors.md` decision 20 (amended 2026-09-08 and
      2026-09-10, before this task was filed) already closed both strands: `CoreConfig` re-exports
      `embarch-core-client::CoreConfig` directly (answer 3, "call the owner", the same route
      `umbrella/036` took for the token half), and `ProjectConfig` — which lives inside
      `embarch-api`'s own binary, not a shared crate — is guarded by a fixture test that parses
      `embarch-api`'s `config.example.toml` through a `deny_unknown_fields` shadow struct.
      `embarch-umbrella/open.md` no longer carries this bullet.
- [x] The choice is a numbered decision, and it says why the topology precedent does **not**
      automatically apply. `embarch-topology` decision 30 (`embarch-topology/decisions/scope.md`).
- [x] If a CI diff: it is mutation-checked — changing one copy turns it red and names both files.
      N/A — the answer taken (elsewhere) was direct re-export + fixture test, not a CI diff.
- [x] `embarch-topology/open.md`'s bullet is struck.
- [x] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green; gate green;
      `changelog.d/` fragment. No source change was needed in this repo — the fix, and the code it
      touches, are entirely `embarch-umbrella`'s and already landed there.

## Note for the supervisor

This task's premise assumed the question was still open and belonged partly to `embarch-topology`.
Neither held: the two config types are `embarch-umbrella`/`embarch-api` code, and the question was
already answered in `embarch-umbrella` on 2026-09-10 (decision 20's amendments), before this task
was filed on 2026-09-12. The only real work here was recognizing that and striking the stale bullet
with a decision explaining why. No `embarch-api` or `embarch-umbrella` change was made or is needed;
nothing to drop in `inbox/`.
