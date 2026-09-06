# 008 — Compact `embarch-topology/open.md` and `spec.md`

**State:** done
**Source:** `scripts/check-doc-size.py` — both files entered reserve on leg 020's bench unit
(`tasks/topology/006`), which added one `open.md` bullet recording two measured reporting defects
and three `spec.md` paragraphs recording the live link-port resolution.
**Scope:** topology
**Hardware:** none
**Owner:** no

**Compacts:** embarch-topology/open.md, embarch-topology/spec.md
**In flux:** no
**Must not delete:** The signal-alert bullet's two supporting facts — that `embarch-ui` needs no
change when the durable half lands, and that the mirrored alert type in the shared Core client
declares those fields non-optional and must move in lockstep. Neither is re-derivable from the
prose around it. The `validate_signal`-has-no-caller bullet's *reason* (resolving a route at the
point of use is the validation and returns the identical mismatch, so calling both would check
twice and report once) — reduced to "no caller, deliberately" it reads as a gap and gets re-filed.
The rejected-centralization bullet's **two** named conditions for revisiting, and its
counter-argument that the API deliberately did not centralize address resolution at setup time
because the value must be right when a build is flashed — that is the whole reason the rejection
is not merely a deferral. The Nordic-identity bullet's statement that fallback registers come back
*mismatch* rather than *undeclared*, which is the one way that arm can be wrong. **And the
measured-defects bullet's load-bearing clause — that `detected_by` "names the weakest rule
consulted rather than the one that chose"** — which is supported today only inside
`tasks/topology/003` and `004`, **both of which are deleted when those tasks close.** If that
clause is dropped here, the observation is gone from the corpus entirely.

**From `spec.md`, all of it bench-measured and none of it re-derivable once the boards are
unplugged:** the **three** SEGGER CDC UART ports and their USB paths (`COM16` `…&MI_00` and
`COM17` `…&MI_02` sharing one device instance, `COM5` on the other J-Link) — the shared instance
is the whole reason the interface is load-bearing and it reads as a detail. **That `COM5` was
eliminated by decision 17's *fallback* and not by a declared serial, and therefore that the
declared-serial path still has no hardware evidence** — this sentence was wrong in this file for
about twenty minutes on 2026-09-06 and a reviewer caught it; shortening it back toward "the
declared facts were exercised" reintroduces exactly that error. The traced `select` counterfactual
(`one_probe && interfaces_known` both hold, so it warns, sorts, takes `COM16` and sets
`guessed_among = Some(2)`) — its value is that it is *traced*, so reducing it to "would have
picked the wrong port" turns a checked claim back into an assertion.

## What

`embarch-topology/open.md` is **5,015 bytes against a 5 KB `open` cap — 105 bytes of runway**,
which is not enough for one more open question of any length. It holds nine bullets.

**The likely compaction is not prose surgery.** Several bullets are no longer open questions at
all and belong in `spec.md` as current truth or in `decisions.md` as settled: the
rejected-centralization bullet records a decision that was *made*, and the
`validate_signal`-has-no-caller bullet records a posture that was *chosen*. `open.md` is
"unresolved only" by its own header, and two of its longest entries are resolved. Moving them is
both the compaction and a correction.

## Why now

Leg 020 spent this file's remaining runway and is filing the debt in the same unit that spent it,
per `../../DOC-COMPACTION.md`. **The file was at 85.8% and therefore not in the pressure list**,
so no dispatch could have warned anyone: it went from unflagged to 97.9% in one edit. That is
worth noting beyond this file — a 90% reserve line gives no warning to an edit larger than 10% of
a cap, and a 5 KB cap makes that 512 bytes, which is one paragraph.

## Done when

- [x] `open.md` is out of reserve (`scripts/check-doc-size.py` clean, no allowance taken).
      **5,015 → 2,865 B, 56.0%.** `spec.md` **9,489 → 8,956 B, 87.5%**, also out. Both PAID.
- [x] Every item in `Must not delete:` survives, in words a reader can still check.
- [x] Anything moved out of `open.md` lands in `spec.md` or `decisions.md` rather than being
      dropped, and the move is stated in the commit message.
- [x] Answered in the compaction commit message, in the compactor's own words:
      *can `spec.md` alone answer what someone needs to work on this component today?*
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## What shipped

**Four bullets left `open.md`; two of them were moves, and the other two were duplicates whose
words already stand elsewhere in this sub-project.**

- **`validate_signal` has no caller** — deleted from `open.md`; `check-duplication.py` had it as a
  22-word overlap with `decisions/links.md`, which already carries the reason verbatim ("resolving
  at the point of use *is* the validation and returns the identical mismatch, so calling both would
  check twice and report once"). What was *not* there — the `embarch-study-designer`
  advertise-scoped-decode cross-reference, and the naming of the function — was added to decision
  18 in the same paragraph. This was a posture chosen, not a question open.
- **Centralizing a remote Core's declared host** — moved whole to `decisions/scope.md` as
  **decision 22**, new number, index row updated. Both named conditions for revisiting and the
  API-did-not-centralize-at-setup-time counter-argument survive; the counter-argument is now
  labelled in the heading as what makes it a rejection rather than a deferral.
- **The signal-alert bullet's two supporting facts** — `embarch-ui` needs no change; the mirrored
  alert type in the shared Core client declares those fields non-optional and must move in lockstep
  — moved into decision 18's durable-alert-trigger paragraph, where someone building it will be
  reading. `open.md` keeps the question and points at the trigger.
- **The Nordic-identity bullet** — the *mismatch*-rather-than-*undeclared* clause is kept in
  `open.md` in checkable words; the surrounding derivation, a 15- and a 22-word overlap with
  `decisions/enrollment.md` decision 21, is now a pointer to it.

**`spec.md`, three cuts, none touching the 2026-09-06 bench measurements:** the incident narrative
(out of role for `spec.md` per `DOC-COMPACTION.md` §3, and retired decision 9 carries it) reduced
to the constraint it implies; the via-bench validation bullet's "why not both" pointed at decision
18 instead of restated; the `Where it stands` validation record trimmed to the gap it names. The
three SEGGER ports and their USB paths, the `COM5`-eliminated-by-*fallback* sentence with its
"the declared-serial path still has no hardware evidence" conclusion, and the traced `select`
counterfactual are all untouched, byte for byte.

Topology's `check-duplication.py` overlaps: **11 → 7**. `collect-open-questions.py`: **9 → 7**
bullets, the two removed being the two named above as settled rather than answered-away.
