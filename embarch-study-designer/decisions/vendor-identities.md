# embarch-study-designer decisions: vendor GATT service identities

**Status:** active, 2026-09-02.

The built-in table of vendor-defined service identities (split verbatim from [gatt.md](gatt.md)).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 41 — A built-in table of vendor-defined GATT service identities

Decision 35's registry is per-repo and engineer-authored **because what a *custom* characteristic's bytes mean is knowledge only that repo's engineers have.** A vendor-defined service is the opposite kind of fact: **Nordic's UART Service has the same UUIDs on every device that implements it, published in the stack's own headers.** Requiring every engineer to transcribe a 128-bit UUID **to write to a service the stack itself defines is pure error surface.** So those identities ship as constants, **picked by id, never by typing a UUID.**

**Identity only. No semantics, ever** — decision 35's rule applied to a table **that would be far more tempting to over-fill.** It records *where* to write and **nothing whatsoever about *what* to write**: no command vocabulary, no line terminator, no "send `help` to list commands". **Whatever sits behind a given DUT's endpoint — a shell, an application protocol, a bootloader, nothing at all — is that DUT's business**, supplied per study as literal bytes.

**An entry is a conditional, not a claim**: *if* a device exposes this service, these are its UUIDs. **Live discovery remains the only thing that answers "does this DUT actually have it?"** — written down rather than assumed **because the first DUT this was pointed at turned out not to expose it at all.**

The vendor's declared properties are included because they decide **whether a chosen operation is even legal**: the builder refuses a write against a notify-only characteristic **rather than letting it fail mid-study as an opaque ATT error.** It remains **the vendor's claim, not a measurement** — a discovered-properties field sits beside it, and **where the two disagree live discovery wins and the disagreement is itself the finding.**

**No schema bump:** a vendor row resolves into an ordinary exchange carrying plain UUIDs before anything is encoded, **so dev-bench never learns the table exists** — pinned by a test asserting a vendor row and the equivalent raw row build the byte-identical action.
