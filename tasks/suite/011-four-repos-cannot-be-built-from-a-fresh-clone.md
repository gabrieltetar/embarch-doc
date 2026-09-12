# 011 — Four repos cannot be built from a fresh clone of themselves, and no README says so

**State:** open — **announced and parked awaiting its window, leg 096, 2026-09-12.**
Announced to `#embarch-fleet` at `ts 1789200593.666659`; the 30-minute silence-as-consent window
(`embarch-fleet/ops.md` §4) closes at **02:39 local**. Execute it as a supervisor unit, not a
worker's, only if no objection has arrived by then. **If a leg ends before the window closes, leave
this line intact and complete the window rather than restarting it** — the `ts` above is the clock.
**Source:** suite review pass 2026-09-06, dimension 1 (standalone-ness). Manifests code-confirmed.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

Measured path-dependency closures: `embarch-core` → 2 siblings; `embarch-api` → 2 (one direct,
two via its own sub-crate); `embarch-umbrella` → 2; `embarch-ui` → 3, one of them a crate
*nested inside* `embarch-api`.

The `## Building` sections say nothing about it: `embarch-core/README.md:92`,
`embarch-api/README.md:34` and `embarch-umbrella/README.md:42` each give `cargo build --release`
with no prerequisite. `embarch-ui` has **no README at all** and has the deepest reach.

The requirement is real and has bitten twice. `embarch-topology/decisions/crate.md` decision 13:
*"Each consumer's release workflow **only ever checked out itself**, so a relative path dependency
could never resolve … **The same gap already existed for `embarch-study-designer`**."* And
`embarch-study-designer/decisions/crate.md` decision 8 names *"a machine without all four repos
cloned side by side"* as the case a git dependency would have covered.

The suite's one honest example of this is the C repo:
`embarch-dev-bench/app/CMakeLists.txt:119` fails with *"embarch-study-designer not found at … —
set EMBARCH_STUDY_DESIGNER_PATH if it isn't a sibling of this repo."* The four Rust consumers fail
with cargo's raw `failed to read ../embarch-topology/Cargo.toml`, and nothing anyone read said the
side-by-side layout was required.

Candidate direction: each consumer README's `## Building` states which siblings must be on disk.
**I am not proposing git dependencies** — `embarch-study-designer` decision 8 rejected those and
the rejection stands.

## Why now

Nothing mechanical can catch this: every gate runs inside a tree that already has the siblings. A
newcomer or an agent that clones one repo — the reasonable first move — gets an error about a path
outside it and no doc that mentions the layout.

## Done when

- [ ] Each of `embarch-core`, `embarch-api`, `embarch-umbrella` and `embarch-ui` states in its
      README which sibling repos must be present to build.
- [ ] No README's `## Building` section implies the repo is self-contained when it is not.
- [ ] Gate green; `changelog.d/` fragments for each repo touched.

**Two notes.** The `embarch-ui/README.md` this needs is also wanted by the
`suite-the-studies-guide-makes-the-ui-mandatory…` drop in this batch — let that one create the
file and this one add the prerequisite line. And the more valuable half of this finding is
**owner-only** and deliberately not filed here: `embarch-dev-workflow.md:11` says *"The three
code-bearing repos are independent Cargo projects, not a workspace. Build each on its own;
**nothing cross-repo is needed to compile.**"* while line 96 of the same file says *"Core has two
`path` dependencies, so syncing Core alone produces a build against stale siblings — which
compiles, and is wrong."* That file is reserved; it is in the suite-review report's owner-only
section.
