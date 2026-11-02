# embarch-ui: making a bench live

**Status:** active, 2026-11-02.

What is true now of phase 4 of [embarch-bench-editor-proposal.md](../../embarch-bench-editor-proposal.md): a saved bench applied to Core from the Topology tab's canvas, and this UI's record of which bench and config are live. What it applies: [bench.md](bench.md); editing it: [bench-editing.md](bench-editing.md). Why: decisions 90–95 ([../decisions.md](../decisions.md)). Routes: [../interfaces/topology.md](../interfaces/topology.md); events: [../interfaces/bench.md](../interfaces/bench.md). Unresolved: [../open/bench-live.md](../open/bench-live.md). What the tab shows: [tabs.md](tabs.md).

## On the bar

Beside Save, the bench's live state in words: *not live*; *live*, or *live · A* with its config; *live: other-bench* when another bench in this repo is; *superseded by repo · bench* when another repo went live after it; *live config A is gone*; *live: bench — its file is gone* or *— its file does not parse*; *unknown: reason* with **Read again**. Then each gesture where it applies:

- **Make live**, or **Save and make live** with edits on screen, or **Make B live** for another config of the live bench — an explicit make-live, which takes the machine.
- **Declare again**, on the live bench: applies it again as saved, for a failed row or for the dev-bench link once its role holds a board.
- **Stop being live**, on the bench the record names, or while its file is gone or broken: the record goes and Core keeps what it holds.
- The **write-through indicator**: *declared · 2 proposals · 1 failed*, a button opening that report; or, lasting until a declare lands, *saved, not declared*, *not declared again* or *declared, not recorded*, saying why.

The config tab the bench was made live with is marked as the live wiring. **Live report** reopens the last report.

## What reaches Core

| On the bench | Core route | When made live |
|---|---|---|
| A board type on a role's part | `PUT /probes/enrolled/{role}/board` | Applied |
| A probe on a role's part, or over its SWD lead | `POST /probes/enroll {role}`, `name` the board type | Proposed |
| A probe reached by a role-less board | `POST /probes/enroll`, no role, `name` its label | Proposed |
| `vcom` on the dev-bench part | `POST /dev-bench/link` | Applied; deferred while the role holds no board |
| Each `[[signals]]` entry | `POST /signals` | Applied |
| `scpi` on a part | `PUT /instruments`, the template's line facts | Applied |
| The DUT's bootload pair | `PUT /bootload/ports` | Applied |

The bench-level cables count, and the live config's; no others.

## The live report

A panel opened after an explicit make-live, its head naming the bench and config and since when:

- **Applied** — each row's subject, Core route and text: *applied*, *failed* in Core's words, or *not sent* and why.
- **Proposed** — each enrolment with its chip and probe and a **Confirm** that sends it to `/api/enroll` as it is, says what Core answered — the role it moved included (61) — marks it *enrolled*, and declares the live bench again.
- **Not proposed** — each part or role, and why.
- **In Core, not on this bench** — each leftover with its own **Retract**, the list coming back from the answer.

Its buttons wait while a make-live, a write-through or a Stop is on its way, and act only while it is the live bench's report; otherwise its head says why not.

## Invariants

- **Only a make-live, a write-through, a Confirm and a Retract reach Core** (90). A config tab, Stop being live and an edit never do.
- **Every enrolment is proposed, never applied** (90, 44): a file is not evidence about what is plugged in.
- **Nothing is retracted without its own click** (91), and **only Make live takes the machine** (93).
- **Which bench is live is this UI's record, one per machine** (92), never the repo's.
- **Every skip is a row**, and so is a Core read that did not answer (90): never a silent skip or an empty list.
- **A refused write-through stays said** until a declare lands (93).
- **The report opens by itself only after an explicit make-live, where the human still is, and focuses the panel, never a button** (93).
- **A make-live row changing a role's board type or the link drops that role's verdict**, and so does a Confirm or a retracted role (93, 85).
- **A read of the record never cancels a write, and an answer after a project switch is dropped** (93).
