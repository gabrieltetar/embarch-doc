# api: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-11

### Added
- `embarch-api person call-log-quota <size>` raises the call log's quota with the person's token after a typed `yes`; `call-log` now prints `size_bytes` and `quota_bytes` (api decision 141).
- A new MCP tool and CLI verb, resume_test / resume-test, prepare a new Test run of an interrupted run's pending tests through Core's resume route; the go stays the engineer's (decision 148).
- A Test report prints each limit's decision rule, `w` and `U`, and `verify` rebuilds those fields from `run.json` (decision 147).
- `verify` checks a Test run's zip: every verdict recomputed through the shared crate, report-data rebuilt, both exports regenerated (decision 146).
- embarch-api: a Test run's zip carries a JUnit XML and an OCP T&V JSON Lines export mapped from its verdicts; a skip for a gap is `<error type="not_verified">` (decision 145).
- `publish` takes a Test run id: one zip over every study run's files and a PDF by requirement; the exports, verify and a resumed pair wait (decision 144).
- embarch-api person (confirm, go, answer, unit, name) acts for the engineer from a terminal with the person's token after a typed yes; no MCP tool (embarch-api decision 141).
- Client StatusResponse carries Core's mode and keyid (api decision 139).
- api: declare_instrument carries an instrument's metrology and calibration (a certificate file sent as its SHA-256); a re-declare keeps what is stored (decision 138)
- The client's PendingPrompt and answer carry a Test run prompt's kind, observation, switched_on and answer value; see [decision 137](../embarch-api/decisions/client-crate.md).
- api: CoreClient::test_run_go carries the person's go for the UI; the go ban narrows to the agent's MCP and CLI sources (decision 135).
- api: run_test prepares a Test run and never starts it; test_status reads it; answer_prompt explains a 403. See embarch-api/decisions/test-run.md
- The core client has pending_confirmations, confirmation_card and confirm for Core's confirmation routes, for the UI's card; no MCP tool or CLI subcommand.
- embarch-api adds cancel_study and cancel-study, which stop a running host or device study through Core's cancel route (EMB-487).
- `test_propose` and `test_plan` (and CLI twins) send a test, capability or hook to Core to confirm and keep plans and custom suites under `embarch/tests/` (decision 134).
- embarch-api person_writer is the confined writer for the person's embarch/ folder: fixed kinds and names, no link followed, atomic ([decision 132](../embarch-api/decisions/person-mirror.md)).
- embarch-api list-studies lists Core's retained studies newest first with each tap's encoding and a flat encoding_kind (EMB-405).
- A shared fixture, `embarch-api/tests/fixtures/live-log/`, pins the five rules both live-log writers follow; a Rust test runs every case ([live-log](../embarch-api/interfaces/live-log.md)).
- `declare_instrument` and `declare_signal` (and their verbs) take `safe_off`; a re-declare that omits it keeps the stored one. [decision 97](../embarch-api/decisions/instruments.md)
- Each call that reaches a lease-gated route appends a line to the firmware repo's embarch/live/ log, citing Core's call-log entry; call_log reads entries back (EMB-255).
- `study_measurements` tool and `study-measurements` subcommand read a finished run's measurements.json before publish, naming Core's four refusals; see embarch-api/interfaces/studies.md.
- `embarch-api core-key` prints Core's public key and fingerprint after checking its signature over a fresh nonce; the HIL guide's Study step 6 uses it (EMB-247).
- verify checks 4, 6 and 9: the PDF's numbers, report-data recomputed, report.typ's syntax tree; publish refuses by the same whitelist.
- `embarch-api verify <zip> --public-key <hex>` checks a published Study zip offline: signatures, manifest, measurements, labels, exports, run log (decisions 118 to 121).
- publish lists every number in the prose and report.typ, names each prose block's author, and writes -r2 from the earlier zip ([decisions](../embarch-api/decisions/publish-revisions.md) 115-117).
- `publish <run id>` (tool and subcommand) writes a finished Study run as one zip: PDF, Core's signed files, both exports, sources. [interfaces](../embarch-api/interfaces/publish.md)
- `run_study` sends Core the project checkout's commit, dirty state and `west` version as build claims, none without a git checkout; [decision 111](../embarch-api/decisions/build-claims.md).
- embarch-api renders a report's `report.typ` to PDF offline, Typst built in, lilaq embedded, root confined to the staged files ([decision 110](../embarch-api/decisions/report-pdf.md)).
- embarch-core-client resolves the agent or the person token by scope; MCP and CLI send only the agent token ([decisions](../embarch-api/decisions/client-crate.md) 109).
- Serve the HIL guide: embarch-api guide hil [live|study|test] prints the text embedded in the binary; an embarch-hil skill points at it (decision 108).
- api: `bundle` verb and MCP tool package a build as a hex, README of flash commands and zip for a bench engineer; see interfaces/tools-bundle.md.
- build --each <base>..<tip> builds every commit in every variant from its own module sources, with --same-tree-as ([decisions](../embarch-api/decisions.md) 104).
- build answers with a verdict (warnings, first error, FLASH/RAM, log_path) and builds named variants in their own directories ([decisions](../embarch-api/decisions.md) 102, 103).

### Changed
- `verify` reads a Test run report's attestation by its signed record's `observed.release`, as for a Study, and its appendix prints Core mode and Release (decision 124).
- embarch-core-client takes LoadAnswer and LEASE_GATED from embarch-core-wire; StudyEvent and the hello stay lenient, drift-tested against it (decision 49).
- `verify` check 6 reads a report's attestation by the signed record's `release` key: Core mode and release instead of `core_attested` ([decision 124](../embarch-api/decisions/verify-report.md)).
- Finding embarch.toml is one function in embarch-core-client (explicit path, EMBARCH_API_CONFIG, walk up); the API uses it. See api decision 152.
- Core-client token discovery takes the machine data directory from embarch-topology; an unset ProgramData now errors by name instead of falling back to C:\ProgramData.
- embarch-core-client's /status exposes host_type_schema_version, read from either key (api decision 150).
- Compacted api spec.md: publish appendix and verify check list moved verbatim to their interface files.
- `verify` judges a refused Exchange step under the `target` Core recorded on its row; a row without one is still read both ways (decision 149).
- The client's `PromptPending` event carries a Test run prompt's kind as `prompt_kind`, read without polling the study (137); `embarch-ui`'s test literal names `prompt_kind: None`.
- `test_show`, `test_pending` and `test_add` read Core's run log and replace `ledger_*`; `run_study` no longer takes `test` (decision 142).
- verify check 2 now recomputes Exchange step outcomes and step-time numbers from the recorded replies and fails naming the step or measurement.
- embarch-api test-propose fills and checks a test's study hash with the crate's `study_hash`, not the study file's bytes ([decision 136](../embarch-api/decisions/test-plans.md)).
- Core's no-measurements refusal is read by its 422 status or `code`, never its wording; the tool no longer says a host study has none ([studies](../embarch-api/interfaces/studies.md)).
- embarch-api: test_propose and test_plan write the repo's test files through the person writer, which refuses links and hard-linked targets (decision 132).
- The client sends Core's token only after a verified challenge, picked by the core-fingerprint beside the token file; `status` shows the mode (api decision 133).
- Compacted embarch-api open.md out of reserve by moving two debts verbatim into open/ files.
- api: the HIL guide's Words entry for Study now names the glossary row as its definition (EMB-317).
- The embedded HIL guide sends the DUT census to `dev-bench.log`: `fail_reason` is capped and names only advertisers that sent a name (EMB-402).
- The embarch-api README no longer counts tools or endpoints and its getting-started follows the user guide (embarch init).
- The live log's contract now states the file name's zone, `sent`'s form per writer, `core_calls` on a failed call and a writer's added fields (`outcome`).
- Check 6 recomputes report-data.json's observed.call_log (head, range, count) from the signed record, and the appendix prints it; a zip from a Core before core/148 fails check 6.
- `verify` check 8 now recomputes a zip's call-log segment against the signed record's range; no segment still reads "no call log".
- A lease Core released after 30 idle minutes now drops this process's token and refuses the next hardware call until `lease_take`; see [lease tools](../embarch-api/interfaces/tools-lease.md).
- Split the verify section of interfaces/publish.md into interfaces/verify.md, verbatim; publish.md leaves reserve (tasks/api/173).
- `publish` republishes a swept run by handing Core the earlier zip's own files back; with no earlier zip it refuses naming the file ([decision 126](../embarch-api/decisions/publish-revisions.md))
- Split embarch-api client-crate.md (decisions 55, 66) and config.md (zephyr-west selection) into topic files, verbatim; both out of reserve.
- Split embarch-api `spec/implementation.md` §4 (deployment and topology) verbatim into `spec/deployment.md`, clearing its size reserve.
- Release workflow signs every archive with cosign (keyless, `.sigstore.json` bundle beside each); see embarch-api/spec/implementation.md §8.
- A server running in a git worktree of the clone source_path is in builds that worktree, in a build dir of its own, or refuses naming both trees; decision 106.
- - embarch-api/open.md split: bench and toolchain verification debts moved verbatim to open/bench-verification.md (api/150).
- `dev_bench_hello` and `dev-bench-hello --json` carry `dev_bench_version`; `run_study` refuses a pinned bench version Core did not report (105).
- Windows tree kill on a timed-out build verified on Windows; decision 75 drops its unix-only qualifier ([decisions/build.md](../embarch-api/decisions/build.md)).

### Fixed
- A swept run's republish no longer PUTs `call-log-segment.jsonl` to Core's restore route, which refused it with 422 (EMB-288).
- Verdict memory is the first linker table, the application's on sysbuild, not MCUboot's; decision 128.
- Zephyr-west scan takes a board's CPU clusters from its SoC's soc.yml when board.yml names none ([decision 127](../embarch-api/decisions/zephyr-scan.md)).
- The bundle README's recover line now states only what core decision 32 measured and no longer says decision 36 maps it to the range erase.
- Bundle README now gives Core's range-erase nrfutil command, not ERASE_ALL, and says it is unconfirmed on a board.
- embarch-api tests name their scratch directories from a process-wide counter (support::unique_dir), not the nanosecond clock; two tests no longer share one.
- embarch-api tests: the binary-spawning tests strip `EMBARCH_REQUIRE_LEASE`, so `cargo test --manifest-path` from the suite root no longer fails 20 tests.
- lease_client tests no longer flake: two tests in one clock tick shared a scratch dir; a counter names it now (api task 151).

### Removed
- Removed the `instrument_exchange` tool and `instrument-exchange` subcommand; Core refuses that route, so an instrument is reached by a host study's `Instrument` step (EMB-257).

### Decided
- The desk's config dir, data dir, token path, port and base URL are one module in embarch-core-client; session_desk.rs uses it (151).
- embarch-api: an identity tool refused 403 on an attested Core names its `--as-person` command and the Topology tab ([143](../embarch-api/decisions/identity-acts.md)).
- Found and pinned in a test: an api build runs the config's source_path, not the session's worktree, so a worktree session builds the main clone; a known defect, bug EMB-181, not fixed here. See [spec](../embarch-api/spec.md).
## 2026-10

### Added
- A call naming no project, or naming desk, builds the open desk's firmware repo (decision 85).
- API: `mem_read` tool and `mem-read` subcommand over Core's live memory read; ranges as `ADDRESS[:WORDS]`.
- API: `signal_exchange` / `signal-exchange` take `port_wait_ms` / `--port-wait-ms`.
- API: signal_exchange tool and signal-exchange subcommand, and baud on declare_signal (decision 82).
- `enroll_probe` without `role` enrolls a bench board; `unenroll_probe` takes `probe_serial` (decision 84).
- `ledger-add`, `ledger-show`, `ledger-pending` (CLI and MCP): a per-project hardware test ledger with a computed pending-by-hardware view; `run-study --test` appends a row.
- `embarch-api stack plan|fold|restack` folds review fixes into their commits by blame, backs up every branch, and restacks a PR stack with one atomic leased push.
- api: serial_log takes signal (+port_wait_ms), the preferred form; Core resolves it; project/port stay the fallback (decision 94).
- `embarch-api patches export|import|regroup`: one scratch tree for a west manifest's patch series; fixes fold by blame, regroup proves tree identity. Decision 92.
- `core_state` tool and `core-state` subcommand over Core's POST /live/core-state; `mem_read` shows found/left/halt_count and marks `halted` deprecated (decision 83).
- declare_signal tool and declare-signal --interface take a direct route's USB interface, refused on a via-dev-bench route (embarch-topology decision 46; suite/052).
- `lease_take`/`lease_renew`/`lease_release`/`lease_show` and `EMBARCH_LEASE_TOKEN` sent on every Core call; `status` shows `lease` and `last_images` (decision 90).
- `bench_exchange` / `bench-exchange`: one call runs console commands and returns every listened console as one filtered timeline; times are client-observed, see embarch-api decision 89.
- api: `capture_start`/`capture_read`/`capture_stop` tools and `capture-*` CLI twins over Core's background signal capture ([tools-capture](../embarch-api/interfaces/tools-capture.md)).
- `signal_exchange` and `signal-exchange` take `match_after_echo` (CLI `--match-after-echo false`), so a console with echo off returns at its prompt instead of the timeout.

### Changed
- embarch-api/open.md compacted 4810 B to 3905 B, out of reserve; all 11 known-wrong items and the settled-deferred reasons kept.
- Compacted embarch-api/decisions/client-crate.md out of the size reserve (11581 to 10817 B); cold incident and provenance sentences cut, rules and reversal conditions kept.
- CLI stream listing says "no records found" for a zero-record report, not "0 of 0 records verified"; see tasks/api/141.
- api: a build now waits for, and says it is waiting on, another process building the same project; one build per key across CLI, MCP and UI ([decision 91](../embarch-api/decisions/build.md))
- bench_exchange places lines at Core's first-byte receive times (core 94) when sent, poll time otherwise; time_basis names the basis per signal; client fields are Option (api 89).
- `status` reports `last_images` as null for a Core that predates it, distinct from `[]` (nothing flashed since start); decisions 58, 90.
- serial_log and serial-log carry Core's truncated flag (true marked, absent from an older Core reported as unknown, never false); config.md says flash_format is required for every project.
- `enroll-probe` (CLI and MCP) says when an enrol vacated or displaced a role; the client mirror carries `displaced`, `vacated`, `vacated_kept`.
- api: signal_exchange and signal-exchange now report Core's wire fields (port_lost, echo, port identity, core state); port_lost exits 5; decision 82 amended.
- api: signal-exchange exits 3 (--until never seen), 4 (zero bytes) or 5 (truncated) with a stderr line; new --clean drops escapes, echo and prompt. Decision 82.
- Flash results carry `erased`, the ranges Core blanked; the `erase` description now says it skips option bytes and never chip-erases (core decision 84).
- `embarch-api/open.md` compacted 4714 to 3780 B: answered bullets deleted, their facts homed in `interfaces/config.md` and decision 70.

### Fixed
- api: ledger_pending matches a role-less bench board by its enrolled name, matches instruments, and flags ambiguous needs (decision 98).
- Study stream 404s (data and arrivals) now keep Core's body, naming the declared taps; the unbuilt MCP startup check is retracted from the spec and decisions 14/17 (api/136).
- `study-status --follow` and `study_watch` now end on an unknown study id (error naming it) or an `interrupted` study (own outcome, CLI exit 1) instead of waiting forever.
- An older Core's exchange and flash replies no longer show fabricated written/bytes_read/port_lost/erased values: absent stays absent ([decision 58](../embarch-api/decisions/client-crate.md)).
- `list_targets` accepts the shortened `<board>.dts` of a single-SoC board and errors with a per-board reason when every board is dropped, not `targets: []`. Decision 86.
## 2026-09

### Added
- A follow renders `StreamText` chunks: one line each on the CLI, counted per tap as `text_chunks` in `study_watch`.
- The shared client mirrors `OutpostRows` and the new event stamps, as `#[serde(default)]` so an older Core still decodes.
- `CoreClient::list_studies()` reads Core's new `GET /studies` — a past study is reachable without its id.
- `bootload`, `build_and_bootload` and three bootload-port tools, each with a CLI twin; `[projects.bootload]` config; sysbuild-aware signed-image lookup. Decisions 80, 81.
- `set-role-board` (CLI and MCP) declares which board type is in a role, over Core's new no-attach route.
- `unenroll-probe` (CLI and MCP) retracts a role; `enroll-probe` gains `--name` for the board it is enrolling.

### Changed
- `config`/`zephyr`/`resolve`/`build`/`json_out` move to a shared `embarch-firmware-build` crate `embarch-ui` can reach too (decision 78).

### Fixed
- Snippet lists keep the order west applies them in; sorting made two different images share one build directory (decision 21).
