# HIL notes: the three modes

**Status:** draft, 2026-11-15.

## What separates them

**Purpose separates the modes; the bench count follows from the purpose.**

| Mode | Purpose | Benches | Output | Example |
|---|---|---|---|---|
| **Study** | A custom question, answered by measurement; "almost scientific" | Exactly one | Measurements and a report | What data rate a DUT's BLE GATT data-acquisition API sustains |
| **Test** | Technical conformance with a verdict per test | One or more, one after another | A verdict per test, coverage, a report | Selected tests of the USB PD R3.2 suite |
| **Live** | Exploration during development | The DUT and its bench boards | An answer now, a live log, findings written back to the atlas | Read a peripheral's registers, run a shell command, reset and watch the log |

A Study may use either runner, the dev bench's (`run_study`) or Core's own (`run_host_study`), because the runner is an implementation detail. Logging a PD voltage profile with no pass criterion is a Study. A Test's tests are studies too, plus verdict rules ([03-test.md](03-test.md)).

## How an agent picks a mode

| The request | Mode |
|---|---|
| Names a specification or conformance: "does the PD contract work", "check R3.2" | **Test**: select the matching tests from the suite |
| A custom question whose answer is a measurement: "what rate does it sustain", "how long does wake-up take" | **Study** |
| Look or poke while developing: "what is in this register", "reset it and show me the log" | **Live** |
| A Live result that is about to be cited in a PR, a ticket or a report | Redo it as a **Study** or a **Test**, so it has a published receipt |

**A spec named is a Test, not a Study** — the owner's own example: "check the PD contract works" runs the Test. **A spec named with no tests runs the project's saved test plan for that suite, and says so**; with no plan, the agent lists the applicable tests grouped by bench and asks which to run.

**A request that fits no row gets one question**: Study, Test or Live, each in one line, the agent's pick first.

## Who may run them

**Interactive sessions only.** The fleet stays off hardware, as it does today ([CLAUDE.md](../../CLAUDE.md), "Parallel agent work"), and the procedure says so in its first lines.

## The lease

**Every mode holds the bench lease** ([embarch-api lease tools](../../embarch-api/interfaces/tools-lease.md)):

- **Live**: a short lease (900 s, renewed by the MCP server's timer), taken with a purpose and released when the exploration ends.
- **Test**: **the run holds its own lease in Core**, named after the run, because a Test run outlives the session that started it: **the go passes the session's lease to the run, and it returns to the session at the run's end or cancel** (review round 2, recommended) ([03-test.md](03-test.md#a-run), item 1).
- **Study**: **the same run-held lease as a Test, passed and returned the same way, once Core can hold one**, by the person's go where the study takes one, by its start otherwise ([02](02-study.md#how-a-study-runs-as-the-procedure-would-say-it)) (review round 3, recommended); until then, the session's lease, and Core still refuses every other hardware call while the study runs (review round 2, recommended) ([03](03-test.md#a-run), item 4).

## Open

- Nothing left open here as of 2026-11-15.
