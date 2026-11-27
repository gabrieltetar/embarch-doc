# embarch-core decisions: The `/status` schema key

**Status:** active, 2026-11-27 (`tasks/core/191`, EMB-314). Index: [../decisions.md](../decisions.md). Surface: [../interfaces/hardware.md](../interfaces/hardware.md) (the `/status` row). Sibling: [surfaces.md](surfaces.md) (decision 13).

### 162 — `/status` serves `host_type_schema_version` beside `study_designer_schema_version`, one value under both

The suite settled on `host_type_schema_version` as the name of `embarch_study_designer::HOST_TYPE_SCHEMA_VERSION` (`embarch-api --json versions` already used it); `/status` alone called it `study_designer_schema_version`. **Core now serves both keys, from the same constant**, and a test pins both the key set and their equality. Additive: every reader in the field today reads the old key.

**The old key may go** only when `embarch-core-client` (`tasks/api/220`) and `embarch doctor` (`tasks/umbrella/125`) both read the new key and a released Core has served it, since a reader falling back to the old key is what keeps an older Core usable. Removal is a follow-up in [../open.md](../open.md), not part of this decision. *Not measured:* host-side unit tests only; nothing ran on a board.
