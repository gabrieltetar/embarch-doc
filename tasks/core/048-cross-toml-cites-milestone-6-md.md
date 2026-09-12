# 048 — `embarch-core/Cross.toml` cites a `milestone-6.md` that does not exist

**State:** done — leg 100, 2026-09-12, branch `agent/core/048-cross-toml-citation`.

**Doc-size reserve for `core`** (check before you write): `decisions/auth.md` 932 B left, filed
against a blocked compaction task. If your work pushes another `core` doc into reserve, file
`tasks/core/<NNN>-compact-core.md` in the same commit.
**Source:** leg 099's refill sweep, 2026-09-12. Verified by reading both sides.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-core/Cross.toml:1-4`:

> `the other three release targets are native builds on their own OS's GitHub-hosted runner (milestone-6.md §3.7).`

No `milestone-*.md` exists anywhere in the suite — every one was folded into its sub-project's four
files and deleted. **This is the only stale-doc citation in all of `embarch-core` outside `*.md`
files**, confirmed by grepping `*.rs`, `*.toml`, `*.py`, `*.sh` and `*.yml`, which is what makes the
closing grep trivially decidable rather than a judgement call.

**One sub-question is deliberately left open for whoever runs this, and it must be answered by
reading, not guessed.** Which doc now owns the "three native builds plus one cross" claim? The
likely home is `embarch-doc/embarch-umbrella/decisions/release.md` (decisions 1, 2, 27, 29) or the
release workflow itself — **open the candidate and confirm it actually says this before repointing
at it.** If nothing says it, state the target list inline with no citation at all; a comment that
states a fact plainly is better than one pointing at a doc that does not back it.

## Why now

Same defect class as `ui/033`, `ui/039` and `api/078`. `embarch-core` is the sub-project the others
cite into most, so a wrong citation here propagates; `core/008` already found five stale citations
in this repo where its task predicted two.

## Done when

- [x] `grep -rn "milestone-\|design\.md" /home/gabriel/Github/embarch/embarch-core --include='*.rs'
      --include='*.toml' --include='*.yml' --include='*.py' --include='*.sh'` returns zero.
- [x] The comment cites a file that was **actually opened and confirmed**, or states the target list
      with no citation.
- [x] The release workflow's real matrix is checked, so the comment's "three native + one cross"
      claim is confirmed true today rather than only correctly cited.
- [x] `cargo build`/`test`/`clippy --all-targets -- -D warnings` green. Note `Cross.toml` is
      configuration, not source — a native Windows build is **not** owed by this unit.

## Resolution

Two stale citations found, not one — `release.yml` had its own `milestone-6.md` reference
(`.github/workflows/release.yml`, header comment and the macOS matrix-entry comment), on top of
`Cross.toml`'s. Both fixed in one commit:

- `Cross.toml`: the "three native builds, one cross" claim is backed by `embarch-umbrella` decision
  14 (read the body: distribution as one release archive, four targets, three native runners GitHub
  already hosts, one `cross`-built aarch64-linux) — confirmed against `.github/workflows/release.yml`'s
  actual matrix (`windows-latest`, `ubuntu-latest` for x86_64, `macos-14` native Apple Silicon, plus
  `ubuntu-latest` + `cross: true` for aarch64-unknown-linux-gnu). True today.
- `release.yml` header's own dead citation: dropped — the next line already states "embarch-umbrella
  decision 14" plainly, so the parenthetical was redundant as well as stale.
- `release.yml`'s macOS-unsigned aside ("§5 open questions"): repointed at `embarch-umbrella/open.md`,
  which is where the Gatekeeper/unsigned-aarch64-darwin fact actually lives today (confirmed by
  reading it) — no decision number exists for it, so cited as the file, not a fabricated number.

No other non-markdown file in `embarch-core` carries a `milestone-*`/`design.md` reference.

Code: `embarch-core` branch `agent/core/048-cross-toml-citation`, commit 1e7a6bd, pushed.
Doc: `embarch-doc` branch `agent/core/048-cross-toml-citation-doc`, this commit.
`cargo build`/`test`/`clippy --all-targets -- -D warnings` all green (196 tests passed).
