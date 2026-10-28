# embarch-topology: decisions

**Status:** active, 2026-09-07.

Why topology is one linked crate. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md).

Decision numbers are permanent and address this sub-project, not a file. Cite them as `embarch-topology decision N`.

| Group | Decisions | What it settles |
|---|---|---|
| [decisions/crate.md](decisions/crate.md) | 1, 2, 3, 6, 13 | A shared crate called live, in-process, with one implementation per question |
| [decisions/probe-selection.md](decisions/probe-selection.md) | 32, 33 | `enroll`'s probe-selection duplicating `embarch-core::resolve_probe`, closed by a shared `select_probe` that reconciles three real divergences |
| [decisions/consumer-boundary.md](decisions/consumer-boundary.md) | 4, 8, 31 | What a consumer may link, and what the crate owes a consumer that cannot link all of it |
| [decisions/storage.md](decisions/storage.md) | 23, 43 | Where the crate's storage physically sits, why it must match embarch-core's, and how a write replaces the file |
| [decisions/scope.md](decisions/scope.md) | 7, 9, 10, 11, 22, 29, 30 | What it models, what it defers, and the override mechanism it deleted |
| [decisions/enrollment.md](decisions/enrollment.md) | 14, 15, 28, 35, 41 (pointer) | The one surface that needs a human, the facts detection cannot produce, the fixed role pair a board's own name was split out of, and the bench board that holds neither |
| [decisions/enrollment-bench.md](decisions/enrollment-bench.md) | 41, 16 | The bench board that holds no role, and the early powered check |
| [decisions/cli.md](decisions/cli.md) | 45 | The CLI's Core guard probes the port the operator names, and the CLI enrols and retracts bench boards the way Core does |
| [decisions/link-declares.md](decisions/link-declares.md) | 20, 27, 42 | A role's declared link facts, the role a moving probe vacates, and what `NotFound` reports when they exclude everything |
| [decisions/bootload-ports.md](decisions/bootload-ports.md) | 36 | A DUT's two declared bootload USB identities, in their own table |
| [decisions/instruments.md](decisions/instruments.md) | 49 | A bench instrument's port identity and line facts, in their own table |
| [decisions/validation.md](decisions/validation.md) | 21, 38, 39, 44 | What the live identity gate asserts about the silicon on a link, what it cannot, why an all-zero ID is a failed read, attaching without rewriting a running target's clocks, and refusing a requested chip that is not the enrolled one before any attach |
| [decisions/validation-classifier.md](decisions/validation-classifier.md) | 25 | Which register pair a chip name resolves to, and the classifier both the gate and the flash path share |
| [decisions/validate-timing.md](decisions/validate-timing.md) | 26, 47 | The `validate` call's own freshness timestamp, distinct from the enrolled record's, and the count of halts the identity gate made |
| [decisions/links.md](decisions/links.md) | 18, 46 | The DUT signal link's declared route, and a declared serial matching several ports |
| [decisions/links-direct.md](decisions/links-direct.md) | 37, 40 | Which signals Core may write, a signal's own line rate, and a direct signal's missing port |
| [decisions/links-origin.md](decisions/links-origin.md) | 48 | A signal that leaves a role-less bench board, stored by its probe serial |
| [decisions/links-port.md](decisions/links-port.md) | 17, 24 | A link's own declared port, distinct from its probe's, and detection's fourth answer |
| [decisions/alerts.md](decisions/alerts.md) | 5, 12, 19, 34 | How a mismatch reaches a human, and the live-push mechanism that was retired |

Decision 9 is **retired** — explicit-override detection, superseded by decisions 2 and 3 removing the override mechanism outright.
