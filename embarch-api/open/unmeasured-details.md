# embarch-api: open questions, what has met only fixtures

**Status:** active, 2026-11-22. Split from [open.md](../open.md) by `tasks/api/168`; bullets verbatim except relative links.

Truth: [spec.md](../spec.md). Rationale: [decisions.md](../decisions.md).

## Met only throwaways, fixtures or one machine

- **`stack` has met only throwaway repos** ([decisions](../decisions/stack.md) 96): no real PR stack or forge; hunks spanning two commits go to the newest.
- **`patches` has met only a 3-patch fixture** ([decisions](../decisions/patches.md) 92). No real `west patch` manifest, plain-diff entries or merge-heavy history; base passed by hand.
- **`embarch init` installs the `embarch-hil` skill** (`skills/embarch-hil/`) from a pinned copy an `embarch-umbrella` test holds equal to this one ([its decision 59](../../embarch-umbrella/decisions/integration.md)); a repo `init`ed earlier gets it from `init` again (its decision 60), and the install path is unconfirmed in a live session. **The guide it points at is a skeleton** until `suite/hil-guide.md` (M1.13) is copied over `guide/hil-guide.md` ([decisions](../decisions/guide.md) 108).
- **The report PDF is unmeasured past one machine and 100,000 rows** ([decisions](../decisions/report-pdf.md) 110): byte-identical across two processes here, not across machines (`06`'s open question stays open); a million-row capture, and `plot_ticks` still lives here, not in the shared crate `hil-pdf.md` names.
- **`publish` has met only a mock Core** ([decisions](../decisions/publish.md) 113, [115 to 117](../decisions/publish-revisions.md)), and Core's pending-revision files (`core/136`) only in Core's own test. Unmeasured: the OCP T&V lines against the format's schema, the first real study's zip size, a real `report.typ` through the oracle scan. A swept run's republish ([decision 126](../decisions/publish-revisions.md)) has not met a real Core either.
- **`artifact_path_for_core` is still tolerated at load.** `embarch-umbrella` stopped scaffolding it 2026-09-13. **Closes with one grep of the real configs** — none carrying it means refuse it by name like `[[projects.targets]]`/`soc_chip_overrides`; not checkable inside the suite: [decisions](../decisions/config-retirement.md) 64
