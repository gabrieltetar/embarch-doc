# 080 — `interfaces/tools.md` still advertises "the three data aliases" that `suite/015` retired

**State:** open
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

- [ ] `tools.md:15` no longer implies three callable aliases. Say what happened (retired by
      `suite/015`, `decisions/study-reads.md` 34) rather than only deleting the phrase — a reader
      arriving from an older transcript needs the forwarding address, which is
      `study_stream_data`.
- [ ] Every other tool count or name in `tools.md` re-derived from the code, not from the file:
      list the `#[tool(...)]` attributes in `embarch-api/src` and check the index against them.
      Say in the task file how many tools there actually are and whether any doc says otherwise.
- [ ] `client.rs:1548`'s historical comment is checked: if it reads as describing a live method,
      fix it; if it is honestly marked historical, leave it and say so.
- [ ] Gate green; `changelog.d/` fragment.

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

## Do not

Do not re-add an alias, and do not change a timeout's value. Both halves of this task are
corrections to what the docs *say* about code that is already right.
