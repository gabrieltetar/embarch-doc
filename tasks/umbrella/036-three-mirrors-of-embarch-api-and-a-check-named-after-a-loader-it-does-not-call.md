# 036 — `embarch-umbrella` mirrors three things from `embarch-api`; the shared crate now holds two of them, the third has drifted three ways, and check 6 is named after a loader it does not call

**State:** open
**Source:** suite review pass 2026-09-06, dimensions 1, 2 and 4 (three hunters, one subsystem). Code-confirmed by diffing both files.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

Three mirrors, one root, and the argument that justified all three expired on 2026-08-24.

**1. `src/token.rs` is a byte-identical copy whose sync comment cites two files that do not
exist.** Diffed against `embarch-api/crates/embarch-core-client/src/token_discovery.rs`: they
differ only in three test-local env-var names, one temp-dir prefix and one comment — roughly 215
lines. Its header says *"This is `embarch-api/src/token_discovery.rs`, copied rather than
shared … Drift risk and mitigation are the same as `topology.rs`'s: this comment, and tests that
port with no adaptation."* `embarch-api/src/token_discovery.rs` has not existed since 2026-08-24,
and `embarch-umbrella/src/topology.rs` was retired by decision 15's own reversal. **The whole
mitigation is a comment, and both of its citations are dead** — which matters because
`decisions/mirrors.md:31` specifies the never-built guard as *"a CI job [that] fetches the source
file from the other repo at the commit the local copy's own header names."*

**2. `src/config.rs`'s `CoreConfig` mirror has already lost fields.** Its header says *"The same
shape `embarch-api/src/config.rs` deserializes"* — also a moved path. The shared `CoreConfig`
carries `*_timeout_secs`; umbrella's does not. Both already source `port`'s default from the same
place (`embarch_topology::software::DEFAULT_CORE_PORT`, at `src/config.rs:18` and
`core-client/src/lib.rs:49`), so the direction is established.

**3. The `ProjectConfig` mirror has drifted three ways, and `doctor` check 6 answers from it.**
The contract at `src/config.rs:1-10` is *"`doctor` has to see **exactly what `embarch-api` would
see**, not a reinterpretation of it — minus the fields none of checks 6-9 read (`flash_format`,
`env`)."* Upstream `ProjectConfig` (`embarch-api/src/config.rs:67-222`) has 22 fields; the mirror
declares 10 and names two omissions. Specifically:

- `flash_format` is **required upstream, no `serde(default)`** (`:89`) and absent from the mirror.
- `embarch-api/src/config.rs:138-172` keeps `retired_targets` and `retired_soc_chip_overrides`
  *solely so a config declaring them is refused by name* (decisions 51/53). The mirror has
  neither, so `doctor` parses such a config cleanly.
- `embarch-api/src/config.rs:351-356`'s `load_from_path` calls `config.validate()` — resolving the
  token, refusing a missing `source_path`, duplicate names, a bad `flash_format`.
  `embarch-umbrella/src/config.rs:129-133` does none of it.
- The mirror still carries `artifact_path_for_core: Option<String>` (`:72`), a field absent from
  `embarch-api/src/config.rs` entirely — and `src/init.rs:534` still **writes** it into scaffolded
  configs.

So check 6, titled `"embarch-api config loads"` (`src/doctor.rs:859-899`), can report green on a
config `embarch-api` would refuse — while **check 8, in the same run, already shells out to the
real loader** (`:1055-1078`: `embarch-api --config <path> --json list-targets <project>`).

Candidate direction: depend on `embarch-core-client` for the token chain and the core-config
shape — it is already a published path-dep that `embarch-ui` consumes cross-repo, and umbrella
already carries all of its dependencies but `bytes` and three tokio features, with no
`probe-rs`/`serialport`, so the manifest's "deliberately absent" constraint survives. For check
6, source the *verdict* from the loader it is named after using the shell-out one check away;
decision 16's permissive reader can stay for reporting **which** field is wrong, which is its
real requirement.

## Why now

An engineer whose `embarch doctor` reports check 6 green and whose `embarch-api` then refuses to
start on the same file has no way to see which is lying. This is the **fourth** module in the
liftable-copy pattern to hit this, and the third — check 8's mirrored Zephyr scanner — was closed
on 2026-09-05 by shelling out, from this very function's neighbour. `decisions/mirrors.md`
decision 20 declined a shared crate on the cost *"a fourth Rust crate in the suite, versioned and
released, to hold one function … is more machinery than the problem justifies"* and chose a CI
diff job instead, recorded as **"Never actually implemented."** Four days later
`embarch-core-client` was created for exactly these files and the third consumer was never wired
to it, so the suite kept the copy *and* the owed CI job *and* an open question, all justified by
a sentence that is no longer true. `embarch-umbrella/open.md` still frames the choice as
"extract a crate, or build the job", which is the framing the new crate obsoleted.

## Done when

- [ ] There is one reader of the token fallback chain in the suite, not two — or the reason
      umbrella must keep its own is written down against the crate that now exists.
- [ ] `doctor` check 6's verdict comes from the loader its title names, or its title stops
      claiming that.
- [ ] No mirror header in `embarch-umbrella/src/` cites a path that does not exist.
- [ ] `decisions/mirrors.md` decision 20 and `open.md`'s bullet reflect that the shared crate now
      exists.
- [ ] Gate green; `changelog.d/umbrella-*` fragment.

**Adjacent, and worth landing after this:** the same `is_wsl2` copy is the subject of the
`api-am-i-in-wsl2-has-three-implementations…` drop in this batch. If that lands first, umbrella's
copy of it disappears here rather than being fixed twice.
