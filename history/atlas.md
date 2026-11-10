# atlas: history

**Status:** active, 2026-10-29. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-11

### Added
- `part_card` (board MPN, refs and nets) and `mismatch_report` (checks needing no build; the rest under Not run) answer from netlists, BOM and coverage before the first atlas; DESIGN.md.
- Live `reg_read` of a banked register on a paged part: a `bus` `bank_select` field, and `allow_bank_select` (CLI, MCP `reg_read_bank`) selects the bank, reads, restores the previous page; DESIGN.md.
- embarch-atlas gains `declare-interface`: it records an engineer-declared board-to-board mating (rule or pin map, note) in boards/system.json, and refuses refs and rules the atlas cannot read.
- embarch-atlas register records take an optional `bank`; check G, codecheck RegMap and `live` read `REG@bank` key on (bank, addr). A register with no bank behaves as before. See DESIGN.md.
- embarch-atlas record schema gains a `variant` kind: one record per orderable part, with `mpn` and `options`; it validates, renders in facts.txt and the datasheet procedure says when to write one.
- embarch-atlas init now writes a placeholder MAP.md saying no atlas is built yet and naming /atlas-translate-docs then /atlas-build; the first join replaces it.
- The atlas renderer reads `Note N: text` footnotes beside `24.` and `(1)`: listed under the table and in the Note column of citing rows.

### Changed
- The atlas-use skill now knows the no-atlas placeholder MAP: step 1 says no atlas is built, names /atlas-translate-docs then /atlas-build, and stops; a test keeps skill and placeholder aligned.
- atlas doc check fails a record or prose cite of a page outside 1..pages, naming the unit and the page (P:).
- atlas check K reads two side-by-side MIN/TYP/MAX groups per header and a lone TYP column; a table it cannot read stays a K warning, not a disagree (atlas 046).
- atlas join now has a synthetic Nordic-project test (P0.xx/P1.xx netlist, Nordic dt.json) asserting the pin map's DT column and a non-zero pin-check count.

### Fixed
- `embarch-atlas doc freeze` counts only pages inside the document, and warns on a unit citing a page outside 1..pages instead of counting it.
- A page-one `REV. A` / `DOC NO. 001` header now gives the manifest and doc.json their rev and number, and `doc check` says "K did not run" when no table has a MIN/TYP/MAX header (atlas 049).
- A part named only on page 2 or later of another part's datasheet is now proposed, not covered: part tokens and the `exact` rung read the title and page 1 (see DESIGN.md Covered, proposed, missing).
- Atlas inventory: an "Application Report" is an appnote, and a user's guide titled as a reference manual is typed reference-manual (DESIGN.md Kinds).
- Nets that meet through the same off-sheet port are one board net in `netlist.json` (aliases kept); an unpartnered port goes to issues (DESIGN.md).
- A page cite naming another document (`other-doc p.7`, a conflict row's Sources) is checked against that document's page by `doc check` M, not this one's.
- A `missing --kind` or `--confirm reference-manual` override now also rewrites the kind in an already-prepped document's doc.json (EMB-31).
- Check S no longer flags a `×`-joined dimension cell (`1.5 × 2.0`) as packed values; `1.0 2.0` is still flagged (EMB-37).
- Check U finds a unit on the cited page as a token, not a substring, and no longer reads a CamelCase symbol like LoadReg as an inductance.
- Check M no longer reads a parenthesised step marker `(1)`, `(2)` as a number to anchor; `(5 V)` still counts.
- Atlas reads `- 0.3` as -0.3 and `1,000` / `12 000` as one number in checks N, C, M and K; `355 505` stays two columns.
- codecheck keeps a hex-addressed *_OFFSET/*_OFS register define as a register; only a decimal or expression bit offset is encoding, so its address is still compared.
- second-look reads high-impedance, hi-z and high-Z as a floating strap, open-drain as no pin state, and drops a negated state, so wording no longer freezes a false conflict.
- A named build dir (config --build, dt_node) picks its sysbuild image by the atlas's app, as atlas build does; no more error on a tree without a domains.yaml default.
- Atlas: a proposed DT-limit mapping must match the property's quantity and role, else it is listed as mapping uncertain, not compared (EMB-53).
- `second-look compare` no longer calls agreeing strap readings a conflict over wording: strap conditions compare by pin state, and the reader states only the pin state.
- `codecheck` no longer reads `*_OFFSET` / `*_OFS` defines as register addresses, so masks stop being tied to a phantom register by position.
- codecheck reads only the driver sources the build compiled plus their quoted includes, and skips `*_UA`/`*_MV`/`*_MAX_*`/`*_STEP_*` constants as register addresses (atlas 030).
- Atlas build directory is keyed on the build arguments too, so changing a target's extra_args (sysbuild or not) no longer fails in CMake on a stale cache.
- atlas `join` decodes devicetree pin use on Nordic nRF (psels, nordic,nrf-gpio), folds nrfx-only nodes out of dt-no-driver, and says when a family has no decoder: [design](../embarch-atlas/design.md)
- atlas build pins a multi-image sysbuild atlas to the application image, picked by domains.yaml default, else the app directory name.
## 2026-10

### Added
- atlas: `missing --answer` records supplied / not-needed / generic-card answers in answers.toml; net_trace walks through answered parts, missing.md ranks open ones by walks stopped (DESIGN.md).
- `embarch-atlas live core-state` / `core_state`: DHCSR and ICSR by bit name, PC samples, PC and LR as functions and lines, named only when the flash matches the ELF; else refused.
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
- Live `shell` uses the signal `[live] consoles` maps from the image's chosen shell UART; unconfirmed, it skips a console that returns no byte. See embarch-atlas DESIGN.md "The live shell".
- atlas: `reg_read` reads the RCC enable bit with the peripheral and says "clock off" instead of decoding zeros as reset values, or says the clock is unknown (DESIGN.md Live).
- Atlas: a bump's second look batches facts whose checked fields changed, and compares cond, condition and width; see DESIGN.md Caching.
- atlas: the live shell tells a silent console, a lost port and an empty success (with its retval) apart, never resends after a write, and the CLI exits non-zero on failure (DESIGN.md Live).
- atlas live: shell runs only [live] read_only commands, new shell_run and reg_read_clear carry no readOnlyHint; reg_read refuses allow_clear (embarch-atlas DESIGN.md MCP server)
- Atlas queries: find_fact shows the best 10 hits above 0.4x the top, names unmatched terms, narrows to a part the query names; register joins MSB/LSB pairs; doc_toc under= takes a title word.

### Fixed
- atlas shell: only a Core that says echo_seen false lets a silent console fall through to the next; an older Core, silent, is the answer on every console. DESIGN.md states the echo-on assumption.
- atlas reg_read: the clock-gate word no longer tips a read past its limits into refusal (reads without it, says clock unknown); only RCC *ENR registers (not SMENR/LPENR) can name the gate.
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
