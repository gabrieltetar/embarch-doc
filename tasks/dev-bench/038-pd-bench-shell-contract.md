# 038 — Make pd-bench's shell replies a contract a host step can check without a person reading them

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — every scripted session stripped escape codes with `sed`, slept two to three seconds after `pd req` and polled `pd status` for the outcome, and an exchange waiting for `pd: ` (the README's own advice) came back as `pd caps\r\npd: o` with the verdict word cut off (2026-10-09, again 2026-10-14)
**Scope:** dev-bench
**Hardware:** bench
**Owner:** no

## What

pd-bench's replies are line-structured human text. A person or an agent with `sed` reads them well, but a host-run study step cannot check one: Core's `signal_exchange` (`embarch-core` decision 79) has only a substring `until`, and the host-study model records the reply as raw text. Two tasks filed alongside this one cover the host side. The core exchange task reads through to the end of the line that holds `until`, and the study-designer host-study-model task decides whether `Exchange` may declare a refusal marker. This task covers pd-bench's side, which those two do not.

1. **The README's wait marker cuts the verdict.** Core stops reading at the first match of `until`. With `until: "pd: "`, the reply ends at `pd: o` or earlier, so `ok` and `error <reason>` cannot be told apart. What works, and what later sessions used, is the prompt the shell prints after a command returns (`until: "uart:~$ "`); the last `pd: ` line before it is then whole. The README must say that. This holds whether or not Core's own fix lands.
2. **Some refusals print no verdict.** Zephyr's shell checks argument counts before the handler runs. `pd req` with no position prints `req: wrong parameter count` and no `pd: ` line. Every `pd` subcommand should accept any arity and refuse by itself with `pd: error usage ...`, so that every `pd` command ends in a verdict.
3. **`pd: ok` means "queued", and a host step has no loop.** The outcome of `pd req`, `pd pps`, `pd drswap`, `pd prswap`, `pd hardreset` and `pd srccaps` (accepted, rejected, wait, not supported, no response) arrives later and is read with `pd status`. There are two ways to make it reachable in one step: the command waits for its outcome up to a bound, as `pd ask` already does for one second, or a `pd wait <what> <ms>` command blocks until it. Pick one, and record it as a decision.
4. **The grammar is close, but not stated.** Most lines are `key: value`, with numbers in fixed units. Four lines (`data:`, `power:`, `requests:`, `tcpp03:`) join several keys with commas. Stack log lines (`CONFIG_USBC_STACK_LOG_LEVEL_INF`, sent through the shell log backend) and VT100 colour codes land inside replies. Make it one key per line, keep logs out of replies unless the host turns them on, and write the grammar into the README as the contract: names are stable, adding a key is compatible, renaming one is a breaking change.

Also add **`pd info`**: the shield, the firmware revision, the Zephyr version and the patch set. The two builds share one Nucleo and one probe serial, so flashing the wrong one is a silent mistake today. A DRP1M1 image on an SNK1M1 board fails its TCPP03 assert at boot, and its console goes silent, which looks exactly like a board held in reset.

## Why now

Host-run studies (`embarch-host-study-proposal.md`, phase 3) are not built yet. This is the cheapest moment to fix pd-bench's side of their contract: no study depends on the current output yet, and the next consumer would otherwise learn the `pd: o` trap from a failed run.

## Done when

- [ ] Every `pd` subcommand ends its output with exactly one `pd: ok` or `pd: error <reason>` line, a wrong arity included. Checked on the bench for each subcommand with too few arguments and with too many.
- [ ] The outcome of a Request, a PPS Request, a DR_Swap and a PR_Swap is readable in one exchange, by the mechanism chosen in item 3, with a bound of at most 5 s. A Reject, a Wait and a timeout each produce a distinct `pd: error <reason>` line. The choice is a new decision in `decisions/pd-bench.md`.
- [ ] `pd status` prints one `key: value` per line. No reply to a `pd` command contains a log line unless the host turned logging on, through a `pd log <on|off>` command or `CONFIG_LOG_CMDS`; the worker picks one and says which.
- [ ] `pd info` prints `shield:`, `revision:`, `zephyr:` and `patches:`. The boot log line `PD bench ready` names the shield too.
- [ ] `pd-bench/README.md`'s Shell section is the contract:
  - wait for the prompt (`until: "uart:~$ "`), never for `pd: `;
  - the verdict is the last `pd: ` line;
  - the key list for each command;
  - colour codes may appear, and ASCII only (non-ASCII renders as `?` through the exchange path).
- [ ] Bench facts for whoever runs this:
  - **Board and shield:** NUCLEO-G0B1RE with the X-NUCLEO-SNK1M1. JP3 and JP4 off; fitted, JP4 holds the MCU in reset and the shell is silent. J1 and J2 in position 1-2.
  - **Console:** USART2 through the ST-LINK VCOM at 115200, declared as a `Direct` bidirectional signal. Today it borrows origin role `dev-bench`; the suite task on bench-board signals fixes that.
  - **Flashing:** enrolled as a bench board with no role, so it is flashed through a project that names its probe serial. `list_targets` shows that serial.
  - **Partner:** a contract needs a USB PD source with fixed PDOs, and PPS for `pd pps`, on the shield's USB-C. Without a partner, only the no-partner paths can be checked.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
