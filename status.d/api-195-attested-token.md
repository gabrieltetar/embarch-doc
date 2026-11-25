**Target:** embarch-token.md §2 — the `embarch-api` row of the holders table
**Was:** "Its config's inline value or env-var name ... otherwise the same token file Core uses", sent on every request
**Now:** sent only after a verified `POST /auth/challenge`: with a `core-fingerprint` beside the token file, a fingerprint match sends the machine-wide token, a mismatch the development store's or none (api decision 133).
