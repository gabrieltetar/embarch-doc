# 066 — A replay harness for atlas lookups against recorded sessions

**State:** open
**Source:** EMB-148, filed by an audit after atlas task 003 (`config` takes a list and `vs=`) replayed five recorded `.config` greps and three `.config` diffs with a throwaway script
**Issue:** EMB-148
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Every atlas unit that claims a lookup saves calls has to prove it on recorded
sessions, and each time a worker writes its own throwaway script to find the
shell calls and replay them through `embarch-atlas q`. Make that one tool, so
the numbers come out the same way every time.

Inputs: one project's Claude Code transcripts
(`~/.claude*/projects/<project>*/*.jsonl` and `<session>/subagents/*.jsonl`), a
named pattern for the shell calls a lookup replaces (for example a multi-symbol
`grep` of a build's `zephyr/.config`, or
`diff <(grep … a/.config) <(grep … b/.config)`), and a mapping from such a call
to the lookup's arguments. Output, per replayed call: calls and result
characters **before** (the shell command re-run read-only against the build
dir as it is now) and **after** (the lookup, its `next=` pages followed to the
end), plus totals — **numbers only**, with no symbol, path or value from the
project in it.

How 003's script did it, as a starting point: a scan pairs each `Bash`
`tool_use` whose command matches the pattern with its `tool_result`; a replay
re-runs the shell segment, runs `embarch-atlas --atlas-dir <copy> q config …`
against a copy of the project's atlas dir under `/tmp` (caches written outside
the project tree, `GIT_OPTIONAL_LOCKS=0`), and counts. It also ran the old
lookup from an `origin/main` archive on `PYTHONPATH` for a before/after on the
atlas side; that part is optional here.

**Direction, from the issue:** a `scripts/replay.py` in `embarch-atlas`, never
shipped as a CLI verb or MCP tool because it reads private transcripts, with
the call patterns and their lookup mappings as a small table, and a `--report`
that prints the numbers-only table a task's `## Result` takes.

**Constraints.**

- The replay re-runs **only** a recorded command matching one of the table's
  named patterns, never an arbitrary command from a transcript, and only
  read-only (`grep`, `diff` over `grep`).
- It never writes into the project's firmware tree or its atlas dir; every
  write goes under a temporary copy.
- Tests use synthetic transcripts and a synthetic atlas dir only. This is a
  public repo: no real transcript, path or symbol goes into a fixture, and
  `test_public_guard` must run, not skip.
- Do not run it against a real project in this task; say in this file that the
  first real run is owed.

**What you may change.** Only `embarch-atlas` and `embarch-doc/embarch-atlas/`.

**Doc reserve.** Nothing of `embarch-atlas`'s is in reserve.

## Why now

The owner moved it to Fleet Ready. The owner reads these numbers to decide what
the next lookup should be, and a per-task script makes them incomparable.

## Done when

- [ ] One command scans a project's transcripts for a named call pattern and lists the matching calls with their recorded result sizes.
- [ ] The same command replays them through the mapped lookup against a copy of the atlas dir and prints calls and characters before and after, numbers only.
- [ ] It never writes into the project's firmware tree or its atlas dir, and a test proves the copy is what gets written.
- [ ] Gate green (`../../embarch-fleet/gate.md`, Python bullet).
- [ ] `changelog.d/` fragment dropped; the code repo's `DESIGN.md` or `embarch-atlas/design.md` says the harness exists and why it is not a verb.
