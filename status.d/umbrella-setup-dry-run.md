**Target:** suite/features.md § embarch-umbrella — the `embarch setup` row
**Was:** "Shipped — **the Windows registry half is type-checked, not run**; `--dry-run` unbuilt"
**Now:** `--dry-run` shipped 2026-09-04 (decision 21). The Windows registry half is still type-checked, not run — unchanged.

Decision 21 is now built, so it should also come out of the row's decision list
only if that list means "unbuilt"; it does not, so leave `3, 21, 28` alone.
Detail: [embarch-umbrella/decisions/install.md](../embarch-umbrella/decisions/install.md) decision 21.
