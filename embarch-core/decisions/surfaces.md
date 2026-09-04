# embarch-core decisions: Error and human surfaces

**Status:** active, 2026-09-02.

The error body and contract version that were designed and not built, and the endpoints a human or a UI reaches enrollment and topology through.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Errors and version handshakes

### 13 — `core_version` on `/status`; no hand-bumped `contract_version` (built 2026-09-03)
The only cross-boundary version check was the study schema, so nothing talking to Core **over HTTP** could say which build answered — the version was reachable only by running the binary, and a deploy that silently did not land is indistinguishable from one that did (`embarch-dev-workflow.md` §4a: `deploy-core` reports `landed` either way, and its own length check cannot discriminate a rebuild of one constant). `/status` now serves `core_version` from `env!("CARGO_PKG_VERSION")`. **Mechanical, not maintained**: `Cargo.toml`'s version already tracks the release tags, so the field cannot drift from the build serving it. Consumers **warn, not refuse**, on a difference from the version they were built against — this decision's original posture on skew, unchanged.

**The `contract_version` half is retired rather than built.** It was to be hand-bumped only for a wire-visible change, and nothing forces the bump: the failure mode is a number reading "same" across contracts that differ, which is worse than no number, and this entry's own history is the evidence — the endpoint table described all three designed fields as shipped **for months when none were**. `core_version` covers the case mechanically and **over**-warns rather than under-warns, the safe direction for a warn-not-refuse consumer. Revisit if a `core_version` skew warning is ever silenced as too noisy to act on; that is the first real evidence a finer-grained number would earn its keep.

The served field set is pinned by a test on `StatusResponse`'s serialized keys (`api.rs`), so **adding** a field without editing [../interfaces.md](../interfaces.md)'s `/status` row fails the suite. That test, not a note, is what answers the "described as shipped when it wasn't" shape here.

### 12 — A `{code, message, cause}` JSON error body — deferred, and it is not Core's alone
Plain-text errors suit a human reading a CLI error, but `doctor --json` and a UI need to branch on error *kind*; a `{code, message, cause}` body would also retire the "finer CLI exit codes" idea, since a script branching on failure kind wants a field, not an exit code. Still worth building, and **deliberately not built here.**

Its value is **entirely** in consumers branching on `code`, which makes the `code` enum a wire contract shared with `embarch-api`, `embarch-ui` and `embarch-umbrella`'s `doctor` — so this is a cross-repo sequenced change (`embarch-fleet/protocol.md` §8), not a Core-local one. Core-side alone it is ~40 error-construction sites re-shaped, every one needing a stable `code` invented for it, while every consumer still reads plain text: the whole cost and none of the benefit. **Trigger:** the first consumer that must distinguish two error kinds sharing one HTTP status and cannot; `study_schema_mismatch` — proposed here, never reconciled against the enum, never fired ([../open.md](../open.md)) — is reachable by nothing until then.

---


## The human enrollment surface

### 25 — `GET /enroll`, a static page served by Core (retired 2026-08-24, see `embarch-ui` decision 1)
Two lessons outlived it. **Real hardware I/O and the system-file write it produces belong in Core**, which already does that under `hw_lock` — a second process calling the same function does not share that lock. And a page a browser navigates to **cannot attach a bearer token**, so it had to ask a human to paste one; `embarch-ui` holds a server-side client instead, which is why it could replace this outright. No unauthenticated route is left.

### 27 — `POST /dev-bench/link`, declaring the runtime link as its own fact
Port detection came back genuinely ambiguous between dev-bench's bridge and the DUT's own J-Link VCOM, because the only signal it had — the enrolled bench probe's *JTAG* serial — can never match a bridge that is a different physical USB device. The endpoint reaches the crate-side setter against the live Core because the standalone CLI equivalent hit exactly the NTFS permission wall this pattern predicts.

**Then `interface` was added and `serial` became optional.** A serial was named as *the* declared fact because the ambiguity it was written for was between two USB devices, which serials distinguish perfectly. The nRF54L15DK is where a serial cannot help at all: its link is on the DK's onboard J-Link — the same device as its JTAG probe — exposing **two** VCOMs under one serial, so both serials narrow to a *pair* and stop. Detection resolved such a pair by silently taking the lowest, and on this DK the console is the higher one: the guess was wrong and the bench answered nothing while the endpoint reported a confident result. **Neither field is a `400`** rather than a silent no-op — an input that cannot be honoured must fail, not be ignored.

### 28 — `POST /validate` and `GET /alerts`, reachable without touching hardware
Every live-identity re-check only ran as a side effect of `flash`/`reset`/the handshake touching hardware, so there was no way to ask "is the board enrolled as this role still the one attached" on its own. Three outcomes, each a distinct named shape rather than one generic error — which needed a typed `NotEnrolled` in the topology crate, since that branch previously raised a non-downcastable error: enough for a CLI's generic fallback, not enough to tell "not configured yet" from "a real I/O error".
