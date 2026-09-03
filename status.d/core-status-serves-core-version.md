**Target:** suite/features.md §4's hardware table — the `GET /status` row
**Was:** "`GET /status` — list connected probes | Shipped | hw | §4"
**Now:** `/status` also reports Core's own build version. It serves `core_version` (compiled in from `CARGO_PKG_VERSION`) alongside `probes` and `study_designer_schema_version`, so a caller can tell which Core binary answered without running it. Not a new feature row — the existing row's description is now partial.

The account is in [../embarch-core/decisions/surfaces.md](../embarch-core/decisions/surfaces.md) decision 13, and the served field set is [../embarch-core/interfaces.md](../embarch-core/interfaces.md)'s `/status` row.

**Deliberately no reversals row for the retired `contract_version` half.** [../embarch-decision-reversals.md](../embarch-decision-reversals.md) requires a row to have been caught by a real build, install, capture, or by reading a real repo's files — "never by inspection alone" — and this retirement was reasoned, not observed. Left to the supervisor to disagree with if it reads it otherwise.
