# 038 — "Am I in WSL2" has three implementations and two incompatible rules, two of them inside one binary that already links the canonical predicate

**State:** claimed by leg 049, 2026-09-08
**Source:** suite review pass 2026-09-06, dimension 2 (DRY across modules). Code-confirmed.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

The canonical predicate is public, pure and takes its inputs —
`embarch-topology/src/software.rs:195-201`:

```rust
pub fn detect_wsl2(proc_version: Option<&str>, wsl_distro_env: Option<&str>) -> bool {
    let kernel_says_so = proc_version.map(|v| v.to_ascii_lowercase().contains("microsoft")).unwrap_or(false);
    let env_says_so = wsl_distro_env.map(|v| !v.is_empty()).unwrap_or(false);
    kernel_says_so || env_says_so
}
```

A second, **different** rule lives at
`embarch-api/crates/embarch-core-client/src/token_discovery.rs:81-87`:

```rust
fn is_wsl2() -> bool {
    std::fs::read_to_string("/proc/version")
        .map(|version| { let lower = version.to_lowercase(); lower.contains("microsoft") || lower.contains("wsl") })
        .unwrap_or(false)
}
```

It ignores `WSL_DISTRO_NAME` and accepts `"wsl"` where `detect_wsl2` accepts only `"microsoft"`.
A third is a verbatim copy of the second at `embarch-umbrella/src/token.rs:97-104`.

**`embarch-core-client` already depends on `embarch-topology`**
(`crates/embarch-core-client/Cargo.toml`), so `detect_wsl2` is one call away and unused. For
contrast, `embarch-umbrella/src/env.rs:9-13` does it correctly: reads the two inputs, delegates
the decision.

**The two rules decide different things in the same process.** `token_discovery::is_wsl2` decides
*where the token file is* — `/var/lib/embarch/token` versus the `/mnt/c/...` translation — while
`resolve_software_topology`, linked into the same binary, uses `detect_wsl2` to decide the
topology class and hence which Core to talk to. A `/proc/version` containing `wsl` but not
`microsoft`, or a stripped `WSL_DISTRO_NAME` with an unusual kernel string, makes them disagree,
and the failure surfaces as "no token found" or a token read from the wrong side while `doctor`
confidently reports the class.

The narrow rule's stated reason (`token_discovery.rs:76-80`: `$WSL_DISTRO_NAME` can be scrubbed by
an MCP launcher) argues for a **union** of signals — which is what `detect_wsl2` already is.

Candidate direction: one predicate for the suite, in the crate that exists to own it; each call
site keeps its own I/O and passes the inputs in. If the token path genuinely needs a narrower
test, that belongs in `detect_wsl2` as a named mode, not as a second function.

## Why now

`embarch-topology/decisions/crate.md` decision 4 **asserts this is already done** — *"the
software-class detection then mirrored between `embarch-api` and `embarch-umbrella` all move here
as the sole implementation. The mirrored-copy CI diff job becomes obsolete: there is nothing left
to mirror once everyone links the same crate"* — and decision 8 says *"there is no way for the two
to disagree, since there is only one of them."* Both are false as written, and each
implementation is unit-tested against its own rule, so nothing compares them.

## Done when

- [ ] `embarch-core-client` answers "am I in WSL2" through `embarch_topology::software::detect_wsl2`,
      or the reason it must not is recorded next to the second implementation.
- [ ] No two answers to that question can disagree inside one process.
- [ ] `status.d/api-*` fragment for `embarch-topology/decisions/crate.md` decisions 4 and 8, which
      are false as written.
- [ ] Gate green; `changelog.d/api-*` fragment.

**Adjacent:** `embarch-umbrella`'s copy disappears with the
`umbrella-three-mirrors-of-embarch-api…` drop in this batch if that one lands. Landing this first
means umbrella inherits the fix rather than porting it.

## Supervisor notes — leg 049

**You own `api` and only `api`.** `embarch-topology` is a shared crate you *depend on*, not one you
may write. If the honest fix turns out to require changing `detect_wsl2` itself — the task's own
"named mode" suggestion would — **do not make that change.** Write the `embarch-api` side against
the predicate as it stands today, and file the topology-side change as a drop in
`/home/gabriel/Github/embarch/embarch-doc/inbox/` (that absolute path, the main checkout — a drop
written into your worktree is invisible at cleanup and has been lost twice this week). Likewise
`embarch-umbrella/src/token.rs`: the third copy is named in this task for context only and is
`umbrella/036`'s to remove. Touching it is out of scope.

**Re-derive every cited line number before acting on it.** The task quotes
`embarch-topology/src/software.rs:195-201`, `token_discovery.rs:81-87` and `:76-80`, and
`embarch-umbrella/src/token.rs:97-104` from a 2026-09-06 survey. **Three consecutive legs have now
found task-file line numbers that had aged out**, most recently `core/010` this same leg, where the
cited span had become a doc comment. Find the construct, not the line, and write any drift into this
task file.

**The union-versus-narrow question is the substance, and the task has already reasoned it one way.**
`token_discovery`'s stated reason for its narrower rule is that `$WSL_DISTRO_NAME` can be scrubbed by
an MCP launcher — which argues for a *union* of signals, and `detect_wsl2` already is that union.
**Check that reasoning against the code rather than inheriting it.** Note the two rules are not
merely different, they disagree in a specific direction: `is_wsl2` accepts a `/proc/version`
containing `wsl` but not `microsoft`, which `detect_wsl2` rejects. If delegating genuinely loses a
case that matters, **say so and leave the second implementation in place with the reason recorded
next to it** — the first Done-when box explicitly allows that outcome, and it is a real answer, not
a failure.

**Doc-size reserve for `api`, and two of these are parked behind blocked compaction tasks:**

- `embarch-api/decisions/tool-wrapping.md` — 12222/12288 B, **66 bytes left**, parked by
  `tasks/api/047` (`In flux: yes`)
- `embarch-api/open.md` — 4734/5120 B, 386 bytes left, parked by `tasks/api/026` (`In flux: yes`)
- `embarch-api/spec.md` — 9087/10240 B, 1153 bytes left, same parked task

**Do not write into `decisions/tool-wrapping.md`.** Sixty-six bytes is not headroom and this is not
a tool-wrapping decision. If this unit lands a numbered decision, `embarch-api/decisions/core-link.md`
is the file whose subject this is (token discovery and which Core to talk to) and it is currently
*out* of reserve at 88.6%. **State the placement argument before you look at the sizes, not after** —
a supervisor pre-picking a decisions file to route around a blocked compaction task, then finding the
argument afterwards, is a defect this log has recorded across three consecutive legs, and I am trying
not to make it a fourth by naming a file here. If `core-link.md` is the wrong home on the merits, say
so and put the decision where it belongs.

**If your work pushes `embarch-api/open.md` into its last 10% — it has 386 bytes — compact that one
file as part of this unit** rather than filing a new debt. Its compaction task `api/026` is blocked
on `In flux: yes` for the *event-stream* half of a different file, which parks the pass but not the
reserve; carry `api/026`'s `Must not delete:` list and close only `open.md`'s item.

**The third Done-when box is the one people skip.** `embarch-topology/decisions/crate.md` decisions
4 and 8 assert this consolidation is already done and that "there is no way for the two to disagree,
since there is only one of them". Both are false as written. That is a `status.d/api-*` fragment, and
it is owed **whichever way you resolve the predicate question** — if you leave two implementations
with a recorded reason, those decisions are still false and still need correcting.

**Do not touch hardware.** No live Core, no token read from a real install, no study.
