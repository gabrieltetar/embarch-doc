# 015 — Retire the three fixed-channel study-data aliases, kept "for one release" on a surface strictly worse than its replacement

**State:** open — announced 2026-09-11 by leg 092, `ts` `1789189358.707879`, 30-minute window per
`embarch-fleet/ops.md` §4. If this leg ends before the window closes, **read the thread and complete
the window rather than restarting it.**
**Source:** suite review pass 2026-09-06, dimension 6 (deletion candidates). Code-confirmed, with a whole-suite caller grep.
**Scope:** suite
**Hardware:** none. Route retirement and one UI call repointed; no board, no study.
**Owner:** no

## What

`GET /study/{id}/stream/{name}` plus `list_study_streams` replaced three fixed channels, and the
three old spellings were kept on an explicit expiry — `embarch-core/src/study.rs:2980-2983`:
*"kept as aliases for one release rather than breaking `embarch-api`'s existing … tools
mid-flight."* `v0.1.0` (2026-08-11) is still the suite's only release
(`suite/roadmap.md` §Release), so the window cannot close on its own, and nothing tracks it.

**The aliases are strictly the worse surface.** `embarch-api/interfaces/studies.md:15` says
`list_study_streams` exists *"since the aliases below structurally cannot report"* truncation —
so they are the only read path that cannot tell a caller its capture was lossy, which is the
class `embarch-decision-reversals.md` row 98 already cost this suite an investigation on. And
`embarch-core/src/stream_store.rs:694`'s `alias_for` maps a `PowerFrontEnd` source to `"power"`,
a capture that cannot exist: power profiling is deferred at the owner's call with no hardware
ordered, and `Step.power_sample` is already retired.

**One caller in the whole suite.** Grepped all nine repos plus the doc corpus for
`get_study_power_data|get_study_waveform_data|get_study_gatt_data|power-data|waveform-data|gatt-data|study_power_data|study_waveform_data|study_gatt_data`.
Outside the definitions and their own tests there is exactly one: `embarch-ui/src/study_designer.rs:1737`,
on the `gatt` alias. `power` and `waveform` have **no caller anywhere**. The replacement is
already wired in the same binary — `embarch-ui/src/main.rs:571` calls
`core.get_study_stream(study_id, name, false)` and the UI already calls `core.study_streams()`
to learn the names.

Retiring all three removes, counted: Core's `power_data_handler`, `waveform_data_handler`,
`gatt_data_handler`, `serve_alias` (and with it its nested pre-`streams/` legacy-filename
fallback and its `legacy_file` parameter), `StreamIndex::find_alias`, `alias_for`, the
**persisted** `StreamIndexEntry::alias` field written into every study's `streams/index.json`,
three route registrations and three rows of the bearer-token route sweep (26 → 23);
`embarch-core-client`'s `get_study_power_data`, `get_study_waveform_data`,
`get_study_gatt_data`; three `embarch-api` MCP tools, three CLI subcommands and three `cli.rs`
functions; and the "kept for one release" sentence in five docs. **16 named things.**

Candidate direction: repoint `embarch-ui`'s `api_gatt_data` at the tap name it already gets from
`study_streams()`, then retire all three together — keeping one keeps `alias`, `find_alias` and
`alias_for`. `streams/index.json` itself stays: it is also the name-to-file resolution that stops
a tap name escaping the directory. Whether the pre-`streams/` on-disk fallback still has local
results to serve is a separate call; if it does, hang it off the generic route rather than off a
retired one.

## Why now

An agent choosing a study-data tool sees four descriptions, three of which say to prefer the
fourth, and the three cannot report a truncated capture. This is the strongest deletion in the
pass: the fix makes the suite smaller in three repos at once, and the expiry it was granted was
recorded as *settled* rather than as owed, so no `open.md` carries it and the fleet's own refill
sweep cannot see it.

## Done when

- [ ] `GET /study/{id}/power-data`, `/waveform-data` and `/gatt-data` no longer exist, or the
      reason to keep one is written down where a later reader will meet it.
- [ ] No caller of a fixed-channel study-data route remains in any repo (grep, not inspection).
- [ ] The route sweep's row count matches the router's, and `embarch-core/interfaces.md` matches
      both.
- [ ] Gate green; `changelog.d/` fragments; `status.d/` fragment for the five docs' "one release"
      sentence.
