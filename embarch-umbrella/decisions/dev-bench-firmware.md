# embarch-umbrella decisions: check 13, the dev-bench firmware comparison

**Status:** active, 2026-09-07.

Split out of [doctor.md](doctor.md) 2026-09-07 (`tasks/umbrella/037`) as this file's own mission, the way [bind.md](bind.md) and [integration.md](integration.md) were split before it — decision 19 moved verbatim, restating nothing.

Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/doctor-chain.md](../interfaces/doctor-chain.md)'s check 13 row.

### 19 — A stale-dev-bench-firmware check

It compares the bench's reported firmware version, over a handshake-only endpoint Core added for exactly this, against `git describe` in whichever local dev-bench checkout is configured — a machine-level state field, settable at setup or overridable per call. A mismatch fails with a fix line naming the reflash step, **whose exact command depends on which board, unlike this decision's original text assumed.**

**The configured path must name a path native to wherever `doctor` itself runs**, not a cross-filesystem view of one: Windows against a WSL2 checkout over a UNC path **spuriously reports the checkout as always-dirty, because Windows' git cannot read that repo's symlinks over that path.**

### 47 — No checkout configured is a fail, and an unresolvable id is not an ordinary mismatch

`umbrella/034`'s bench run found decision 19's check silent by default: nothing in `setup` or `init` ever writes `dev_bench_repo_path`, so an unconfigured machine read a `Warn` that looked like background noise on every default install. **Promoted to `Fail`, naming `setup --dev-bench-repo <path>` as the fix.** This arm only runs once a bench has answered `/dev-bench/hello` — "no bench at all" is a separate, unaffected `Pass` — so nagging a benchless machine, the candidate direction's own worry, does not apply here.

*Rejected: have `setup`/`init` auto-detect the checkout.* `state.rs`'s own comment on this field already says why not: a checkout "can live anywhere," and probing for it would find a stale tree as often as the right one — the same reasoning that keeps this the one field `core_exe` autodetection does not extend to.

**A reported `firmware_version` that resolves to no commit in the configured checkout is its own fail, `unresolvable`, not the ordinary `stale` mismatch.** The same run flashed a bench from a checkout whose history had since been rewritten (a client-name scrub, unproven but the leading candidate): `git describe`'s hash survives unchanged in the flashed firmware but the commit it names is gone from the checkout — not in `git cat-file -e`, a tag, or any reflog. `stale` and `unresolvable` want different operator actions to *understand* the result even though the fix line is identical either way (rebuild and reflash): a `stale` reading names how far behind the flash is, an `unresolvable` one cannot.
