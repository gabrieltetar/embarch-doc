# embarch-umbrella decisions: The binary and its releases

**Status:** active, 2026-09-02.

What it is built as, what it is called, and how a version gets shipped.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 1 — Rust, one static binary, no runtime dependencies

Matching the rest of the suite. **It must run on a machine where nothing else from EmbArch is installed yet**, so a runtime or a system library dependency would be self-defeating.

### 2 — Repo `embarch-umbrella`, binary `embarch`

The repo name says what it is in the suite; the binary name is **what a new engineer types on their first day.** `embarch-umbrella setup` was rejected purely on ergonomics — this is the most-typed command in the suite for someone who has never used it before.

### 27, 29 — A release-CI job asserts each repo's `Cargo.toml` version matches its pushed tag

**These are one decision under two numbers.** The commit that added decision 28 inserted it in the middle and **renumbered the entry below it from 27 to 29**, so every prose reference to `decision 27` written before that commit silently began pointing at a different entry. Recorded rather than renumbered again, which is why numbers are permanent here now (DOC-COMPACTION.md §5).

Prompted by a real, already-corrected drift: a `Cargo.toml` had drifted from its `v0.1.1` tag, **caught only because someone happened to compare `--version` against the tag by hand that day.** Every repo's release workflow now asserts the two agree *before building any target*, failing the release outright rather than **shipping a binary whose `--version` disagrees with the tag that produced it** — exactly the class of bug `doctor`'s manifest check depends on nobody forgetting to avoid.

**Written 2026-09-04, and "now" is true from that date.** It was false for the
year before it: the audit of 2026-09-03 found this repo's
`.github/workflows/release.yml` going tag push → checkout → toolchain →
`cargo build` → package → upload with **no step that read `Cargo.toml`'s version
or the tag it was pushed from**, and the same absence in `embarch-core`,
`embarch-api` and `embarch-topology`. The drift the entry describes was real and
was corrected by hand; the guard against a repeat had been designed and never
written. Kept here rather than deleted, because a decision that claimed a thing
was built for a year is worth a reader knowing about.

Each of those four workflows now carries a `verify-version` job that the build
matrix `needs:`, so a mismatch fails on one ubuntu runner before any target is
cross-compiled or any asset uploaded. Three choices in it are deliberate:

- **It parses `Cargo.toml` with `awk`, not `cargo metadata`.** Three of the four
  manifests have sibling path dependencies that only resolve after the other
  repos are checked out, and the whole point is to fail *before* that setup.
- **It compares against `GITHUB_REF_NAME` with a leading `v` stripped**, and
  passes on a tag pushed without the prefix rather than treating the prefix as
  the assertion. The claim is that the version and the tag agree, not that the
  tag is spelled a particular way; `on.push.tags` already fixes the spelling.
- **`workflow_dispatch` exits 0 with a reason**, because the ref is then a
  branch and there is no tag to disagree with. A silent pass would have read as
  a check that ran.

The four sub-projects with no release workflow at all — `embarch-study-designer`,
`embarch-dev-bench`, `embarch-outpost`, `embarch-ui` — still have none, so
**"every repo" means every repo that releases.** Whichever gains a release
workflow first inherits the obligation to copy this job.

**Verified without pushing a tag**, which is a release and therefore not the
fleet's to do. The evidence is the step's own `run:` block, extracted from all
four YAML files and executed against each repo's real `Cargo.toml` under four
refs: matching tag, mismatched tag, unprefixed tag, and a `workflow_dispatch`
branch — 16 scenarios, each exiting as intended. What that does **not** cover is
the YAML wiring itself: that `needs: verify-version` really gates the matrix is
checked structurally here and will first be proven by the next real release.
