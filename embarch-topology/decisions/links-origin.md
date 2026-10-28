# embarch-topology decisions: Which board a signal leaves

**Status:** active, 2026-10-28.

Decision 48: a signal can leave a bench board that holds no role, named by its probe.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Siblings: [links.md](links.md) (decision 18, the signal and its route), [enrollment-bench.md](enrollment-bench.md) (decision 41, the bench board).

### 48 — A signal's origin is a role or a bench board, and a board origin is stored by its probe serial (`tasks/suite/046`)

**Amends decision 18's `origin_role`**, which was the only way to say which board a signal leaves. Decision 41 made a role-less bench board enrollable, flashable and resettable by its probe, and the first live session on one (a USB PD bench Nucleo, 2026-10-09 to 10-19) then needed its console declared as a signal. The only origin on offer was a role, so the console was declared from `dev-bench`, which holds a different board: refusals named that role's board, and a reset resolved from the signal would have reached it, not the Nucleo.

**`SignalLink` gains `origin_board: Option<String>`**: the probe serial of the bench board the signal leaves. It is `None` in every row declared before it, which keeps `origin_role` the origin, and is omitted from the file when absent, so no enrollment file migrates and none grows a key nobody declared. When it is set, `origin_role` is the empty string. `SignalLink::origin()` returns a `SignalOrigin` — `Role(&str)` or `Board { probe_serial }` — and `find_signal_origin_board` returns the enrolled board behind either, which is what a consumer resets or reads. `SignalMismatch` and `SignalAmbiguous` carry `origin_board` too and name the board instead of the empty role.

**A declaration may name the board by its enrolled name or its probe serial, and `declare` stores the probe serial.** A bench board's name changes on re-enrolment (decision 41 keys the row by probe), so a stored name could stop resolving while the board sits on the bench unchanged.

**Unlike a role, a board origin must be enrolled when it is declared.** Decision 18 lets a role be declared before anything is enrolled under it, because a role is a short fixed vocabulary. A board reference is free text, and an unresolved one stored as-is would make a typo indistinguishable from a board not yet plugged in. So `declare` refuses a reference that matches no enrolled probe and no bench board's name, and a name two bench boards share (name it by probe).

**A probe enrolled under a role is refused as a board origin.** One board is then never the origin by two names, and the role keeps its meaning: a signal declared from a role follows whatever board holds the role. A signal naming both a role and a board, or neither, is refused.

**What it costs.** A board origin is fixed to one probe: moving the bench board to another probe means re-declaring the signal. A role origin does not have that cost, which is why the role form stays the default for a DUT.

**Reverses if** a bench board ever needs to be swapped for an identical one without re-declaring its signals, which would want a stable board identity that is neither a role nor a probe.
