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
