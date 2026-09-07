# 017 — `schema_version.rs` carries ten legacy `design.md §3 decision N` citations

**State:** open
**Source:** `embarch-reviewer` on `tasks/study-designer/016`, leg 031, 2026-09-07 — the reviewer
found *two* such citations that unit had newly authored; the supervisor fixed those two in scope
(`embarch-study-designer` **`f70e4ae`**) and found ten more while doing it. This task is the ten.
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`src/schema_version.rs` cites decisions in the retired `design.md §3 decision N` form in **twelve**
places. Two were authored by unit 016 and are already corrected. The remaining **ten** are
pre-existing, at these lines as of `f70e4ae`:

| line | citation | whose decision |
|---|---|---|
| 1 | `design.md §3 decision 12` | this crate's own |
| 70 | `` `embarch-dev-bench/design.md` §3 decisions 7/18 `` | `embarch-dev-bench` |
| 147 | `§3 decision 47, `embarch-core/design.md` §3 decision 35` | own, and `embarch-core` |
| 155 | `` `embarch-outpost/design.md` §3 decision 9 `` | `embarch-outpost` |
| 198 | `` `embarch-dev-bench/design.md` §3 `` | `embarch-dev-bench` |
| 203 | `design.md §3` (decisions 31/32) | this crate's own |
| 214 | `§3 decisions 58-62`, `` `embarch-dev-bench/design.md` §3 `` | own, and `embarch-dev-bench` |
| 239 | `design.md` §3 (decision 52 area) | this crate's own |
| 312 | `design.md §3 decision 52` | this crate's own |
| 323 | `design.md §3 decision 12` | this crate's own |

**`design.md` does not exist for any sub-project.** Every one was split into
`spec.md` / `open.md` / `decisions/<mission>.md` on 2026-09-04, so each of these points a reader —
including a connecting agent with no cwd — at a file that is gone.

## The correct spellings, per `DOC-CONVENTIONS.md` *Referring to a decision*

- **This crate's own decision, cited from inside this crate:** the bare number — `decision 12`.
  `decisions/removed.md` already does this correctly for decision 19.
- **Another sub-project's:** `embarch-dev-bench decision 7`, `embarch-core decision 35`,
  `embarch-outpost decision 9` — repo name plus bare number, **no file**.
- **Prefer the bare number over a link either way.** A link names a *file*, and a mission split
  moves an entry between a sub-project's decision files without changing its number — which is
  what `tasks/doc/022` is, and what this leg hit for real in `history/study-designer.md`.

## Why now

This is the same defect `tasks/api/040` closed for `embarch-api`'s six MCP tool descriptions, in
the sub-project that is **the most depended-on crate in the suite** — three consumers in two
languages, one of them C through an FFI boundary. `embarch-api` decision 57 recorded the rule for
tool descriptions; nothing has swept Rust doc comments, and `cargo doc` does not flag a citation
that is merely wrong (only a broken *intra-doc link*, which these are not — they are prose).

**`embarch-study-designer` decision 68 is why no gate will ever catch these:** that decision, filed
by unit 016 in `decisions/ci.md`, deliberately keeps `cargo doc` warnings out of the gate. It is a
defensible call and this task is not an argument against it — it is the consequence, written down.

## Scope note

**Doc comments only, in `embarch-study-designer`.** Do not edit another sub-project's repo to
correct a citation *about* it — the citation lives here and is fixed here. If a decision number
turns out not to exist under the repo the citation names, **stop and report it** rather than
guessing which number was meant: a citation fixed to a different wrong number is the same defect
in new clothes, which is the trap `enroll_probe` fell into in `tasks/api/040`.

## Done when

- [ ] All ten citations use a bare `decision N` (own) or `<repo> decision N` (another's), with no
      `design.md` and no `§3` anywhere in `src/schema_version.rs`.
- [ ] Every number verified to resolve against the named sub-project's current `decisions.md`
      index — say in the task file which ones you checked and how.
- [ ] A repo-wide `grep -rn 'design\.md' src/` reports what is left, if anything, and the task
      says whether that is a further sweep or nothing.
- [ ] `cargo doc --no-deps --all-features` still reports **0** warnings — and run it after a
      `cargo clean -p embarch-study-designer`, because a cached green here is the worker's own
      previous run replayed, not a check.
- [ ] Gate green; `changelog.d/study-designer-*` fragment.
