# embarch-topology: decisions

**Status:** active, 2026-09-07.

Why topology is one linked crate. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md).

Decision numbers are permanent and address this sub-project, not a file. Cite them as `embarch-topology decision N`.

| Group | Decisions | What it settles |
|---|---|---|
| [decisions/crate.md](decisions/crate.md) | 1, 2, 3, 4, 6, 8, 13 | A shared crate called live, in-process, with one implementation per question |
| [decisions/storage.md](decisions/storage.md) | 23 | Where the crate's storage physically sits, and why it must match embarch-core's |
| [decisions/scope.md](decisions/scope.md) | 7, 9, 10, 11, 22 | What it models, what it defers, and the override mechanism it deleted |
| [decisions/enrollment.md](decisions/enrollment.md) | 14, 15, 16 | The one surface that needs a human, and the facts detection cannot produce |
| [decisions/link-declares.md](decisions/link-declares.md) | 20, 27 | A role's declared link facts, and what `NotFound` reports when they exclude everything |
| [decisions/validation.md](decisions/validation.md) | 21, 25 | What the live identity gate asserts about the silicon on a link, and what it cannot |
| [decisions/validate-timing.md](decisions/validate-timing.md) | 26 | The `validate` call's own freshness timestamp, distinct from the enrolled record's |
| [decisions/links.md](decisions/links.md) | 17, 18, 24 | Declared facts about wires: a link's own port, and a DUT signal's route |
| [decisions/alerts.md](decisions/alerts.md) | 5, 12, 19 | How a mismatch reaches a human, and the live-push mechanism that was retired |

Decision 9 is **retired** — explicit-override detection, superseded by decisions 2 and 3 removing the override mechanism outright.
