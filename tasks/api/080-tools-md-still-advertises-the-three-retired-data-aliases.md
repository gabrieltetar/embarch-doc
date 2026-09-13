# 080 — `interfaces/tools.md` still advertises "the three data aliases" that `suite/015` retired

**State:** done — leg 107, `agent/api/080-tools-md-retired-data-aliases`, 2026-09-13.
**Doc-size reserve for `api`:** `embarch-api/decisions/surface.md` 11258/12288 B (1030 B left,
filed as blocked `tasks/api/069`), `embarch-api/interfaces/config.md` 11198/12288 B (1090 B left,
filed as blocked `tasks/api/071`). `interfaces/tools.md` and `interfaces/studies.md` are not in
reserve. If your work pushes a file into reserve or leaves one there unfiled, file
`tasks/api/<NNN>-compact-api.md` in the same commit. If you must write into `surface.md` or
`config.md` and the edit would not fit, compact that file in-unit per `DOC-COMPACTION.md` §2,
carrying the parked task's `Must not delete:` list.
**Source:** leg 106 refill sweep, 2026-09-13, scout-verified. Re-read the file:lines below.
**"Scout-verified" is one reader, and it has already been wrong once** — the same scout, same
sweep, reported a quoted source comment as never having existed when it had existed and was later
rewritten (`umbrella/058`). Re-derive the counts here rather than inheriting them.
**Scope:** api
**Hardware:** none — one documentation line, and a sweep to prove it is the only one.
**Owner:** no

## What

`embarch-doc/embarch-api/interfaces/tools.md:15` lists the Studies tools as *"`run_study`,
`study_status`, `study_watch`, `study_stream_data`, `list_study_streams`, **the three data
aliases**"*.

They are gone. `suite/015` retired them 2026-09-11 and recorded it at
`embarch-doc/embarch-api/decisions/study-reads.md:34` — *"`study_power_data`,
`study_waveform_data` and `study_gatt_data` are gone…"* — and the **sibling interface file already
says so**: `embarch-doc/embarch-api/interfaces/studies.md:15` reads *"the three **retired**
fixed-channel aliases"*. So two interface docs in one directory disagree, and the wrong one is the
index a reader meets first.

`grep -rn 'power_data\|waveform_data\|gatt_data' embarch-api/src
embarch-api/crates/embarch-core-client/src` returns **1** hit, a historical doc comment at
`crates/embarch-core-client/src/client.rs:1548`. No tool, no CLI arm, no client method survives.

## Why now

`tools.md` is the tool index — the one file whose job is to be a true list. A tool count or a name
in it is what an agent reads before deciding what to call, and the three names it implies do not
exist, so the failure is a call that 404s rather than a sentence that reads oddly. No gate sees it:
nothing checks a prose enumeration against the `#[tool]` attributes.

## Done when

- [x] `tools.md:15` no longer implies three callable aliases. Say what happened (retired by
      `suite/015`, `decisions/study-reads.md` 34) rather than only deleting the phrase — a reader
      arriving from an older transcript needs the forwarding address, which is
      `study_stream_data`.
- [x] Every other tool count or name in `tools.md` re-derived from the code, not from the file:
      list the `#[tool(...)]` attributes in `embarch-api/src` and check the index against them.
      Say in the task file how many tools there actually are and whether any doc says otherwise.

      **26 `#[tool(...)]`-annotated functions in `embarch-api/src/tools.rs`** (all in one file, one
      per attribute, no duplicates): `list_projects`, `list_targets`, `status`, `build`, `flash`,
      `build_and_flash`, `build_dev_bench`, `flash_dev_bench`, `build_and_flash_dev_bench`,
      `reset_dev_bench`, `dev_bench_hello`, `reset`, `enroll_probe`, `validate`, `alerts`,
      `list_serial_ports`, `declare_signal`, `list_signals`, `remove_signal`, `dev_bench_link`,
      `serial_log`, `run_study`, `study_status`, `study_watch`, `study_stream_data`,
      `list_study_streams`. `tools.md`'s five section lists (3 + 6 + 5 + 6 + 6 = 26, once the
      "three data aliases" phrase is removed rather than counted) match this exactly — `versions`
      correctly noted as CLI-only, no tool attribute. No other count or name in `tools.md` disagreed
      with the code.
- [x] `client.rs:1548`'s historical comment is checked: if it reads as describing a live method,
      fix it; if it is honestly marked historical, leave it and say so.

      Now at `crates/embarch-core-client/src/client.rs:1562` (line drifted from the suite/015 fold
      shifting lines above it — the comment's *text* was already there and unchanged). It reads
      "**This replaced three fixed-channel calls** — `get_study_power_data`/`get_study_waveform_data`/
      `get_study_gatt_data` … which were kept as aliases for one release and are now retired."
      Honestly historical, past tense, correctly named as retired. Left as-is.
- [x] Gate green; `changelog.d/` fragment.

### Re-derived counts (this leg, 2026-09-13)

- `self.status_timeout` in `crates/embarch-core-client/src/client.rs`: **13** call sites, in **13
  distinct functions** (`status`, `alerts`, `list_enrolled`, `dev_bench_port`, `logs_recent`,
  `resolve_chip`, `declare_signal`, `list_signals`, `remove_signal`, `set_dev_bench_link`,
  `list_serial_ports`, `study_streams`, `study_steps`) — confirms the scout's count. Fixed
  `decisions/dev-bench.md` decision 68's "Nine sites reuse `status_timeout` legitimately" to state
  13/13. **Checked whether it was ever right and it was not**: `git show` at
  `57d27f7` (api/037, the commit `dev-bench.md`'s decision 68 was filed alongside) already had 13
  `self.status_timeout` sites in the code at that moment — the doc was wrong the day it was
  written, not a case of the source moving later.
- `study_timeout` (not `status_timeout`) is used at exactly **3** call sites: `post_study`
  (`client.rs:1463`), `get_study_status` (`:1498`), `get_study_csv` (`:1536`, which
  `get_study_stream` delegates to). `study_streams` (`client.rs:1716`) uses `status_timeout`, not
  `study_timeout` — `lib.rs:81`'s doc comment was wrong to name it as a `study_timeout_secs`
  consumer. **Checked whether it was ever right and it was not**: the comment naming
  `study_streams` was introduced by commit `3041549` (the suite/015 fold, 2026-09-11), and at that
  same commit `study_streams` already called `Some(self.status_timeout)` — wrong from the moment
  it was written. Fixed `lib.rs:81`'s doc comment to list `post_study`, `get_study_status`,
  `get_study_stream` and to say explicitly that `study_streams` is not one of them.

## Also worth doing in the same unit, if it holds up

The scout found a second, independent `api` defect and it is cheap to fold in — **verify it before
acting, the counts are the scout's**: `decisions/dev-bench.md:38` (decision 68) says *"Nine sites
reuse `status_timeout` legitimately"*, and
`grep -c "self\.status_timeout" embarch-api/crates/embarch-core-client/src/client.rs` returns
**13**, across 13 distinct functions — 12 reuses beside `status()` itself. In the same cluster,
`crates/embarch-core-client/src/lib.rs:81` names `study_streams` as a `study_timeout_secs`
consumer, but `study_streams` (`client.rs:1702`) uses `status_timeout`; only three sites use
`study_timeout` (`client.rs:1449`, `:1484`, `:1522`). Fix the number and the misattribution, or
say why the count was right as written.

**Done — both re-verified and both fixed.** See "Re-derived counts" above: 13/13 confirmed (fixed
`decisions/dev-bench.md` decision 68's "Nine sites" to state 13), and the `study_streams`
misattribution confirmed and fixed in `crates/embarch-core-client/src/lib.rs:81`. Neither count was
ever right — both traced via `git show` to the commit that introduced the claim, and both were
already wrong in the code at that same commit.

## Do not

Do not re-add an alias, and do not change a timeout's value. Both halves of this task are
corrections to what the docs *say* about code that is already right.
