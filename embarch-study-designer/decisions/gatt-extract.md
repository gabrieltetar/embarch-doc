# embarch-study-designer decisions: GATT extraction and naming

**Status:** active, 2026-09-02.

Reading a firmware repo for its own GATT table, and giving a characteristic a name.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 33 — A GATT-config extraction tool ships here: a generic trait, one narrow implementation

Distinct from live discovery, which answers the same question over BLE against whatever is running. **The firmware repo is usually already checked out, and its GATT table is source, not a runtime mystery** — extracting it statically authors a step with real UUIDs before dev-bench connects, and gives a second source to diff against a live result, catching a service compiled out of a build.

The trait's output **reuses live discovery's types, so static and live results compare without translation.** One implementation ships, scoped to one firmware's actual conventions — confirmed against real source, not a generic Zephyr layout. `std`-only, behind its own feature, **never linked by dev-bench or Core.** Generic at the trait boundary, narrow at the implementation: a second firmware's extractor is a new impl, not a redesign.

**Byte-for-byte comparability is weaker than claimed** — see 57: services return in a stable but *non-handle* order, so **compare them as sets.**

### 56 — A characteristic gets a name: the vendor's, or the C identifier the firmware declared it under

Raised one decision after a study gained something to name characteristics *for*: **"the option show up as numbers."** They did — every picker labelled its options with the head of a 128-bit UUID, the only thing this crate could tell a UI. On the real DUT that means choosing between eight values **differing in one hex digit and ordered by service definition, not by anything a human is thinking in.**

**A UUID is the correct identity and a poor label.** Identity is unchanged: still what a checkbox carries, what crosses the wire, what tooltips show.

**Two name sources, neither a guess:** the vendor table's own published name, or **the declaring C identifier — already resolved to build the table, and dropped on the floor.** Keeping it covers everything custom, **nearly everything on a real DUT — named without asking its engineers anything, because they already wrote the names down.** Vendor wins where both apply: source is one repo's spelling of a thing the vendor has already named.

**A label, never semantics** — the same line the vendor table and the registry both hold. An identifier says what the firmware's authors *call* a characteristic; **it says nothing about what its bytes mean, when it notifies, or what writing to it does.** So the shortening is mechanical and reversible: trim the suffix naming a *variable* rather than a characteristic, and nothing else. No title-casing, no underscore substitution, and **no expanding an abbreviation into words — every one of those is this crate deciding what a firmware team's shorthand stands for, being wrong occasionally, and being trusted anyway.** The name carries its source and the untrimmed original, so a UI renders provenance rather than presenting a vendor name and a local variable's spelling identically.

**A name is optional and its absence is ordinary** — a live-only characteristic on a repo with no extractor shows the UUID head as before. Nothing fails, and nothing is invented to fill the gap.

**Services get names the same way**, their identifier thrown away for the same reason and length of time. Two maps rather than one, because a merged map would have to guess which lookup a UUID wanted.

*Rejected: a `name` field on the characteristic type.* That type is the wire-comparable shape **a live discovery fills in from an ATT response, and an ATT response carries no names.** A source-only field would be **one hardware can never populate**, breaking the comparability decision 33 exists to provide. So names ride *beside* the table, from one text scan — **an extractor asked for the table and then for the names would read and re-parse the same files twice to answer one request.**

### 57 — The extraction scans the repo, not two files it was told about

Raised as a question rather than a bug report: *"maybe the gatt discovery check can be project wide?"* **It could, and it had to.** The extractor hardcoded two paths and the DUT repo has **a third service-definition block.** Everything needed was already parseable in files it could read — **the UUID macros are in the very header it opens — it was simply never handed the file. A third of this DUT's GATT table had been missing for as long as the extractor had existed, and nothing anywhere could have said so.**

**That is worse than the missing service**, because the module's own doc comment opened by claiming it *"fails loudly rather than silently under-extracting"*. **A bounded read of two named files cannot fail loudly about a third, because it has no idea the file exists. The loudness was real for everything inside its scope and vacuous about its scope.**

**Scope is now the firmware repo's own ignore files, not a list this crate maintains** — every C source and header under the root, honouring ignore files, skipping hidden directories, **and honouring them with no `.git`, because widening the scan whenever pointed at a tarball would be the same silent failure in a different costume.**

**A naive glob is not the alternative it looks like:** on this repo it finds the service macro **twice as many times as there are services**, a worktrees directory holding two extra copies — **and that fits under the cap with room to spare, so it would have emitted duplicated services without a word:** the same silent wrongness, inverted from under- to over-extraction.

**One hard block on top: any directory named `embarch`, at any depth, whatever the ignore files say** — gitignored only because this suite put it there, so it cannot depend on the firmware repo having remembered. Never the walk root itself: pointing the extractor there is deliberate, not the accident the block is for. What it pruned is reported, **because a hard block is exactly the rule that stays invisible until it excludes something it should not.**

**The loudness moves to the point of use.** Under a two-file read every declaration scanned was in use, so raising on an unresolvable one was free. Under a wide walk it is not: **a malformed macro in some third-party corner nothing references must not be able to blank the whole table.** So an unresolvable symbol is *recorded as* unresolvable and raises only if a service block actually reaches for it. **Failing loudly about things that affect the answer is the property worth keeping; failing loudly about everything a wide walk happens to see is how a defensive posture turns into a broken tool.**

**Three failure modes a wide walk creates, all named rather than absorbed:** two blocks resolving to one service UUID; one name carrying two values in two files, **reported rather than resolved by whichever file the walk read last**; and **a walk that finds no C at all, which would otherwise return an empty table — a plausible-looking answer to a question nobody asked.** C statics are file-scoped, so **two files declaring the same static name is ordinary C and must not cross-resolve.**

**The scan reports what it scanned** — files read, which contributed what, what the block pruned, what was not valid UTF-8. **This kills the failure mode rather than patching this instance of it:** a bounded read cannot report that it is incomplete, and a walk that reports nothing is one commit away from being incomplete again.

Order is **stable but not a claim about ATT handle order**, which the linker decides across files — a build fact this scanner cannot read out of source and does not guess. The text scan still **does not evaluate preprocessor conditionals**, so a config-gated characteristic is reported unconditionally.

*Rejected: a configured file or glob list per project* — explicit and auditable, but **silently incomplete in exactly the way the two-file read was, the moment someone adds a file.** *Rejected for now: an exclude knob* — the escape hatch if a *tracked* vendored copy trips the duplicate error, and that error names the two files, a better time to design it than in advance. *Rejected: shelling out to `git ls-files`* — same file set, no new dependency, but **needs the git binary and a real checkout, and an extractor returning nothing against an export is the silent failure again.**

Validated: three services where a bounded read found two, every characteristic named.

### 78 — A properties macro defined twice under a `#if` resolves to the union of its branches, named in the report

Found by running the extractor against the reference DUT, which returned **nothing at all**: `unrecognized characteristic-properties token: WDS_CHRC_TX_PROP`. That macro is `BT_GATT_CHRC_INDICATE` under `CONFIG_WDS_CONFIRMED_TX` and `BT_GATT_CHRC_NOTIFY` without it, and decision 57's scan **does not evaluate preprocessor conditionals** — one `#define` in one service took **four services and nineteen characteristics** down with it. [embarch-ui](../../embarch-ui/decisions/designer-panels.md) decision 41 recorded it as "a real extractor limitation"; its decision 51, removing the extractor's off switch, made it load-bearing — a blanked table is now **every picker back to hex UUIDs.**

**Properties tokens now resolve through `#define`s**, the using file's first and the whole repo's second — **the same local-then-repo-wide order, and reason, as the UUID variables.** **Two definitions of one name are unioned, not picked.** Which branch a build compiled **is not a fact in the source** — the same class of build fact as the linker's handle order that 57 refuses to guess. Three candidate answers: pick one, *a guess indistinguishable from an answer*; fail, *what it was already doing, and the characteristic exists in every build*; or read it as **"the source declares this characteristic as one of these"**, the only one of the three that is true.

**The union is only defensible because it is visible**, which is the actual decision here. `notify | indicate` is a properties byte **no build compiles**, so `ScanReport` grew `conditional_properties` — the alias, its branches, what was used — and the panel says it in words. Recorded **at the point of use**: a repo-wide walk reads plenty of conditional macros nothing reaches for, and listing those is the defensive posture 57 warns turns a scanner into a broken tool.

**The loud failure is untouched.** A token that is neither a `BT_GATT_CHRC_*` macro nor an alias resolving to one is still `UnparseableProperties`, and a half-read expression is refused rather than contributing the bits it recognized. Alias chains follow to a bounded depth, not a fixpoint.

Validated: four services, nineteen characteristics, every one named, where the extraction had been returning an error.

