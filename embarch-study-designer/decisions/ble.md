# embarch-study-designer decisions: BLE link control

**Status:** active, 2026-09-02.

Naming the DUT, elevating the link, and dropping the bond.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 43 — `Action::BleConnect.target_name` — naming the DUT instead of taking whichever advertises first

`target_address: None` was documented as "the common case", on the assumption that a bench has one advertiser. **It does not.** Found live on the first real stimulate-and-capture run: consecutive runs of the *same* study connected to visibly different peripherals — one saw a GATT table with a `0x1910` service, the next an entirely different table carrying two Apple 128-bit services, neither of them the DUT — and every study then failed with `"service not found on DUT"`, which is true and completely misleading. The service wasn't on the device dev-bench happened to reach.

`target_address` remains the precise filter but can't be authored ahead of time for a DUT advertising a resolvable private address, and nobody knows their DUT's MAC by heart. A name is what an engineer actually knows (`CONFIG_BT_DEVICE_NAME`). Both may be set; both must then match. Matched **exactly**, and against the advertised Local Name only — never the GAP Device Name characteristic (`0x2A00`), which would require connecting first, i.e. the very thing this exists to avoid. A blank or whitespace name means "no filter", not "match the empty name", so an untouched UI field can't become a filter nothing satisfies.

**A failed name match reports what *was* on the air** (`"no name match; on air: 'GABRIEL', …"`) rather than a bare `TimedOut`, because "nothing called X appeared, but these did" is the answer to the only question anyone asks at that point — and it immediately proved its worth: the DUT's real advertised name turned out not to be its configured `CONFIG_BT_DEVICE_NAME` at all. Wire v6 → v7, same append-don't-insert discipline as v6.

### 44 — `Action::BleSecurity { level }` — elevating the link is a step an engineer authors

The DUT this milestone was built for **requires an encrypted, MITM-authenticated link (Zephyr `BT_SECURITY_L4`) before it will tolerate GATT service discovery.** That is the engineer's answer to a direct question, per decision 35's no-inference rule — not something read off behavior. And the level has to be *authorable*, not pinned to what one DUT happens to need: the same requirement stated as "L4 always" would be wrong for the next DUT.

`BleSecurityLevel` is `L1`/`L2`/`L3`/`L4`, one-to-one onto Zephyr's `BT_SECURITY_L1..L4` — no security, encrypted-unauthenticated, encrypted-authenticated, LE Secure Connections authenticated with a 128-bit key. A study says which it needs; nothing in the suite defaults it, and `L1` is the honest way to say "this DUT needs none" rather than omitting the step and hoping.

**Why its own `Action` rather than a `require_security` field on `BleConnect`** — considered, and rejected on the ambiguity it would preserve. A `BleSecurity` step gets its own `StepResult` row with its own `Outcome` and error text, so *"connected, then failed to pair"* is distinguishable from *"couldn't connect"* and from *"discovery failed"*. Not hypothetical: this milestone lost a session to a deterministic `"disconnected during service discovery"` (4 of 4 attempts), which is what a failed elevation looks like when nothing in the pipeline can name elevation as a thing that happens. A separate step also composes with `delay_before_ms` (decision 42) and lets a study elevate at a point of its own choosing, or not at all.

**Semantics:** request at least `level` and wait for the link's security to actually change — or for the connection to drop — within the step's own `timeout_ms`. A link **already** at or above `level` is a `Pass`, not an error, since a peripheral that initiates its own elevation on connect (this DUT does, after a 200 ms delay of its own) can win the race. The **achieved** level is reported back, so a study that asked for L4 and got L2 fails loudly at the step that asked instead of proceeding into a discovery the DUT will refuse.

**What it deliberately does not carry:** a pairing method, a passkey, an IO capability, or anything about bonding. Same identity-only discipline decision 41 states for the vendor table — how dev-bench answers a pairing exchange is dev-bench's design ([embarch-dev-bench/decisions.md](../../embarch-dev-bench/decisions.md) decision 34), and whether a bond survives the run is decision 11 there. A study says *what security the link must reach*, and nothing about how.

Appended at discriminant 7. Wire v11 → v12 / host v13 → v14, **re-derived at implementation time** rather than using the 8 → 9 this decision originally reserved: decision 39's amendment shipped first and took v9. That is [embarch-decision-reversals.md](../../embarch-decision-reversals.md) row 18's protocol working as intended rather than a number being corrected.

Three things implementation had to settle:

- **Where the achieved level is reported.** This decision said "reported back" without saying where, and there was nowhere: `StepResult` had no field. It gets `security_level: Option<BleSecurityLevel>`, appended (§4.5), populated on **every** step, not only a security step. That is a strictly larger claim than this decision made, and it is the one that pays: `"disconnected during service discovery"` at L1 and the same failure at L4 are different findings, and until this field existed a result could not tell them apart. `None` means there was no connection to ask about, never that nobody looked.
- **What "fails loudly" is, mechanically.** The step `Fail`s when the reached level is lower than asked. No separate "request it but don't insist" flag: `continue_on_fail` (decision 13) is already exactly that knob, and adding a second would be two ways to say one thing.
- **`L1` really is authorable, and the first implementation got that wrong.** It refused `L1` as "a level to report, not one to elevate to" — which reads sensibly and contradicts this decision's own text. Corrected before commit; the refusal is gone from the builder, the firmware and the UI dropdown, and an `L1` step passes under the same already-at-or-above rule as every other level rather than by a special case. Recorded because the failure is instructive: **the design was already written and the implementation invented a stricter rule than the design asked for**, which is the same shape as ignoring it.

[Validated on hardware 2026-08-26] against `the client S11 B9C3`: `connect` `Pass` at L1, `BleSecurity { level: L4 }` `Pass` reporting **L4**, then `GattDiscover` `Pass` returning **7 services**. Discovery of that table had never once succeeded before this pass. Three runs of the same study, identical results. dev-bench's own log names the pairing method that actually ran — `LE SC Numeric Comparison (authenticated)` — rather than leaving it inferred.

### 50 — `Action::BleUnbond {}` — dropping the bond is a step

Decision 44 gave a study a way to *reach* a security level and no way to get back, and [embarch-dev-bench/decisions.md](../../embarch-dev-bench/decisions.md) decision 11 clears bonds only between studies. So the only way to author a second pairing exchange was to end the study — which is not the same experiment: a bond re-established inside one run exercises the reconnect path, and one re-established across two runs exercises the bench's reset. "Pair, do work, drop the bond, pair again" is a real test.

Field-less, appended at discriminant 8 alongside decision 44's variant, one wire bump for the pair — `BleUnbond` is only reachable once something can establish a bond, so shipping decision 44 alone would have shipped half a feature at two reflashes' cost.

**It drops the link, and that is stated rather than mitigated.** Zephyr's `bt_unpair` disconnects a peer whose keys it clears. dev-bench does not choose that and does not work around it: a link whose keys just went away is not a link. So a study that unbonds mid-run needs its own `BleConnect` afterwards — which is what "pair again" meant. `StepResult.security_level` is `None` for the step, correctly: by the time it returns there is no connection to ask about.

**Why an action rather than a lifecycle setting**, having considered the alternative: decision 44's own argument. A step gets its own `Outcome` row, composes with `delay_before_ms`, and lets the author choose the moment. A `clear_bonds_between_steps` flag on `Study` could not express "here, and not there". The companion half — bonds cleared at *study end* rather than only on the next `Hello` — is dev-bench's ([embarch-dev-bench/decisions.md](../../embarch-dev-bench/decisions.md) decision 37).

---

