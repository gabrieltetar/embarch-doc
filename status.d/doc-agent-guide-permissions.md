**Target:** suite/agent-guide.md §1.1 — the permission lists (the paragraph from "That is the whole surface" through the `run_study` paragraph)
**Was:** "the 53 tools of 2026-10-29 still served"; ten reads and lease calls (`reset`, `reset_dev_bench`, `signal_exchange`, `mem_read`, `core_state`, `bench_exchange`, `validate`, `lease_take`, `lease_renew`, `lease_release`) under ask; no atlas tool named
**Now:** 58 tools registered in `embarch-api/src/tools.rs` on origin/main at 2026-11-23, each in exactly one list below; the ten move to allow per `notes/hil/05-live.md` ("Reach and permission"); the atlas's MCP server gets its own lists; `instrument_exchange` is gone (api/178).

**For the owner, placements the section's own rule ("reads and host-side builds that touch no hardware" allow; reaching a board or rewriting what EmbArch remembers asks) does not settle by itself:**

- `bundle` — allow. A host-side package of a finished build, no hardware; it writes a folder and a zip, so it is a build in the rule's sense. Move it to ask if writing outside the build tree should be a decision.
- `publish` — ask. No hardware, but it writes a signed deliverable to the configured publish folder, a record the person releases; kept a decision. Move it to allow if you read it as a host-side build.
- Rule-settled, listed for the check: `build_each` (host-side build) allow; `call_log` and `study_measurements` (reads) allow.
- The atlas's 23 non-live tools are all `readOnlyHint` in `mcp_server.py` and go under allow; its `core_state`, `shell`, `shell_run` and `live_stacks` are allow per 05 ("any shell command ... free"); `reg_read_clear` and `reg_read_bank` ask. The atlas's live tools exist only when Core answers at start.
- Do not write that the identity tools leave the MCP surface: the attested Core does not exist yet (05 says they stay on the surface, labelled as the agent's, on an unattested Core).

**Replacement text for §1.1** (the intro sentence keeps its lead; replace from "That is the whole surface" to the end of the `run_study` paragraph):

That is the whole surface, the 58 tools of 2026-11-23, split for `.claude/settings.local.json`. The server is registered as `embarch-api`, so each rule is `mcp__embarch-api__<tool>`:

- **allow** — reads, host-side builds that touch no hardware, resets, and the lease calls a Live session takes with a purpose (a prompt on each would make every session ask): `alerts`, `bench_exchange`, `build`, `build_dev_bench`, `build_each`, `bundle`, `call_log`, `capture_read`, `capture_start`, `capture_stop`, `core_state`, `dev_bench_hello`, `lease_release`, `lease_renew`, `lease_show`, `lease_take`, `ledger_pending`, `ledger_show`, `list_instruments`, `list_projects`, `list_serial_ports`, `list_signals`, `list_study_streams`, `list_targets`, `mem_read`, `reset`, `reset_dev_bench`, `serial_log`, `show_bootload_ports`, `signal_exchange`, `status`, `study_measurements`, `study_status`, `study_stream_data`, `study_stream_load`, `study_watch`, `validate`
- **ask** — flashing and bootloading, and what writes what EmbArch has recorded or answers for you: `answer_prompt`, `bootload`, `build_and_bootload`, `build_and_flash`, `build_and_flash_dev_bench`, `clear_bootload_ports`, `declare_bootload_ports`, `declare_instrument`, `declare_signal`, `dev_bench_link`, `enroll_probe`, `flash`, `flash_dev_bench`, `ledger_add`, `publish`, `remove_instrument`, `remove_signal`, `run_host_study`, `run_study`, `set_role_board`, `unenroll_probe`

The atlas's MCP server is registered as `embarch-atlas` (`mcp__embarch-atlas__<tool>`):

- **allow** — its static lookups (`applies`, `code`, `config`, `decode`, `doc_section`, `doc_toc`, `dt_node`, `find_fact`, `find_text`, `footprint`, `mismatch_report`, `net_find`, `net_trace`, `part_card`, `parts`, `pin_trace`, `rc_timing`, `register`, `schematic_text`, `shell_commands`, `stacks`, `states`, `transitions`) and, on a Live board, `core_state`, `live_stacks`, `reg_read`, `shell` and `shell_run`
- **ask** — `reg_read_bank` (writes a page select) and `reg_read_clear` (reads a register whose read clears a flag or pops a FIFO)

**`run_study` is the one to be deliberate about**: with `reflash` it builds and flashes from your working tree *as it currently stands*, on both boards. **Live reads and resets are free because a lease gates them and Core refuses them while a study or test runs**; `validate`, `mem_read` and `core_state` are reads. **`answer_prompt` relays *your* answer to a host study waiting on a person**, and a lab supply or load is driven only by a host study's `Instrument` step, run with `run_host_study`: both ask, so the person stays the one deciding. **A tool missing from both lists is newer than this page**: treat it as ask.

(Counts: allow 37 + ask 21 = 58 for `embarch-api`; the old paragraph's sentence "validate ... sits with the rest — as do mem_read and core_state" and "The capture tools read a console the way serial_log does" are replaced as above, the latter dropped as the capture tools now sit with the reads without needing a remark.)

**For `embarch-chat` (filed by the supervisor, not this unit):** `plugin/commands/embarch-permissions.md` carries its own copy, dated 2026-10-29, which must match: the ten tools move from ask to allow; `instrument_exchange` is removed from ask; add `build_each`, `bundle`, `call_log`, `study_measurements` to allow and `publish` to ask (today step 1 sends them to ask as "in neither list"); its closing sentence "`answer_prompt` and `instrument_exchange` ask" loses `instrument_exchange`; and it needs a second block for `mcp__embarch-atlas__*` with the lists above.
