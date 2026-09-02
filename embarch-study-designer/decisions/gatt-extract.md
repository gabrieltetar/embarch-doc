# embarch-study-designer decisions: GATT extraction and naming

**Status:** active, 2026-09-02.

Reading a firmware repo for its own GATT table, and giving a characteristic a name.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 33 — A GATT-config extraction tool ships in this crate: a generic `GattConfigExtractor` trait, one concrete implementation

Distinct from decisions 31/32, which answer the same question live over BLE against whatever is running. A study author working against a specific firmware repo usually has it checked out already, and its GATT table is *source*, not a runtime mystery — extracting it statically means a `DataExchange` step can be authored with real UUIDs before dev-bench connects to anything, and gives a second independent source to diff against a live result (catching, say, a service compiled out of a specific build).

The trait's output reuses §4.3a's own `GattServiceInfo`/`GattCharacteristicInfo`, so a static extraction and a live `GattDiscover` result are comparable without a translation step. One implementation ships: `ZephyrBleDefExtractor`, scoped narrowly to one firmware's actual conventions — confirmed against real source (`ble_def.h`'s `..._UUID_VAL` macros, `ble.c`'s `BT_GATT_SERVICE_DEFINE`/`BT_GATT_PRIMARY_SERVICE`/`BT_GATT_CHARACTERISTIC` calls) rather than guessed against a generic Zephyr peripheral layout. It lives in `tools/`, a `std`-only binary behind a `gatt-extract` feature, not the `no_std` core — an authoring-time tool, never something dev-bench or Core links. Deliberately generic at the trait boundary and narrow at the implementation, per the repo owner's explicit call: a second firmware project's extractor is a new `impl GattConfigExtractor`, not a redesign of the trait or the output shape.

**Byte-for-byte comparability is now weaker than this decision claimed** — see decision 57: services come back in a stable but *non-handle* order, so a caller comparing static against live should compare them as **sets**.

### 56 — A characteristic gets a name: the vendor's, or the C identifier the firmware declared it under

Raised by the repo owner one decision after 53/55 gave a study something to name characteristics *for*: "the option show up as numbers." They did — every picker labelled its options with the head of a 128-bit UUID, because that was the only thing this crate could tell a UI about a discovered characteristic. On the real DUT that means choosing between `00000002` … `00000008`, **differing in one hex digit and ordered by service definition, not by anything a human is thinking in.**

**A UUID is the correct identity and a poor label.** Nothing about identity changes: the UUID is still what a checkbox's value carries, what crosses the wire, and what every tooltip shows.

Two name sources, neither a guess:

- **The vendor table.** A vendor-published characteristic already carries the vendor's own name; `VendorCharacteristic` gains a `short_name` (`"NUS TX"`) beside its full `name`, because a picker's label has room for a few characters and the place to decide the short form of a vendor's sentence is the table holding both. New `vendor::find_by_uuid` is the lookup direction the table never had: `find_characteristic` resolves a selection made *by name*, this resolves one something else found *by UUID*.
- **The firmware's own source.** The extractor always had the declaring C identifier in hand — it resolves the symbol to 16 bytes to build the table at all — and **dropped it on the floor**. Keeping it costs one push and covers everything custom, which on a real DUT is nearly everything: [measured] 15 characteristics named **without asking its engineers for anything, because they already wrote the names down.**

Vendor wins where both apply: source is one repo's spelling of a thing the vendor has already named.

**A label, never semantics** — the same line the vendor table and the registry both hold, and the one this decision could most easily have crossed. `sds_hrm_rrm` says what the firmware's authors *call* this characteristic; it says nothing about what its bytes mean, when it notifies, or what writing to it does. So the shortening is mechanical and reversible: trim the suffix naming a *variable* rather than a characteristic, and nothing else. No title-casing, no underscore substitution, and emphatically **no expanding `hrm`/`sds` into words** — every one of those is this crate deciding what a firmware team's abbreviation stands for, being wrong occasionally, and being trusted anyway. The name carries its source and the untrimmed original beside the label, so a UI renders provenance rather than presenting a vendor's published name and a local variable's spelling identically.

**A name is optional and its absence is ordinary.** A live-only characteristic on a repo with no configured extractor has no name, and the picker shows the UUID head exactly as everything did before. Nothing fails, and nothing is invented to fill the gap.

**Services get names too, by exactly this mechanism** (amended the same session): the *service*'s declaring identifier was being thrown away for the same reason and for the same length of time. Trimming keeps `_service` — `bds_service` is a heading, `bds` would be this crate deciding what the abbreviation stands for. **Two maps rather than one**, because a service UUID resolves against the vendor table's *services* and a merged map would have to guess which lookup a UUID wanted; one symbol list covers both, since a lookup is keyed by UUID and a service UUID never collides with a characteristic's.

**Why not a `name` field on the characteristic type.** That type is the `no_std`, wire-comparable shape a *live* discovery fills in from an ATT response, and an ATT response carries no names. A source-only field would be one hardware can never populate, and would break the static-vs-live comparability decision 33 exists to provide. So names ride *beside* the table, produced by one text-scan — an extractor asked for the table and then for the names would read and re-parse the same files twice to answer one request.

### 57 — The GATT extraction scans the repo, not two files it was told about
Raised by the repo owner as a question rather than a bug report: "maybe the gatt discovery check can be project wide?" It could, and it had to. The extractor hardcoded two paths, and the DUT repo has **three** service-definition blocks. Everything the scanner needed was already parseable and already in files it could read — the UUID macros are in the very header it opens — **it was simply never handed the file. A third of this DUT's GATT table had been missing for as long as the extractor had existed, and nothing anywhere could have said so.**

That is the actual finding, and it is worse than the missing service: the module's own doc comment opened by claiming it "fails loudly … rather than silently under-extracting". **A bounded read of two named files *cannot* fail loudly about a third file, because it has no idea the file exists. The loudness was real for everything inside its scope and vacuous about its scope.**

**What decides the scope now: the firmware repo's own ignore files, not a list this crate maintains.** Every `.c`/`.h` under the root, honouring `.gitignore` and friends and skipping hidden directories. Ignore files still apply in an exported tree with no `.git` — **an extractor that quietly widened its scan whenever pointed at a tarball would be the same silent failure in a different costume.**

**The measurement is the argument.** [Measured 2026-08-26] a naive glob reads **1663** files and finds the service macro **six** times, because a worktrees directory holds two entire extra copies of the repo. Six fits under the cap with room to spare, so **the naive walk would have emitted three duplicated services without a word** — the same silent wrongness, inverted from under- to over-extraction. Honouring the ignore files reads **218** files and finds the three real services.

**One hard block on top of that, at the repo owner's call: any directory named `embarch`**, at any depth, whatever the ignore files say — [measured] 917 build-output files on this DUT. It is gitignored there, but **it is this suite that put it there, so this suite does not get to depend on the firmware repo having remembered.** Never the walk root itself: pointing the extractor at such a directory is a deliberate act, not the accident the block is for. What it pruned is reported, because a hard block is exactly the kind of rule that stays invisible until it excludes something it shouldn't have.

**The loudness moves to the point of use.** Under a two-file read every declaration scanned was in use, so raising on an unresolvable one was free. Under a wide walk it is not: a malformed macro in some third-party corner nothing references must not be able to blank the whole table. So an unresolvable symbol is *recorded as* unresolvable and raises only if a service block actually reaches for it. **Failing loudly about things that affect the answer is the property worth keeping; failing loudly about everything a wide walk happens to see is how a defensive posture turns into a broken tool.**

**Three failure modes a wide walk creates, all named rather than absorbed:** two blocks resolving to one service UUID (a duplicated or vendored tree the ignore files missed); one name carrying two different values in two files, **reported instead of resolved by whichever file the walk read last**; and a walk that reaches a real directory and finds no C at all, which would otherwise return an empty table — a plausible-looking answer to a question nobody asked. C `static`s are file-scoped, so a reference inside a service block resolves **against its own file first** and only then repo-wide: two files each declaring the same static name is ordinary C and must not cross-resolve.

**The caps are reached, not bypassed**, and there are tests that say so. A repo-wide walk is precisely what makes finding nine services plausible, so the assertion stopped being theoretical.

**The scan reports what it scanned** — files read, which contributed and what each contributed, what the block pruned, what wasn't valid UTF-8. **This is the half that kills the failure mode rather than patching this instance of it:** a bounded read cannot report that it is incomplete, and a walk that reports nothing is one commit away from being incomplete again. Against the real DUT it prints three contributing files out of 218, so "it never opened the file I expected" is something an engineer can *see* rather than infer from a table that came back plausible.

**Order became a real question and is answered narrowly.** Sorted path order, then source order within a file: *stable*, and deliberately **not** a claim about ATT handle order, which across files is decided by the linker's section ordering — a build fact this scanner cannot read out of source and does not guess. **Decision 33's byte-for-byte comparability is therefore weaker than it was: compare the two as sets.** Flagged rather than papered over.

**What deliberately did not change:** the text-scan still does not evaluate preprocessor conditionals, so a Kconfig-gated characteristic is still reported unconditionally — this widens *which files* are read and touches nothing about how a file is understood.

*Rejected: a configured file/glob list per project* — explicit and auditable, and **silently incomplete in exactly the way the two-file read was the moment someone adds a file, which is the bug.** *Rejected for now: an exclude-glob knob* — the escape hatch if a *tracked* vendored copy ever trips the duplicate error, and that error names the two files, which is a better time to design the knob than in advance. *Rejected: shelling out to `git ls-files`* — same file set with no new dependency, but it needs the git binary and a real checkout, and an extractor that returns nothing when pointed at an export is the silent failure again.

[Validated 2026-08-26] against the real checkout: **3 services and 18 characteristics, up from 2 and 15**, all 18 named.

