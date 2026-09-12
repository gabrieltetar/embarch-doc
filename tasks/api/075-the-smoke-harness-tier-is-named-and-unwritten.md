# 075 — Decision 30's smoke-harness tier is named and still unwritten

**State:** claimed by agent/api/075-smoke-harness-tier, 2026-09-12 01:32
**Source:** `embarch-api/open.md` — "**The smoke harness (decisions/tests.md 30) is
named, unwritten.** Six mocked criteria live in `tests/` (decisions/tests.md 46);
end-to-end is `#[cfg(unix)]`, Windows gets direct tests."
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api` decision 30 named the methodology that actually finds bugs in this project — a
throwaway Core instance plus a synthetic fixture repo, re-running a fixed sequence of calls — and
said it gets a name and a script. **The name exists; the script does not.** Six mocked criteria sit
in `tests/` under decision 46, which is a different tier and was never claimed to be this one.

Write the tier. It runs against a throwaway Core and a synthetic fixture repo, with **no real
hardware, no probe, and no live Core** — that constraint is what makes it runnable in this fleet at
all, and a version of it needing a board is not this task.

## Why now

Decision 30 records that *every real bug found in this project to date came from a live run*. A
methodology that only a human remembers to run is the same failure `suite/decisions.md` 2 caught in
`embarch-outpost` — and here it has been named-and-unwritten long enough to be a standing entry in
`open.md`.

## Done when

- [ ] A named smoke tier exists under `embarch-api/tests/`, runnable with `cargo test` and needing
      no hardware, no probe and no live Core.
- [ ] It is **not** a rename of decision 46's mocked criteria — the two tiers stay distinguishable,
      and the task's own report says what each covers.
- [ ] What stays `#[cfg(unix)]`-only is stated where a Windows reader of a green run meets it.
- [ ] `embarch-api/open.md`'s bullet is struck or narrowed to what remains.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green; gate green;
      `changelog.d/` fragment.

**Reserve note:** `embarch-api` is the most compaction-indebted sub-project in the suite — three
files in reserve behind blocked tasks (`decisions/client-crate.md` 94.7%, `decisions/surface.md`
91.6%, `interfaces/config.md` 91.1%). **Do not relocate text into any of them**, and if this work
spends a reserve, file `tasks/api/<NNN>-compact-api.md` in the same commit.
