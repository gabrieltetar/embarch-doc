# Teach zephyr-west discovery the `apps/` layout

**State:** done — leg 062, 2026-09-09. Decision 63
(`embarch-api/decisions/zephyr.md`) records the layout choice: both `app/` and
`apps/` scanned unconditionally and merged, `apps/` wins a same-name
collision, neither present is `ScanError::NoAppDir` distinct from one present
but empty. `resolve.rs`'s `west build <app_path>` argument had the same
`app/`-only hardcoding and is fixed alongside `zephyr.rs`. Filed
`tasks/api/057-compact-api.md`: this fix pushed `decisions/zephyr.md` into its
size reserve.
**Source:** found wiring up a real repo (chargerito-fw) on 2026-09-09; `embarch-api/src/zephyr.rs::scan_apps`
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`scan_apps` reads `<source_path>/app/<name>/CMakeLists.txt` — directory `app`,
singular, hardcoded. A repo that uses `apps/` (plural) gets an empty app list,
and `push_targets_for_soc`'s `for app in apps` loop then emits **zero targets**
— so `list_targets` returns nothing and a `discovery = "zephyr-west"` project is
unusable there, with no error saying why. When this is done, such a repo scans
correctly, and a repo with neither directory still says so rather than
returning an empty list that reads like "nothing is buildable."

Worth deciding rather than just patching: whether the fix is a second hardcoded
name, a small ordered list of conventional names, or a per-project
`app_dir` config field. A repo with *both* `app/` and `apps/` needs a defined
answer either way.

## Why now

Real, not hypothetical. `chargerito-fw` has `apps/{chargerito,driver_test,mlp_test}`
and two boards (`chargerito_core`, upstream `nucleo_g0b1re`) — exactly the
multi-target case decision 12 built live discovery for — and had to be
configured as three hand-written `discovery = "static"` projects instead
(`/home/gabriel/Github/chargerito/chargerito-fw/embarch/embarch.toml`, whose
header comment records this). That is the maintenance burden decision 12 exists
to remove, reintroduced by one hardcoded directory name.

Note the same assumption is in the user-facing contract, not only the code:
`tools.rs`'s `list_targets` description says it "live-scans boards/ and app/".

## Done when

- [x] A repo laid out with `apps/` scans and returns its real targets.
- [x] `app/` keeps working unchanged; a fixture covers each layout.
- [x] The both-directories-present case has a defined, tested behaviour.
- [x] Neither present is distinguishable from "found no apps".
- [x] `tools.rs`'s `list_targets` description no longer says only `app/`.
- [x] Gate green; `decisions.md` (new decision 63) and `interfaces/modules.md`
      updated, a `changelog.d/` fragment dropped. `spec.md`/`open.md` left
      unchanged — both are in the size reserve per leg 062's dispatch notes.
      Filed `tasks/api/057-compact-api.md`: this fix put
      `decisions/zephyr.md` itself into reserve.
