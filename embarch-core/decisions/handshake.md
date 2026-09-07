# embarch-core decisions: The handshake

**Status:** active, 2026-09-06.

What Core establishes about a bench *before* any step runs: the firmware version gate, and whether the serial link and the JTAG probe reach the same chip. Split out of [studies.md](studies.md) on 2026-09-06 — the study loop and what guards its start are two missions, and a session is here for one. The loop itself: [studies.md](studies.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## The version gate

### 31 — Core enforces exactly what Core can verify, and records how every version was established
**What Core can verify, it verifies:** the bench's version against what it reports over the handshake, before `StudyStart` is sent, so no step ever runs. The gate and the send are **one function taking the send as a parameter**, deliberately — the property is an *ordering*, and an ordering is only worth asserting if a test can assert it. `StudyStart` is the only message that makes dev-bench execute anything, so "the closure was never called" and "no step ran" are the same statement.

**What Core cannot verify, it must not pretend to.** There is no readback path from a DUT, so the result records the *source* of each version rather than presenting an unchecked declaration as a fact.

**The override and the flashed version arrive as query parameters**, not `Study` fields: reflash is a run parameter, and it leaves the body's bytes and both seals untouched. Query rather than a header for the same reason the override is recorded rather than honoured silently — it is visible in Core's request log and in a hand-typed `curl`, and only `1`/`true` counts, since a typo'd value is not permission. **The flashed version carries two facts in one parameter**, because a boolean saying "I flashed something" without saying what is exactly the assertion-without-content this area exists to remove — and its presence is what makes the DUT requirement checkable at all, which this decision claimed and had no mechanism for. **Permission is not an assertion:** a run given the override that then passes on its own merits records nothing.

**Core does not orchestrate the reflash** — that needs a build, which is `embarch-api`'s job. Flashed-this-run is structurally unreachable from Core alone, since `/flash` and `/study` are separate calls with nothing linking them, and the alternative would be a persisted "last thing I flashed" record. A study submitted straight to Core with a stale bench is still rejected.

---


## Handshake identity

### 35 — `HelloAck` carries dev-bench's own hardware ID
The runtime serial link is a *physically separate USB device* from the JTAG connection, and nothing observable over USB proved the two reach the same chip: Core could confirm "the enrolled probe is attached" and "some dev-bench answered" without either implying the other. `HelloAck` is the right frame because it is already where the schema and firmware versions get checked.

*Rejected:* recording it as structurally unclosable — declined on precedent, since `embarch-topology` exists at all because a stale serial once resolved to the wrong port undetected.

**The comparison half belongs to `embarch-topology`:** the two IDs arrive in different encodings, one read over JTAG and one from whatever Zephyr's per-SoC driver decides, so relating them is *chip knowledge* — and getting that boundary wrong would have put a vendor register layout in Core. **Only a declared disagreement refuses the link:** undeclared and not-reported both pass, because the tempting rule — refuse unless it matched — would refuse every healthy bench on any chip whose relation is not yet written down.

---
