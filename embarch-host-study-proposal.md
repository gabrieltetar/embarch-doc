# Proposal: host-run studies, operator prompts, bench instruments and a USB PD bench

**Status:** proposal, 2026-10-09.

Spans `embarch-topology`, `embarch-core`, `embarch-study-designer`, `embarch-api`, `embarch-ui` and `embarch-dev-bench`, which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3).

## Why

**A USB Power Delivery DUT is tested with three things the dev bench cannot be: a PD partner on the cable, an electronic load, and a person who plugs and unplugs cables.** The partner and the load are host-side serial devices (shell lines, SCPI lines); the person is a prompt. None of them needs a BLE counterpart.

**Studies today are bench-executed.** Core sends `StudyStart` and nothing mid-study; dev-bench runs every step ([embarch-study-designer](embarch-study-designer/decisions.md) decision 60). A prompt, an SCPI query or a shell exchange is host work, so it cannot be a bench step without a mid-study Core→dev-bench message, which the stream-pipeline proposal already withdrew once.

## What the owner chose (2026-10-09)

1. **A second study kind that Core executes itself: a host-run study.** It needs no dev bench and changes nothing on the dev-bench wire, so decision 60 stays true for bench studies. Mixing BLE steps with host steps is not in scope.
2. **The PD partner is a PD bench:** a NUCLEO-G0B1RE with an X-NUCLEO-SNK1M1, running a Zephyr USB-C sink with a shell. It is reached as a declared `Direct` signal on its ST-LINK virtual COM port, so **no third role is added** ([embarch-topology](embarch-topology/decisions.md) decision 35 and [embarch-core](embarch-core/decisions.md) decision 75 stand).
3. **Bench instruments are declared in topology**, first one an East Tester ET5410A+ electronic load speaking SCPI over a CH340 USB serial port.
4. **An operator prompt is a host step**: a dialog in the UI, answerable from the UI or from an MCP tool, with the answer and who gave it recorded in the result.
5. **The PD bench builds on Zephyr 4.4.2 plus the USB-C PD fixes that are not upstream yet**, the same stack as the DUT that prompted this. A bug common to both ends passes unseen, so key results still need a third-party partner.

## Shape

### Study model (`embarch-study-designer`)

- `HostStudy { name, steps: Vec<HostStep>, streams }`: streams are `Signal` taps only.
- `HostStep { name, action: HostAction, timeout_ms, continue_on_fail, delay_before_ms }`.
- `HostAction`:
  - `Exchange { signal, line, until, match_after_echo }`: write one line to a declared writable signal and read until the marker or the timeout ([embarch-core](embarch-core/decisions.md) decision 79 semantics, with the echo rule declared rather than defaulted).
  - `Prompt { text }`: block until an answer (`confirmed`, `cancelled`) or the timeout.
  - `Instrument { instrument, command, query }`: one SCPI command, or a query whose reply is recorded.
  - `Wait { ms }`.
- `HostStepResult { step_name, outcome, reply, answered_by }`. The reply is raw text, capped and marked truncated rather than cut silently. **JSON only, never on the dev-bench wire**: a host-type schema bump, no wire bump.
- **Numbers stay exact or absent:** v1 records SCPI replies as text. A declared numeric parse can come later.

### Core

- `POST /host-studies` takes the same `study_lock` as a bench study, validates, and runs the steps on one executor thread.
- `StepCompleted` is reused. Two new events: `PromptPending { step_index, text, deadline }` and `PromptResolved { answer, answered_by }`. `POST /study/{id}/prompt` answers. A pending prompt is also readable on `GET /study/{id}`, because SSE has no replay.
- **A signal that is both tapped and exchanged is opened once**, by its tap thread. The exchange writes through that thread and reads its reply from the same byte stream, since Windows allows one open per COM port.
- An instrument port is opened per command, paced by its declared minimum interval (200 ms for the ET54 family), and refused while a tap or another exchange holds it.

### Topology

- A new `instruments` table in `enrollment.toml`, copying the `bootload_ports` pattern: `Instrument { name, protocol: scpi, port: UsbPortId { vid, pid, serial?, interface? }, baud, write_terminator, read_terminator, min_interval_ms }`.
- **`UsbPortId` rather than a USB serial:** a CH340 reports none, and signals are identified by USB serial only.

### API and UI

- MCP tools, each with its CLI subcommand: `declare_instrument`, `list_instruments`, `remove_instrument`, `instrument_exchange` (one SCPI line, outside a study), `run_host_study`, `answer_prompt`. `study_watch` returns early on a pending prompt.
- UI, Live Study tab: a modal prompt on the existing dialog pattern, with Confirm and Cancel. Host-study rows in the designer come later.

### PD bench (`embarch-dev-bench`)

- A second app, `pd-bench/`. It does not speak the dev-bench wire; its console is a Zephyr shell.
- NUCLEO-G0B1RE with an X-NUCLEO-SNK1M1:
  - CC1 is PA8 and CC2 is PB15 (UCPD1).
  - VBUS is sensed on PB1 (ADC1_IN9) through 200 k / 40 k.
  - The TCPP01-M12 needs DB_OUT (PB6) and VCC_OUT (PC10) high.
  - These pins come from ST's X-CUBE-TCPP example for the NUCLEO-G071RB, which has the same Nucleo-64 pinout.
- Shell: `pd status` (contract, VBUS), `pd caps` (the partner's Source_Capabilities), `pd req <pos>` (a fixed PDO), `pd pps <pos> <mV> <mA>` (a PPS APDO), `pd max` (the default: the highest power).
- The SNK1M1's VBUS output feeds the load, so the PD bench plus the load is a scriptable PD/PPS sink.

## Phases

1. **PD bench firmware.** Usable at once through `signal_exchange`.
2. **Instruments:** the topology table, the Core route and the MCP tools. One-off SCPI is usable at once.
3. **Host-run studies with the prompt:** study-designer, core, api and ui.
4. **Fold:** decisions into each sub-project's docs; this file is deleted as it is absorbed.

## Open questions

- Who may answer a prompt, and its default timeout.
- Whether a host study may also drive the dev bench later (mixed studies). Out of scope here.
- A self-hosted workspace for `pd-bench/` once the USB-C fixes are upstream.
