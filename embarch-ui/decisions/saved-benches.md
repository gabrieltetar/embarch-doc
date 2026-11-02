# embarch-ui decisions: Retracting and saved benches

**Status:** active, 2026-09-20; 73–75 added 2026-11-01; 44 and 75 amended 2026-11-02.

Part of decision 44 — the counterpart enrolling never had, and a saved bench
that proposes rather than enrols. Split out of
[topology-boards.md](topology-boards.md) 2026-09-28 under
`DOC-COMPACTION.md`'s size cap; the role/name split and the validate pass stay
there. 73–75 are the bench editor's: the file grown parts, cables and
configs, the one writer every repo file goes through, and the apply path
reading either shape; its model is [bench-model.md](bench-model.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### Retracting: the counterpart enrolling never had

`DELETE /probes/enrolled/{role}` is new in Core, wrapped here as the `✕` on a role row. Until it existed, enrolling could *displace* a row but nothing could remove one, so a mis-enrolment — or a board under an invented role — stayed in `enrollment.toml` for good, short of hand-editing a file behind the NTFS permission wall on the real deployment. **It opens no probe**: a board that no longer answers is precisely the one a human is most likely to be clearing.

### A saved bench: portable, and loading never touches hardware

`embarch/topologies/<slug>.toml` holds which named board played which role, on which probe, plus dev-bench's link and every declared signal. **Loading splits by what each half claims.** The signals and the link are *declarations* — re-stating them changes a file on Core and asserts nothing about silicon — so they apply immediately, each reporting its own outcome. Each enrolment is an *identity claim*, bound after a live hardware-ID read, so it comes back as a **proposal** with a button, and confirming it runs the ordinary enroll.

*Rejected: applying the enrolments directly.* A file on disk is not evidence about what is plugged in, and a load that enrolled from one would be the stale-declared-state failure [`embarch-topology`](../../embarch-topology/spec.md) exists to prevent, rebuilt inside the UI. A proposal carries three facts and decides on none of them: whether the role already holds that probe, whether the probe is attached at all, and which board would be displaced.

**dev-bench's link is deferred rather than skipped.** Core amends it onto the dev-bench enrolment row, so it is refused while that role is empty — the state a fresh load is usually in. The apply report says so in words, and the link is declared with the enrolment when the proposal is confirmed; a silent skip would leave a bench half-loaded with nothing on screen about it.

**Amended 2026-11-02 (phase 4):** the page no longer loads a bench this way. Saved benches' Open puts it on the canvas, and Make live there keeps this split, its declarations applied and its enrolments proposed, while this route stays for API callers (90).

**A file name is derived from the name, never taken from it**: lowercase, every other run of characters collapsed to one hyphen, so `../../etc/passwd` slugs to `etc-passwd` and a saved bench cannot address anything outside `embarch/topologies/`.

### 73 — A saved bench gains parts, cables and configs, and today's files load as the BLE bench

**The bench editor's file is the saved bench, not a second store** (owner, 2026-11-01: benches in `embarch/topologies/`, several per repo): `<slug>.toml` gains `[[parts]]`, `[[cables]]` and `[[configs]]` — config slots are in the first version (owner) — and `[[signals]]` stays `SignalLink` verbatim. So the apply route, a desk's saved bench (57) and the Saved benches panel read the same files the canvas draws.

**The `parts` key marks the shape, and a save always writes it, even empty.** A file without it is *legacy*: its `dut` and `dev-bench` become parts laid out as the BLE dev bench — this machine as `host`, each board drawn as the built-in its west board names (`nrf54l15dk`, `nucleo_g0b1re`) or else the generic board, each cabled to the hub — and **it is rewritten only when it is saved**, never by being read. A file with parts writes no `dut`/`dev-bench`; the topology routes that still read them get them derived from the parts holding the roles.

**A `usb` binding has three spellings, because the identities differ.** A probe is its USB serial (`probe = "0671FF…"`); a VCOM on the same device as that connector's probe is an interface number (`vcom = 1`); a port of its own is a serial, or a table of `serial`, `interface`, `vid` and `pid` — `vid`/`pid` for a bridge with no serial (`embarch-topology` decision 49). **A part's map is written whole, as one inline table, and its keys must be connectors its template declares** (a slug, while the template is missing): a connector spliced into `usb.<connector>` by hand was not quoted correctly, and a key naming no connector names nothing a check can read.

**A legacy file's chip is kept with its board**, `chip = { board, chip }`, and used only while the part's board still equals that board: a chip outliving its board would enrol new silicon as the old. Even then it is a fallback (75).

**A bench loads tolerantly**, like a role row (44): an unknown key is ignored rather than refusing the file — which also means a save drops it ([../open/bench.md](../open/bench.md)). A part template is strict instead, because it is the vocabulary's to judge.

### 74 — One writer for every repo file: create and update are two routes, and nothing lands unread-back or outside the repo

**`POST` creates and `PUT` updates.** `POST` refuses `409` when anything is at the derived path, parseable or not, so a new bench never lands on an old one. `PUT` names the `version` its `GET` returned — an FNV-1a hash of the file's bytes and their length, a concurrency token rather than a security measure, stable across a restart — and is refused `409` when the file changed since or no longer parses, so two windows cannot silently overwrite each other. **A rename is refused** (`409`): a desk names a bench by its slug (57), and a study will name its configs through it. A path that is not a slug is `400`, never slugified into another bench's name. Part templates take the same two routes.

**Every write goes through one function, because a repo is someone else's checkout**: a link committed at `embarch/parts/x.toml` must not get a file outside it rewritten. The directory must resolve inside the resolved repo, checked before it is created; the bytes go to a temporary file opened `create_new`, which never follows a link; a replace renames it over the target, replacing a link rather than writing through it, and a create hard-links it into place, which fails on anything already there. **The text is parsed back and compared with what was meant before it replaces anything**: a serializer that wrote something unloadable would otherwise turn a good file into one unreadable from then on. A mismatch is `500`, the file untouched.

**The old Topology save and delete keep off the editor's files, under its lock.** `POST /api/topology/profiles` writes the old shape from the snapshot, which knows nothing of parts, cables or configs, so it and the delete refuse `409` on a file holding any of those keys **or one that does not parse** — it may be an editor bench with one typo. Both take the editor's write lock across their check and their write, and go through the same containment rule.

### 75 — Applying a bench looks the chip up once, follows an SWD lead, and proposes nothing it knows will fail

`POST /api/topology/profiles/{slug}/apply` reads either shape. **The chip is looked up once per role and used for both halves** — the board write and the enrolment proposal the browser confirms with it — as the role picker does (48, "looked up, never typed"): for `dev-bench` the supported pair's own chip first, then the catalog row's, then the scan's SoC through Core's `/resolve-chip`. The enrol and role-board routes take the same lookup when no chip is stated. A recorded chip is the fallback, under 73's rule. **A lookup that fails says which step failed** — the catalog unreadable, no row, no scan, no single SoC, Core refusing — because each has a different fix.

**A role whose probe is a separate pod is reached over its SWD lead**: a part binding no probe takes the probe of the part at the far end of an SWD cable, bench-level or in any config. **Leads that reach different probes in different configs are not guessed between** — which config is live is phase 4's record — and the row names each probe and where it was reached. Making a bench live reads the live config's leads alone (90).

**Never a silent skip, and never a proposal that can only fail.** A role with no probe, leads to two probes, or no chip to attach as gets a row saying why instead of a proposal. The dev-bench link's row is worded after the proposals are decided, so "declared with its enrolment" appears only when that enrolment is proposed; otherwise it says to enrol dev-bench and apply again.
