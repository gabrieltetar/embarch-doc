# 038 — "Am I in WSL2" has three implementations and two incompatible rules, two of them inside one binary that already links the canonical predicate

**State:** open
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
