# embarch-study-designer decisions: GATT extraction and naming

**Status:** active, 2026-09-02.

Reading a firmware repo for its own GATT table, and giving a characteristic a name.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 33 — A GATT-config extraction tool ships here: a generic trait, one narrow implementation

Distinct from live discovery, which answers the same question over BLE against whatever is running. **A study author usually has the firmware repo checked out already, and its GATT table is *source*, not a runtime mystery** — so extracting it statically lets a step be authored with real UUIDs before dev-bench connects to anything, and **gives a second independent source to diff against a live result**, catching a service compiled out of a specific build.

The trait's output **reuses the same types a live discovery fills in, so static and live results are comparable without a translation step.** One implementation ships, scoped narrowly to one firmware's actual conventions — **confirmed against real source rather than guessed against a generic Zephyr layout.** It is a `std`-only authoring-time tool behind its own feature, **never something dev-bench or Core links.** Deliberately **generic at the trait boundary and narrow at the implementation**: a second firmware's extractor is a new impl, not a redesign.

**Byte-for-byte comparability is weaker than this decision claimed** — see 57: services come back in a stable but *non-handle* order, so **compare them as sets.**

### 56 — A characteristic gets a name: the vendor's, or the C identifier the firmware declared it under

Raised one decision after a study gained something to name characteristics *for*: **"the option show up as numbers."** They did — every picker labelled its options with the head of a 128-bit UUID, **because that was the only thing this crate could tell a UI.** On the real DUT that means choosing between eight values **differing in one hex digit and ordered by service definition, not by anything a human is thinking in.**

**A UUID is the correct identity and a poor label.** Nothing about identity changes: it is still what a checkbox carries, what crosses the wire, and what every tooltip shows.

**Two name sources, neither a guess:** the vendor table's own published name, or **the declaring C identifier the extractor always had in hand — it resolves the symbol to 16 bytes to build the table at all — and dropped on the floor.** Keeping it covers everything custom, **which on a real DUT is nearly everything — named without asking its engineers for anything, because they already wrote the names down.** Vendor wins where both apply: **source is one repo's spelling of a thing the vendor has already named.**

**A label, never semantics** — the same line the vendor table and the registry both hold, **and the one this decision could most easily have crossed.** An identifier says what the firmware's authors *call* a characteristic; **it says nothing about what its bytes mean, when it notifies, or what writing to it does.** So the shortening is mechanical and reversible: trim the suffix naming a *variable* rather than a characteristic, and nothing else. No title-casing, no underscore substitution, and **emphatically no expanding an abbreviation into words — every one of those is this crate deciding what a firmware team's shorthand stands for, being wrong occasionally, and being trusted anyway.** The name carries its source and the untrimmed original, **so a UI renders provenance rather than presenting a vendor's published name and a local variable's spelling identically.**

**A name is optional and its absence is ordinary** — a live-only characteristic on a repo with no extractor shows the UUID head exactly as before. **Nothing fails, and nothing is invented to fill the gap.**

**Services get names by the same mechanism**, their identifier having been thrown away for the same reason and the same length of time. **Two maps rather than one, because a merged map would have to guess which lookup a UUID wanted.**

*Rejected: a `name` field on the characteristic type.* That type is the wire-comparable shape **a live discovery fills in from an ATT response, and an ATT response carries no names.** A source-only field would be **one hardware can never populate**, breaking the comparability decision 33 exists to provide. So names ride *beside* the table, from one text scan — **an extractor asked for the table and then for the names would read and re-parse the same files twice to answer one request.**

### 57 — The extraction scans the repo, not two files it was told about

Raised as a question rather than a bug report: *"maybe the gatt discovery check can be project wide?"* **It could, and it had to.** The extractor hardcoded two paths and the DUT repo has **a third service-definition block.** Everything needed was already parseable in files it could read — **the UUID macros are in the very header it opens — it was simply never handed the file. A third of this DUT's GATT table had been missing for as long as the extractor had existed, and nothing anywhere could have said so.**

**That is worse than the missing service**, because the module's own doc comment opened by claiming it *"fails loudly rather than silently under-extracting"*. **A bounded read of two named files cannot fail loudly about a third, because it has no idea the file exists. The loudness was real for everything inside its scope and vacuous about its scope.**

**What decides the scope now: the firmware repo's own ignore files, not a list this crate maintains.** Every C source and header under the root, honouring ignore files and skipping hidden directories — **and still honouring them in an exported tree with no `.git`, because an extractor that quietly widened its scan whenever pointed at a tarball would be the same silent failure in a different costume.**

**A naive glob is not the alternative it looks like.** On this repo it finds the service macro **twice as many times as there are services**, because a worktrees directory holds two entire extra copies — **and that fits under the cap with room to spare, so it would have emitted duplicated services without a word.** The same silent wrongness, **inverted from under- to over-extraction.**

**One hard block on top of that: any directory named `embarch`, at any depth, whatever the ignore files say.** It is gitignored on this repo, but **it is this suite that put it there, so this suite does not get to depend on the firmware repo having remembered.** Never the walk root itself: pointing the extractor at such a directory is **a deliberate act, not the accident the block is for.** What it pruned is reported, because **a hard block is exactly the kind of rule that stays invisible until it excludes something it should not have.**

**The loudness moves to the point of use.** Under a two-file read every declaration scanned was in use, so raising on an unresolvable one was free. Under a wide walk it is not: **a malformed macro in some third-party corner nothing references must not be able to blank the whole table.** So an unresolvable symbol is *recorded as* unresolvable and raises only if a service block actually reaches for it. **Failing loudly about things that affect the answer is the property worth keeping; failing loudly about everything a wide walk happens to see is how a defensive posture turns into a broken tool.**

**Three failure modes a wide walk creates, all named rather than absorbed:** two blocks resolving to one service UUID; one name carrying two values in two files, **reported rather than resolved by whichever file the walk read last**; and **a walk that finds no C at all, which would otherwise return an empty table — a plausible-looking answer to a question nobody asked.** C statics are file-scoped, so **two files declaring the same static name is ordinary C and must not cross-resolve.**

**The scan reports what it scanned** — files read, which contributed and what each contributed, what the block pruned, what was not valid UTF-8. **This is the half that kills the failure mode rather than patching this instance of it:** a bounded read cannot report that it is incomplete, and **a walk that reports nothing is one commit away from being incomplete again.** Printing the handful of contributing files out of hundreds read is what makes **"it never opened the file I expected" something an engineer can *see* rather than infer from a table that came back plausible.**

Order is **stable but deliberately not a claim about ATT handle order**, which across files the linker decides — **a build fact this scanner cannot read out of source and does not guess.** And the text scan still **does not evaluate preprocessor conditionals**, so a config-gated characteristic is reported unconditionally: this widens *which files* are read and **touches nothing about how a file is understood.**

*Rejected: a configured file or glob list per project* — explicit and auditable, and **silently incomplete in exactly the way the two-file read was, the moment someone adds a file, which is the bug.** *Rejected for now: an exclude knob* — the escape hatch if a *tracked* vendored copy ever trips the duplicate error, **and that error names the two files, which is a better time to design the knob than in advance.** *Rejected: shelling out to `git ls-files`* — same file set with no new dependency, but **it needs the git binary and a real checkout, and an extractor that returns nothing when pointed at an export is the silent failure again.**

Validated against the real checkout: **three services where a bounded read found two**, every characteristic named.
