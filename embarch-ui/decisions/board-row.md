# embarch-ui decisions: What a board row states, and what it stops stating

**Status:** active, 2026-09-20.

Two corrections to the catalog row decisions 44 and 47 built ([topology-boards.md](topology-boards.md)), split out when that group reached its size cap: the chip a row does not state is *derived* rather than asked for, and the app list it did state is gone from both surfaces that carried it.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 48 — A chip is looked up, not typed: the SoC the scan reports resolves it

`Rescan` seeds a catalog row with an empty `chip`, on the stated grounds that the scan knows west targets and not probe-rs ones. **Half of that is wrong, and it cost the tab its main gesture.** The scan reports each target's *SoC* (`nrf54l15`), and SoC → probe-rs target is a table that already exists, compiled into Core, checked against probe-rs's own registry and reachable at `POST /resolve-chip` ([`embarch-core` decision 8](../../embarch-core/decisions.md)) — the same lookup a build for that target does on its way to `/flash`. So every row a rescan seeded held an unanswerable question whose answer was one HTTP call away, and setting the board in a role came back as `502 embarch-core returned 400 Bad Request: a role's board needs both a board type and the chip it attaches as` — a message naming the field that was missing and not the one thing a human could do about it.

**The chip is therefore derived where the row states none**, in `GET /api/topology/pickers`, once per distinct SoC. Both dialogs that attach a role to silicon read their chip out of that one list — the board-type picker and the enrol dialog's read-only chip field — so a row with no chip used to make one of them refuse in the browser and the other fail at Core, for the same reason, from two different messages.

Three rules keep it a lookup rather than a guess:

- **A stated chip always wins.** A row that names one is never asked about, so a hand-corrected spelling cannot be overwritten by a derived one, and the field stays what decision 44 made it: what a board *is*, in the project's own file. Nothing writes a derived chip back — it is a function of the scan and probe-rs's registry, and a copy in `boards.toml` is a copy that goes stale when either moves.
- **Two SoCs under one board type abstain**, and so does a Core that cannot answer. A board whose combinations disagree about its silicon is exactly where picking the first would attach to the wrong target.
- **What survives that is refused here, not relayed.** `POST /api/topology/roles/{role}/board` derives a chip the request did not carry and answers its own `400` naming the board and the row to set it on, rather than proxying Core's field-level refusal. Core's requirement is unchanged and right: it is what every later attach on that role opens as.

### 49 — A board type's apps are not a column, and a combination stops at its variant

The catalog row carried an **Apps** column and every line of the DUT's combination picker ended in the same list — `rev 1 · no variant — plank@1/nrf54l15/cpuapp  (blinky, test-basic, test-ble)`. Decision 47 put both there as part of "the row is its build menu". **Neither earns its place.** Which apps a board type appears in is a fact about the tree, not about the bench a human is reading the list to identify, and it is repeated identically on every line of a picker that chooses between revisions and variants. **The app is a study's parameter, not a board's** — it is the one build axis decision 45 left with the study, precisely because board, variant and revision follow the bench while the app is what the study is *of* — and the Build card picks it from the same scan, which this change does not touch.

So the row is the board type, its revisions, its variants and its notes; a combination reads `rev 2 · variant ns` and stops. **The west qualifier moves to the option's tooltip** rather than leaving — it is the honest spelling and it is worth one hover, but a list of `plank@1/nrf54l15/cpuapp` differing from its neighbour in one character is the string the picker exists to spare a human, which decision 47 said while printing it anyway. The scan still groups by combination, so two apps sharing one target are still one entry; what is no longer kept is which apps those were.
