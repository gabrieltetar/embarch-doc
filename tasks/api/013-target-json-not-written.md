# 013 — `target.json` is documented as beside every build directory and is never written

**State:** open
**Source:** embarch-umbrella/005 (doctor check 16, 2026-09-05) — found while looking for a build directory's provenance
**Scope:** api
**Hardware:** none

## What

`embarch-api` decision 19 says "**a `target.json` recording the full resolved
selection**" is written beside every per-target build directory, and
`embarch-api/interfaces/config.md`'s build-directory paragraph states it as
current truth: "each build directory gets a `target.json` recording the full
resolved selection so a human can recover what produced it without
reverse-engineering a hash."

**Nothing writes it.** `grep -rn 'target\.json' embarch-api` over the whole repo
(`.rs` and `.md`) returns only the two doc mentions above and no source hit at
all; `resolve.rs` assembles `build_dir` and the build command and never touches
a manifest file. So the decision's own stated remedy for the `-args<hash>`
segment — the thing that makes a directory listing debuggable — does not exist.

Either build it (a serde write of the resolved `Target` + snippets + extra_args
into `<build_dir>/target.json`, at the point `resolve.rs` returns the plan) or
retire that half of decision 19 with a tombstone and drop the sentence from
`interfaces/config.md`. **The doc stating it as truth is the part that must not
survive either way.**

## Why now

It is load-bearing for something already deferred on it. `embarch-umbrella`
decision 26's `doctor --prune` would delete build directories for targets no
longer valid, and the only sound per-directory evidence of *which* target
produced one is this file — the directory name is not reliably parseable back
into a target, because board, app and snippet names all contain `-`
(`…-ble-shell_wdt31`). Umbrella deferred `--prune` on 2026-09-05 partly for this.

Not urgent on its own; it is a two-line doc fix or a small write, and it unblocks
somebody else's decision.

## Done when

- [ ] Either `target.json` is written beside each `zephyr-west` build directory
      with the resolved board/variant/revision/app, snippets and extra_args, and
      a test asserts it round-trips — or decision 19's `target.json` half is
      retired with a tombstone.
- [ ] `embarch-api/interfaces/config.md` no longer states as truth whatever is
      not built.
- [ ] `changelog.d/` fragment; gate green.
