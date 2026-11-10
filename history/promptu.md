# promptu: history

**Status:** active, 2026-11-09. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-11

### Added
- Promptu's pass accepts the chat's context usage (prep --context-usage) and names a way in Who does it for high-context work, footer way=; see contract §7.10.

### Changed
- Split promptu spec.md: build steps 2 and 3 moved verbatim to spec/build-steps.md, 9,563 to 6,949 B ([spec](../embarch-promptu/spec.md)).
- Promptu decision 39 retired: the chat's handoff card and chip are gone (embarch-chat 36, 97).
- Promptu decision 40 amended: the rail's icons are one-colour SVGs, not emoji, following chat 94 (EMB-56).
- promptu I2 on a header-less MEMORY.md now says the first `## <domain>` header may be added in the same write (decision 21).
