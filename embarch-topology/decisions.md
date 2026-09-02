# embarch-topology: decisions

**Status:** active, 2026-09-02.

Why topology is one linked crate. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md).

Decision numbers are permanent and address this sub-project, not a file. Cite them as `embarch-topology decision N`.

| Group | Decisions | What it settles |
|---|---|---|
| [decisions/crate.md](decisions/crate.md) | 1, 2, 3, 4, 6, 8, 13 | A shared crate called live, in-process, with one implementation per question |
| [decisions/scope.md](decisions/scope.md) | 7, 9, 10, 11 | What it models, what it defers, and the override mechanism it deleted |
| [decisions/enrollment.md](decisions/enrollment.md) | 14, 15, 16, 20, 21 | The one surface that needs a human, and what two same-family boards taught it |
| [decisions/links.md](decisions/links.md) | 17, 18 | Declared facts about wires: a link's own port, and a DUT signal's route |
| [decisions/alerts.md](decisions/alerts.md) | 5, 12, 19 | How a mismatch reaches a human, and the live-push mechanism that was retired |

Decision 9 is **retired** — explicit-override detection, superseded by decisions 2 and 3 removing the override mechanism outright.
