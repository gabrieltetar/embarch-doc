# 071 — Citation census: `grep` also misses a citation split across a line wrap

**State:** open — drained from `inbox/` by leg 126 at `core/068`'s fold, 2026-09-16.
**Source:** `core/068` (2026-09-16), rechecking the 11 plural-citation lines `core/058`/`066`/`067`
missed. Re-censusing `embarch-core` with the corrected plural pattern (`[Dd]ecisions [0-9]`)
reproduced exactly the filed 11 lines — but a further check, `grep -rlIE
'[Dd]ecisions[[:space:]]*$'` (lines ending in "decisions" with nothing after), found **four more
citation sites in `embarch-core/src/study.rs` that no line-based census, past or present, could
ever see**: the sub-project name or the numbers land on the far side of a doc-comment line wrap,
e.g. `` (`embarch-study-designer` decisions\n// 58/60) `` — one citation, two lines, invisible to
any pattern that greps a single line.
**Scope:** doc
**Hardware:** none — re-classified by me at the drain and it holds: a census method is a regex and a
grep, nothing is built for a board, no probe, no live Core, no study.
**Owner:** required — the drop said `no`, and I am overriding it. Its first `Done when` bullet asks
for the method to be "written or specified... a shared script, whichever this repo's owner prefers",
and `scripts/` is owner-reserved; the second asks for follow-up tasks to be filed across seven
sub-projects, which is a queue-shaping call rather than a unit of work. A supervisor could file
those tasks, but not until somebody settles the method they are supposed to name.

## What

Every citation-sweep task run across this suite so far (`core/058`, `066`, `067`, `068`, and
whatever the `ui`/`dev-bench`/`api`/`study-designer`/`outpost`/`topology`/`umbrella` chain has
already closed) has censused with a single-line regex — first singular-only, then, since the
`core/068` chain, plural-aware. **None of them can see a citation whose "decisions"/"decision" and
its number(s), or whose repo-prefix and its "decisions", fall on opposite sides of a `rustfmt`-style
doc-comment line wrap.** In `embarch-core` alone this cost:

- **Four missed citation lines** (`study.rs:1072-1073`, `1084-1085`, `2313-2314`, `3689-3690`;
  `core/068` checked all four — 0 wrong numbers, 0 false sentences, so no live defect today, but the
  next wrong number or stale sentence in a wrapped citation would sail through every future sweep
  unless this is fixed).
- **Two citations mis-filed as "bare — own repo"** in `core/068`'s own filing task, because the
  single line the filing census matched (`service.rs:107`, `main.rs:165`) didn't carry the repo
  prefix that was sitting on the line immediately above it. The source code was correct both times
  (`embarch-umbrella`, `embarch-study-designer` respectively) — only the census's classification was
  wrong, and only because it never read the line before the match.

## Why now

The whole citation-sweep chain exists because `inbox/citation-census-grep-cannot-see-a-plural-
citation.md` named one structural blindness in the census pattern and asked for it to be re-run
everywhere the old pattern had been trusted. This is the same finding, one level up: the fix for the
plural case (a smarter regex) is still a **single-line** tool being asked to see a **multi-line**
fact, and it will keep missing citations that wrap, in any repo, for as long as sweeps stay
single-line. `embarch-core`'s decision-heavy files (`study.rs`, `api.rs`) wrap doc comments
routinely; other sub-projects' equivalents (`embarch-api`'s `client.rs`, `embarch-study-designer`'s
larger modules) are exactly as exposed and have not been re-censused against this.

## Done when

- [ ] A census method that can see a wrapped citation is written or specified — e.g. joining each
      comment block (`///`/`//`/`#`-prefixed contiguous run) into one string before matching, rather
      than matching line by line — and named somewhere a future sweep task will read it (this repo's
      own sweep-task template, or a shared script, whichever this repo's owner prefers).
- [ ] Each sub-project already declared "citation swept" end to end (`core` is one; check which
      others in the chain claim the same) gets a follow-up task re-censusing with the wrap-aware
      method, scoped the same way `core/068` was scoped from the plural finding.
- [ ] `embarch-core` itself does not need re-re-checking — `core/068` already did the wrap-aware pass
      by hand for its one repo and found 0 defects among the 4 wrapped instances it located.
