# atlas: history

**Status:** active, 2026-10-29. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-10

### Added
- atlas: find_text searches a document's page text layer; each hit cites its page and section and says if it is distilled (DESIGN.md Query surface).
- Every atlas lookup's `src:` line now carries `stale=<reasons> (HEAD <sha>)` when the atlas is behind HEAD; the MAP's RM chapters follow `join`; `mcp` runs `status` at start.
- Atlas config and dt_node: a Kconfig symbol and why it has its value, a DT node with each property's source line; pinned build or a named build dir (read only).
- Atlas footprint and stacks: flash/RAM vs the DT flash, SRAM and code partition, top contributors or a diff between builds; thread stacks with their defining line.
- Atlas net_trace: any net, part pin or part on any board, its power feed walked upstream from datasheet pin `flow`, enables to their MCU port, datasheets still needed.
- Atlas: `update` bumps an atlas by its diff only; second-look verdicts keyed on the fields the look checks, so unrelated edits keep them.
- Atlas: live `live_stacks`: thread stack peaks on the board joined to stack symbol and option, after a flash-vs-ELF check.
- Atlas: live `reg_read` decodes an MCU register or peripheral read on the board; read-to-clear registers refused.
- Atlas: live `shell` and external `reg_read` over the board shell; new `bus` record (byte order, address windows).

### Changed
- Atlas: a bump's second look batches facts whose checked fields changed, and compares cond, condition and width; see DESIGN.md Caching.
- atlas: the live shell tells a silent console, a lost port and an empty success (with its retval) apart, never resends after a write, and the CLI exits non-zero on failure (DESIGN.md Live).
- atlas live: shell runs only [live] read_only commands, new shell_run and reg_read_clear carry no readOnlyHint; reg_read refuses allow_clear (embarch-atlas DESIGN.md MCP server)
- Atlas queries: find_fact shows the best 10 hits above 0.4x the top, names unmatched terms, narrows to a part the query names; register joins MSB/LSB pairs; doc_toc under= takes a title word.

### Fixed
- atlas: a declared board with no netlist is a stale reason, MAP line and join log; config quotes a failed Kconfig extraction and `kconfig-extract` recovers it without a rebuild (DESIGN.md).
- atlas: every lookup takes offset (function, q --offset, MCP), so a cut answer's next= can always be followed; a test walks TOOLS (DESIGN.md Query surface).
- Atlas lookups: part_card board="all", register by CMSIS member name, undistilled sections answer with the next call, and src lines carry the PDF path. See embarch-atlas DESIGN.md.
- Atlas `reg_read` on an external part: a missing I2C shell says "build CONFIG_I2C_SHELL=y", and a clear-on-read sentence naming another register guards that one, quoting the sentence.
- Atlas: a W1C field no longer guards its register against reg_read; an SVD reset is null where resetValue or resetMask leaves bits undefined, and vote and the decode skip them.
- Atlas: save_records writes a non-object record-file line back as it was; doc check reports it as V: by file and line.
- doc check validates the schema first: a record of the wrong shape gets a V: line and stays llm-unverified instead of crashing the run.
- atlas live reg_read refuses words from a chip that is not the atlas MCU; live_stacks says console and probe are different boards, not "another build" (DESIGN.md Live).
- Atlas: find_fact also searches distilled prose (kind=prose); procedures make take-backs and silent wrong reads quirks and must-notes rule records.
- Atlas: second-look verdicts carried under the checked-field key now count as current instead of being re-queued.

### Removed
- research/06-ui-concept.md folded into embarch-ui decisions 52-54 and deleted.
## 2026-09

### Added
- First atlas UI concept: an embarch-ui tab drawing a layered stack map; owner answers held, backend needs listed (research/06).
- Landscape survey toward resuming atlas: research/ intake, 5 notes; a Zephyr build computes ~85% of config+HW binding, the join does not exist anywhere.
