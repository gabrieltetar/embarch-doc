# api: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- `dev_bench_hello` MCP tool exposes `GET /dev-bench/hello`'s identity cross-check (`link_identity`) — see decisions/tool-wrapping.md 59.
- Every `zephyr-west` build directory now gets a `target.json` recording the resolved selection ([decisions](../embarch-api/decisions/build.md) 19).
- An oversized study is now refused naming every field over a bound and the bound itself, not `serde`'s raw error — [decision 27](../embarch-api/decisions/studies.md).
- Decisions 20/21 built, not retired: `[projects.default_target]` pins a zephyr-west base selection, and `snippets = ["none"]` forces zero over a default.
- `embarch-api versions` prints the compiled study-designer host schema version, with no config and no Core: embarch-api/decisions/surface.md 52.
- study-status --follow and the study_watch tool consume Core's SSE study events; lagged is reported, a drop falls back to polling.
- The six recorded acceptance criteria now have tests: `embarch-api/tests/`, a loopback mock Core, no new dependency. See embarch-api decision 46.

### Changed
- `validate`'s response (client, MCP tool, CLI) now also surfaces `validated_at_utc_ms`, distinct from `confirmed_at_utc_ms`.
- `embarch-api`'s [spec.md](../embarch-api/spec.md) and [open.md](../embarch-api/open.md) are back out of doc-size reserve; closed test gaps and config detail already in `interfaces/config.md` went.
- `crates/embarch-core-client` is a workspace member, so the root gate lints and runs its own 28 tests: [decision 56](../embarch-api/decisions/tests.md).
- The bearer token is applied by one funnel in `embarch-core-client`, not at 9 hand-written sites: [decision 55](../embarch-api/decisions/core-link.md).
- embarch-api's test-reach decisions 30, 46 and 54 move verbatim out of `decisions/shape.md` (12,281/12,288 B) into a new `decisions/tests.md`; nothing reworded.
- The bearer sweep's route set is derived from the client's source, so a new networked method fails a test instead of escaping it.
- A static project is refused all five zephyr-west-only config fields at load, not just default_target; the `none`-snippet collision names a remedy that works.
- `spec.md` is 12% smaller and out of reserve: selection semantics point at `interfaces/config.md`, and decision 30 moved to the group holding the test tiers — `decisions/shape.md` then, `decisions/tests.md` since ([decisions.md](../embarch-api/decisions.md) routes a number to its file).
- `decisions/zephyr.md` split by mission: `decisions/build.md` takes 5, 18, 19, 42; discovery and selection stay.
- Sixteen claims that lived in two api docs each now live in one, with a pointer where each moved from; the reflash invariant stays in both, on purpose (decision 40).
- A truncated build log now keeps its first 16 KB as well as its last 48 KB, so an early error is not scrolled off; total still capped at 64 KB (decision 18).
- Four api docs off their caps: study tools split to interfaces/studies.md, three decision groups cut to their hot half.
- `embarch-api`'s spec and open questions had run out of headroom; the module map moved to `interfaces/modules.md` and the cold narrative is gone.
- `embarch-api`'s 158 KB `design.md` became spec.md, open.md, two `interfaces/` files and six `decisions/<mission>.md` — 71 KB, all 45 decision numbers intact.

### Fixed
- `EnrolledBoardResponse` no longer drops `link_port_interface`; it and `AlertResponse` are now pinned against a JSON literal each.
- Six MCP tool descriptions citing the retired `design.md` now cite `<repo> decision N`, verified; `enroll_probe`'s wrong decision number fixed.
- open.md stops reading as unaddressed: `init`'s no-inference refusal shipped (`embarch-umbrella` 41) and check 11 reads `versions` now (33/36, 42).
- A static project setting `west_binary`/`build_dir_root` is no longer told to remove and re-add the same field.
- The `-args<hash>` build-dir segment is a crate-owned FNV-1a, so a Rust upgrade no longer renames and orphans build directories ([decision 19](../embarch-api/decisions/build.md)).
- A `zephyr-west` config declaring the retired `[[projects.targets]]` is now told to delete the rows, not to store the three fields decision 12 removed.
- A static project now refuses board/variant/revision/app/snippets/extra_args, naming them, instead of discarding them and reporting success. See embarch-api decision 51.
- A CLI startup failure (unreadable config, unresolvable token) now emits a `--json` object on stdout, not a Rust error on stderr. See embarch-api/interfaces/tools.md.
- spec.md claimed the build-log cap keeps head and tail; it has only ever kept the 64 KB tail. Doc corrected, gap logged in open.md.
- `embarch-api` decisions 31 and 33 were byte-identical — the duplicate created in the very commit that deleted 31, which is why the deletion went unnoticed. One entry now owns both numbers.

### Removed
- `soc_chip_overrides` is retired unbuilt and refused at load on both kinds — an unmapped SoC stops at Core's registry-validated table ([decision 13](../embarch-api/decisions/zephyr.md)).
- `[[projects.targets]]` retired — refused at config load; `list_targets` now reports a `static` project's one real target, itself ([decision 53](../embarch-api/decisions/shape.md)).

### Decided
- `validated_at_utc_ms` is `Option<u64>`; an older Core parses, matching 13 other fields (decision 58).
- `schema_version` is on every `--json` and MCP object, stamped by one serializer; `error_kind` retired unbuilt — Core serves no error codes. See embarch-api/decisions/surface.md 16, 24, 50.
