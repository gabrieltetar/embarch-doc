# embarch-study-designer decisions: BLE link control

**Status:** active, 2026-09-02.

Naming the DUT, elevating the link, and dropping the bond.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 43 — `Action::BleConnect.target_name` — naming the DUT instead of taking whichever advertises first

No target address was documented as **"the common case", on the assumption that a bench has one advertiser. It does not.** Found live on the first real stimulate-and-capture run: **consecutive runs of the *same* study connected to visibly different peripherals, neither of them the DUT** — and every study then failed with `"service not found on DUT"`, **which is true and completely misleading. The service was not on the device dev-bench happened to reach.**

An address remains the precise filter **but cannot be authored ahead of time for a DUT advertising a rotating private address, and nobody knows their DUT's MAC by heart.** A name is what an engineer actually knows. Both may be set; both must then match. Matched **exactly, and against the advertised name only — never the GAP name characteristic, which would require connecting first, the very thing this exists to avoid.** A blank name means **"no filter", not "match the empty name", so an untouched UI field cannot become a filter nothing satisfies.**

**A failed match reports what *was* on the air** rather than a bare timeout, because **"nothing called X appeared, but these did" is the answer to the only question anyone asks at that point** — and it immediately proved its worth: **the DUT's real advertised name turned out not to be its configured one at all.**

### 44 — `Action::BleSecurity { level }` — elevating the link is a step an engineer authors

The DUT this milestone was built for **requires an encrypted, authenticated link before it will tolerate GATT service discovery. That is the engineer's answer to a direct question, per decision 35's no-inference rule — not something read off behaviour.** And the level has to be *authorable*, **not pinned to what one DUT happens to need: the same requirement stated as "always the highest" would be wrong for the next DUT.**

Four levels, one-to-one onto the stack's own. **A study says which it needs; nothing in the suite defaults it, and the lowest is the honest way to say "this DUT needs none" rather than omitting the step and hoping.**

**Why its own action rather than a field on connect** — rejected **on the ambiguity it would preserve.** Its own step gets its own result row and error text, **so *"connected, then failed to pair"* is distinguishable from *"could not connect"* and from *"discovery failed"*. Not hypothetical: this milestone lost a session to a deterministic `"disconnected during service discovery"`, 4 of 4 — which is what a failed elevation looks like when nothing in the pipeline can name elevation as a thing that happens.** A separate step also **lets a study elevate at a point of its own choosing, or not at all.**

**Semantics:** request at least that level and wait for the link's security to actually change — or the connection to drop — within the step's own timeout. **A link already at or above it is a pass, not an error, since a peripheral that initiates its own elevation on connect — this DUT does — can win the race.** The **achieved** level is reported back, **so a study that asked high and got low fails loudly at the step that asked instead of proceeding into a discovery the DUT will refuse.**

**What it deliberately does not carry:** a pairing method, a passkey, an IO capability, or anything about bonding. **How dev-bench answers a pairing exchange is dev-bench's design. A study says *what security the link must reach*, and nothing about how.**

Its schema bump was **re-derived at implementation time** rather than using the one this decision reserved, another decision having shipped first and taken it — [reversals](../../embarch-decision-reversals.md) row 18's protocol **working as intended rather than a number being corrected.**

Three things implementation had to settle:

- **Where the achieved level is reported.** This decision said "reported back" without saying where, **and there was nowhere.** The result gains a level field, **populated on *every* step, not only a security step. That is a strictly larger claim than this decision made, and it is the one that pays: the same discovery failure at the lowest level and at the highest are different findings, and until this field existed a result could not tell them apart.** Absent means **there was no connection to ask about, never that nobody looked.**
- **What "fails loudly" is, mechanically:** the step fails when the reached level is lower than asked. **No separate "request it but do not insist" flag — continue-on-fail is already exactly that knob, and adding a second would be two ways to say one thing.**
- **The lowest level really is authorable, and the first implementation got that wrong.** It refused it as "a level to report, not one to elevate to" — **which reads sensibly and contradicts this decision's own text.** Corrected before commit, and it now passes under the same already-at-or-above rule rather than by a special case. **Recorded because the failure is instructive: the design was already written and the implementation invented a stricter rule than the design asked for, which is the same shape as ignoring it.**

[Validated on hardware 2026-08-26]: connect passed, elevation passed reporting the level asked for, then discovery returned **7 services. Discovery of that table had never once succeeded before this pass.** Three runs, identical results. **The bench's own log names the pairing method that actually ran rather than leaving it inferred.**

### 50 — `Action::BleUnbond {}` — dropping the bond is a step

Decision 44 gave a study a way to *reach* a security level **and no way to get back**, and the bench clears bonds only between studies. **So the only way to author a second pairing exchange was to end the study — which is not the same experiment:** a bond re-established inside one run exercises the reconnect path, one across two runs exercises the bench's reset. **"Pair, do work, drop the bond, pair again" is a real test.**

Field-less, and **one wire bump for the pair — this is only reachable once something can establish a bond, so shipping decision 44 alone would have shipped half a feature at two reflashes' cost.**

**It drops the link, and that is stated rather than mitigated.** The stack disconnects a peer whose keys it clears; **the bench does not choose that and does not work around it: a link whose keys just went away is not a link.** So a study that unbonds mid-run **needs its own connect afterwards — which is what "pair again" meant.** The level field is absent for the step, correctly: **by the time it returns there is no connection to ask about.**

**Why an action rather than a lifecycle setting:** decision 44's own argument. **A flag on the study could not express "here, and not there".**

---

