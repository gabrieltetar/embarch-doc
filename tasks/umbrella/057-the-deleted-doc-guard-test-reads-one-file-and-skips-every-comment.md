# 057 — the deleted-doc guard test reads one file and skips every comment, so it cannot catch the defect it names

**State:** claimed — leg 100, 2026-09-12, branch `agent/umbrella/057-deleted-doc-guard`.

**Doc-size reserve for `umbrella`** (check before you write): `decisions/bind.md` 841 B left,
`decisions/doctor.md` 1206 B left — both already filed against blocked compaction tasks. If your
work pushes another `umbrella` doc into reserve, file `tasks/umbrella/<NNN>-compact-umbrella.md`
in the same commit.
**Source:** leg 099's refill sweep, 2026-09-12. Verified by reading the test and the file it misses.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`embarch-umbrella/src/doctor.rs:3529-3566`, test
`no_check_text_names_a_document_the_four_file_split_deleted`:

```rust
let source = include_str!("doctor.rs");
...
if trimmed.starts_with("//") { continue; }
assert!(!lower.contains("design.md") && !lower.contains("milestone"), ...)
```

**The invariant is repo-wide and the implementation is one file.** It `include_str!`s itself, so
nothing outside `doctor.rs` is covered — and it `continue`s past every `//` line, so comments, which
are where this whole class of defect lives, are exempt by construction. Four other sub-projects have
had stale `design.md`/`milestone-*.md` citations found in comments this month (`ui/033`, `ui/039`,
`core/008`, and `api/078`/`core/048`/`dev-bench/019` filed alongside this one); a guard that skips
comments would have caught none of them.

`embarch-umbrella/src/install.rs:144,145,149,706` carries the names right now — and **that one is a
legitimate exemption, not a defect.** `LEGACY_MARKER` is
`"# added by \`embarch setup\` (embarch-umbrella/design.md decision 28)"` and it must stay
**byte-for-byte** because it has to match what older installs already wrote into real shell
profiles; changing it orphans those lines. The exemption is real and is recorded **only in a prose
comment**, never encoded anywhere a check can read it — which is the second half of this task.

## Why now

`embarch-decision-reversals.md` shape 4: a check whose stated scope is wider than its implementation
reads as green coverage of ground it never walks. This one is worse than uncovered, because its name
asserts the repo-wide claim.

## Done when

- [ ] The test reads **every** `src/*.rs`, not just `doctor.rs`.
- [ ] Comments are no longer skipped wholesale.
- [ ] `install.rs`'s `LEGACY_MARKER` is exempted **by name**, in the test, with the reason inline —
      an exemption a reader can see, not one that depends on a comment three files away.
- [ ] The test actually fails when it should: inserting `let _ = "design.md";` into a production
      line of a non-`doctor.rs` source file makes `cargo test` red. **Demonstrate this and say so in
      the report** — a guard that cannot be shown to fail is the defect being fixed.
- [ ] `cargo build`/`test`/`clippy --all-targets -- -D warnings` green.

**Doc-size note:** `embarch-umbrella/decisions/doctor.md` is at 90.2% (1,206 B left) and filed
against blocked `tasks/umbrella/048` — stay out of it.
