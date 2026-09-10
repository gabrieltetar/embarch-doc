# 036 — `embarch-umbrella` mirrors three things from `embarch-api`; the shared crate now holds two of them, the third has drifted three ways, and check 6 is named after a loader it does not call

**State:** claimed by agent/umbrella/036-mirrors-two-and-three, 2026-09-10 15:36 — **partially
done**: mirror 1 (token) closed 2026-09-08; mirrors 2 and 3 are what this dispatch takes, see the
leg 066 dispatch note at the end
**Narrowed 2026-09-08 (leg 051):** dispatched as **mirror 1 only** — the token
chain — plus the two doc items that ride on it (`Done when` bullets 1, 3, 4, 5).
Mirrors 2 and 3 (`CoreConfig`'s lost fields, `ProjectConfig`'s three-way drift,
and `doctor` check 6's title) are **explicitly out of this dispatch** and stay
open; see the state note this unit leaves.
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

- [x] There is one reader of the token fallback chain in the suite, not two — or the reason
      umbrella must keep its own is written down against the crate that now exists.
- [ ] `doctor` check 6's verdict comes from the loader its title names, or its title stops
      claiming that.
- [x] No mirror header in `embarch-umbrella/src/` cites a path that does not exist.
- [x] `decisions/mirrors.md` decision 20 and `open.md`'s bullet reflect that the shared crate now
      exists.
- [x] Gate green; `changelog.d/umbrella-*` fragment.

**Adjacent, and worth landing after this:** the same `is_wsl2` copy is the subject of the
`api-am-i-in-wsl2-has-three-implementations…` drop in this batch. If that lands first, umbrella's
copy of it disappears here rather than being fixed twice.

## State note (2026-09-08, leg 051 dispatch, mirror 1 only)

**Closed this run:** `src/token.rs` is deleted. `embarch-umbrella/Cargo.toml` depends on
`embarch-core-client = { path = "../embarch-api/crates/embarch-core-client" }`; the three
`doctor.rs` call sites and the one in `main.rs` now call
`embarch_core_client::token_discovery::resolve_token` directly, in-process. Confirmed
byte-for-byte-equivalent behavior against `token_discovery.rs` (identical signature; test
differences were only three env-var names and one temp-dir prefix — every umbrella-specific
test case has a direct upstream counterpart, so none needed a local `tests/` file).
`src/config.rs`'s `CoreConfig`-mirror header no longer cites the dead `embarch-api/src/config.rs`
path — corrected to name `embarch-api/crates/embarch-core-client/src/lib.rs` as where
`CoreConfig` actually lives now, while noting umbrella's `CoreConfig` is still its own hand-kept
mirror (that mirror itself is untouched — see below). Every other in-repo comment that referred
to the now-deleted `token.rs` as a sibling module was repointed at
`embarch_core_client::token_discovery`. `decisions/mirrors.md` decision 20 got a 2026-09-08
amendment paragraph recording the token half closed, the config half still open.
`embarch-umbrella/open.md`'s bullet was rewritten to the same effect. `cargo tree` confirms
`probe-rs`/`serialport` stay absent after picking up the shared crate's `reqwest`
(`json`/`query`/`multipart`) and `tokio` (`sync`/`fs`/`process`) feature unification, as the task
file's own reasoning predicted. Gate green: `cargo build`/`test`/`clippy --all-targets -D
warnings` clean (216 tests pass) in the code worktree; `check-docs.py`, `check-ownership.py
--scope umbrella` (both worktrees) and `check-client-names.py` all clean.

**Left open, explicitly not touched by this dispatch (mirrors 2 and 3):**

- **Done-when bullet 2** — `doctor` check 6 (`src/doctor.rs:859-899`, titled `"embarch-api config
  loads"`) still answers from the hand-mirrored `ProjectConfig`, not the real loader. Untouched.
- **`CoreConfig`'s missing `*_timeout_secs`** (`src/config.rs`'s `CoreConfig` struct vs.
  `embarch-api/crates/embarch-core-client/src/lib.rs`'s). Untouched — the header now cites the
  right file, but the field gap itself remains.
- **`ProjectConfig`'s three-way drift**, all still present in `src/config.rs`:
  - missing `flash_format` (required upstream, no `serde(default)`);
  - missing `retired_targets`/`retired_soc_chip_overrides` refusal-by-name fields
    (decisions 51/53 upstream);
  - no call to `.validate()` on load (`src/config.rs:129-133` area) — token resolution,
    `source_path` presence, duplicate-name and `flash_format` checks all skipped;
  - the phantom `artifact_path_for_core: Option<String>` field, absent from upstream
    `ProjectConfig` entirely, and **`src/init.rs:534` still writes it** into scaffolded configs.

None of the above were touched, per this dispatch's explicit narrowing. This task stays open —
**do not close it** — for whichever leg picks up mirrors 2 and 3.

## Dispatch note (leg 066, 2026-09-10 15:36) — mirrors 2 and 3, and this closes the task

**You are taking everything leg 051 left**, so if you finish it, this task closes: `Done when`
bullet 2, `CoreConfig`'s missing `*_timeout_secs`, and all four strands of `ProjectConfig`'s
drift. Bullets 1, 3, 4 and 5 are already ticked and are not yours to revisit.

**Bullet 2 is the one with a real choice in it, and the task's own candidate direction is the one
I would take**: source check 6's *verdict* from the loader its title names, using the shell-out
that check 8 already performs one function away (`src/doctor.rs:1055-1078` — read it; it is the
worked precedent in this same file, landed 2026-09-05 for exactly this reason). Decision 16's
permissive reader stays for reporting **which** field is wrong, which is its actual requirement.
**If you conclude instead that the title should stop claiming the loader, that is a legitimate
answer** — but then say what check 6 *is* answering, because "parses under a permissive mirror"
is a fact about umbrella, not about whether `embarch-api` would start.

**The four `ProjectConfig` strands are each independently checkable, and none needs a design
call**: `flash_format` required upstream with no `serde(default)`; the `retired_targets` /
`retired_soc_chip_overrides` refuse-by-name fields (upstream decisions 51/53); the missing
`.validate()` call on load; and the phantom `artifact_path_for_core`, which `src/init.rs:534`
**still writes into scaffolded configs** — so removing the field without removing that write
leaves `init` producing a config its own loader drops silently. Do those two together or neither.

**Verify every claim above against the code as it stands before you act on it.** This task's body
was written 2026-09-06 and cites line numbers on both sides; leg 051 landed in between and moved
things. `embarch-api/crates/embarch-core-client/src/lib.rs` is where `CoreConfig` lives now, not
`embarch-api/src/config.rs`. **Read `embarch-api`, do not write it** — it is another
sub-project's repo and `check-ownership.py --scope umbrella` will refuse any edit to it. If the
right fix turns out to need an `embarch-api` change, stop and write that half into
`/home/gabriel/Github/embarch/embarch-doc/inbox/` by that absolute path, per `inbox/README.md`.

**Doc-size reserve, and this is the constraint most likely to bite you.**

- `embarch-umbrella/spec.md` — **10,104 / 10,240 B (98.7%), 136 bytes left.**
- `embarch-umbrella/open.md` — **4,870 / 5,120 B (95.1%), 250 bytes left.**
- `embarch-umbrella/decisions/bind.md` — 11,409 / 12,288 B, 879 B left.
- `decisions/mirrors.md` — **6,267 / 12,288 B, ~6 KB free.** This is where your decision or
  amendment goes. `decisions/doctor.md` is 11,019 / 12,288 (1,269 B left) — usable but tight.

`spec.md` holds the eighteen-row `doctor` chain table, and check 6's row is in it. **136 bytes
will not cover a row rewrite.** Its compaction task `tasks/umbrella/038` is `blocked` on
`In flux: yes` — legitimately, because `tasks/umbrella/033` is an open check-17 row change — and
under `DOC-COMPACTION.md` §2 **a blocked compaction task parks the pass, not the reserve**: since
you are the actor making the flux in this table, you are the only one who can shorten what you
are rewriting. So:

1. **First try to make your `spec.md` edit net-zero or net-negative.** A row whose status changes
   from "designed" to "sourced from the real loader" may well be shorter. That is the cheap out
   and you should take it if it is available.
2. **If it is not, compact `spec.md` as part of this unit**, carrying `tasks/umbrella/038`'s
   `Must not delete:` list — go read it, it is specific and two of its items are there because a
   previous pass got them wrong. Close **only** the `spec.md` item on `038`; leave its `open.md`
   item and its `blocked` state alone, and say in `038`'s body what you paid and what you left.
   `038`'s own note says to run `scripts/check-duplication.py embarch-umbrella` first — do that;
   `decisions/doctor.md` re-arguing what `spec.md`'s table already owns is the suspected
   duplication and would be the cheapest real shave.
3. **Do not trim wording alone.** `038` records the measured finding that 37 bytes of reworded
   prose is not a real shave.
4. Keep `open.md` net-zero or net-negative. If your work answers the `open.md` bullet about
   check 6, strike it — that is a genuine paydown and worth more than the bytes.

**Answer `DOC-COMPACTION-PASS.md`'s question in your closing note if and only if you ran a
compaction pass**: can `spec.md` alone answer what someone needs to work on `embarch-umbrella`
today?

**Gate reminders specific to this unit.** `cargo build` / `test` / `clippy --all-targets --
-D warnings` must be clean in the code worktree — leg 051's run of this task passed 216 tests, so
a drop in that count is a signal, not noise. `embarch-umbrella` path-depends on
`embarch-topology`, `embarch-study-designer` and `embarch-api`; I have symlinked all three into
your worktree's parent, so if a build fails on a path under `.worktrees/`, tell me rather than
making a link yourself. Run `scripts/check-client-names.py --repo <your code worktree>` too —
`check-docs.py` does not reach the code repo.
