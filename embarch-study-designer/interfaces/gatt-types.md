# embarch-study-designer: GATT and transcript types

**Status:** active, 2026-09-02.

What a discovery reports, what an extraction adds, and one line of a GATT transcript.

Every sequence and string is fixed-capacity ([../decisions/limits.md](../decisions/limits.md) holds each bound). Index: [types.md](types.md). Why: [../decisions.md](../decisions.md).

## GATT types

- **`GattCharacteristicInfo { uuid, properties }`** — `properties` is the **raw ATT byte**, passed through unchanged rather than re-encoded into a crate-invented bitflag, matching the raw-not-symbolic stance on UUIDs.
- **`GattServiceInfo { uuid, characteristics }`** — one primary service, in discovery order.
- **`GattTarget { service_uuid, characteristic_uuid }`** — one characteristic a study names. Both UUIDs, because subscribing needs the service to discover within; it is also the pair a notify tap carries, **so a characteristic named as a monitor target and one given its own decoded file are addressed identically.**
- **A live discovery and a static extraction produce the same type**, so the two are directly comparable rather than needing separate diffing logic — though **as sets, not positionally** ([../decisions/gatt-extract.md](../decisions/gatt-extract.md) 57).
- **`ExtractedGatt { services, symbols, scan }`** / **`GattSymbol { uuid, identifier, kind }`** — the table, plus the C identifier each service and characteristic was declared under, plus the walk's own account of itself. Host-only and **uncapped**: names never cross the wire, so there is no buffer on the far end for them to fit. One symbol list covering both kinds, since a lookup is keyed by UUID and a service UUID never collides with a characteristic's.
- **`ScanReport`** — files read, which contributed and what each contributed, what the hard block pruned, what was not valid UTF-8. **Counts rather than a second copy of the parsed values:** this is the report an engineer reads to answer "did it open the file I expected", which a bounded read could never answer at all.
- **`GattName { label, source, origin }` / `GattNameBook`** — a display name from the vendor table (winning where both apply) or from an extraction's symbols. `origin` is the untrimmed identifier, `label` what a picker shows. `None` — nothing names this characteristic — is an **ordinary answer, not an error**.

## Transcript types

The **exhaustive**, streamed record. `GattDirection` is `Out`/`In`/`Local` (a bench-side event that is not an ATT PDU in either direction). `GattEventKind` covers connect, disconnect, discovery, each service and characteristic found, subscribe, unsubscribe, read and write request and response, notification, indication, error — append-only, same discipline as the message enum.

**`GattTranscriptEntry { rx_utc_ms, direction, kind, service_uuid?, characteristic_uuid?, att_status, payload }`.** UUIDs are carried **in full** rather than as an index into a step's discovered table, because a transcript spans steps — including steps that ran no discovery — so **there is no single flattened table an index could mean anything against.** `att_status` is the raw ATT error code, `0` when there was none; for a characteristic-discovered entry it carries the raw properties byte instead, documented here rather than adding a field used by one event kind.

The rendered row puts the payload in **twice by design**: exact hex, and printable bytes as themselves with everything else as `.`, so a shell transcript is directly readable while nothing is lost for a binary protocol. A row that would not fit is **dropped and logged, never truncated**.

