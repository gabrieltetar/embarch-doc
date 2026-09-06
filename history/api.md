# api: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB — older windows roll into [archive/](archive/).

## 2026-09

### Removed
- `soc_chip_overrides` is retired unbuilt and refused at load on both kinds — an unmapped SoC stops at Core's registry-validated table ([decision 13](../embarch-api/decisions/zephyr.md)).
## 2026-09

### Changed
- A static project is refused all five zephyr-west-only config fields at load, not just default_target; the `none`-snippet collision names a remedy that works.
## 2026-09

### Fixed
- The `-args<hash>` build-dir segment is a crate-owned FNV-1a, so a Rust upgrade no longer renames and orphans build directories ([decision 19](../embarch-api/decisions/build.md)).
## 2026-09

### Changed
- `spec.md` is 12% smaller and out of reserve: selection semantics point at `interfaces/config.md`, and decision 30 moved to `decisions/shape.md` where the test tiers live.
## 2026-09

### Fixed
- A `zephyr-west` config declaring the retired `[[projects.targets]]` is now told to delete the rows, not to store the three fields decision 12 removed.
## 2026-09

### Added
- Every `zephyr-west` build directory now gets a `target.json` recording the resolved selection ([decisions](../embarch-api/decisions/build.md) 19).
## 2026-09

### Changed
- `decisions/zephyr.md` split by mission: `decisions/build.md` takes 5, 18, 19, 42; discovery and selection stay.
## 2026-09

### Added
- An oversized study is now refused naming every field over a bound and the bound itself, not `serde`'s raw error — [decision 27](../embarch-api/decisions/studies.md).
## 2026-09

### Removed
- `[[projects.targets]]` retired — refused at config load; `list_targets` now reports a `static` project's one real target, itself ([decision 53](../embarch-api/decisions/shape.md)).
## 2026-09

### Added
- Decisions 20/21 built, not retired: `[projects.default_target]` pins a zephyr-west base selection, and `snippets = ["none"]` forces zero over a default.
## 2026-09

### Changed
- Sixteen claims that lived in two api docs each now live in one, with a pointer where each moved from; the reflash invariant stays in both, on purpose (decision 40).
## 2026-09

### Changed
- A truncated build log now keeps its first 16 KB as well as its last 48 KB, so an early error is not scrolled off; total still capped at 64 KB (decision 18).
## 2026-09

### Changed
- Four api docs off their caps: study tools split to interfaces/studies.md, three decision groups cut to their hot half.
## 2026-09

### Changed
- `embarch-api`'s spec and open questions had run out of headroom; the module map moved to `interfaces/modules.md` and the cold narrative is gone.
## 2026-09

### Added
- `embarch-api versions` prints the compiled study-designer host schema version, with no config and no Core: embarch-api/decisions/surface.md 52.
## 2026-09

### Fixed
- A static project now refuses board/variant/revision/app/snippets/extra_args, naming them, instead of discarding them and reporting success. See embarch-api decision 51.
## 2026-09

### Fixed
- A CLI startup failure (unreadable config, unresolvable token) now emits a `--json` object on stdout, not a Rust error on stderr. See embarch-api/interfaces/tools.md.

### Decided
- `schema_version` is on every `--json` and MCP object, stamped by one serializer; `error_kind` retired unbuilt — Core serves no error codes. See embarch-api/decisions/surface.md 16, 24, 50.
## 2026-09

### Added
- study-status --follow and the study_watch tool consume Core's SSE study events; lagged is reported, a drop falls back to polling.
## 2026-09

### Added
- The six recorded acceptance criteria now have tests: `embarch-api/tests/`, a loopback mock Core, no new dependency. See embarch-api decision 46.

### Fixed
- spec.md claimed the build-log cap keeps head and tail; it has only ever kept the 64 KB tail. Doc corrected, gap logged in open.md.
## 2026-09

### Changed
- `embarch-api`'s 158 KB `design.md` became spec.md, open.md, two `interfaces/` files and six `decisions/<mission>.md` — 71 KB, all 45 decision numbers intact.

### Fixed
- `embarch-api` decisions 31 and 33 were byte-identical — the duplicate created in the very commit that deleted 31, which is why the deletion went unnoticed. One entry now owns both numbers.
