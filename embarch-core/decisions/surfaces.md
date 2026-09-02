# embarch-core decisions: Error and human surfaces

**Status:** active, 2026-09-02.

The error body and contract version that were designed and not built, and the endpoints a human or a UI reaches enrollment and topology through.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Errors and version handshakes

### 12, 13 — A structured error body and a contract version — designed, not built
Plain-text errors suit a human reading a CLI error, but `doctor --json` and a UI need to branch on error *kind*; a `{code, message, cause}` body would also retire the "finer CLI exit codes" idea, since a script branching on failure kind wants a field, not an exit code. Separately, the only cross-boundary version check is the study schema, so nothing can notice a materially different HTTP contract until a call breaks — `contract_version` would be hand-bumped only for a wire-visible change, and `embarch-api` would **warn, not refuse**, matching the suite's posture on skew. The endpoint table described all three fields as shipped for months when none were.

---


## The human enrollment surface

### 25 — `GET /enroll`, a static page served by Core (retired 2026-08-24, see `embarch-ui` decision 1)
Two lessons outlived it. **Real hardware I/O and the system-file write it produces belong in Core**, which already does that under `hw_lock` — a second process calling the same function does not share that lock. And a page a browser navigates to **cannot attach a bearer token**, so it had to ask a human to paste one; `embarch-ui` holds a server-side client instead, which is why it could replace this outright. No unauthenticated route is left.

### 27 — `POST /dev-bench/link`, declaring the runtime link as its own fact
Port detection came back genuinely ambiguous between dev-bench's bridge and the DUT's own J-Link VCOM, because the only signal it had — the enrolled bench probe's *JTAG* serial — can never match a bridge that is a different physical USB device. The endpoint reaches the crate-side setter against the live Core because the standalone CLI equivalent hit exactly the NTFS permission wall this pattern predicts.

**Then `interface` was added and `serial` became optional.** A serial was named as *the* declared fact because the ambiguity it was written for was between two USB devices, which serials distinguish perfectly. The nRF54L15DK is where a serial cannot help at all: its link is on the DK's onboard J-Link — the same device as its JTAG probe — exposing **two** VCOMs under one serial, so both serials narrow to a *pair* and stop. Detection resolved such a pair by silently taking the lowest, and on this DK the console is the higher one: the guess was wrong and the bench answered nothing while the endpoint reported a confident result. **Neither field is a `400`** rather than a silent no-op — an input that cannot be honoured must fail, not be ignored.

### 28 — `POST /validate` and `GET /alerts`, reachable without touching hardware
Every live-identity re-check only ran as a side effect of `flash`/`reset`/the handshake touching hardware, so there was no way to ask "is the board enrolled as this role still the one attached" on its own. Three outcomes, each a distinct named shape rather than one generic error — which needed a typed `NotEnrolled` in the topology crate, since that branch previously raised a non-downcastable error: enough for a CLI's generic fallback, not enough to tell "not configured yet" from "a real I/O error".
