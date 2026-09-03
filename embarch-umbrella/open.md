# embarch-umbrella: open

**Status:** active, 2026-09-03.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md).

- **`doctor` checks 11 and 15 have never been run against a real deployed Core or a flashed bench.** Both were built and unit-tested host-side on 2026-09-03 (decisions 33, 34) with every number injected; **what has not happened is one `embarch doctor` against the live pair**, which is the owner's to run, not a worker's. Three things only that run can establish: that Core's `/status` really carries `study_designer_schema_version` **and** `core_version` on the deployed build; that `/dev-bench/hello` returns a `compatible` field the check can read; and that the check reads **pass** on a pair that is genuinely in step, rather than warning on some field-name detail no host test can see. The stub it replaces reported "not available yet" through the 2026-08-26 Core-v13-against-bench-v14 incident, so **a green here is the first evidence this check works at all.**

- **Check 11 compares *this* `embarch` binary's compiled host schema version, not the located `embarch-api`'s.** `embarch-api` exposes its compiled `HOST_TYPE_SCHEMA_VERSION` nowhere — not on `--version`, not on `status --json` — so the number that binary actually holds cannot be read from outside it. The stand-in is exact whenever all three binaries came from one suite archive, which check 1's manifest is what establishes, and **it is wrong exactly in the case that matters most: a hand-built mixed install with no manifest.** Closing it needs a change in `embarch-api`, which is a different repo; dropped in `inbox/` as `api-expose-compiled-host-schema-version.md`.

- **Check 15 catches a *cross-version* stale deploy and not a same-version one.** `core_version` is `CARGO_PKG_VERSION`, so it moves only when the crate version moves: a rebuild-and-failed-deploy at the same version reads as a match. Strictly better than nothing — `deploy-core` has reported `landed` with nothing installed, and its own check compares byte length — but **it is not a hash comparison and should not be read as one.** A content hash served on `/status` would close it and is `embarch-core`'s to decide, not this sub-project's.

- **Several later decisions are recorded as designs with no implementation note, and whether each shipped is not established here.** Check 16 (bind address versus topology) is explicitly design-only. Also unconfirmed: `setup --dry-run` (21), the firewall and disk checks (22b, 22c), the MCP-handshake spawn (23), `doctor --prune` (26), and the release version assertion (27/29). Reading the code is the way to close this, not reading this repo.

- **Config fragments or includes**, so the Core section is not duplicated into every firmware repo's config (decision 10). Needs an include mechanism in `embarch-api`'s config loader. **Deferred rather than rejected.**

- **The token and config mirrors still have nothing mechanical keeping them in step with `embarch-api`'s originals** (decisions 16, 20). The CI diff job that was supposed to guard them **was never implemented**, and decision 15's reversal removed only the third mirror. Extract them into a shared crate, or build the diff job — the question is open for these two specifically.

- **A user-level service would avoid needing any elevation at all on Linux and macOS** (systemd `--user`, a launch agent), **but would not start before login, which defeats decision 3's whole point.** Not yet weighed properly. Self-elevation also does not help the no-GUI/no-TTY case — CI, a headless remote session — which still needs decision 7's original print-the-command fallback.

- **Mirrored-mode WSL2 networking has defined behaviour and no evidence.** Only NAT mode has ever run here, so **what got live-validated is NAT mode.** The ambiguity decision 30 resolves is real either way; what is untested is the mode that creates it.

- **macOS is entirely unvalidated and has no machine to validate on.** Deliberately not blocking: ship it and have a Mac-only engineer walk the guide once the primary topology is proven. **Gatekeeper may also make the "just download and run" promise false there specifically**, since the aarch64 build is unsigned.

- **MCP registration has never been verified for real.** Every walk of the onboarding guide ran from an environment with no agent CLI present, so check 10 could not be exercised. Needs one run from an environment that has it.

- **Whether `init` should warn when a repo holds more than one recorded build** is undecided. It surfaced on a real repo: `init` read whichever recorded build it found first, **which was an ad hoc dev board's rather than the production board the prior config targeted**, and `init` has no way to know which of several past builds is the "real" one. Resolved that day by hand-adding a second project entry rather than picking one — the zephyr-west discovery of decision 17 is the structural answer for a repo shaped that way, but **a static-discovery repo with several recorded builds still silently gets one picked for it.**
