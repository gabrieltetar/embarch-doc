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

### 56 — `hardware_id` is the probe-read ID everywhere, and the deferred rename is cancelled rather than scheduled
Decision 47 left the rollout shape open — compatibility window, or one coordinated commit across `embarch-core` and `embarch-api`. **Neither. The rename does not happen, and this is the settlement rather than a further deferral** (`tasks/api/044`).

**The defect decision 47 was protecting against is already gone.** It was one *spelling* carrying two *concepts*: `hardware_id` meant the JTAG-read ID on `/probes/enroll`, `/probes/enrolled` and `POST /validate`, and the bench's self-reported ID on `GET /dev-bench/hello`. Renaming the `/dev-bench/hello` field to `self_reported_hardware_id` removed the collision outright. What survives is the much weaker shape of one *concept* under two spellings — `hardware_id` on the three probe routes, `probe_hardware_id` on `/dev-bench/hello` — and no reader of a single response can now get the wrong fact from either.

**So `hardware_id`, unprefixed, is this suite's name for the probe/JTAG-read identity**, and that is a rule about the default rather than an exception to one. `probe_hardware_id` exists on exactly one route, `GET /dev-bench/hello`, because there it sits four fields from `self_reported_hardware_id` and a row of two hardware IDs is unreadable unless both say which they are. A prefix that disambiguates against a neighbour is worth its inconsistency; the same prefix on a route with no neighbour to disambiguate against is cost with no reader.

**The cost side is what settles it.** `embarch-core-client` deserializes the three probe routes with `hardware_id: String` — required, no `#[serde(default)]`, and freestanding structs rather than types shared with Core, so a wire rename is not a compile error anywhere. It fails at runtime, on the first call, in another repo, and reaches the CLI, every MCP tool and `embarch-ui` at once. A compatibility window buys that back only by making Core serve both spellings for a release — two names for one field, live, which is the state this whole thread exists to end.

**What this decision owes in exchange for not renaming: the concept has to be legible at the struct, not only on the wire.** `EnrollProbeResponse` and `ValidateOkResponse` — the two response structs this crate actually defines for `/probes/enroll` and `POST /validate` — each carry a doc comment on `hardware_id` saying it is the probe-read value and pointing here, so the next reader settles it without re-deriving it from two repos. **`EnrolledBoardResponse` does not exist in this crate**: `GET /probes/enrolled` serves `embarch_topology::hardware::EnrolledBoard` directly, so the comment this decision owes on that third route belongs on `EnrolledBoard`'s own `hardware_id` field, in `embarch-topology` — out of this crate's reach, filed to that repo's queue instead of paid here (`tasks/core/044`). That is the whole remaining work this crate can pay, and `embarch-core`'s wire surface does not change.

*Rejected:* leaving it open a third time. `tasks/core/020` deferred it, decision 47 recorded the deferral, and `tasks/api/044` inherited it — a question re-filed rather than answered accumulates the cost of being re-read without ever paying it down.

---
