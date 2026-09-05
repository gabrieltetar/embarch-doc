# 013 — `embarch-umbrella` decision 26 says `target.json` is not written; it is, as of 2026-09-05

**State:** open
**Source:** `agent/api/013-target-json-not-written` — the branch that built it
**Scope:** umbrella
**Hardware:** none

## What

`embarch-umbrella/decisions/projects.md` decision 26's third bullet ends: "The
per-directory `target.json` decision 19 says would record the resolved selection
**is not written by `embarch-api`** (no occurrence in its source, 2026-09-05), so
a build directory carries no provenance to read either." That was true when
written and is false now — `agent/api/013` built it the same day. Correct the
bullet, and state the one rule a consumer must not get wrong:

- **A `zephyr-west` build directory gets `<build_dir>/target.json`**, the
  resolved `{project, board, soc, cpucluster, variant, revision, app, snippets,
  extra_args}` plus `schema_version`, written after the build command into a
  directory that already exists.
- **Absence means "unattributable", never "orphaned".** Every directory built
  before 2026-09-05 has none, the write is best-effort, and a `static` or
  dev-bench build never gets one. A `--prune` that reads a missing file as "no
  valid target claims this" deletes exactly the directories it has no evidence
  about.

The `--prune` blocker itself is **unchanged**: naming the currently-valid targets
still needs decision 17's unbuilt `embarch-api list-targets` shell-out. This
removes the second of the two blockers that bullet named, not the first.

## Why now

Cheap (one bullet), and it is a false statement about another repo's shipped
behaviour sitting in the entry that will be re-read the day `--prune` is picked
up. `doctor` check 16 may also now be able to report how many build directories
are attributable, which is a strictly better number than a raw count — that half
is a judgement call for whoever takes this, not a requirement.

## Done when

- [ ] Decision 26's third bullet states what `embarch-api` writes today, and the
      absence rule above.
- [ ] Anything else in `embarch-umbrella` asserting no build-dir provenance
      exists is corrected in the same pass.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
