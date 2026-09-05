# embarch-umbrella: open

**Status:** active, 2026-09-03.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **`doctor` checks 11 and 15 have never been run against a real deployed Core, a flashed bench, or an installed `embarch-api`.** Both are built and unit-tested host-side with every number injected (decisions 33, 34, 35); **what has not happened is one `embarch doctor` against the live install**, which is the owner's to run, not a worker's. Four things only that run can establish: that Core's `/status` really carries `study_designer_schema_version` **and** `core_version` on the deployed build; that `/dev-bench/hello` returns a `compatible` field the check can read; that the *installed* `embarch-api` answers `--json versions` with a `host_type_schema_version` (fabricated binaries and a local debug build are all that has been asked so far, decision 35); and that the check reads **pass** on an install that is genuinely in step, rather than warning on some field-name detail no host test can see. It replaces a stub that reported "not available yet" straight through a real live-pair mismatch, so **a green here is the first evidence this check works at all.**

- **Check 15 catches a *cross-version* stale deploy and not a same-version one.** `core_version` is `CARGO_PKG_VERSION`, so it moves only when the crate version moves: a rebuild-and-failed-deploy at the same version reads as a match. Strictly better than nothing — `deploy-core` has reported `landed` with nothing installed, and its own check compares byte length — but **it is not a hash comparison and should not be read as one.** A content hash served on `/status` would close it and is `embarch-core`'s to decide, not this sub-project's.

- **Five designed pieces are confirmed unbuilt; what is open is whether each is still wanted.** Decisions 18, 22(a-c), 26, 27/29 and 17's amendment: **none is built** (21 and 23 shipped 2026-09-04). [spec.md](spec.md) and each entry say so, and the work is queued in `inbox/`. **Some may be worth retiring instead**: 26's pruning has drawn no pressure, and 18 is a Linux-first-run fix on a Windows-primary suite. Nobody has weighed that.

- **Config fragments or includes**, so the Core section is not duplicated into every firmware repo's config (decision 10). Needs an include mechanism in `embarch-api`'s config loader. **Deferred rather than rejected.**

- **The token and config mirrors still have nothing mechanical keeping them in step with `embarch-api`'s originals** (decisions 16, 20). The CI diff job that was supposed to guard them **was never implemented**, and decision 15's reversal removed only the third mirror. Extract them into a shared crate, or build the diff job — the question is open for these two specifically.

- **A user-level service would avoid needing any elevation at all on Linux and macOS** (systemd `--user`, a launch agent), **but would not start before login, which defeats decision 3's whole point.** Not yet weighed properly. Self-elevation also does not help the no-GUI/no-TTY case — CI, a headless remote session — which still needs decision 7's original print-the-command fallback.

- **Mirrored-mode WSL2 networking has defined behaviour and no evidence.** Only NAT mode has ever run here, so **what got live-validated is NAT mode.** The ambiguity decision 30 resolves is real either way; what is untested is the mode that creates it.

- **macOS is entirely unvalidated and has no machine to validate on.** Deliberately not blocking: ship it and have a Mac-only engineer walk the guide once the primary topology is proven. **Gatekeeper may also make the "just download and run" promise false there specifically**, since the aarch64 build is unsigned.

- **Nothing here has ever seen `claude mcp get`'s output.** No walk of the guide has run with an agent CLI present, so check 10 has never been exercised — and it now parses that output for the command to spawn (decision 23), so that format is assumed rather than observed.

- **Whether `init` should warn when a repo holds more than one recorded build** is undecided. It surfaced on a real repo: `init` read whichever recorded build it found first, **which was an ad hoc dev board's rather than the production board the prior config targeted**, and `init` has no way to know which of several past builds is the "real" one. The zephyr-west discovery of decision 17 is the structural answer for a repo shaped that way, but **a static-discovery repo with several recorded builds still silently gets one picked for it.**
