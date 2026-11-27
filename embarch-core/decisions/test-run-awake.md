# embarch-core decisions: Keeping the host awake through a Test run

**Status:** active, 2026-11-26 (`tasks/core/168`, EMB-371; decision 152; `notes/hil/03-test.md`, "A run", item 9). Index: [../decisions.md](../decisions.md). Builds on [test-run-executor.md](test-run-executor.md) (136, 137) and [test-run-go.md](test-run-go.md) (135), which it does not grow.

### 152 — Core holds the host awake from a run's go to its end, behind a trait, and a hold is a guard

**The need.** A Test run can outlast a laptop's idle timeout. While a run holds the lease, Core asks the OS to keep the system awake and gives the request back when the run ends. **Inferred, not measured**: that the request keeps a Windows service's host awake through an idle timeout.

**The seam.** `keep_awake::KeepAwake` has `hold` and `release`; `Hold` is a guard that holds when made and releases when dropped. `test_executor::drive_awake` wraps [`drive`](test-run-executor.md) in one `Hold`, and `spawn` calls it with `HostKeepAwake`. Because the guard releases on drop, a run that completes, is cancelled, ends in an error or panics gives the hold back once. A unit test sees one hold and one release on each of those four paths with a recording keeper.

**Windows.** `HostKeepAwake` calls `SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` and releases with `ES_CONTINUOUS`. The state belongs to the calling thread, which is why the guard lives inside the run's own blocking thread, where `drive` also runs. It asks for the system, not the display. A failed call is a warning and the run goes on. **Elsewhere** it is a no-op that logs once at info, at the go.

**Not measured.** Whether the request keeps a service's host awake through an idle timeout, and whether the host sleeps normally afterwards. **Debt**: the first Test run on the bench host (`tasks/core/168`). The Windows half is `cfg(windows)` and **unbuilt**: the native Windows build is the owner's debt. The owner may strike this unit to defer it to the attested phase.
