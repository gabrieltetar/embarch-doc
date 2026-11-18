# 086 — Check the USB PD PDO decode against the standard's tables, and pin it with tests

**State:** open
**Source:** Fleet Ready issue: the config-vs-standard check (`atlas/004`) decodes Fixed, Variable, Battery and Augmented PDOs from a bit layout written from memory, and nothing has compared those positions and units with the standard.
**Issue:** EMB-159
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`_pdo` in `src/embarch_atlas/fwcheck.py` (and its unit constants, lines 54-58) is checked field by field against the PDO tables of **USB PD R3.2 V1.2**, and a test pins at least one known word per PDO and APDO type, source and sink, to its expected decoded fields. Any position, unit or name that disagrees is fixed in the same unit.

The owner read the tables from his own copy and gave the layout below: bit ranges, field names and units only. Quote no more of the standard than this into the repo.

- **PDO:** B31..30 type: 00b Fixed, 01b Battery, 10b Variable, 11b APDO. **APDO:** B29..28 kind: 00b SPR PPS, 01b EPR AVS, 10b SPR AVS, 11b invalid.
- **Fixed, vSafe5V, Source:** B29 Dual-Role Power, B28 USB Suspend Supported, B27 Unconstrained Power, B26 USB Communications Capable, B25 Dual-Role Data, B24 Unchunked Extended Messages, B23 EPR Capable, B22 reserved, B21..20 Peak Current, B19..10 Voltage in 50 mV, B9..0 Maximum Current in 10 mA.
- **Fixed, vSafe5V, Sink:** B29 Dual-Role Power, B28 Higher Capability, B27 Unconstrained Power, B26 USB Communications Capable, B25 Dual-Role Data, B24..23 Fast Role Swap required current, B22..20 reserved, B19..10 Voltage in 50 mV, B9..0 Operational Current in 10 mA.
- **Fixed, above 5 V:** B29..22 reserved, B21..20 Peak Current (Source), B19..10 Voltage in 50 mV, B9..0 Maximum or Operational Current in 10 mA.
- **Battery:** B29..20 Maximum Voltage in 50 mV, B19..10 Minimum Voltage in 50 mV, B9..0 Maximum Power in 250 mW.
- **Variable:** B29..20 Maximum Voltage in 50 mV, B19..10 Minimum Voltage in 50 mV, B9..0 Maximum Current in 10 mA.
- **SPR PPS Source:** B27 PPS Power Limited, B26..25 reserved, B24..17 Maximum Voltage in 100 mV, B16 reserved, B15..8 Minimum Voltage in 100 mV, B7 reserved, B6..0 Maximum Current in 50 mA. **Sink:** B27..25 reserved, the rest as the Source.
- **SPR AVS:** B27..26 Peak Current (Source), B25..20 reserved, B19..10 Maximum Current for 9 to 15 V in 10 mA, B9..0 Maximum Current for 15 to 20 V in 10 mA.
- **EPR AVS Source:** B27..26 Peak Current, B25..17 Maximum Voltage in 100 mV, B16 reserved, B15..8 Minimum Voltage in 100 mV, B7..0 PDP in 1 W. **Sink:** B27..26 reserved, B25..17 Maximum Voltage in 100 mV, B15..8 Minimum Voltage in 100 mV, B7..0 Maximum Power in 1 W.

## Why now

The owner supplied the tables on the issue, so the check needs no distilled standard document.

## Dispatch notes

- A first reading, for the worker to confirm or refute, not to take on trust: the positions and units look right, and three things look off. (1) A fixed PDO above 5 V has B29..22 reserved, but `_pdo` decodes the vSafe5V flags from every fixed word, so a 9 V PDO reports `drp=False` and the like where the field is not carried; decide whether a word with a voltage other than 5 V gets those flags as `None`, and say so in `DESIGN.md`. (2) A sink EPR AVS APDO's B7..0 is Maximum Power, not PDP, yet both land in `pdp_w`. (3) The SPR AVS currents are for the 9 to 15 V and 15 to 20 V ranges, while `__str__` prints "at 15 V" and "at 20 V".
- Changing a field name changes what an expression or `decode` input sees: grep the helpers' consumers (`HELPERS`, the standard check's expressions, tests, any skill reference) and keep every caller working.
- In code comments and `DESIGN.md`, cite the standard by name and revision only ("USB PD R3.2 V1.2"), never a section or table number: those move between revisions.
- No file of this sub-project is in reserve.

## Done when

- [ ] Every PDO and APDO type's field positions and units in `_pdo` agree with the layout above, source and sink, and any that did not is fixed.
- [ ] `tests/test_fwcheck.py` pins at least one known word per type (Fixed 5 V source and sink, Fixed above 5 V, Battery, Variable, SPR PPS source and sink, SPR AVS, EPR AVS source and sink) to its expected fields.
- [ ] `DESIGN.md` says the decode was checked against USB PD R3.2 V1.2 and what a reserved field decodes to.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
