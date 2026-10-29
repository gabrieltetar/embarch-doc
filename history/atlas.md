# atlas: history

**Status:** active, 2026-10-29. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-10

### Added
- Atlas config and dt_node: a Kconfig symbol and why it has its value, a DT node with each property's source line; pinned build or a named build dir (read only).
- Atlas footprint and stacks: flash/RAM vs the DT flash, SRAM and code partition, top contributors or a diff between builds; thread stacks with their defining line.
- Atlas net_trace: any net, part pin or part on any board, its power feed walked upstream from datasheet pin `flow`, enables to their MCU port, datasheets still needed.
- Atlas: `update` bumps an atlas by its diff only; second-look verdicts keyed on the fields the look checks, so unrelated edits keep them.
- Atlas: live `live_stacks`: thread stack peaks on the board joined to stack symbol and option, after a flash-vs-ELF check.
- Atlas: live `reg_read` decodes an MCU register or peripheral read on the board; read-to-clear registers refused.
- Atlas: live `shell` and external `reg_read` over the board shell; new `bus` record (byte order, address windows).

### Changed
- Atlas queries: find_fact shows the best 10 hits above 0.4x the top, names unmatched terms, narrows to a part the query names; register joins MSB/LSB pairs; doc_toc under= takes a title word.

### Fixed
- Atlas: find_fact also searches distilled prose (kind=prose); procedures make take-backs and silent wrong reads quirks and must-notes rule records.
- Atlas: second-look verdicts carried under the checked-field key now count as current instead of being re-queued.

### Removed
- research/06-ui-concept.md folded into embarch-ui decisions 52-54 and deleted.
## 2026-09

### Added
- First atlas UI concept: an embarch-ui tab drawing a layered stack map; owner answers held, backend needs listed (research/06).
- Landscape survey toward resuming atlas: research/ intake, 5 notes; a Zephyr build computes ~85% of config+HW binding, the join does not exist anywhere.
