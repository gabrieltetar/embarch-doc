# suite: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-09

### Added
- `embarch-outpost` gets host-only CI on push and PR; what it deliberately does not cover: [suite/decisions.md](../suite/decisions.md) 2.
- The fleet ran a study against the real bench and green 2/2; where the DUT half stops is [studies-guide.md](../suite/studies-guide.md) §3a.
- Every release workflow now fails before building when `Cargo.toml`'s version disagrees with the pushed tag ([decisions 27, 29](../embarch-umbrella/decisions.md)).
- `history/<scope>.md`, assembled per sub-project from `changelog.d/` fragments by `scripts/build_changelog.py`, capped at 20 KB with older windows rolled to `history/archive/`.

### Changed
- `suite/decisions.md` is an index and its three decisions live in `suite/decisions/` — the shape every sub-project already uses; nothing re-worded.
- `suite/decisions.md` compacted out of its reserve, 9,472 -> 9,035 B, with both decisions' reasoning, measurements and reversal conditions intact.
- `suite/user-guide.md` tightened by 317 B with no fact removed; its §7 split is blocked by `DOC-PROTOCOL.md`, not `DOC-BUDGET.md` (`tasks/doc/045`).
- One definition of the Study Designer's built-in actions; the picker renders what it is served ([decision 73](../embarch-study-designer/decisions/authoring.md)).
- Suite-wide decisions have a home, `suite/decisions.md`. `embarch.md` §5's rustfmt bullet moved into it verbatim, and §5 reads as five one-line principles again.
- The rustfmt reversal condition in [embarch.md](../embarch.md) §5 now says why neither `cargo fmt --check` nor `--all --check` is right on its own.
- Core's on-disk result layout moved from spec.md §5 to interfaces.md, beside the routes that serve it; study-designer's citation follows.
- suite/features.md is assembled from features.d/ row fragments, and a worker now writes its own inventory row.
- suite/features.md pared back to pointers: every row kept, the cells that restated an owning decision cut.

### Fixed
- Decision 7 no longer claims `cbindgen` prevents C-side drift or that C does not re-implement the wire format; both were false ([crate.md](../embarch-study-designer/decisions/crate.md)).
- - `suite/user-guide.md` §6 no longer denies the cwd-upward config search, and §7.1's permission split now names all 29 MCP tools rather than 7 of 23 with every hardware-touching one omitted.
- Power sampling no longer reads as built in the glossary, [embarch.md](../embarch.md) or the [studies guide](../suite/studies-guide.md); a step was never a power-sampling window after wire v9.
- Two reachable client-name leaks removed by history rewrite: embarch-api (reintroduced 2026-09-05) and embarch-study-designer (missed by the 2026-09-04 scrub). All ten repos verified clean.

### Removed
- The three fixed-channel study-data aliases are retired; `study_stream_data` is the read path, and only it reports truncation ([embarch-api decision 39](../embarch-api/decisions/studies.md)).
- 22 shipped milestone docs and implementation guides, 334 KB. Two open items they alone recorded moved to their design docs' open questions first; 122 dangling file references became milestone names.

### Decided
- `rx_utc_ms` keeps its name in both homes and each now says which clock it is — a trace's is Core's epoch, a study's is bench uptime ([suite decision 3](../suite/decisions.md)).
- rustfmt is not enforced and nobody runs cargo fmt: 81 files / 1,881 lines across six crates, and it decays without a check only protocol §10 can carry. embarch.md §5 has the reversal condition.
