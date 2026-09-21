# embarch-ui decisions: Boards, roles, saved benches and the validate pass

**Status:** active, 2026-09-20.

Why a role stopped being a board's name, and the surfaces that followed: the project catalog, the validate pass, retracting, saved benches. **Decision 45 corrected two things about the model this entry set up** and is in [topology-roles.md](topology-roles.md): a probe is not an attribute of a board, and a board is a *type* rather than a unit of hardware. The tab's other half — signal routing (10) and enrolling by dropping a probe on the diagram (43) — is in [topology-tab.md](topology-tab.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 44 — A role is a slot, a board is a name, and the alert list becomes a validate pass

**The defect was a word.** `EnrolledBoard.role` was a free string, and the only place to put a board's *name* was that string — so a bench with a third board acquired a third role, `client-nucleo`. Every surface that asked "which board is the DUT" then had to answer from a list in which a role, a name and a typo are the same kind of thing. `dut` rendered beside it read as one more name someone chose, which is exactly backwards: **there are two roles, they are fixed, and every board that is not in one of them is still a board.**

So the two facts split, each to the owner that can actually answer it:

- **A role** is one of `dut` and `dev-bench`, and Core's `POST /probes/enroll` answers `400` to anything else ([`embarch-core` decision 75](../../embarch-core/decisions.md)). **Closed on the write path, tolerant on the load path**: nothing re-checks a row already in `enrollment.toml`, because a store predating a later fact must keep loading — which is also what keeps the pre-existing `client-nucleo` row visible instead of silently dropped.
- **A board's name** is a new `name` field on the enrolment, opaque to Core and to `embarch-topology` ([its decision 35](../../embarch-topology/decisions/enrollment.md)) — recorded, never interpreted.
- **What a board *is*** — its chip, what it builds as, a note — lives in the **open firmware repo**, at `embarch/boards.toml`, beside `embarch/studies/`. *Rejected: a machine-wide catalog in Core's data directory.* A board is a thing a project's engineers talk about, and putting it beside the studies that ran on it is what makes a second engineer's checkout describe the same bench. The cost is re-adding a dev bench per project, which is one row.

**A catalog entry carries no probe serial, and that is the load-bearing half.** One probe is moved between three boards over a week, so a probe serial is a fact about *the current wiring* — the enrolment's business, and the saved bench's. What stays with the board is what stays true while it sits in a drawer.

**A name that does not resolve renders as unresolved, never as absent.** A board enrolled under one project and read under another shows its name plus *not in catalog*: the board is on the bench either way, and a renderer that dropped the name would be answering a question about the catalog with a claim about the hardware. Same rule as an unreadable signal list (decision 10).

### The alert list is replaced by Validate topology, not moved

**The alert card answered a question nobody was asking at the moment they looked at it** — "did a mismatch happen at some point" — and it was structurally silent about half of what this tab declares: [`embarch-topology`](../../embarch-topology/spec.md) never writes a *signal* mismatch to that log, because an alert's shape is board-specific and a wire has none of those fields. The button answers "is the bench in front of me what this tab says it is", now, and names each check.

**Three kinds of check, and the difference between them is what each can honestly assert.** A role re-reads the enrolled board's live hardware ID over the probe (Core's `POST /validate`) — the only one that touches hardware. The dev-bench link resolves the port live, and **a guessed port is a warning, never a pass**: the lowest-interface fallback is wrong on a two-VCOM probe, which is the failure `link_port_interface` exists for ([`embarch-topology` decision 20](../../embarch-topology/decisions.md)), and a report that called it a pass would hide exactly the state it was written to surface. A signal route is checked only as far as it was declared — a `direct` route's serial must still be enumerable, a `via-dev-bench` one rides the bench link — and **every one of those lines says what it cannot confirm**, because no software can see a cable between two headers.

**Core's own words are printed, never paraphrased.** A mismatch reason, a `fix_it_url`, a refusal: this UI did not diagnose the failure and a second, worse description of it helps nobody. The Dashboard keeps its alert cards; Core keeps the durable log and the MCP tool over it. What went is the card that stood where a live check belonged.

### Retracting: the counterpart enrolling never had

`DELETE /probes/enrolled/{role}` is new in Core, wrapped here as the `✕` on a role row. Until it existed, enrolling could *displace* a row but nothing could remove one, so a mis-enrolment — or a board under an invented role — stayed in `enrollment.toml` for good, short of hand-editing a file behind the NTFS permission wall on the real deployment. **It opens no probe**: a board that no longer answers is precisely the one a human is most likely to be clearing.

### A saved bench: portable, and loading never touches hardware

`embarch/topologies/<slug>.toml` holds which named board played which role, on which probe, plus dev-bench's link and every declared signal. **Loading splits by what each half claims.** The signals and the link are *declarations* — re-stating them changes a file on Core and asserts nothing about silicon — so they apply immediately, each reporting its own outcome. Each enrolment is an *identity claim*, bound after a live hardware-ID read, so it comes back as a **proposal** with a button, and confirming it runs the ordinary enroll.

*Rejected: applying the enrolments directly.* A file on disk is not evidence about what is plugged in, and a load that enrolled from one would be the stale-declared-state failure [`embarch-topology`](../../embarch-topology/spec.md) exists to prevent, rebuilt inside the UI. A proposal carries three facts and decides on none of them: whether the role already holds that probe, whether the probe is attached at all, and which board would be displaced.

**dev-bench's link is deferred rather than skipped.** Core amends it onto the dev-bench enrolment row, so it is refused while that role is empty — the state a fresh load is usually in. The apply report says so in words, and the link is declared with the enrolment when the proposal is confirmed; a silent skip would leave a bench half-loaded with nothing on screen about it.

**A file name is derived from the name, never taken from it**: lowercase, every other run of characters collapsed to one hyphen, so `../../etc/passwd` slugs to `etc-passwd` and a saved bench cannot address anything outside `embarch/topologies/`.

### The one link between a board and a build

A catalog entry carries the **west** board target it builds as — a different thing from the physical board the entry is, which is why the field is `build_target` and not `board`. The Build card *offers* it, as a button naming the DUT's own target, and applies it only when pressed and only when the scan actually found that target. *Rejected: filling the Build card from the DUT automatically.* Which target a study builds is the study's own field; a bench rewired this morning must not re-target a study saved last week.

**Driven in a real browser**: `tests/browser/drive_topology.py` grew from eighteen checks to forty — the roles table and its labels, a foreign role flagged and cleared, the box titled by role with the board underneath, a passing role beside a failing one with Core's reason printed verbatim, a guessed port as a warning, a board added to the catalog and offered in the enroll dialog, a bench saved to the project and loaded back, and a proposal confirmed into a real enrolment.

### 47 — A board type's row is its build menu, and a DUT is picked as a real combination

The catalog list carried **Chip** and **Builds as**. Both are true and neither is what a human reads a bench list for: a chip is set once and never looked at again, and the west target mostly restates the row's own name. **What is worth a column is what this repo can actually build that board as** — which is also the menu the DUT is picked from, so the list and the picker became two views of one scan instead of two descriptions of one row.

So the row is now the board type, its **revisions**, its **variants**, and the **apps** it is in the tree for, each as a chip. Chip and west target did not leave the model — they are on the row's tooltip and in its Edit dialog, where a value you set once belongs.

**Four states, said four different ways**, because they are four different facts: the repo could not be scanned at all (with the reason on the tooltip), this board type is not in the scan, it is in the scan and declares none of that axis, or here they are. Folding any pair together would state something about the bench nobody established — the same split the catalog is already under for an unreadable file (44) and the signal list for an unreadable route (10).

**The pinned combination is marked, and a stale pin is marked differently.** `embarch/boards.toml` records which revision and variant a build for this board uses; that chip renders in the accent, and a pin the scan no longer backs renders in the warning colour with a `?` rather than being dropped. It is what a run for that role would ask for and it is about to be refused — a list that hid it would be silent about exactly the row that is going to fail.

**The DUT picker binds to a combination, not to two dropdowns.** Under the board type is one select of the combinations the repo's own scan reports, each naming its revision and variant and carrying the west qualifier it assembles to. *Rejected: a revision list and a variant list side by side.* Zephyr backs a `(variant, revision)` pair only where a real file backs it — a named variant does not inherit the default-revision shortcut — so a cross product offers targets `west build` then refuses. The browser test's fixture is exactly that case: two revisions and one named variant is four pairs and **three** real combinations.

**One gesture, two owners, and the order is fixed.** Confirming the picker writes the board type to Core (`PUT /probes/enrolled/{role}/board`) and *then* the combination to `embarch/boards.toml`. Which board type is in a role is Core's fact; which combination of it this repo builds is the project's, and **Core is never told about a revision**. Writing the file first would leave a catalog pinned for a role Core then refused. A board type outside the catalog — a dev-bench type, a name from another project — pins nothing and says nothing: both are states already rendered honestly elsewhere, and neither is a reason to fail a write to Core that has already happened.

**A dev-bench board is offered no combination at all**, for the reason decision 45 already gives: a bench is a piece of the suite, not a project's board, so it has no catalog row to pin one on.

### A dev-bench board type is shown by its label, never by its qualifier

The suite's supported bench list has always carried a human label beside the west qualifier, and only the picker used it — so the diagram box, the Dashboard's table and every validate line read `esp32c5_devkitc/esp32c5/hpcore`. **That is a path, and the picture is asking which board is on the desk.** The label is what is rendered now (the qualifier stays on the tooltip, and stays the value everywhere it is *sent*), and the two labels were rewritten to name the products: *Nordic nRF54L15 DK* and *Espressif ESP32-C5-DevKitC*. A bench type the list does not carry renders unchanged — an unknown bench board is still the bench's board.
