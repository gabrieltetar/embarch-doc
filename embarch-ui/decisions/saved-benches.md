# embarch-ui decisions: Retracting and saved benches

**Status:** active, 2026-09-20.

Part of decision 44 — the counterpart enrolling never had, and a saved bench
that proposes rather than enrols. Split out of
[topology-boards.md](topology-boards.md) 2026-09-28 under
`DOC-COMPACTION.md`'s size cap; the role/name split and the validate pass stay
there.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### Retracting: the counterpart enrolling never had

`DELETE /probes/enrolled/{role}` is new in Core, wrapped here as the `✕` on a role row. Until it existed, enrolling could *displace* a row but nothing could remove one, so a mis-enrolment — or a board under an invented role — stayed in `enrollment.toml` for good, short of hand-editing a file behind the NTFS permission wall on the real deployment. **It opens no probe**: a board that no longer answers is precisely the one a human is most likely to be clearing.

### A saved bench: portable, and loading never touches hardware

`embarch/topologies/<slug>.toml` holds which named board played which role, on which probe, plus dev-bench's link and every declared signal. **Loading splits by what each half claims.** The signals and the link are *declarations* — re-stating them changes a file on Core and asserts nothing about silicon — so they apply immediately, each reporting its own outcome. Each enrolment is an *identity claim*, bound after a live hardware-ID read, so it comes back as a **proposal** with a button, and confirming it runs the ordinary enroll.

*Rejected: applying the enrolments directly.* A file on disk is not evidence about what is plugged in, and a load that enrolled from one would be the stale-declared-state failure [`embarch-topology`](../../embarch-topology/spec.md) exists to prevent, rebuilt inside the UI. A proposal carries three facts and decides on none of them: whether the role already holds that probe, whether the probe is attached at all, and which board would be displaced.

**dev-bench's link is deferred rather than skipped.** Core amends it onto the dev-bench enrolment row, so it is refused while that role is empty — the state a fresh load is usually in. The apply report says so in words, and the link is declared with the enrolment when the proposal is confirmed; a silent skip would leave a bench half-loaded with nothing on screen about it.

**A file name is derived from the name, never taken from it**: lowercase, every other run of characters collapsed to one hyphen, so `../../etc/passwd` slugs to `etc-passwd` and a saved bench cannot address anything outside `embarch/topologies/`.
