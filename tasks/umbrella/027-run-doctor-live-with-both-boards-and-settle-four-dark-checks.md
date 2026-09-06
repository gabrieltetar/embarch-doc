# Run `embarch doctor` live with both boards attached, and settle the checks that have never run

**State:** open
**Source:** `embarch-umbrella/open.md` — "the rebuilt check has never run live" (check 10); plus the standing `/dev-bench/hello` `compatible` debt, which needs a bench plugged in
**Scope:** umbrella
**Hardware:** bench
**Owner:** no

## Roles this needs

`dut` and `dev-bench`. Validate both first; if either is unattached, leave this `open`.

## Bench facts — owner-supplied, do not infer

- Dev bench: **nRF54L15DK**, link **COM17 / VCOM1, interface 2** — the *higher* interface,
  not the lowest. Enrolled `link_port_interface=2`.
- `dut` = probe `000852006107`; `dev-bench` = probe `001057729826`. Both nRF54L15.
- The live Core is the **Windows service**, not the WSL debug build. A `doctor` run that
  reports on "a" Core must say which one it reached.
- **Read-only or near it.** This task does not flash and does not run a study.

## What

`embarch doctor` runs end to end with the bench attached, and **every check's real verdict is
recorded** — including the ones that have never executed against hardware. Four are named:

- **Check 5** (probe udev) — has a probe to see for the first time in a while.
- **Check 10** — rebuilt to read the agent CLI's config structurally, and per `open.md` it
  **has never run live**. Its residual is recorded there too: a server needing something only
  the CLI supplies fails here and works there. Say which case this run exercised.
- **Check 14** (flash-backend resolution) — its `Remote`/`WslHost` arms are prose today.
- **`/dev-bench/hello`'s `compatible` field** — the outstanding live debt; it needs a bench,
  and there is one.

A check that passes for the wrong reason is worse than one that fails, so record *what each
check actually observed*, not just its verdict.

## Why now

`doctor` is the suite's own self-diagnosis, and several of its checks have only ever been
reasoned about. The boards are attached now and this is read-only, so it is cheap.

## Done when

- [ ] A full `doctor` run is recorded with every check's verdict **and what it observed**.
- [ ] Checks 5, 10 and 14 each have a live result, and `open.md` says what is still unknown
      about each rather than being silently closed.
- [ ] `/dev-bench/hello`'s `compatible` field is answered, and the debt is discharged or
      restated with what is still missing.
- [ ] Which Core the run reached (Windows service vs WSL build) is stated explicitly.
- [ ] Any check that passed for a reason the run could not confirm is called out as such.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
