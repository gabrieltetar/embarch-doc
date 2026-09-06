# embarch: decision reversals

**Status:** active, 2026-09-02.

Assumptions reality has already overturned — **the highest-signal page in this repo for anyone new, and the best predictor of which remaining assumptions to distrust.** Every entry is handled correctly in its own owning doc. **This page does not restate a correction's mechanism; it names the assumption, what reality showed, and where to read the rest.**

## The rows

| Range | File |
|---|---|
| 1-50 | [reversals/rows-1-50.md](reversals/rows-1-50.md) |
| 51-72 | [reversals/rows-51-72.md](reversals/rows-51-72.md) |
| 73-92 | [reversals/rows-73-92.md](reversals/rows-73-92.md) |
| 93-109 | [reversals/rows-93-109.md](reversals/rows-93-109.md) |

**A row number is a permanent identity, not a position.** Numbers are never reused or renumbered, so a row may sit out of date order and a range file never re-splits an existing row into a different file. Rows 106-109 were renumbered from duplicates that shared a number.

Owners are abbreviated in the tables: `core` [embarch-core](embarch-core/decisions.md) · `api` [embarch-api](embarch-api/decisions.md) · `bench` [embarch-dev-bench](embarch-dev-bench/decisions.md) · `sd` [embarch-study-designer](embarch-study-designer/decisions.md) · `outpost` [embarch-outpost](embarch-outpost/decisions.md) · `topo` [embarch-topology](embarch-topology/decisions.md) · `ui` [embarch-ui](embarch-ui/decisions.md) · `umb` [embarch-umbrella](embarch-umbrella/decisions.md)

## The recurring shapes

Every row was caught by a real build, install, capture, or by reading a real repo's actual files — **never by inspection alone.** Read across them and the same eleven shapes keep arriving. This list is the page's actual predictive content; the rows are its evidence.

**1. Documented as implemented, wasn't.** The single most common shape here, and it survives every kind of test suite. Rows 15, 28, 33, 35, 55, 71, 99. **A decision recorded as settled — even one carrying its own note that it is unbuilt — is indistinguishable in a later reader's eyes from one that shipped** (55). A stub whose blocking reason is written into its own message **ages into a check that asserts a falsehood, and reads as a known gap rather than a wrong answer** (71). A feature can be fully typed, wired into two repos, enabled by a Cargo feature and advertised to every agent that ever called it, **and still be inert** (33).

**2. A bound measured on the wrong side of the wire.** Rows 25, 39, 60, 63, 69, 70, 74, 89, 96. **A `size_of` on the sending side is not a bound on the receiving side, and a serialized worst case can exceed the value it serializes** (69). A buffer sized for a message that cannot arrive costs kilobytes twice, **because fixing one direction makes the mirror-image bound harder to see, not easier** (60, 70). And a capacity requirement derived from **a capture of a broken system** would have bought a six-component wire change to fix a number a one-line study change removed (96).

**3. An input accepted, silently discarded, and reported as success.** Rows 73, 75, 76, 81, 98, 101, 102. **A flag that cannot be honoured must fail, not be ignored; "only meaningful for X" in a help string is documentation, and documentation is not a gate** (81). The variants that hurt most are the ones where the *flag that reports the loss* is itself unfalsifiable (98) or fed from the wrong counter (73).

**4. Two things that must agree, with nothing mechanical keeping them in step.** Rows 8, 22, 30, 44, 63, 103. **A note describing a gap is not a mechanism for closing one** (44) — the comment recording that a mirrored constant had been four bumps stale stayed accurate and did not prevent the immediate recurrence. A capacity constant is a contract the moment both sides have one (30).

**5. A guess indistinguishable from an answer.** Rows 14, 82, 105. **The expensive part is never the guess, it is that nothing downstream can tell it was one** — a warning in a log while the endpoint reports full confidence turns a wrong port into a bench that flashes, boots, runs, and times out on a handshake, **which says nothing about a port having been chosen at all** (105).

**6. A wire capability verified to *exist* rather than verified to be *used*.** Rows 26, 68, 86. **A wire-format change is not done when the DUT emits it — it is done when every host that decodes it has been re-measured against it** (86), which cost a 46× error on the single number the next session was briefed to reduce. **A message type is the one place a "this half is someone else's scope" split can hide a hole**, because the half you are not building is exactly the half whose input you never construct (68).

**7. A rule that exists in some of the places it applies.** Rows 27, 97. **A rule that exists in two of the three places it applies is not a rule anyone will find; it is a coincidence** (97). And a decision can borrow a lifetime trigger **from the very sources it was defining itself against** (27).

**8. The comment names the right invariant; the code does not implement it.** Rows 100, 101, 102, 104. Three were found in one pass, and the quoted sentence is usually **what made the defect invisible: it names a class it does prevent, which reads as though it had considered the space** (104). One even had a test **asserting the loss as intended behaviour** (102).

**9. Graceful degradation hiding a retirement.** Rows 31, 48, 99. Code that still compiles, still runs, and can no longer do the one thing it exists for. **A stale premise carried into a plan reads exactly like a live one, and the only thing that separated them was running `grep` before believing it** (48).

**10. What real silicon actually said.** Rows 1, 3, 4, 16, 19, 38, 41, 42, 49, 54, 83, 84, 85, 89, 95. Twice the suite reached a **well-evidenced wrong answer** and needed a fact no amount of reading could supply — three diagnoses on one fault, two of them wrong, settled by the owner naming his board in a sentence (85); and three on another, **each refuted by a check on the *other* end rather than by more reading of the same bytes** (92). Note also that **tolerating a fault is what exposed it** (92): the resilience fix, not an investigation, is what let a run keep reading long enough to observe the silence that was the whole diagnosis.

**11. A cost charged to the path it measures.** Rows 62, 65, 88. **Instrumentation that travels over the mechanism it instruments can amplify itself, and it only shows up at the verbosity nobody tests at** (65). And a decision can be re-argued and re-priced twice **without anyone asking *where* the cost landed** (62).

## Review-driven reversals — found by a documentation pass, not a real build

Lower-signal than the rows above — no hardware or build forced the question — but worth distinguishing from a fresh decision rather than letting them read as one.

- **Core's default bind address flipped from all-interfaces to loopback.** Not wrong when written — reachability from WSL2 and a future LAN was sound reasoning — but **never assessed *together* with no-TLS-plus-a-static-token-plus-an-arbitrary-local-path**, which composed into a real gap once looked at as a whole. [core](embarch-core/decisions.md) decision 6.
- **`doctor`'s target-count check stopped maintaining its own mirrored scanner one day after building it.** The liftable-copy pattern — written for cases where a real dependency genuinely does not exist yet at call time — was applied a third time to a check that **could have just shelled out to `embarch-api` like every other check already does.** **Documented 2026-09-02, executed 2026-09-05**: for three days this entry described a shell-out that did not exist, and the mirrored scanner it claimed had been dropped was still the only thing check 8 called. **Shape 8's variant with the *decision* as the false witness rather than a comment** — an amendment that reads as shipped is indistinguishable from one that is, and only [umb](embarch-umbrella/decisions/projects.md) decision 17's own "built 2026-09-05" line says which. Found by the 2026-09-03 design-only audit, closed by `umbrella/007`. [umb](embarch-umbrella/decisions.md) decision 17.
- **A retirement's error message advised the caller to rebuild the thing being retired.** `[[projects.targets]]` was retired for both discovery kinds, but the refusal sat above the `match` on kind, so a `zephyr-west` project was told to declare one entry per target with its own `build_command`/`chip`/`artifact_path` — the snapshotted static schema [api](embarch-api/decisions.md) decision 12 exists to prevent, and three fields the same function refuses thirty lines later. **Shape 8 with the test as the tell**: a refusal test asserting only that it refuses gates half the surface, so decision 51's "the surface text is what a caller reads" had no mechanical form until the test read the text too. Found by a reviewer on a landed diff, which is the first defect that pass has caught. [api](embarch-api/decisions.md) decision 53.
- **Open-questions bullets are not covered by any check.** Two bullets had been answered by shipped work and never closed; the pre-close grep and `check-staleness.py` both watch *status tables*. Row 32, and [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §4.
