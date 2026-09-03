**Target:** suite/features.md — the `embarch-umbrella` table, the `embarch doctor` row plus three neighbours
**Was:** "`embarch doctor` — the whole chain, `--json` | Shipped — **checks 16–19 are designed and unbuilt**"
**Now:** checks 16–19 are unbuilt, and so are three pieces *inside* checks and commands the table calls Shipped. Audited against the source 2026-09-03 ([embarch-umbrella/spec.md](../embarch-umbrella/spec.md), decisions 18/21/22/23/26/27/29 and 17's amendment).

Four row changes, all in the `embarch-umbrella` table:

- **`embarch doctor` row** — the caveat is bigger than checks 16–19. Check 5 has no
  not-permitted branch (decision 18) and check 10 tests only that a registration
  entry exists, never that the registered command handshakes (decision 23), so
  registered-but-broken still passes. `--prune` and its always-on reporting half
  (decision 26) do not exist.
- **`embarch setup` row** — `--dry-run` (decision 21) is designed and unbuilt. The
  row does not claim it today; it is worth naming so the next reader does not
  re-derive it.
- **`init`/`doctor` support for live target discovery** (cites decision 17) —
  shipped, **except** the amendment: check 8 still counts zephyr-west targets with
  umbrella's own approximating scanner rather than shelling out to `embarch-api`'s
  listing.
- **A new row is needed**, because this has none: *Release CI asserts each repo's
  `Cargo.toml` version matches its pushed tag* (decisions 27/29) — **designed,
  unbuilt in every repo.** `embarch-umbrella`, `embarch-core`, `embarch-api` and
  `embarch-topology` release workflows have no such step, and the other four
  sub-projects have no release workflow at all. Read-only check; only umbrella's
  half would have been this worker's to write.
