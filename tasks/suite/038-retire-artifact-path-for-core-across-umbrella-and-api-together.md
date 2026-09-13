# 038 — Retire `artifact_path_for_core` in `embarch-umbrella` and `embarch-api` in one change, or record why it stays

**State:** open
**Source:** leg 110's refill sweep, 2026-09-13, from the **"Ends when"** clause of `embarch-api`
decision 64 (`embarch-api/decisions/shape.md:58`) rather than from anything a leg observed — the
decision named its own retirement condition and nothing has been filed against it.
**Scope:** suite — `embarch-api` and `embarch-umbrella` must move together; neither half is legal
alone, and both decision bodies say so.
**Hardware:** none to decide and implement. See "The one thing an agent cannot settle" below for
why this may still need the owner.
**Owner:** no — but read the last section before dispatching.

## What

`artifact_path_for_core` is a `[[projects]]` config field that `embarch-api` **retired** (its
decision 15) and no longer reads. Three things still reference it:

| repo | site | what it does |
|---|---|---|
| `embarch-api` | `src/config.rs:278`, `:287` | tolerates the key at load — no `deny_unknown_fields` on `ProjectConfig`, so it loads silently unread |
| `embarch-umbrella` | `src/init.rs:534` | **scaffolds** it, for a static project on a WSL2 split |
| `embarch-umbrella` | `src/doctor.rs:1399`–`:1497` | **check 9** reads it and compares its UNC form against `artifact_path` |

Plus `src/config.rs:101` (the field itself) and `src/init.rs:136` (`wsl_unc_path`).

**Each repo's decision correctly refuses to act alone, and the refusals interlock.**

- `embarch-api` decision 64 tolerates the key *because* umbrella still scaffolds it, and states
  plainly: *"**Ends when:** `embarch-umbrella` stops scaffolding `artifact_path_for_core` and no
  config in the field still carries it — then refuse it too, as a separate load-behaviour task this
  decision does not authorize."*
- `embarch-umbrella` decision 16 (`decisions/mirrors.md:27`) says removing it *"needs `embarch-api`'s
  toleration retired in the same change, out of this repo's scope."*

So it is a suite-scope change by both repos' own reasoning, and that is the whole reason it has sat.

## Why now

The mechanism it served is **fully retired, not merely unused**. `embarch-api` decision (core-link)
records that `artifact_path_for_core` *"and its UNC computation are **fully retired** rather than left
unchanged as originally planned"* — the WSL2-host case now uploads bytes over `/flash` multipart
instead of naming a path. The 2026-08-15 design-improvement review (item 9) costed this exact cleanup
as **four moving parts removed for one endpoint change**, and the endpoint change has since shipped:
`artifact_path_for_core`, umbrella's `wsl_unc_path`, `doctor` check 9, and api's call-time UNC
computation. Three of the four are still standing.

## Done when

- [ ] `embarch-umbrella`'s `init` stops emitting the field, and `wsl_unc_path` goes with it if nothing
      else uses it (check — do not assume).
- [ ] `doctor` check 9 is retired or re-scoped. **It is a numbered check**; decide and record whether
      the number is retired-in-place or reused, because `embarch-umbrella`'s check numbers are cited
      from `open.md` and from `suite/user-guide.md`.
- [ ] `embarch-api` refuses the key by name at load, matching `[[projects.targets]]` (decision 53)
      and `soc_chip_overrides` (decision 13) — decision 64 calls that the default for a retired key
      and says toleration is *earned*, so removing the earning removes the toleration.
- [ ] Both repos' decision bodies are amended, not just the code: decision 64's "Ends when" has
      fired, and `embarch-umbrella` decision 16's out-of-scope paragraph no longer describes reality.
- [ ] `embarch-api/open.md`'s `artifact_path_for_core` bullet is struck.
- [ ] Gate green in both repos; `changelog.d/` fragments for each.

## The one thing an agent cannot settle

Decision 64's end condition has **two** clauses and only the first is checkable from here: *"stops
scaffolding"* **and** *"no config in the field still carries it"*. The second is a fact about configs
on real machines — the owner's own `embarch-api` config among them — and **a refusal-by-name turns a
stale field into a startup error**, which is the loudest possible failure for the cheapest possible
defect.

Two ways to take this, and whoever runs it should pick deliberately rather than drift into the first:

- **Split it.** Do the umbrella half (stop scaffolding, retire check 9) and leave `embarch-api`
  tolerating the key, with decision 64 amended to say the first clause has fired and what is left. No
  config anywhere breaks. This is the version an unattended leg can run.
- **Do both**, which needs the owner to confirm no live config carries the field — one grep of his own
  machine — because that is the clause no agent can check.

**Do not silently do the second without that confirmation.** Refusing a key by name is exactly the
change whose blast radius lives outside this repo.

## Not in scope

- The multipart `/flash` upload path itself, which is shipped and working.
- Any other retired-key toleration. Decision 64 names three keys and settles the other two; this task
  is about the one whose end condition has now fired.
