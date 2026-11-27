# EmbArch: driving it from Claude Code

**Status:** active, 2026-11-23. For a firmware engineer letting an LLM coding agent drive EmbArch. Continues [user-guide.md](user-guide.md), which gets EmbArch working in the first place; this was its §7 until 2026-10-29.

## 1. Using it from Claude Code

`embarch init` already registered the MCP server for this repo, at local scope — **nothing was written into the repo for your teammates to trip over.** Open Claude Code in the repo and the tools are there.

**You do not call them by name.** You say what you want:

- *"Build this and flash it to the board."*
- *"Flash it, then show me the serial log for the first 5 seconds after reset."*
- *"This won't compile — build it and fix the errors."* ← **the one that pays for the whole setup**, because the agent sees the real compiler output and iterates without you relaying it.

**For hardware work, read the HIL guide first.** `embarch-api guide hil` prints what every mode shares (what you are trusted with and never do, choosing Live, Study or Test, what comes before any hardware), and `embarch-api guide hil study` prints the Study walkthrough, from writing a study to publishing it. The same text is [hil-guide.md](hil-guide.md). Live and Test are not written yet.

### 1.1 Which operations should need your approval

**Reading and building are safe and frequent, and so are a Live session's reads and resets under the bench lease; flashing a board, or rewriting what EmbArch remembers about one, should be a decision you make.** That is the whole surface, the 65 tools of 2026-11-26, split for `.claude/settings.local.json`. The server is registered as `embarch-api`, so each rule is `mcp__embarch-api__<tool>`:

- **allow** — reads, host-side builds that touch no hardware, resets, the lease calls a Live session takes with a purpose (a prompt on each would make every session ask), the Test tools that read, plan, propose or prepare, stopping a study, and an export of a finished one: `alerts`, `bench_exchange`, `build`, `build_dev_bench`, `build_each`, `bundle`, `call_log`, `cancel_study`, `capture_read`, `capture_start`, `capture_stop`, `core_state`, `dev_bench_hello`, `export_audio`, `lease_release`, `lease_renew`, `lease_show`, `lease_take`, `list_instruments`, `list_projects`, `list_serial_ports`, `list_signals`, `list_study_streams`, `list_targets`, `mem_read`, `reset`, `reset_dev_bench`, `resume_test`, `run_test`, `serial_log`, `show_bootload_ports`, `signal_exchange`, `status`, `study_measurements`, `study_status`, `study_stream_data`, `study_stream_load`, `study_watch`, `test_pending`, `test_plan`, `test_propose`, `test_show`, `test_status`, `validate`
- **ask** — flashing and bootloading, and what writes what EmbArch has recorded or answers for you: `answer_prompt`, `bootload`, `build_and_bootload`, `build_and_flash`, `build_and_flash_dev_bench`, `clear_bootload_ports`, `declare_bootload_ports`, `declare_instrument`, `declare_signal`, `dev_bench_link`, `enroll_probe`, `flash`, `flash_dev_bench`, `publish`, `remove_instrument`, `remove_signal`, `run_host_study`, `run_study`, `set_role_board`, `test_add`, `unenroll_probe`

The atlas's MCP server is registered as `embarch-atlas` (`mcp__embarch-atlas__<tool>`):

- **allow** — its static lookups (`applies`, `code`, `config`, `decode`, `doc_section`, `doc_toc`, `dt_node`, `find_fact`, `find_text`, `footprint`, `mismatch_report`, `net_find`, `net_trace`, `part_card`, `parts`, `pin_trace`, `rc_timing`, `register`, `schematic_text`, `shell_commands`, `stacks`, `states`, `transitions`) and, on a Live board, `core_state`, `live_stacks`, `reg_read`, `shell` and `shell_run`
- **ask** — `reg_read_bank` (writes a page select) and `reg_read_clear` (reads a register whose read clears a flag or pops a FIFO)

**`run_study` is the one to be deliberate about**: with `reflash` it builds and flashes from your working tree *as it currently stands*, on both boards. **Live reads and resets are free because a lease gates them and Core refuses them while a study or test runs**; `validate`, `mem_read` and `core_state` are reads. **`answer_prompt` relays *your* answer to a host study waiting on a person**, and a lab supply or load is driven only by a host study's `Instrument` step, run with `run_host_study`: both ask, so the person stays the one deciding. `bundle` writes only a folder and a zip from a finished build; `publish` writes a signed deliverable, so it asks. **`run_test` and `resume_test` prepare a Test run and never start one** (`resume_test` from an interrupted run's pending tests): the go is the engineer's, on Core's card, so both are free; `test_add` relays a manual verdict for the record, so it asks, though it never counts toward a requirement. `cancel_study` is free because stopping is the safe direction and a prompt would only delay it. The person's own terminal commands (`embarch-api person ...` and `--as-person`, api decisions 141 and 143) are not MCP tools and are not on this page. **A tool missing from both lists is newer than this page**: treat it as ask.

If your `CLAUDE.md` tells the agent never to build firmware on its own — **a sensible rule when a stray `west build` can blow away a build tree** — note the exemption explicitly, or the agent will keep asking:

```markdown
Never build firmware or flash devices autonomously — ask me to run it.
  Exception: builds routed through EmbArch's `build` tool, which uses its own
  build directory and can't disturb my interactive build tree.
```
