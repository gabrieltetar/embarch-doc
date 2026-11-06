# embarch-ui: open

**Status:** active, 2026-09-13.

Unresolved only. Current truth: [spec.md](spec.md). Why: [decisions.md](decisions.md). The bench editor's: [open/bench.md](open/bench.md); trace and live-study checks: [open/trace.md](open/trace.md); making a bench live, its configs and a prompt naming one: [open/bench-live.md](open/bench-live.md).

- **Nothing installs `embarch-ui.service` but a hand-run `embarch-ui service install`** (decision 101). `embarch-umbrella`'s `setup` runs the desk's own `service install` and not this one, so a fresh machine has no UI until someone runs it. **Trigger:** the release-archive question below is settled, or a second machine needs the UI.

- **Whether `embarch-ui` belongs in the suite release archive is undecided** — [`embarch-umbrella`](../embarch-umbrella/decisions/install.md) decision 14's and the suite's. `assemble-suite.yml` ships three binaries, not this one, so a fresh `embarch setup` can't author or read back a trace. **Trigger:** first non-owner engineer walks the studies guide end to end.

- **The run dialog does not read a *stored* study's build spec.** It knows the step table's Build card and says so; a run-only file's spec is in the file, and the dialog names which case it is, not the wrong study's build. **Trigger:** running a saved study with a build spec from the Live Study tab and wanting to see what it will flash before it does. Decision 38.

- **A flash or a reset that fails mid-run has never been watched.** Only unit-tested are the two steps after a build failure — a `POST /flash` Core refuses, and a reset that does not take. Both would surface as a `failed` frame at phase `build` with a Core error in it, and neither has been seen. **Trigger:** unplug the DUT's probe between build finish and flash start, the cheap way to produce the first one.

- **A signal mismatch has nowhere durable to land**, so a declared-but-wrong signal shows up in the Topology tab or nowhere. Closed upstream as not-needed-yet; two-part trigger: half fired (declarable through this tab), half not (no wire, no bridge). Carried by the row's own carrier cell, not the alert list.

- **A reload no longer re-marks what a link named** (58); his call.
