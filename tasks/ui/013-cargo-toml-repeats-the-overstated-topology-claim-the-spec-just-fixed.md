# 013 — `Cargo.toml` still says `embarch-ui` never depends on `embarch-topology` at all

**State:** claimed by agent/ui/013-manifest-topology-claim, 2026-09-07 17:32
**Source:** reviewer of `ui/012`, leg 026, 2026-09-06 — found while verifying that unit's own
correction, reproduced against `embarch-ui` at `fa3b7b6`
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`ui/012` corrected `embarch-ui/spec.md`, which said the UI `does NOT link embarch-topology, at all,
deliberately`. It does link it — transitively, `embarch-topology → embarch-core-client →
embarch-ui`, features `default,software` — and what is actually true is the narrower claim
`decisions/wiring.md` decision 5 makes: **never the `hardware` feature.**

**`embarch-ui/Cargo.toml` lines 23–24 carry the same overstated sentence, and cite decision 5 for
it:**

```
embarch-ui / never depends on embarch-topology or its hardware feature at all
```

Decision 5 says only the hardware-feature half. So the manifest comment attributes to a decision a
claim that decision does not make — the identical defect `ui/012` fixed, one file over.

**`ui/012` could not fix it**: it was a doc-only unit and the comment is in the code repo, so
changing it would have made its "the code is right and unchanged" claim false. That was the correct
call and this is the follow-up.

## Why it is worth a task rather than a shrug

It is a **comment in a manifest**, which is the file a reader opens precisely when they want to know
what this crate links — and it is the one place the wrong version now survives after `spec.md` and
`embarch.md` §5 both state the transitive shape correctly. A reader who trusts it concludes the
dependency does not exist and reasons from that.

## Watch for

- **The measurement, so it need not be re-derived:** `cargo tree -e normal -i embarch-topology -f
  "{p} FEATURES={f}"` gives `embarch-topology FEATURES=default,software → embarch-core-client →
  embarch-ui`; `embarch-topology`'s `default = ["software"]` and `hardware = ["dep:probe-rs",
  "dep:serialport", …]`; and the count of `probe-rs|serialport` in `cargo tree -e normal` is **0**,
  and still 0 with dev-dependencies [measured 2026-09-06, twice — by `ui/012`'s worker and
  independently by its reviewer].
- **The invariant that is actually being protected is the `probe-rs`/`serialport` count, not the
  absence of the crate.** `embarch-ui/spec.md`'s Invariants section already measures it correctly.
  Whatever the comment ends up saying should point at that rather than restate it.
- Check whether any *other* manifest in the suite carries the same sentence before concluding this
  is one line.

## Supervisor's note, leg 040

**"Check whether any *other* manifest carries the same sentence" is a read, not a reach.** You own
`embarch-ui` and nothing else (`protocol.md` §5 rule 2, and `check-ownership.py` will refuse the
alternative on your own branch). If another repo's manifest carries the same overstated claim,
**write an `inbox/` drop naming the file and the line and scoping it to that repo** — do not edit
it, and do not widen this unit.

**Do not re-run the `cargo tree` measurements to "confirm" them and then report the confirmation as
this unit's finding.** They are already measured twice and recorded above with their provenance;
re-measuring is cheap and fine, but the unit's product is the corrected comment.

### Doc-size reserve for `ui`

Three `ui` files are in reserve, all filed against **open** (not blocked) compaction tasks, so do
not file a second debt for any of them:

- `embarch-ui/decisions/study-designer.md` — 12064/12288 B, **224 B left** → `tasks/ui/011`
- `embarch-ui/decisions/trace-chart.md` — 11833/12288 B, **455 B left** → `tasks/ui/019`
- `embarch-ui/spec.md` — 9461/10240 B, **779 B left** → `tasks/ui/018`

This unit should need none of them: a manifest comment plus, at most, a `changelog.d/` fragment.
**If you conclude a numbered decision is warranted, stop and say so in the task file instead** —
`decisions/wiring.md` is the right home and 224 B is not where that call should be made blind.

## Done when

- [x] `embarch-ui/Cargo.toml`'s comment states what is true and what decision 5 actually says.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment if anything user-visible changed — a manifest comment alone may not
      warrant one; say which and why.

## Closed

Corrected `embarch-ui/Cargo.toml` lines 18-30 (the `embarch-core-client` dependency comment): it
previously said `embarch-ui never depends on embarch-topology or its hardware feature at all` and
cited decision 5 for the whole sentence. Decision 5 only makes the narrower claim (never the
`hardware` feature); the crate is in the tree transitively via `embarch-core-client`, default
`software` feature. New comment says both halves correctly and points at
`embarch-ui/spec.md`'s Invariants section (the `probe-rs`/`serialport` count in `cargo tree -e
normal`) as where the actual measurement lives, rather than restating it inline.

Filed a `changelog.d/ui-manifest-topology-comment.fixed.md` fragment (152 B) — precedent is
`ui/012`'s equivalent spec.md fix, which got one (`history/ui.md` line 19), and this is the same
class of reader-facing correction one file over.

**Other-manifest sweep (read-only, per the supervisor's note):** grepped all sub-project
`Cargo.toml`s for the same overstated sentence and for other topology-related dependency
comments. `embarch-api/Cargo.toml` (dropped `embarch-topology` as a *direct* dependency after the
`CoreConfig` extraction) and `embarch-api/crates/embarch-core-client/Cargo.toml` both make
accurate, narrower claims about their own direct dependencies — neither claims "never depends on
embarch-topology at all" the way this file did. No other manifest carries the defect, so no
`inbox/` drop was filed.

No new decision was warranted; the fix is a comment correction, not a new architectural claim, so
none of the three reserved `ui` files were touched.

Gate: `cargo build`, `cargo test` (101 passed, 2 ignored), `cargo clippy --all-targets -- -D
warnings` all clean in `embarch-ui`. `scripts/check-docs.py` (10/10 green),
`check-client-names.py --repo <code worktree>` (clean against 7 denylist entries), and
`check-ownership.py --scope ui` / `--code-repo` both green from this repo's worktrees.
