# 168 — Core keeps the host awake through a Test run

**State:** done — decision 152: guard-held SetThreadExecutionState behind a trait; Windows half unbuilt, two debts recorded
**Source:** EMB-371 — a Test run can be cut short by the host going to sleep
**Issue:** EMB-371
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

A Test run can last longer than a laptop's idle timeout, and nothing in Core
keeps the host awake. The design: "Core keeps the host awake while a run holds
the lease (the need on Windows is inferred, not measured)"
(`embarch-doc/notes/hil/03-test.md`, "A run", item 9). When this is done:

- **On Windows**, Core asks the OS to keep the system awake at the go and
  releases it at the run's end, its cancel, or an error that ends it.
- **Behind a small trait**, so the hold and the release are tested without the
  OS.
- **Elsewhere**, a no-op that says so in the log once per run.
- A hold is never left behind: a run that ends by any path releases it.

**Not measured**: whether the request keeps a Windows service's host awake
through an idle timeout. The owner may strike this unit to defer it to the
attested phase.

## Where to look

- `src/test_executor.rs` — the go and the run's end; `src/api.rs` — the go route
- `src/service.rs`, `src/main.rs` — the Windows service
- `embarch-doc/embarch-core/decisions/test-run-executor.md` (136, 137) and
  `test-run-go.md` (135)

## Where the doc goes

A new core decision, in a new topic file or `test-run-executor.md`.
`check-doc-size.py --pressure` lists `signing#110`, `analog-capture#127`,
`host-study#95`, `definitions#133`, `lease#93`, `stopping-a-study#128` (over),
`test-run-go#135` (95 B left), `run-log#111` and `instruments#104` near or over
their limits: do not grow any of them; point at them from the new decision.

## Hardware verification

The native Windows build is the owner's debt (`gate.md`): write the Windows half
under `cfg(windows)` and record it. Leave a hardware-verification debt for the
first Test run on the bench host: the host stays awake through an idle timeout
while a run holds the lease, and sleeps normally after it ends.

## Done when

- [x] A unit test sees one hold at the go and one release at the end, at a
      cancel and at an error.
- [x] The Linux build logs the no-op; the Windows half is behind `cfg(windows)`.
- [x] Both debts are recorded here.
- [x] Gate green (`cargo build`, `test`, `clippy --all-targets -- -D warnings`).

## Debts

- **Hardware-verification debt**: on the first Test run on the bench host, check that the host stays awake through an idle timeout while the run holds the lease, and sleeps normally after it ends (decision 152). The need and the effect on a Windows service are inferred, not measured.
- **Native Windows build debt (the owner's)**: `src/keep_awake.rs`'s `cfg(windows)` half and the `Win32_System_Power` feature on `windows-sys` in `Cargo.toml` are unbuilt here.

## Done

Decision 152 (`decisions/test-run-awake.md`); `keep_awake.rs`, `test_executor::drive_awake`; four unit tests (complete, cancel, error, panic) each see one hold and one release. The Linux build logs the no-op at the go.
