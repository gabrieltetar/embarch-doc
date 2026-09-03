**Target:** suite/features.md — the `embarch doctor` row ("Shipped — **check 11 is a stub and check 14 is unbuilt**")
**Was:** "Shipped — **check 11 is a stub and check 14 is unbuilt**"
**Now:** check 11 is built — it compares Core's served `study_designer_schema_version` against this binary's compiled `HOST_TYPE_SCHEMA_VERSION` and reports Core's own `compatible` verdict on the bench's wire version, failing on a real disagreement (embarch-umbrella decision 33). The "check 14 is unbuilt" half is stale twice over: the flashing-backend check took number 14 and shipped 2026-08-31 (this table's own next-but-one row says so), and the bind-address check it meant is now numbered 16 in `embarch-umbrella/spec.md`. Neither check 11 nor check 15 has been run against a live Core or a flashed bench.

A new row belongs beside the existing check-13/14 rows:

| `doctor` check 15 — the running Core's `core_version` is the located build | Shipped, unverified on hardware | unit | 34 |

Both new checks are `embarch-umbrella/decisions/doctor.md` 33 and 34.
