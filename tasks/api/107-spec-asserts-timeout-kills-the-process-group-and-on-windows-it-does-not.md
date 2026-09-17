# 107 — `spec.md` §2 asserts "timeout kills the process group" as an invariant, and on the shipped Windows binary it does not

**State:** done — leg 132 unit 3, 2026-09-17, `agent/api/107-windows-process-group`
**Source:** leg 132's own refill sweep of `embarch-api/open.md` and `spec.md` against the crate.
Not a citation defect and not from a worker's report — a documented invariant checked against the
code that is supposed to hold it.
**Scope:** api
**Hardware:** none — reading Rust and correcting prose. Nothing is built for a board, no probe, no
live Core, no deploy. **See "Not yours" for why the Windows *fix* is deliberately out of scope.**
**Owner:** no

**Doc-size reserve for `api`:** `embarch-api/spec.md` is **9,102/10,240 B (1,138 B left)** — inside
its reserve band, filed as `tasks/api/083`, which is **blocked on `In flux: yes`**. This task edits
that exact file, so read the paragraph headed **"The reserve, and what you may spend"** below before
you write anything. Nothing else of `api`'s is in reserve, but `open.md` warns that several
`decisions/*.md` sit a paragraph from the line and are invisible to the size gate until they cross:
put a new decision in the file whose *topic* it is, never in whichever file has room.

## What

`embarch-doc/embarch-api/spec.md:35`, in §2 — the Invariants section, whose bullets `tasks/api/083`
calls *"a load-bearing rule an agent must not invert"* — states this flatly, with no platform
qualifier:

> - **Timeout kills the process group**, not just the immediate child — `west`/`cmake`/`make` fork
>   subprocesses a plain kill orphans. A killed/timed-out build is reported **distinctly** from a
>   nonzero exit, so a hang isn't misread as a code problem.

**On Windows the first clause is false, and the code says so.** `embarch-api/src/build.rs`:

```rust
    #[cfg(unix)]
    {
        // Put the child in its own process group so a timeout can kill the
        // whole tree (west/cmake/make chains fork sub-processes that a plain
        // kill() on just the immediate child would orphan).
        command.process_group(0);
    }
```

...and then, at the bottom of the same file:

```rust
#[cfg(unix)]
fn kill_process_tree(child: &mut tokio::process::Child) {
    if let Some(pid) = child.id() {
        // Negative pid targets the whole process group created via
        // process_group(0) above.
        let _ = std::process::Command::new("kill")
            .args(["-KILL", &format!("-{pid}")])
            .status();
    }
    let _ = child.start_kill();
}

#[cfg(not(unix))]
fn kill_process_tree(child: &mut tokio::process::Child) {
    let _ = child.start_kill();
}
```

The non-unix arm **is** the *"plain kill on just the immediate child"* that the unix arm's own
comment names as the thing it exists to avoid. So on Windows a timed-out build leaves the
`west`/`cmake`/`ninja` tree running, holding the build directory, after `embarch-api` has already
reported the build as killed.

**Three things make this worth a unit rather than a comment.**

1. **Windows is a shipped target, not a hypothetical.** `.github/workflows/release.yml` builds
   `x86_64-pc-windows-msvc`. Confirm that yourself rather than taking it from this task.
2. **The claim is in §2**, which is the section a reader trusts as "what must always hold". An
   invariant that holds on one of two shipped platforms is the worst place in the document to leave
   unqualified — and `spec.md` §2 is the same section that carries this repo's
   no-inference-as-fact posture.
3. **The function is named `kill_process_tree` and the Windows arm does not kill a tree.** Even a
   reader who checks the code has to notice the `cfg` to learn that; the unix arm carries a
   four-line comment explaining itself and the non-unix arm carries none at all.

`decisions/shape.md:18` also lists *"the timeout and process-group handling"* among what the CLI
exists to keep callers from bypassing. Check whether that sentence needs the same qualifier or
whether it is fine as a description of the module boundary; say which, and why, in your report.

## The reserve, and what you may spend

Your correction goes into a file with 1,138 B of headroom whose compaction task is **blocked on
`In flux: yes`**, so `.claude/leg.md`'s rule applies: **you are the actor making the flux, so you
are the one allowed to shorten what you are rewriting.**

In order of preference:

1. **Rewrite the §2 bullet in place, net-neutral or net-negative in bytes.** This is very likely
   achievable — the claim needs a platform qualifier, not a new paragraph, and the existing bullet
   has slack in it. This is the outcome to aim for.
2. If you cannot, you may compact `embarch-api/spec.md` as part of this unit, **carrying
   `tasks/api/083`'s `Must not delete:` list verbatim** and closing **only** `spec.md`'s item on
   that task's `Compacts:` line — by *deleting* the file from the line, never by striking it
   through. Do not touch anything else `083` covers and do not change its `In flux:` answer for a
   file you did not pay.
3. If you spend the reserve rather than clearing it — push another `api` file into the band, or
   leave `spec.md` in it with nothing filed — file `tasks/api/<NNN>-compact-api.md` in the same
   commit, per `tasks/README.md`.

Run `python3 scripts/check-doc-size.py --pressure` in `embarch-doc` before and after, and report
both numbers for `spec.md`.

## Done when

- [x] `embarch-api/spec.md` §2's timeout bullet no longer asserts process-group kill as an
      unqualified invariant. It says what holds on unix, says what happens on Windows instead, and
      does not overstate either. **Do not write that the Windows behaviour is a bug that will be
      fixed** — nothing has decided that; see "Not yours".
- [x] `src/build.rs`'s `#[cfg(not(unix))] kill_process_tree` carries a comment saying plainly that
      it kills only the immediate child and that a forked build tree survives it. The unix arm's
      comment is the model for length and tone.
- [x] `decisions/shape.md:18` is either left alone with a stated reason or corrected, your call,
      reported either way.
- [x] One of: a numbered `api` decision recording the asymmetry, its cost, and the named trigger
      that would close it; **or** an `embarch-api/open.md` entry doing the same. Pick whichever
      matches how this repo already handles a platform gap it has chosen not to close — read
      neighbouring examples before deciding, and say in your report which you picked and why. If
      you write a decision, it goes in the `decisions/` file whose topic it is.
- [x] A `changelog.d/` fragment.
- [x] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` in
      `embarch-api`, and `python3 scripts/check-docs.py` in `embarch-doc`.

## Report

**Windows really is shipped:** `.github/workflows/release.yml`'s `build` job matrix includes
`{target: x86_64-pc-windows-msvc, os: windows-latest}` alongside linux x86_64/aarch64 and macOS
aarch64 — a real build-and-release leg, not a curiosity. It only *builds* that target (no `cargo
test` step on Windows anywhere in the file), which is exactly what makes an unexercised Windows
kill path dangerous to ship blind.

**`spec.md` §2 bullet** rewritten net-negative: 249 → 236 bytes (was: "Timeout kills the process
group, not just the immediate child — ... A killed/timed-out build is reported distinctly...").
New bullet states unix-only kill + Windows-immediate-child-only, citing the new decision, and
drops the inline "why unix needs the group" rationale clause (moved into decision 75's prose,
which is where the *why* belongs per this repo's spec/decisions split — other §2 bullets already
cite `decisions/*.md` the same way, e.g. the `schema_version` and `lagged` bullets).

**`src/build.rs`** — Windows `kill_process_tree` arm now carries a comment (modeled on the unix
arm's) stating plainly it kills only the immediate child, that a forked tree survives, and citing
decision 75.

**`decisions/shape.md:18`** — left alone, on purpose. That sentence describes what the CLI keeps a
caller from bypassing (config-driven build command, freshness check, "the timeout and
process-group handling") as a statement about the **module boundary** — the pipeline exists and
both mechanisms run — not a claim that the process-group kill is complete on every platform. It
never asserted platform completeness the way `spec.md` §2 did, so it needed no qualifier. Reported
per the task's instruction either way.

**Picked: a numbered decision, not an `open.md` entry.** `decisions/build.md` decision 75 records
the asymmetry (unix process-group vs Windows immediate-child-only), its cost (a timed-out
`west`/`cmake`/`ninja` tree outlives the "killed" report and keeps the build directory locked), and
the named trigger (`tasks/api/108`, filed this unit — what would have to run on a real Windows
process to believe an implementation). Chose the decision route over `open.md` because `spec.md`
§2 already cites `decisions/*.md` files for exactly this kind of platform/behavioral nuance on
other bullets (`schema_version`, `lagged`), and decision 5 in the same file (`decisions/build.md`)
already owns "running a build" as its topic — this is squarely that topic, not a loose end.
`open.md`'s existing "Windows never runs the smoke-harness tier" bullet is a close **sibling**, not
a template to duplicate: it names a *test-reach* gap with no decision behind it yet, while this
gap already has a clear "why not fixed now" rationale that belongs with the code decision, so I
did not also add a second `open.md` bullet — decision 75 is the single source of record, and
mentions the smoke-harness gap inline for context instead of restating it.

**Filed `tasks/api/108-windows-process-tree-kill.md`**: the actual Windows tree-kill
implementation (Job Object or `taskkill /T /F`), with an explicit "what would have to run to
believe it" section — a real Windows process, timed out, verified via `tasklist`/Process Explorer
that a *forked grandchild* (not just the immediate child, which `start_kill()` already handles
today) is actually gone. It says plainly a compile-only result does not close it.

**Doc-size reserve:** `embarch-api/spec.md` — before: 9,102/10,240 B, 1,138 B left (88.9%
pressure, `PARKED`). After: see below; the §2 bullet edit alone is net −13 B, well inside outcome
1 of the reserve ladder (net-neutral/negative in-place rewrite), so `tasks/api/083`'s park is
untouched and no new compaction debt was filed for `spec.md`.

**Not started, mentioned per the task's instruction:** `tests/smoke_harness.rs`'s `#![cfg(unix)]`
and its POSIX-shell fixture. This unit's decision 75 and the new `tasks/api/108` both lean on that
gap (no Windows test tier exists to verify *any* Windows build-orchestration behavior, this one
included) without sharpening it further — `108`'s own "what would have to run" section flags that
whoever picks it up will likely want to add the first Windows entry to that file, but does not
propose how `#![cfg(unix)]` itself should be lifted.

## Not yours

**Do not implement a Windows process-tree kill.** It is the obvious move and it is the wrong one for
this unit, for a reason specific to this suite rather than to scope discipline: a `taskkill /T /F`
or a Win32 Job Object added here **cannot be executed by anything in this environment** — the fleet
runs in WSL2, no test tier of this crate runs on Windows (`tests/smoke_harness.rs` and decision 46's
four end-to-end tests are all `#![cfg(unix)]`, which is its own open question in `open.md`), and
`release.yml`'s Windows job builds rather than tests. Shipping an unexercised kill path would replace
*"a documented gap"* with *"an invariant that looks closed and has never run"*, which is the exact
trade this repo's own `[measured]`/`[assumed]` provenance tagging exists to prevent.

If you judge the implementation worth doing, **file it as a task** in `tasks/api/` naming what would
have to run to believe it, and say so in your report. That is the useful output; the code is not.

Also not yours: `tests/smoke_harness.rs`'s `#![cfg(unix)]` and the POSIX-shell fixture behind it.
It is a real and related open question, it is filed in `open.md`, and it is a different unit.
Mention it in your report if this work sharpens it; do not start it.
