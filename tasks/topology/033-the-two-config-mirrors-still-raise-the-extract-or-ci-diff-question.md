# 033 — `CoreConfig`/`ProjectConfig` still mirror `embarch-api` internals, and the extract-or-CI-diff question is unanswered

**State:** claimed by agent/topology/033-config-mirrors, 2026-09-12 01:32
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

- [ ] One of the answers above is implemented, or the duplication is kept with a **named trigger**.
- [ ] The choice is a numbered decision, and it says why the topology precedent does **not**
      automatically apply — that is the part the open bullet got right and that a later reader will
      otherwise re-derive wrongly.
- [ ] If a CI diff: it is mutation-checked — changing one copy turns it red and names both files.
- [ ] `embarch-topology/open.md`'s bullet is struck.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green; gate green;
      `changelog.d/` fragment.
