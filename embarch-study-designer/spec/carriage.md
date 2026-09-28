# embarch-study-designer spec: What a study carries

**Status:** active, 2026-09-28.

Split verbatim from [../spec.md](../spec.md), 2026-09-28, once decision 77's
`requires` row and the `record_checks` row (`tasks/study-designer/031`) took
that file to 9,400/10,240 B — 840 B left (`tasks/study-designer/032`). This
section's mission — which fields cross the wire to dev-bench and which seal
covers them — is distinct from the rest of `spec.md`, which stays there.
Nothing below is reworded from the version that moved.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

| Field | Crosses to dev-bench? | Sealed by |
|---|---|---|
| `steps` | yes | `steps_crc` |
| `streams` (declared taps) | yes | `streams_crc` |
| `protocols` (`.eap` manifests) | yes — dev-bench *executes* them | `protocols_crc` |
| `requires` (firmware versions; the DUT build spec and outpost mode, decision 77) | **no** | — |
| `decoders` (payload layouts) | **no** — only an index rides on a tap | — |
| `dev_bench_log_level` | yes | **deliberately neither** |
| `record_checks` (per-tap record framing) | **no** — Core checks the capture after the run | — |

**Three sibling seals, not one widened one.** `struct Study`'s declaration order — which postcard encoding follows — carries the two step/stream seals *together*, after both of their spans: `steps, streams, steps_crc, streams_crc`, then `protocols, protocols_crc` on its own. Only `protocols_crc` immediately follows the one span it covers; a hand-written C decoder digesting `steps` and then `streams` before either seal still gets, at the end, one run of bytes per seal and a mismatch that names **which third** arrived wrong.

**What is outside every seal is a rule, not an oversight:** how the host later *renders* a captured byte, and how loud the bench is while capturing it, change neither what dev-bench executes nor what it captures. **Re-rendering a capture with a corrected layout, or re-running at a louder log level, must leave it the same study** — otherwise debugging a failure would require altering the artifact under investigation.
