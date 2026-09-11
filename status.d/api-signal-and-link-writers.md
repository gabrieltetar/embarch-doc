**Target:** embarch-ui/decisions/topology-tab.md decision 10
**Was:** "The only human surface for retracting or moving a wire had no working way in" / "there is deliberately no `embarch-topology` CLI mirror, so this tab is the only human surface there is."
**Now:** false as of `embarch-api` decision 67 (`agent/api/042-signal-and-link-writers`, 2026-09-10): `embarch-api` now wraps `POST /signals`, `GET /signals`, `DELETE /signals/{name}` and `POST /dev-bench/link` as both an MCP tool and a CLI subcommand each (`declare_signal`/`declare-signal`, `list_signals`/`list-signals`, `remove_signal`/`remove-signal`, `dev_bench_link`/`dev-bench-link`). The rejection this line generalised from (`embarch-topology/decisions/links.md` decision 18) was specific to a CLI *inside the topology crate* writing the enrollment file directly and hitting the real deployment's permission wall — it never named `embarch-api`, which reaches the same Core route over HTTP exactly as the UI does.

**Target:** embarch-topology/decisions/links.md decision 18
**Was:** rejected "a signal-declaring CLI in the topology crate," on grounds specific to that binary (direct file write, real-deployment permission wall).
**Now:** still true for `embarch-topology`'s own CLI — unaffected — but two other docs generalised it into "no CLI at all" without ever testing it against `embarch-api`, and that generalisation is now false: see `embarch-api` decision 67.

**Target:** suite/studies-guide.md:114
**Was:** (uncited verbatim here — the auditor should re-read the current line) states or implies the UI is the only way to declare a signal/dev-bench link before running a study.
**Now:** false as of `embarch-api` decision 67 — an agent or a human at a terminal can now declare a signal, list them, remove one, and set dev-bench's link, all via `embarch-api`, with no GUI involved. `embarch-api`'s own row for this: [features.d/api-250-signal-and-dev-bench-link-writers.md](../features.d/api-250-signal-and-dev-bench-link-writers.md).
