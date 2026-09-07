**Target:** suite/user-guide.md — the `embarch status` example output
**Was:** "Core: up at http://127.0.0.1:4884 (local)\n  auth: not checked (this probe is unauthenticated)"
**Now:** `status` now makes a second, authenticated `GET /status` and prints `  probes: <count>` (or `unknown — <why>` when no-token/unauthorized/the request itself fails) instead of the "auth: not checked" line — embarch-umbrella decision 46, `embarch-umbrella/spec.md`'s `status` row.
