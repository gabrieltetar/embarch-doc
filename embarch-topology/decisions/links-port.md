# embarch-topology decisions: A link's own declared port, and the fourth `detected_by` answer

**Status:** active, 2026-09-02.

Split verbatim from [links.md](links.md), 2026-09-10, once the `embarch-api` decision 67
annotation pushed that file into reserve. Decision 18, the DUT signal entity and its route, stays
in `links.md` because other sub-projects already cite that path by name; this file holds decision
17, a link's own USB serial as a declared fact distinct from its JTAG probe's, and decision 24,
which depends on the filter decision 18 introduced.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 17 — The dev-bench link's own USB serial is a second declared fact, distinct from its JTAG probe's

**Found live, running the first real study against both real boards enrolled together for the first time.** Port resolution reported dev-bench's detection as **ambiguous between its real link (a Silabs bridge) and the DUT's own probe's VCOM** — both pass the vendor-ID and product-string filter, and **the only disambiguation signal available, the enrolled dev-bench probe's *JTAG* serial, can never match either**, because the bench's link had moved to a dedicated UART bridge chip that is **a different physical USB device from its JTAG probe.** The JTAG-serial fallback **assumed those two were the same device — which held until a second same-vendor device was enrolled onto the same bench at the same time, never previously exercised.**

So an enrolled board gains the link port's *own* USB serial: **a directly declared fact, because no identity readback is possible over a plain UART**, so this cannot be inferred the way JTAG identity is. Resolution **prefers it, hard**, over the JTAG-serial fallback whenever set; unset, behaviour is unchanged, **so today's common case where the link and the probe really are the same device keeps working.**

**Exposed two ways, matching decision 8** — a CLI subcommand writing the crate's storage directly, and a Core endpoint going through the already-elevated service process. **The endpoint had to exist because a plain-user CLI run on the live Windows deployment hit exactly the NTFS permission wall that motivated Core, not a second process, owning system-file writes.** A unit test reproduces the exact real ambiguity, and it was verified against the real live deployment end to end.

**Only the *fallback* has hardware evidence.** The one live two-probe resolution narrowed its candidates on `probe_serial` with `serial_is_fallback` set, because that bench declares no `link_port_serial` of its own [measured 2026-09-06] — so the **declared** path is exercised by unit test only, and this decision exists precisely to keep a reader from reading the fallback's success as its.

### 24 — `detected_by` gets a fourth answer for a declared serial with the VID gate off, and one over-crediting case is accepted rather than chased

**Found the same way decision 20 was: an invisible answer that looked confident.** A direct signal route ([links.md](links.md) decision 18) resolves through `Filter::for_declared_serial`, which turns the VID gate off — a DUT signal may land on any USB-UART bridge, so gating on vendor could only exclude the right answer. But `detected_by` was still set by the same VID lookup every other path uses, which falls back to a generic `"vid-match"` for an unrecognized vendor — a label naming a rule that, with the gate off, never ran at all.

**The fix: a fourth, distinct constant, `DECLARED_SERIAL`, set unconditionally whenever `Filter::no_vid_gate` is on** — not derived from the candidate's actual VID, because under this regime the VID played no discriminating role regardless of what it happens to be. Decision 18's own precedent, read the way decision 20 already reads honesty: `ENUMERATED` exists because an unfiltered listing applied no rule; `DECLARED_SERIAL` exists because a *different* rule ran and the VID-named ones did not.

**A related over-crediting case is accepted rather than chased.** With the VID gate genuinely on, `Filter::resolve` can credit `segger-vid-match` for a bench with several same-vendor candidates where the VID rule matched all of them and eliminated none, while the declared link serial and interface (decisions 17, 20) did the actual narrowing. This is not the bug just fixed — the gate did run, and did exclude every other vendor, a real if coarse fact — so crediting it under-sells how much was pinned down without asserting something false.

**Kept as one field.** `detected_by` names which of three *regimes* resolved a port — a VID rule ran and gated, a declared serial ran and did not, or nothing ran at all — not which individual comparison eliminated the last other candidate. Naming the latter would mean every narrowing step in `select` (serial, product string, interface) reporting what it actually changed, tracked per candidate rather than per regime — a materially larger shape than a `&'static str`, for a case that is honest today, just imprecise. Pinned by a unit test (`a_vid_rule_that_narrowed_nothing_is_still_credited_when_the_gate_ran`).
