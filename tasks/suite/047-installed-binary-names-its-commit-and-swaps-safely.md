# 047 — An installed suite binary names its commit, and can be replaced while an MCP server runs it

**State:** done — landed 2026-10-28 by the supervisor (embarch-api `525cda7`, embarch-core `2d3532d`, embarch-umbrella `97b1358`; decisions api 93, core 100, umbrella 57). Window closed 14:09:45 with no reply in the thread or the channel; run by the 13:45 leg as its last unit. Earlier: **announced and parked** by the 2026-10-28 leg at 13:39 (`ts` `1793216385.010889`, no `--action`); the 30-minute window closes **14:09**. That leg ended at its unit cap before the window closed, so the next leg polls `fleet-read.py --thread 1793216385.010889` and, with no objection from the owner, runs this as its **last** unit (`ops.md` §4). Repos: `embarch-api`, `embarch-core`, `embarch-umbrella`. Source re-checked at announcement: `embarch-api` still prints the crate's `0.1.0` (`#[command(name = "embarch-api", version)]`, `src/main.rs:38`) and `embarch-umbrella/src/install.rs:88` still installs with `std::fs::copy`.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — the MCP server ran an installed `embarch-api` built 2026-10-06 19:23 while api `main` moved on to `f82f8b6` (2026-10-09, role-less `enroll_probe`); sessions called `target/debug/embarch-api` directly 138 times (2026-10-06 to 10-19) to get the newer behaviour; replacing the installed binary failed with "Text file busy" (2026-10-06) and was done by hand with copy-and-rename; `embarch-api --version` prints `embarch-api 0.1.0` for every build
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

Nothing tells a user or an agent that the api an MCP server runs is older than its checkout. The version is the crate's `0.1.0` (`embarch-api/src/main.rs:35`), `versions` reports the crate, schema and JSON-shape versions only (`main.rs:568-577`), and the `status` tool reports Core's probes, not the client's build. The one install path writes over the destination in place (`embarch-umbrella/src/install.rs:91`, `std::fs::copy`), which Linux refuses while that file is executing, so an install with an MCP client open fails. Stamp every suite binary with its commit and a dirty flag at build time and print them in `--version`, `versions --json` and the MCP `status` tool. Install by writing a temporary file in the destination directory and renaming it over the old one. Have `embarch doctor` report an installed binary that is behind its checkout's `HEAD`, and say that running MCP clients keep the old binary until they reconnect.

## Why now

Sessions checked which build was installed by comparing md5 sums and file times by hand, and for two weeks the field sessions bypassed the MCP tools for the CLI of a debug build, which no permission rule or doc covers.

## Done when

- [x] `embarch-api`, `embarch-core` and `embarch` print commit and dirty flag in `--version`, and `versions --json` and the MCP `status` tool carry them.
- [x] Install replaces a binary that is executing (temporary file and rename), tested with a running copy on Linux; Windows behaviour is stated in the decision.
- [x] `embarch doctor` reports an installed binary older than its checkout's `HEAD` and the reconnect it needs.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) in each repo touched.
- [x] `spec.md`/`decisions.md`/`open.md` updated in each repo touched, `changelog.d/` fragment dropped.

## Result

Done by the supervisor as a cross-repo pass. Check 18 covers `embarch-api` and `embarch` itself, not
`embarch-core` (decision 57 says why). **Owed, not done here:** nothing installed or deployed; the owner's
installed `embarch-api` and the live Core still print `0.1.0`/`0.1.4` until rebuilt. `deploy-core`'s
`WSLENV` hand-off has never run against the real service, and Windows install behaviour is stated, not
tested. An umbrella built before this reads the new `--version` lines as a manifest mismatch.
