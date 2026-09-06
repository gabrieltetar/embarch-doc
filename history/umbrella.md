# umbrella: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB — older windows roll into [archive/](archive/).

## 2026-09

### Changed
- `init` writes an inferred board as CHANGE-ME with the value and build age in a comment, and names every candidate rather than picking one of several recorded builds: decision 41.
## 2026-09

### Fixed
- check 17's `bound-narrow` fix line now names the class a bare `embarch setup` really infers, and withdraws the offer where that is `remote`.
## 2026-09

### Fixed
- `doctor` check 17 withdraws `embarch setup` where it would reinstall the narrow bind, and no longer judges a `remote` Core by this host: [decision 22](../embarch-umbrella/decisions/bind.md).
## 2026-09

### Fixed
- doctor's two spawn tests retry past ETXTBSY: another test thread's fork inherits the just-written fake's write fd, so Linux refuses the exec. Both flaked ~1 run in 20 (task umbrella/019).
## 2026-09

### Fixed
- `doctor` check 17's `bind-too-narrow` now needs the service registration, not a loopback hit, and its fix no longer offers the `setup` that would green it.
## 2026-09

### Changed
- `doctor` check 17 tells a Core that is down from one bound where you cannot reach it; decision 22's firewall and disk-space checks are retired unbuilt.
## 2026-09

### Changed
- `doctor` check 8 asks `embarch-api list-targets` instead of umbrella's own scanner, which is deleted: [decision 17](../embarch-umbrella/decisions/projects.md).
## 2026-09

### Changed
- Decision 37 cites spec.md's table for which checks carry `code` instead of listing them; check 10's MCP entries split into [decisions/mcp.md](../embarch-umbrella/decisions/mcp.md).
## 2026-09

### Fixed
- Decision 26 stops saying `target.json` is unwritten: it exists now, and absence means "unattributable", never "orphaned" ([decisions/projects.md](../embarch-umbrella/decisions/projects.md)).
## 2026-09

### Fixed
- `doctor` check 10 reads the agent CLI's own config for the command to spawn: the `claude mcp get` format it parsed does not exist, so its handshake was unreachable code.
## 2026-09

### Changed
- `doctor` check 16 names the `study_results/` directory it resolved, in its detail line and in `--json`'s new `path` field; `tasks/umbrella/014`'s three stale decision lines rode along.
## 2026-09

### Fixed
- `doctor` check 1 finds the Windows service's own Core on `wsl-host` instead of failing, so check 14 runs there: [decision 38](../embarch-umbrella/decisions/topology.md).
## 2026-09

### Added
- `doctor` check 5 fails on a Linux probe that is attached but not permitted, instead of calling it unplugged: [decision 18](../embarch-umbrella/decisions/doctor.md).

### Fixed
- First live `doctor` run on the real installed suite: check 16's data dir and check 11's api-versions read confirmed; checks 1, 10 and 16 filed as defects.
## 2026-09

### Added
- `doctor` check 16 reports `study_results/` size and per-project build directories; `--prune` stays deferred ([decision 26](../embarch-umbrella/decisions/projects.md)).
## 2026-09

### Changed
- `embarch doctor` check 10 now spawns the registered MCP command and completes an `initialize`; registered-but-broken reads Fail, not Pass.
## 2026-09

### Added
- `embarch setup --dry-run` runs every detection step and prints the whole plan — install, `PATH`, service call — changing nothing.
## 2026-09

### Changed
- `doctor` check 11 reads the located `embarch-api`'s `versions`, not `embarch`'s own constant; unaskable is its own warn.
## 2026-09

### Changed
- umbrella spec.md, open.md and decisions/doctor.md off their caps; "is it built" now lives once, in spec.md's table.
## 2026-09

### Changed
- Seven `embarch-umbrella` decisions audited against the source: 18, 21, 22, 23, 26, 27/29 and 17's amendment are all unbuilt — [spec.md](../embarch-umbrella/spec.md) claimed four shipped.
## 2026-09

### Changed
- `doctor` check 11 compares real schema versions instead of a hardcoded warn, and new check 15 catches a cross-version stale Core deploy.
## 2026-09

### Changed
- embarch-umbrella compacted to spec/decisions/open, 116 KB to 54 KB; design.md and milestone-6.md deleted.

### Fixed
- Decisions 27 and 29 are one entry an insertion renumbered, not a deletion; same for api 31 and 33.
