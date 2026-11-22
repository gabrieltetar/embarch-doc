# embarch-umbrella: spec — the plugin marketplace

**Status:** active, 2026-11-21.

Split verbatim out of [../spec.md](../spec.md) on 2026-11-21 under [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 (`tasks/umbrella/101`). Current truth: [../spec.md](../spec.md). Why: [../decisions.md](../decisions.md).

This repo also holds the suite's Claude Code plugin marketplace, `.claude-plugin/marketplace.json`, named `embarch`: `embarch-desk`, `embarch-promptu` and `embarch-chat`, each a `git-subdir` source (`url` + `path: plugin`), so each plugin installs from its own repo's pushed `plugin/` — a `github` source with `path` installed the whole repo instead [measured on Claude Code 2.1.287, 2026-10-29] ([`embarch-promptu` decision 20](../../embarch-promptu/decisions/what.md)). It moved here from `embarch-desk` on 2026-10-29. `setup` installs `embarch-desk@embarch` but does not add the marketplace (58).
