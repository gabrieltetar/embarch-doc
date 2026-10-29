# EmbArch: driving it from Claude Code

**Status:** active, 2026-10-29. For a firmware engineer letting an AI coding agent drive EmbArch. Continues [user-guide.md](user-guide.md), which gets EmbArch working in the first place; this was its §7 until 2026-10-29.

## 1. Using it from Claude Code

`embarch init` already registered the MCP server for this repo, at local scope — **nothing was written into the repo for your teammates to trip over.** Open Claude Code in the repo and the tools are there.

**You do not call them by name.** You say what you want:

- *"Build this and flash it to the board."*
- *"Flash it, then show me the serial log for the first 5 seconds after reset."*
- *"This won't compile — build it and fix the errors."* ← **the one that pays for the whole setup**, because the agent sees the real compiler output and iterates without you relaying it.

### 1.1 Which operations should need your approval

**Reading and building are safe and frequent; anything that reaches a board — or rewrites what EmbArch remembers about one — should be a decision you make.** That is the whole surface, all 54 tools as of 2026-10-29, split for `.claude/settings.local.json`:

- **allow** — reads, and host-side builds that touch no hardware: `alerts`, `build`, `build_dev_bench`, `capture_read`, `capture_start`, `capture_stop`, `dev_bench_hello`, `lease_show`, `ledger_pending`, `ledger_show`, `list_instruments`, `list_projects`, `list_serial_ports`, `list_signals`, `list_study_streams`, `list_targets`, `serial_log`, `show_bootload_ports`, `status`, `study_status`, `study_stream_data`, `study_stream_load`, `study_watch`
- **ask** — reaches a board, or writes what EmbArch has recorded about one: `answer_prompt`, `bench_exchange`, `bootload`, `build_and_bootload`, `build_and_flash`, `build_and_flash_dev_bench`, `clear_bootload_ports`, `core_state`, `declare_bootload_ports`, `declare_instrument`, `declare_signal`, `dev_bench_link`, `enroll_probe`, `flash`, `flash_dev_bench`, `instrument_exchange`, `lease_release`, `lease_renew`, `lease_take`, `ledger_add`, `mem_read`, `remove_instrument`, `remove_signal`, `reset`, `reset_dev_bench`, `run_host_study`, `run_study`, `set_role_board`, `signal_exchange`, `unenroll_probe`, `validate`

**`run_study` is the one to be deliberate about**: with `reflash` it builds and flashes from your working tree *as it currently stands*, on both boards. `validate` only re-checks an enrolled board's identity, but it does attach to the probe, so it sits with the rest — as do `mem_read` and `core_state`. **`answer_prompt` relays *your* answer to a host study waiting on a person**, and `instrument_exchange` drives a lab supply or load: both ask, so the person stays the one deciding. The capture tools read a console the way `serial_log` does. **A tool missing from both lists is newer than this page**: treat it as ask.

If your `CLAUDE.md` tells the agent never to build firmware on its own — **a sensible rule when a stray `west build` can blow away a build tree** — note the exemption explicitly, or the agent will keep asking:

```markdown
Never build firmware or flash devices autonomously — ask me to run it.
  Exception: builds routed through EmbArch's `build` tool, which uses its own
  build directory and can't disturb my interactive build tree.
```
