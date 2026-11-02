# embarch-ui decisions: Making a bench live

**Status:** active, 2026-11-02; 93 amended by 98 the same day.

A saved bench applied to Core from the Topology tab's canvas — phase 4 of the bench editor: what a bench declares and proposes, what it leaves for a human to retract, which bench is live, and when a save declares again. The old diagram it replaced, and what the canvas does in its place: [bench-canvas.md](bench-canvas.md) (94). The apply path it extends: [saved-benches.md](saved-benches.md) (44, 75). The file it reads: [bench-model.md](bench-model.md) (71, 72). Recording another config of the live bench, phase 5: [bench-configs.md](bench-configs.md) (98).

Index: [../decisions.md](../decisions.md). Current truth: [../spec/bench-live.md](../spec/bench-live.md).

### 90 — The drawing declares, every enrolment is proposed, and Make live is the page's one apply

**Making a bench live extends the apply and replaces it in the page** (owner, 2026-11-01). `POST /api/bench/benches/{slug}/live` reads the bench **as saved**, naming the `version` the browser last read (`409 version-changed` otherwise; the browser saves first), and applies what its parts declare. **A declaration applies at once and reports its own outcome; an enrolment comes back as a proposal**, because a file is not evidence about what is plugged in (44):

- a board type on a part holding a role → `PUT /probes/enrolled/{role}/board`, applied: it claims nothing about silicon (45);
- a probe on a role's part, its own or over an SWD lead → a proposal whose `name` is the role's **board type**, since `/api/enroll` writes `name` as the board (45) and the part's label would overwrite what the board write just set;
- a role-less part of category `board` that reaches a probe → a bench-board proposal named by its label, else its id (`embarch-topology` decision 41, `embarch-core` 83). A probe pod, an analyzer or an instrument with a probe bound is not a bench board;
- `vcom` on the dev-bench part → `POST /dev-bench/link`, decided on Core's row as it stands after the board write: deferred while the role holds no board, and not declared over another board's probe in that row;
- every `[[signals]]` entry, verbatim → `POST /signals`;
- an `scpi` binding → `PUT /instruments` (`embarch-topology` decision 49), one per part, named by its label or id; the port must name a VID and PID, which Core finds a port by, the line facts come from the template, and a baud it lacks is a row while missing terminators and interval default;
- the DUT's `bootload-bootloader`, with its `bootload-app` if bound → `PUT /bootload/ports`. An app binding alone is refused; a pair on another part is not declared.

**Only the bench-level cables and the live config's count**, so an SWD lead in another config is not the role's probe; with no config named, the bench-level cables alone — what 75 could not yet choose between.

**Never a silent skip** (75's rule, carried over). A template that will not load, a part whose template is missing and a binding on a connector that does not carry it are rows with route `(not sent)`, saying what happened; a Core record differing from the bench is a row against `GET /probes/enrolled`; a Core refusal — a lease the UI does not hold included — is one `ok: false` row in Core's words, the rest still applied; a Core read that fails is a row, never an empty list.

**The page no longer calls `/api/topology/profiles/{slug}/apply`** (coordinator decision): Saved benches' Open and the desk banner put the bench on the canvas and offer Make live. The route stays for API callers, and shares each role's step, the signal step and the link step with this one, its answer unchanged.

### 91 — Nothing is retracted silently: what Core holds and the bench does not name is listed, each with its own Retract

**Core's store is machine-wide, not this repo's** (owner, 2026-11-01), so making a bench live retracts nothing. The answer lists **leftovers**: signals and instruments the bench does not name, bench boards by probe serial, a role no part holds or whose probe in Core is none the role's part reaches, and a bootload pair when the bench declares none.

**What the bench names is read from its raw bindings**, never only from what its templates let it declare: any `scpi` key names an instrument, a `bootload-bootloader` key on the DUT names a pair, any role-less part with a probe names a bench board. A part whose template is missing declares nothing, and its Core record must not then turn into a leftover with a Retract beside it. For the same reason **a role's probe is offered as a leftover only when every cable from its part can be read** — a part at either end with a missing template, or a connector its template lacks, may be the SWD lead to the very probe Core holds.

**`POST /api/bench/live/retract` retracts one listed leftover**, recomputed when it is asked, through the matching Core delete; anything the list does not hold is `409 not-offered`. When Core did not answer the read for that kind, nothing is retracted and the answer is `ok: false` saying so, not a `409`: whether it is a leftover cannot be told. **A retracted role's row held the bench's board type too**, so it is written back, and dev-bench's link declared again, and the answer says so — never lost silently.

### 92 — Which bench is live is this UI's record, and one bench is live per machine

**The record is this UI's, never the repo's** (owner, 2026-11-01): a checkout shared between two machines would otherwise claim one machine's bench on the other. It is `live-benches.json` in the UI's per-user data directory, or beside the file `EMBARCH_UI_STATE` names, keyed by the repo's canonical path.

**One bench is live per machine: the last explicit make-live takes it** (owner, 2026-11-01). The record keeps each repo's last live bench and one machine-wide entry naming the repo live now. A repo another took over from reads `superseded`, naming who holds the machine, and **its saves write the file only** until an explicit make-live takes the machine back. `DELETE /api/bench/live` clears this repo's entry, and the machine's only when it points here; it touches nothing in Core.

**What the record names is said, never guessed**: the file gone (`missing`), its config gone (`config_missing`), the file not parsing (`unparseable`). An I/O error is a `500` with its reason everywhere, never a state of the file. **The record file is strict**: an older shape does not parse, and is never read as empty and overwritten. A make-live whose record could not be written says so in a row, and the page keeps its report as declared, not recorded.

**One make-live, retract or clear at a time**, a lock held across Core's answers with every check made after taking it, and `/api/enroll` waits on it too: a write-through checked and then overtaken by an explicit make-live would take the machine back, and a Confirm could land between a retract's check and its delete.

### 93 — A save of the live bench writes through, and only Make live takes the machine

**Write-through after an explicit Save of the live bench** (owner, 2026-11-01; Save is explicit, 80), so Core follows the file it was told. **Every call says which it is** (coordinator decision): `write_through` is required: `false` only from the buttons that make a bench live — Make live and Save and make live — which take the machine; `true` from every re-apply — after a Save, after a Confirm, and Declare again — which is refused while the bench is not this repo's live one (`not-live`), another repo holds the machine (`superseded`) or the live config is gone (`config-missing`). **A write-through names the record's config** (`config-differs` otherwise): changing config is recorded, never declared (98, amending this entry: it was an explicit make-live).

**A confirmed proposal re-applies the live bench** (coordinator decision): that declares the dev-bench link the deferred row waited on, with no second click. **Switching config tabs never calls Core** (owner): a tab is a view, the live config's tab is marked, and making another live is a button that records it (98).

**A refused write-through is said, and stays said.** The bar shows a re-apply's outcome as a button — `declared · 2 proposals · 1 failed` — opening its report, and a refusal as a lasting `saved, not declared` naming why, until a declare lands. **The report opens only after an explicit make-live, where the human still is, and focuses itself, never a button**: one Space must not confirm an enrolment nobody chose. Its buttons wait while a write is on its way and act only while it is the live bench's report; a read of the record never cancels a write, and an answer landing after a project switch is dropped.

**A make-live row that changes a role's board type or the link drops Validate's verdict for that role** — on a re-apply, only a row the last report did not already show — and so does a Confirm or a retracted role (45, 85): the verdict described the binding before it.
