# embarch-outpost decisions: The record layout

**Status:** active, 2026-09-02.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 4 — Compact fixed-shape records carrying a per-record `cycles` stamp, postcard-encoded, COBS-framed in batches

**The emit path from an ISR is: write one record into the ring, return.** The drain thread does all framing. **Records carry IDs, never strings** — decision 9 is what makes IDs sufficient.

**The counter read is the only clock access in the module, and where it happens is the constraint.** It is read per record by a header that reaches the counter's low word directly, **not through the kernel's cycle call, which takes a spinlock around a driver call that takes a second critical section around a 64-bit read in a retry loop.** Layout 2 removed the stamp entirely on the grounds that any read inside a context switch and inside the ISR wrapper is **the instrument charging its cost to the exact path it exists to measure** — the same class of objection that already refuses an `irq_lock` there, since **a trace whose cost is a latency floor on unrelated interrupts distorts what it measures.** Layout 3 restored it because **the objection was to the lock, not to the clock, and only the lock had to go.**

**A ring slot is exactly 16 bytes plus the stamp, and a `BUILD_ASSERT` holds that equality** against the constant the ring size is divided by. Without it every ring was quietly 1.25× its configured size, **and a unit test asserting slots × slot-size ≤ ring-bytes passed the whole time, because it measures the product through that same constant.**

**The version went 2 → 3, not back to 1, although the wire is byte-for-byte what 1 was.** A version byte exists so a host can say *"I decode up to N"*, **and a number reused after an incompatible wire has worn a higher one cannot say that.**

**A wire change is not done when the DUT emits it — it is done when every host that decodes it has been re-measured against it.** A host written against layout 2 kept timing spans by frame arrival after layout 3 landed and **misreported the instrument's own cost by 46×** ([reversals](../../embarch-decision-reversals.md) row 86). **Nothing was wrong with the wire; the host was reading the older of the two clocks it carried.**

*Rejected: a per-record delta varint.* About one byte per record instead of five, and — computed at drain time between consecutive records *in the ring* — **a dropped record just widens one delta, so the timeline stays correct.** Declined because **it does not address the stated problem: the emit path still reads the counter, which is the cost being removed.**

*Rejected: one cycle stamp per frame, read by the drain thread.* **This genuinely answers the emit-path cost** — the read moves out of the hooks into a thread — and was declined because **it buys no resolution: intra-frame timing is gone either way, so all it adds is a second clock, with a rate field, an unwrap, and a cycles-to-host-time fit to keep honest.** One clock, coarse and shared with every other stream, beat two clocks at the same resolution.

*Rejected: keeping the per-record stamp behind a Kconfig.* **Two wire layouts to decode, two sets of host arithmetic, and a rendered CSV whose columns depend on a DUT's build options** — for a choice with no measurement either way. **When there is one, the layout version is the mechanism for changing it again.**

### 27 — The Python reference decoder refuses a stream whose layout it does not speak, with no override

`scripts/decode_outpost.py` read the header's `record_layout_version` and then parsed every records frame with the layout-3 grammar whatever it said, so a layout-4 stream would have decoded into a whole capture of plausible, wrong rows. **It now refuses: exit 2, no rows, both numbers on stderr.** `embarch-study-designer`'s Rust decoder already behaved this way (`ManifestRefusal::LayoutVersion`); the two decoders now keep the one promise decision 4's version byte exists to make.

**A manifest whose `record_layout_version` disagrees with the header is refused like a build-ID mismatch** — names dropped, stream kept, `manifest_refused` set — and the same `--allow-build-id-mismatch` overrides it. A manifest with no such key (older schema) is not refused. **No third flag**, per decision 24.

**The stream refusal has no override at all**, unlike decision 24's two: those let an operator vouch for provenance the decoder cannot see, but nothing an operator knows makes a layout-3 grammar read layout-4 bytes correctly. *Measured:* `tests/decoder_unit.py` `TestLayoutRefusal`; `tests/cross_decoder.py` still agrees with the Rust decoder on all 831 rows of the layout-3 fixture. Only the first header frame is checked, as for build ID.
