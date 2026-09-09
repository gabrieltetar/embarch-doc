# umbrella: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- Check 16's first live reading: study_results/ is 809 MiB across 50 entries — the sweep bounds count, not size, which is the argument for decision 26's deferred --prune half.
- `doctor` check 5 fails on a Linux probe that is attached but not permitted, instead of calling it unplugged: [decision 18](../embarch-umbrella/decisions/doctor.md).
- `doctor` check 16 reports `study_results/` size and per-project build directories; `--prune` stays deferred ([decision 26](../embarch-umbrella/decisions/projects.md)).
- `embarch setup --dry-run` runs every detection step and prints the whole plan — install, `PATH`, service call — changing nothing.

### Changed
- `embarch-umbrella` drops its own token mirror; depends on `embarch-core-client` for `resolve_token`.
- decision 43 split out of decisions/reporting.md into decisions/message-rendering.md (reserve).
- Check 14's per-class skip wording documented as one skip phrased three ways, not flashing verdicts.
- `embarch status` now authenticates to report the probe count spec.md promised; no-token/unauthorized/unreachable are distinct states, never a probe count of `0` (decision 46).
- `spec.md` and `open.md` compacted out of reserve; each duplicated clause now sits only in the decision or task that owns it.
- - `doctor`'s one-line message rule is now stated as a runtime property, with the live check-1 counter-example — [decision 43](../embarch-umbrella/decisions/reporting.md).
- A live doctor run after the Core redeploy closes check 11's core_version unknown (Core answers 0.1.4) and decision 38's wsl-host arm: check 14 answers here, nRF54L15=jlink.
- `init` writes an inferred board as CHANGE-ME with the value and build age in a comment, and names every candidate rather than picking one of several recorded builds: decision 41.
- `doctor` check 17 tells a Core that is down from one bound where you cannot reach it; decision 22's firewall and disk-space checks are retired unbuilt.
- `doctor` check 8 asks `embarch-api list-targets` instead of umbrella's own scanner, which is deleted: [decision 17](../embarch-umbrella/decisions/projects.md).
- Decision 37 cites spec.md's table for which checks carry `code` instead of listing them; check 10's MCP entries split into [decisions/mcp.md](../embarch-umbrella/decisions/mcp.md).
- `doctor` check 16 names the `study_results/` directory it resolved, in its detail line and in `--json`'s new `path` field; `tasks/umbrella/014`'s three stale decision lines rode along.
- `embarch doctor` check 10 now spawns the registered MCP command and completes an `initialize`; registered-but-broken reads Fail, not Pass.
- `doctor` check 11 reads the located `embarch-api`'s `versions`, not `embarch`'s own constant; unaskable is its own warn.
- umbrella spec.md, open.md and decisions/doctor.md off their caps; "is it built" now lives once, in spec.md's table.
- Seven `embarch-umbrella` decisions audited against the source: 18, 21, 22, 23, 26, 27/29 and 17's amendment are all unbuilt — [spec.md](../embarch-umbrella/spec.md) claimed four shipped.
- `doctor` check 11 compares real schema versions instead of a hardcoded warn, and new check 15 catches a cross-version stale Core deploy.
- embarch-umbrella compacted to spec/decisions/open, 116 KB to 54 KB; design.md and milestone-6.md deleted.

### Fixed
- `schema-skew.md`'s decision 52 citation points at `embarch-api/decisions/tool-wrapping.md`, not the split-away `surface.md`.
- `doctor` check 2's Fail now names the host input it inferred `remote`/`wsl-host`/`local` from, and is test-covered.
- doctor normalises another program's raw text at every interpolation point, not just check 1 (decision 43).
- doctor check 13: no checkout configured now fails with a fix; an unresolvable firmware id reports as that, not stale (decision 47).
- `status --json`'s `probes.state` gains `bad-response`: a 200 with no `probes` array no longer reads as `request-failed`.
- `doctor` gives `/dev-bench/hello`'s serial handshake its own 10 s budget, not `GET /status`'s 500 ms, and a call that fails says whether it timed out or never connected (decision 44).
- `doctor` check 14's `remote` skip loses eighteen stray spaces, and every check's text is now guarded against a wrapped literal ([spec.md](../embarch-umbrella/spec.md)).
- `doctor` check 1 finds `embarch-api` by the agent CLI's registration and `setup`'s install dir, not `PATH` alone (decision 42).
- check 17's `bound-narrow` fix line now names the class a bare `embarch setup` really infers, and withdraws the offer where that is `remote`.
- `doctor` check 17 withdraws `embarch setup` where it would reinstall the narrow bind, and no longer judges a `remote` Core by this host: [decision 22](../embarch-umbrella/decisions/bind.md).
- doctor's two spawn tests retry past ETXTBSY: another test thread's fork inherits the just-written fake's write fd, so Linux refuses the exec. Both flaked ~1 run in 20 (task umbrella/019).
- `doctor` check 17's `bind-too-narrow` now needs the service registration, not a loopback hit, and its fix no longer offers the `setup` that would green it.
- Decision 26 stops saying `target.json` is unwritten: it exists now, and absence means "unattributable", never "orphaned" ([decisions/projects.md](../embarch-umbrella/decisions/projects.md)).
- `doctor` check 10 reads the agent CLI's own config for the command to spawn: the `claude mcp get` format it parsed does not exist, so its handshake was unreachable code.
- `doctor` check 1 finds the Windows service's own Core on `wsl-host` instead of failing, so check 14 runs there: [decision 38](../embarch-umbrella/decisions/topology.md).
- First live `doctor` run on the real installed suite: check 16's data dir and check 11's api-versions read confirmed; checks 1, 10 and 16 filed as defects.
- Decisions 27 and 29 are one entry an insertion renumbered, not a deletion; same for api 31 and 33.

### Decided
- `doctor`'s two GET budgets are measured, not assumed: `/dev-bench/hello` takes 0.73 s against 10 s, `/dev-bench/port` 5–13 ms against 500 ms. Check 11 read `compatible: true` off a bench at last.
