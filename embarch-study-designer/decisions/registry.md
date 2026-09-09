# embarch-study-designer decisions: The custom-action registry

**Status:** active, 2026-09-06.

`study-actions.toml` — the one place engineer-supplied knowledge about a DUT enters this crate, what it may say, and what `validate` refuses a hand-edited file for. Split out of [authoring.md](authoring.md) on 2026-09-06, when decision 67 met that file's size cap: the UI and the registry file are two missions, and this is the one still growing a rule at a time. The surfaces that *use* the registry — the table, the raw-payload row, the saved-study library — stay there.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 35 — A user-authored custom-action registry: names and enumerated parameter choices only, never a semantic description

The fix for decision 34: reading a DUT firmware's own source to infer what a custom GATT write does, then presenting that inference as fact, was flagged as destructive to the dev process. **The fix is not a smarter inference; it is removing inference from the loop entirely.**

**What the engineer provides — mechanical, not documentary:** a freely-chosen name, which characteristic it targets, its operation, and — for a write — a payload described as named fields, **each with a small enumerated set of engineer-supplied label/value pairs.** Building a step means clicking a name and clicking a value; **nothing is typed as raw hex, and there is deliberately no "what this does" field** — that would be this crate inventing a place to write down another guess.

A value's bytes are **the engineer's own literal bytes, never a numeric type this crate encodes itself**, which would require assuming a width and endianness nobody here is in a position to know.

**Persisted in the firmware repo's own folder** (`<firmware_repo_root>/embarch/study-actions.toml`, sibling to `embarch.toml`), so it travels with the firmware and is versioned there — not a catalog this tool owns separately, and not re-entered per study.

**A hand-edited file's mistakes are named refusals, on read *and* on write.** `validate` — called by both `load` and `save` — refuses a value whose bytes do not fill its declared field, and refuses **two actions sharing a name**: the builder resolves a row by the first name match, so the second is unreachable and the row silently carries a payload nobody chose. Decision 52's struct registry refuses its duplicate the same way, so one hand-edit mistake gets one refusal regardless of which registry it lands in. Refusing in `save` is the load-bearing half: **a file that can be written and not read back is worse than one rejected on the way in.**

**The durable principle, stated plainly since it generalises past this crate:** *no EmbArch component should ever present an inference about what a specific piece of hardware or firmware does — derived from reading its source, its comments, or any heuristic — as established fact.* Where that knowledge is needed, **the answer is a pipeline for the engineer who actually knows to supply it explicitly, built once, generically.** Decisions 41, 45, 52, 56 and 58 are each that rule applied somewhere else.

### 66 — A registry field's byte range is bounded at `validate` time, and an over-long payload is named as a payload

Decision 35's "named refusals" had a hole: `validate` checked what a value *contained* and never where a field *sat*. `byte_offset` and `byte_len` are the two numbers in `study-actions.toml` nothing bounded — **the widest field sizes the buffer the builder allocates**, so a mistyped offset was a hand-edited file choosing how much memory this host reserves. `byte_offset + byte_len` was plain addition on engineer-supplied numbers, against this crate's own invariant that addition saturates rather than wraps: an offset near `usize::MAX` panicked a debug build and, in release (`panic = "abort"`, overflow checks off), wrapped to a length of **0** that passed every check — the following slice index then panicked, so this was a crash on a hand edit, not a memory-safety hole. **The un-overflowing case is the real hazard**: a 4 GB offset does not wrap, passes, and sizes a 4 GB allocation. That is what bound-before-allocate refuses.

**The bound is `MAX_PAYLOAD_LEN`, checked in both places, deliberately.** `validate` refuses it on read and on write; the builder checks again **before the allocation**, since it takes a registry as an argument and an in-memory one has never been through `validate`. Same bound, one spelling, two genuinely different entry points.

`FieldRangeTooLong` is its own error rather than reusing `FieldLengthMismatch`: a value that is the wrong length and a field that sits outside the payload are different edits to make and fix.

**The message has to name the right bound.** An over-long registered payload used to report `TooManySteps` — a true number attached to the wrong noun, sending the reader to a one-row table instead of the field they mis-offset. `PayloadTooLong` already existed with the right wording, for the identical condition on the raw-payload path. The rendered string is asserted in a test, because the string was the defect.

### 67 — Fields of one action must cover disjoint bytes, and only a `Write` carries fields

Decision 66 bounded where a field *ends* and left where two *meet* unchecked. `study_builder` copies each chosen value into `buffer[byte_offset..byte_offset + byte_len]` **in declaration order**, so two fields sharing a byte is decision 35's duplicate-name failure applied to offsets instead of names, from the same hand-edited file.

**Worse than "the later declaration wins", and the error says so.** On a *partial* overlap the earlier field's bytes become a **splice** of both picks — a byte string in neither field's `values`, never registered at all. Pinned by a builder test: picks `[0xA1, 0xA2]` and `[0xB1, 0xB2]` yield `[0x00, 0xA1, 0xB1, 0xB2]`. **Which end of the splice comes from which pick depends on the declaration order, not the offsets** — that test declares the lower-offset field first, so the earlier field keeps its own head; declare the higher-offset field first and the ends swap. The invariant is that the earlier field's range holds a value nobody registered; the head/tail attribution is arrangement-specific and must not be stated as the rule. A total overlap is the milder case. Ranges are half-open, so fields that merely *meet* (`0..2`, `2..3`) pass, and a zero-length field collides with nothing.

**Fields on a non-`Write` action are refused rather than documented as ignored**: ignoring leaves the mistake in the file and defers the only signal to a build-time `NotWritable` blaming the *row* for choosing what the *registry* offered it, naming neither field nor file. Refusing names the wrong line at load and at save, where the edit was made — 66's posture. `subscribe`/`notify`/`indicate` too: only a write has a payload.

**Both are `validate`-only, unlike 66's bound**, which the builder repeats only because that number sizes an allocation it makes first. The builder re-derives no other registry rule — a duplicate action name is still whatever `.find()` reaches first — so a registry assembled in memory and never passed through `validate` can still build a wrong payload.

*Rejected: an overlap as deliberate layering* (a wide preset with a narrow override). Nothing in the file marks it intentional, the UI shows both choices as honoured, and it is indistinguishable from a mistyped offset; making declaration order load-bearing is this crate inferring an intent nobody stated.

### 69 — Two fields of one action sharing a name are refused, the third of this family and its own decision rather than an amendment to 67

`resolve_write_payload` (`study_builder.rs`) and the UI's own dropdown both key a field's chosen value by `field.name`, in one `HashMap<String, String>`. Two fields of one action sharing a name collapse to **one** entry, so the row can produce two different bad outcomes depending on the picked label's luck: if the label also names a value on the *other* field, both byte ranges are written from that single pick, silently, with the UI still showing both dropdowns as independently honoured; if not, the row fails with `UnknownFieldChoice`, naming a label the engineer *did* choose, for the field that never offered it. Either way the registry advertised two choices and offered one — decision 35's duplicate-action-name failure one level down, refused by the same `validate` pass before either outcome can happen.

**A new decision, not an amendment to 67.** 67 is about where two *ranges* sit; this is about what two fields are *named*, and the failure it produces — a silent double-write *or* a misleading `UnknownFieldChoice`, decided by nothing the engineer controls — is not a restatement of 67's splice. 66 and 67 already set the precedent inside this same function: two closely related, incrementally discovered rules on `validate` got two numbers, not one revised entry, because each stays independently citable once code depends on it (`scripts/check-decision-refs.py`).

**One `RegistryError` variant family, considered and declined.** `DuplicateRegisteredAction`, `FieldRangesOverlap`, `FieldsOnNonWriteAction` and this decision's `DuplicateActionField` are four distinct named refusals already, and decision 35's own opening move — a named, literal failure in place of an inferred one — is exactly what a shared family would blur: nesting them under one variant trades four self-describing `Display` arms for one arm plus an inner match. Every consumer either matches one specific variant or calls `.to_string()`; `embarch-ui`'s only use (`study_designer.rs`) is the latter. `RegistryError` already mixes `ActionRegistry` and `StructRegistry` failures in one flat enum, so a family covering three of twelve variants would be a partial regrouping around this one function, bought at the price of every future field rule asking which variant of the family it is before it asks what it refuses.

---
