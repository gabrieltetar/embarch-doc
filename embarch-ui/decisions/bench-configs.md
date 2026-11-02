# embarch-ui decisions: Bench configs

**Status:** active, 2026-11-02.

Config slots on the Topology tab's canvas — phase 5 of the bench editor: adding, renaming and deleting a config, what a config may be called, and which config of the live bench is live. Where a new cable goes and config `A`: [bench-editing.md](bench-editing.md) (82). Making a bench live, which 98 amends: [bench-live.md](bench-live.md) (90–93). A host study's prompt naming a config: [operator-prompt.md](operator-prompt.md) (99). The cross-repo field: `embarch-study-designer` decision 88, `embarch-core` 107, `embarch-api` 100.

Index: [../decisions.md](../decisions.md). Current truth: [../spec/bench-editing.md](../spec/bench-editing.md), [../spec/bench-live.md](../spec/bench-live.md).

### 96 — A config is added, renamed and deleted on the canvas as a bench edit, and renaming or deleting one is never refused

**Config slots are edited on the canvas** (owner, 2026-11-01); until phase 5 a config was made only by a bench's first part-to-part cable (82). The config row under the canvas holds a tab per config, then **+ Config**, and **Rename** and **Delete** for the config on screen; it stays while a bench is on screen, with no tab when the bench has none. + Config asks for a name, offering the first single letter no config holds (then `config-<n>`), with an unchecked box to copy the cables of the config on screen; Rename asks for the new name; Delete takes the config and its cables at once, undo bringing them back. **Each is an edit like any other** (80): undone and redone, held in the page, written by Save, never Core. The dialog judges a name by the served rule (97) and against the bench's other configs, and says why in the server's sentence.

**Renaming or deleting a config is never refused** (owner, 2026-11-01, replacing a `409` that would have had to scan for every study naming the config, when host studies are not saved in a repo at all). A study names a config by name, resolved when it needs one: a prompt naming a config the live bench lacks says so and offers a pick (99). The Rename dialog says so — a host study naming the old name is asked about when it runs — or, for the live config, that the live record follows the new name once saved.

**Each config on screen carries an id of the page's own**, given when the file is read or the config added and kept through renames, undo and redo, so a save tells a rename from a delete and an add — an added config renamed, a rename undone — by id. That is what lets the live record follow a rename (98). *Rejected:* matching by name, where a rename reads as a delete and an add, and by position, which a delete shifts.

### 97 — A config name is one a host study can write, judged by study-designer's own check

A `Prompt` names a config by exact name (`embarch-study-designer` decision 88), so **a config holds only names a study can write** (coordinator decision): not blank, at most `MAX_HOST_NAME_LEN` (96) bytes of UTF-8, no control character, no U+2028/U+2029 or bidi format character, no whitespace at either end. **The judge is study-designer's own validation** of a one-step study naming it, never a copy of the rule, so a change there moves the UI with it. It extends 72's "ambiguous to address": a name no study can write cannot be addressed by one.

- **A save refuses it** (`400`) in a sentence ending in the rule, and **a check reports it** as the error `config-name-refused`, the same sentence plus "Rename it to save the bench", so a hand-edited name shows before Save is pressed.
- **The vocabulary serves it** as `config_name {max_bytes, refused, refused_at_ends, rule}`: the byte cap, the code-point runs refused anywhere and those refused only at the ends, and the sentence, so the dialog restates nothing (88's rule). study-designer's predicate is private, so the runs are **a mirror**, held to the real check by a test over every Unicode scalar value — inside a name, first, last and alone — so a character study-designer starts or stops refusing fails `cargo test` instead of the dialog accepting a name the save then refuses.

*Rejected:* a looser rule here with the refusal left to the study, which would leave a config no study could ever name.

### 98 — Another config of the live bench is made live by recording it, and Core is told nothing

**Amends 93**, where *Make config live* was an explicit make-live (coordinator decision, following the owner's "configs only change part-to-part cables, so switching config never calls Core", 2026-11-01). **A config declares nothing a make-live applies**: board types, the dev-bench link, signals, instruments and the bootload pair come from the parts and the bench-level cables (90). It does change which probe a role's part reaches over an SWD lead, so **its enrolment proposals and role leftovers appear at the next Declare again**, and the bar's notice says so.

**`POST /api/bench/live/config {config, slug, renamed_from?}` changes only the live record's config**, under `bench_live_lock` with every check made after taking it (92). `config` and `slug` are required (`400`); `409` names `not-live` (no record, its file gone, or `slug` another bench), `superseded`, `unparseable` or `config-missing` (the bench as saved lacks it). **`since` moves only when the wiring changes** — not for the config already live, nor for a rename: `renamed_from` keeps it when the record names that old name and the bench no longer has it.

- **Make *config* live** on this repo's live bench while it holds the machine — another config's tab, or any while the live config is gone — records it. With edits on screen it saves first, records, then declares the save, as every save of the live bench is (93).
- **A save that renamed the live config** (96's id) records the new name with `renamed_from` before it writes through; one that deleted it leaves the record `config_missing` and says *saved, not declared*, Make *config* live the way out.
- **The operator prompt** marks the config a study asked for once it is answered (99).

Make live on a bench that is not live, or is superseded, is still the explicit make-live that takes the machine (93). *Rejected:* keeping 93's form, which re-declared every row to change one name, and asked Core to write what had not changed.
