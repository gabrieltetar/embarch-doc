# embarch-chat interfaces: the wire probe

**Status:** active, 2026-11-17.

Reference for `tools/wire-probe.mjs` in the code repo. Current truth: [../spec.md](../spec.md).

## When to reach for it

A new `claude` release has shipped and one question about its wire is open: does a request still answer, what does `initialize` carry now, what comes back for a message sent at a given moment. Ask the live CLI that one question with the probe before raising `TESTED_RANGE` in `src/wire/version.ts`, instead of writing a throwaway script whose key filter can hide the field that matters. To record a whole session for a fixture use `test/record.mjs`; for a fixed pass/fail script use `test/live.smoke.mjs`. The probe is neither: `npm test` does not run it and nothing in the extension imports it.

## Use

Build the test bundle first (`node build.mjs --tests`): the probe takes the panel's own flags from `claudeArgs` in `test-out/core.js`, not a copied list.

```
node tools/wire-probe.mjs [--config-dir <dir>] [--bin <claude>] [--model <m>] [--cwd <dir>] [--wait <ms>] --send <json>[@<delay-ms>] ...
node tools/wire-probe.mjs --list <fixture.jsonl>
```

- `--config-dir` sets `CLAUDE_CONFIG_DIR` (the login); `--bin` the `claude` to run (default `claude`); `--model` the model; `--cwd` the folder (default a fresh temporary one); `--wait` how long to keep listening after the last write (default 5000 ms).
- It sends `initialize` first, as the panel does, then each `--send` in order. `<delay-ms>` is the wait before that write, after the previous one (default 0). The JSON is written as one line, as given.
- Every stdout line prints as `<ms since spawn> <line>`, whole and unfiltered, the `initialize` answer included. stderr passes through.
- `--list` prints a recorded fixture under `test/fixtures/wire/`, one row per entry: direction (`in`/`out`), type, and the subtype or request id.

## What is tested

`test/probe.test.mjs` covers argument parsing, the `--send` delay syntax and `--list` against `basic.jsonl`. The live path (spawn, send, print) is untested: it needs a real `claude`, and owes a run by the owner.
