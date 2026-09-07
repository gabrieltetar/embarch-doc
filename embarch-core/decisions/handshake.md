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

### 47 — `HelloAckInfo`'s self-reported field is renamed; the rest of the surface is not, yet
`GET /dev-bench/hello`'s JSON body called the self-reported ID `hardware_id` and the probe-read one `probe_hardware_id` — so a caller reading `hardware_id` off this route and off `/probes/enrolled` under the same name got two different facts, four fields apart in one response, differing only by a swap of their two 4-byte halves (`tasks/core/020`). **Renamed here to `self_reported_hardware_id`**, since nothing in this suite parsed the old name off this specific route (`embarch-core-client`'s `HelloAckResponse` carries neither ID at all yet); `probe_hardware_id` keeps its existing spelling.

**The other three routes that serve the probe-read ID as `hardware_id` — `/probes/enroll`, `/probes/enrolled`, `POST /validate` — are deliberately left alone.** `embarch-core-client` deserializes all three with `hardware_id: String`, required, no `#[serde(default)]`; renaming the wire field there breaks every existing caller (`embarch-api`'s CLI and MCP tools, `embarch-ui`) rather than adding a new one, which is a different kind of change than this decision makes. Closing that gap needs either a compatibility window (both spellings served together for a release) or one coordinated commit across `embarch-core` and `embarch-api`, and deciding which is *this suite's* call, not a single sub-project's — left open, `tasks/core/020` names it explicitly rather than doing it silently.

*Rejected:* renaming all four routes in one pass — the candidate direction named in `tasks/core/020` — because it trades a same-spelling-different-meaning bug (confusing, but visible the moment two values are compared) for a silent runtime deserialization failure in a different repo (worse: invisible until something calls it).

---
