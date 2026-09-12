# embarch-api decisions: What board.yml/app scanning trusts and how it's kept honest

**Status:** active, 2026-09-12.

Split verbatim out of [zephyr.md](zephyr.md) on 2026-09-12 — that file was 1,950 B past its cap. Decisions 12, 20, 21 and 51 (what a call may name and how it resolves) stayed there; 13, 22 and 63 (what `board.yml`/app scanning trusts and how it's kept honest) moved here unchanged.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). What a call may name and how it resolves: [zephyr.md](zephyr.md). How a build then runs: [build.md](build.md); what it produces: [target-json.md](target-json.md).

### 13 — `soc_chip_overrides`, an escape hatch for a SoC Core cannot map (retired unbuilt 2026-09-05, no replacement)
A per-project `{soc, chip}` list consulted *before* `POST /resolve-chip`: a hand-resolved SoC had somewhere to live, and a hit skipped the call. **Never implemented**: no field, an unconditional call, no `deny_unknown_fields`, so the key was silently dropped on *both* discovery kinds — decision 20's shape 1 again, found by `api/016`.

**Retired because the short-circuit was the design and is the defect.** Core validates every mapping against probe-rs's registry (`embarch-core` decision 8), so a hit here skips that check: one typo reaches `/flash` as a plausible chip name and attaches the wrong physical target, which is what decision 8 refused fuzzy matching to avoid. And it is per-project for a per-silicon fact, consulted *first* — restated per project and per repo, and still winning after Core's table is fixed.

***Rejected: build it anyway.*** The dead end is real — a 404 naming the SoC, nowhere to put the answer — but bounded: one row in the repo that owns the table plus a redeploy this suite already runs, and no unmapped SoC in three months. **What reverses this:** a Core the operator cannot rebuild; the hatch then belongs in Core's own config, machine-scoped and still registry-validated, not in a per-project field here.

Declaring the key is now **refused at load naming the retirement**, on both kinds, pointing at Core's table and `chip-list` — decision 53's posture.

### 22 — The uncached scan's cost bound is written down
Decision 12 never caches, reasoned as "already cheap enough", and **no bound was ever stated for what that assumes**. Stated: single-digit boards, low tens of variant/revision/app combinations, low hundreds of files, comfortably sub-100 ms on ordinary local storage. A repo an order of magnitude larger has not been measured — if the scan ever becomes perceptibly slow, *that* is the signal to revisit caching, not a reason to add it pre-emptively.

### 63 — `apps/` scans exactly like `app/`, and their overlap has a defined outcome
`scan_apps` read `<source_path>/app/<name>/CMakeLists.txt` — `app`, singular, hardcoded — so a repo using the equally-conventional plural `apps/` scanned zero apps, and `push_targets_for_soc`'s `for app in apps` loop then emitted **zero targets**: `list_targets` returned an empty list with nothing saying why, indistinguishable from "this repo genuinely has no buildable app yet". Real, not hypothetical: `chargerito-fw` uses `apps/{chargerito,driver_test,mlp_test}` and had to be hand-configured as three `discovery = "static"` projects instead of the live discovery decision 12 exists to remove that maintenance burden for (`chargerito-fw`'s `embarch/embarch.toml` header comment records this).

**Both `app/` and `apps/` are scanned, unconditionally, and merged.** Not a per-project `app_dir` config field: that would restate, per repo, a fact the filesystem already states, and reintroduces exactly the kind of hand-maintained fact decision 12 exists to stop needing. Not a single ordered "first hit wins" choice between the two either — a repo can plausibly hold both mid-migration, and a project author who only remembers to add one directory to config would silently lose every app under the other. Scanning both, always, means a repo using either name — or, transiently, both — gets its full real app list back with nothing to configure.

**A same-name collision (`app/<name>` and `apps/<name>` both real) resolves to `apps/`, deterministically** — the newer, plural spelling, picked once in `app_dir` and used everywhere a name is later turned back into a path (`scan_snippets`, and `resolve.rs`'s `west build <app_path>` argument, which had the same `app/`-only hardcoding and is fixed alongside this). This is the pathological case of one repo keeping two identically-named app directories at once; the ordinary case (a repo uses exactly one of the two names) never reaches it. *Rejected: refuse the whole scan on a collision* — one misplaced leftover directory during a migration would then break every target in the repo, a worse failure than picking a name deterministically and moving on.

**Neither directory present is now its own error, kept apart from "found no apps".** `scan_apps` returns `Result<Vec<String>, ScanError>`: `Err(ScanError::NoAppDir)` when neither `app/` nor `apps/` exists at all, `Ok(vec![])` when one exists but holds no real (`CMakeLists.txt`-backed) app subdirectory. `scan`'s prior single-purpose `NotZephyrWest` unit struct became `ScanError`'s `NoBoardYml` variant to carry both cases through one type without a second error path threaded separately. Before this, both states produced the same empty `Vec<Target>` from `list_targets` — a caller had no way to tell "this doesn't look like a Zephyr/west project" from "it does, and it currently builds nothing".

Surface text carried the same hardcoded assumption: `tools.rs`'s `list_targets` description said it "live-scans boards/ and app/", now "boards/ and app/ or apps/" — decision 44's lesson that a tool description is itself a claim a caller reads and trusts, not decoration.
