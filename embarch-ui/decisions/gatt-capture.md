# embarch-ui decisions: Authoring GATT capture

**Status:** active, 2026-09-02.

Per-characteristic taps, characteristic names, and the target picker. The rest of the Study Designer tab is in [study-designer.md](study-designer.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 15 — GATT capture is authored here: a per-characteristic tap, a decoder from the firmware repo, and a transcript nobody has to remember

The UI half of [embarch-study-designer](../../embarch-study-designer/decisions/gatt.md) decisions 52–55, raised by the repo owner authoring a real study here and finding monitor-everything was the only monitor available.

Three surfaces. A **selective monitor row** renders a checkbox per notify/indicate-capable characteristic — never a free-text UUID list, since the point is picking from what discovery actually found, and **the service UUID comes from the same entry the checkbox was rendered from, so a row's two UUIDs cannot disagree.** A **GATT notify tap** gives one characteristic its own file, its decoder dropdown populated from the firmware repo's own struct declarations, with raw bytes selectable and the honest default. And **taps became a tagged union** rather than one struct with optional fields — "no signal" and "no characteristic" are **different authoring mistakes with different fixes**, and an untagged shape makes them the same one.

**The transcript tap is auto-declared, not a checkbox, and that is the decision worth arguing.** Any study with a monitor step gets an uncapped transcript tap whether or not the author asked. Before this pass **this tab authored no GATT tap at all**, so a monitor step's capture existed only as the first 32 records of a field that is now retired. **A checkbox would make "monitor everything and record none of it" reachable by leaving a box unticked** — not a configuration anyone wants, and precisely the silently-empty capture this suite keeps rediscovering. An author who declares their own transcript tap keeps it; the auto tap is skipped rather than duplicated.

**A tap whose characteristic no step subscribes to is refused here, before submit.** It would otherwise **capture nothing, pass, and look fine.** This tab is the only place holding both the resolved steps and the taps, so it is the only place that can catch it: Core sees a tap list that is internally valid, and dev-bench sees a tap it will faithfully route zero notifications to. Checked against the *resolved* actions rather than the raw rows, because **whether something is subscribed is a property of what a row became.**

### 16 — Every characteristic picker shows a name; the UUID moves to the tooltip

The human half of [embarch-study-designer](../../embarch-study-designer/decisions/gatt-extract.md) decision 56, raised by the repo owner immediately after 15 shipped the pickers: "the option show up as numbers." They did — `00000002`, `00000003`, `00000004` — and **on this DUT the choice was between eighteen characteristics differing in one hex digit.**

**One name map for the whole response, not a `name` field on the subscribable list.** Four places in the browser render a characteristic, and **three of them read from the actions response, not from the subscribable list** — so a field on one list would have named the options in one picker and left the same characteristic a bare UUID in the next, **which is worse than uniformly showing UUIDs.** It covers every characteristic any source found rather than only the notify-capable ones: a name is a name regardless of what a study can do with it.

**The UUID never stops being the identity** — it is what a checkbox's value carries, what the collector sends, and what every tooltip shows alongside **the label's provenance**: "the vendor publishes this name" reads differently from "your own source spells it this way", and an engineer has to be able to tell them apart. A characteristic nothing names falls back to the UUID head.

**A tap's default file name is the characteristic's name**, sliced to the stream-name limit **here, where it was chosen**, rather than refused at submit.

**One CSS fix that is a real bug, not a polish pass.** A parameter caption's style uppercases its span, and a selective-monitor checkbox borrows that layout — so the name rendered as `SDS_HRM_RRM`. Invisible while that span held hex digits; **wrong the moment it holds a C identifier**, because an identifier's case is part of it and the firmware source does not spell it that way. A separate value class opts out.

### 17 — The selective-monitor target list becomes a dialog, grouped by named service

Raised one decision after 16 on the same row: "instead of having all options with check box can we have a drop down menu with checkbox? Or something better." Decision 15's **inline checkbox per characteristic** was eleven on this DUT, thirteen once the repo-wide scan found a third service — **one row taller than the rest of the table put together, and it could only grow.**

**A dialog, not a dropdown and not an inline disclosure**, and the app's own history picked between the three:

- **Rejected outright: `<select multiple>`.** No visible checkboxes, ctrl-click discovery, and it renders as a text field where every other multi-select here is explicit. **A native control that looks like a text box is not "something better".**
- **Rejected: a floating popover in the cell.** The step table lives inside a horizontal-scroll wrapper, so **an absolutely-positioned panel in a cell is clipped by the table's own scroll container**; escaping it means fixed positioning plus scroll-tracking plus outside-click handling — a lot of machinery for a zero-build vanilla app (decision 2).
- **Rejected: an inline `<details>`.** The obvious first answer, losing on two counts: there is **no `<details>` anywhere in this app**, so it is a new pattern to be consistent about, while the dialog pattern is one **four** existing places already use. And expanding inline still makes the row tall, just on demand. It also collides with how this table works — **the step table re-renders its HTML on every change, so a `<details>` would snap shut on each click** unless its open state were tracked in the row model, machinery a dialog does not need because its state lives outside the table.

**What the cell holds instead: one line** — `2 of 13`, the first two picks as chips, `+N more`, and a `Choose…` button. **Nothing new was drawn for it**: both the chip and the modal are existing patterns.

**Grouped by service, with per-group all/none** — which is what made the service-naming work worth doing in the same pass, since the headings read `bds_service` rather than `00000020`. **Groups keep discovery's own order rather than sorting**: that order is the DUT's, and a picker that reorders it stops matching what Discover GATT printed. A filter matches label, origin identifier, characteristic UUID and service alike.

**Decision 15's two invariants are untouched, and that is the point of the shape.** Options come from discovery and nowhere else — still deliberately no free-text UUID box, because **a step naming a characteristic nothing has seen is a run that fails on the bench.** A pick's *service* UUID is still read back from the same discovery entry at submit. And an empty selection is still **refused rather than promoted to "everything"**, in the cell, in the dialog, and in the collector.

**The cap becomes visible, having been enforced only server-side.** The limit is now *served* rather than restated in `app.js`, because **a browser-side copy of a limit is a number that drifts silently the day the limit moves.** The dialog shows `n of N · max 16`, disables unchecked boxes at the cap — **rendered, not hidden, since hiding one would look like discovery had lost it** — disables the per-group `all` rather than offering a control that would add nothing, and says what to do instead.

**Two silent losses found and fixed while in here, neither cosmetic.** A saved study's monitor targets **did not survive being reopened**: the loader read a built-in row's action fields and stopped, so targets came back empty and the security level reset to default, both without a word, **even though the row type round-trips them perfectly well.** And a picked characteristic the current discovery no longer knows about **was dropped in silence** — the correct behaviour, since there is no service UUID to pair it with, done invisibly. It is now named in the cell and the dialog.

**The list is patched on a toggle, not rebuilt — found by deploying it, not by review.** Re-rendering the list's HTML on every change **destroys the node that was just clicked**, so focus falls back to `<body>` and **a keyboard user pressing Space is returned to the top of the tab order.** Measured against the deployed binary, before and after, for single toggles and for bulk all/none. Scroll position happened to survive because the rebuilt content had identical height — **luck, not design.** So the list is built on open and on a filter change, and a separate sync patches checked/disabled/counter in place. Worth recording because **the inline list this replaces had the same flaw and worse** — it re-rendered the entire step table on every tick — so this is a defect that was inherited invisibly rather than introduced.

**Validated against the deployed binary itself**, driving the real page with real clicks rather than a harness, because the assets are compiled in and **the deployed artifact is the only thing that can be checked.** Two sequential clicks landing at all is itself the check that the patch-in-place fix works: against the rebuild-on-toggle version the second click hit a detached node and the count went to 1 instead of 2. The cap path was exercised by **lowering the served cap to 3**, since this DUT has fewer characteristics than the real limit.
