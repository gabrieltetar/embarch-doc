# embarch-outpost decisions: The operator's override

**Status:** active, 2026-09-02.

An operator may proceed past either post-hoc refusal, explicitly and once.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The refusals: [manifest.md](manifest.md) decision 9 and [clocks.md](clocks.md) decision 18.

### 24 — An operator may override either post-hoc refusal explicitly, at the command line, once per invocation, and the override is never a config default

Decision 9's manifest mismatch and decision 18's unverified join are the suite's two post-hoc refusals: both protect a reader from a rendering that is plausible and wrong, and both are one flag away from an operator proceeding anyway — `--allow-build-id-mismatch` and `--allow-unverified-join` in `scripts/decode_outpost.py`.

**This is one posture, not two accidents.** A refusal protects a reader who trusts the render at face value; an operator who knows the capture's provenance out-of-band — a manual reflash they made themselves, a sidecar file they hand-verified — may accept the risk the refusal exists to prevent. That knowledge cannot live in the decoder, so the tool takes the operator's word for it **once, for this invocation, on the command line** — never a project setting, never a default, never anything that survives past the run that passed it.

**Neither refusal's default behavior changes.** Both flags are opt-in; the unconditional language in decision 9 and decision 18 describes what happens with neither flag set, which is every invocation that does not name one. An override is visible in the command that produced the render, not hidden inside it: **the two flags are the entire mechanism, and there is no third way to reach either bypass.**

**Rejected: folding the override into the manifest or arrival-CSV format itself** — a flag that survives in a file survives past the operator who set it, which is exactly the silent-staleness failure decision 9 exists to close. The override has to cost a keystroke every time or it stops being a considered exception.
