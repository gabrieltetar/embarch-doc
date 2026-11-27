# embarch-api: open questions

**Status:** active, 2026-11-22.

Truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Known wrong / unfinished

- **`verify` has never read a real Core's zip, and check 4 has met one Typst font set.** Its footer band is 8 to 16 mm, as `hil-pdf.md` now says ([decision 123](decisions/verify-report.md)); a number only `appendix.typ` prints keeps check 4 partial; `report-data.json`'s recompute is a second copy of Core's builder that can drift ([decision 124](decisions/verify-report.md)), as is a Test run's ([146](decisions/verify-test-run.md)), whose step targets Core must record.
- **`person_writer`'s Windows branch has never been built or run.** It is `#[cfg(windows)]` (`symlink_metadata`, reparse-point and `GetFileInformationByHandle` link-count checks); the Unix branch is unit-tested, and Linux cannot compile the Windows target here (a dependency's C build needs a Windows toolchain). Run `cargo test person_writer` on Windows ([decisions](decisions/person-mirror.md) 132, `tasks/api/193`).
- **A `[[projects]]` `board` is a hardware fact nothing checks against hardware.** From `build_info.yml`, it names the last build, not the desk's board; violates [spec.md](spec.md) §2's no-inference-as-fact invariant. `init` no longer writes one (`embarch-umbrella` decision 41); older configs do.
- **Nothing gives a scripted caller a failure *kind*.** `error_kind` is retired unbuilt ([decisions](decisions/surface.md) 16, 50); branching on a cause means matching prose. **Not this repo's fix**: Core's `{code, message, cause}` body (`embarch-core` decision 12) is deferred. **Never derive a kind from the HTTP status.**
- **`artifact_path_for_core` is still tolerated at load** ([decisions](decisions/config-retirement.md) 64); the item, verbatim, is in [open/unmeasured-details.md](open/unmeasured-details.md).
- **`stack`, `patches`, the `embarch-hil` skill install and the report PDF have met only fixtures or one machine** ([decisions](decisions/stack.md) 96, [92](decisions/patches.md), [108](decisions/guide.md), [110](decisions/report-pdf.md)); the four items, plus Windows never running the smoke-harness tier, verbatim, are in [open/unmeasured-details.md](open/unmeasured-details.md).
- **`publish` has met only a mock Core** ([decisions](decisions/publish.md) 113, [115 to 117](decisions/publish-revisions.md), [126](decisions/publish-revisions.md)); the item, verbatim, is in [open/unmeasured-details.md](open/unmeasured-details.md).
- **Real-hardware and real-toolchain verification debts** (bootload, `bench_exchange`, `study_watch`, ledger, lease, build verdict, `build --each`, the live log) live in [open/bench-verification.md](open/bench-verification.md), moved verbatim.

## Structural limits

- **Nothing can read a firmware version off a DUT** — a declared version names the tree built.
- **The artifact-transfer gap reaches the manifest too** ([decisions](decisions/study-reads.md) 39): a remote Core can't see local paths.
- **`list-targets`' `build_dir_name` names only the default combination** ([decisions/target-json.md](decisions/target-json.md) 77) — a non-default snippet/`extra_args` build gets no name; only its `target.json` (decision 69) attributes it. `embarch-umbrella` decision 26's `--prune` must fold `target.json` in beyond the default build.

## Settled-deferred

- **PATH/toolchain preflight** — a build failure surfaces naturally; preflighting taxes the common case for an uncommon message. Expected as a `doctor` check.
- **`serial_log` stays one-shot** — Core's endpoint is bounded; streaming needs Core to grow one, **not this crate's call**.
- **The decision corpus runs narrow across `api`** — several `decisions/*.md` sit near the reserve line; never file an entry in whichever file has room instead of its topic's. `tasks/api/*-compact-api.md` tracks which.
