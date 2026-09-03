# embarch-ui decisions: Navigating the trace chart

**Status:** active, 2026-09-02.

Zoom, pan, aggregation, and the study-action row. What the chart renders and on which clock is in [trace-view.md](trace-view.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 10 — Chart half: the trace chart is navigable, and the study's steps are projected onto its axis

**A fixed-width SVG puts a 34 µs ISR run inside one pixel column with no way to open it.** Wheel zooms at the pointer, drag pans, **and the window is clamped to the capture so a reader cannot end up staring at empty axis wondering whether the trace stopped.**

**It stays SVG, and "too many rects to re-render" is the wrong way to frame it.** Once sub-pixel spans are aggregated into per-pixel occupancy runs per lane, **the element count is bounded by pixels × lanes, not by the dataset.** A canvas rewrite would have cost CSS-variable theming, hand-written hit-testing, and the browser harness's ability to inspect what was drawn — **to solve an element count aggregation had already bounded.**

**Aggregation is exact, and that is checked rather than asserted.** A merged run splits wherever a gap, a below-resolution flag or an open edge changes, **so a block can never fold an unvouched-for span into a clean-looking bar** — the quiet lie this whole decision exists to prevent, **arriving through the back door of a performance optimisation.** Splitting on all four costs nothing on real data, **so the honest version is also the cheap one.** A block that merged more than one run says so and **refuses to report a duration.**

Three things came with it, **because navigating without them is half a feature:**

- **Vertical scroll with the axis and step row pinned**, since **an axis that scrolls off the top leaves every bar below it undated.**
- **Lane filtering, hiding and reordering** — the reading that found a real connection-interval fault was *"watch these three ISRs and ignore everything else"*. **Filtering changes the drawing and nothing else:** the load repartition stays computed across every lane and says so, **since a denominator that quietly followed a view filter is the same class of error as everything else here.**
- **Axis labels keeping exactly as many digits as the window can distinguish**, sharing one tier across a drawing **so an axis never makes a reader convert in their head to compare its own ends.**

**The study-action row: which step was running, projected onto the axis and told which clock it is on.** A timeline with no answer to *"what was the study doing here"* is a picture; **with one it is a diagnosis.** One band per step, coloured by the recorded outcome, **shaded to separate the declared delay from the execution** — not cosmetic: **the bench sleeps that delay as part of dispatching, so it genuinely falls inside the step's window, and without the split a step reads as 5 seconds when it ran for 23 ms.**

**The stamps had to be recorded, because the result file's step entries carried no time at all.** Core writes both edges plus the declared delay. **Core's own arrival stamps, deliberately** — a timestamp in the step result would be **a dev-bench wire bump, a schema version, a hand-written C encoder change, and a third clock in a picture that already has two.** The GATT transcript was the tempting UI-only version and **covers only steps inside its declared scope that produced traffic — missing exactly the long drain that anyone actually wants to look at.**

**Three axis cases, the three tiers again.** On the DUT clock each band is **projected** through frames carrying both clocks and the row **carries its own accuracy — invisible against seconds-long steps, and said out loud anyway, because the lanes beneath are microsecond-exact and a row that looked aligned to them would claim a precision it does not have.** On the host clock the axis already *is* that clock: no projection, exact. On frame indices a step **cannot be placed, and none is** — no bands, and the reason said instead.

**Three ways the projection goes quietly wrong if built the obvious way.**

- It drops a **stale pre-reset prefix** — the DUT's counter restarts at reset and **a capture can open with bytes already inside the USB-UART bridge, past any port flush.** The prefix ends at the largest *backward* step between anchors, **filtered so the benign kind is left alone: a hook stamps before it reserves its ring slot, so a preempting interrupt is stamped before the thread it preempted — microseconds at worst, against *seconds* for a restart.**
- **An anchor is a frame's arrival against the *last* DUT stamp in it**, since a frame is sent once the last record it batched is in.
- **A step overrunning the capture is clipped, not moved**, with a step entirely outside the window **left out rather than squashed against the edge.**

**A gap record must not anchor that projection.** A gap is stamped when the first *dropped* record was lost rather than when it was reported, **so its stamp sits outside the run its own frame carries — far ahead of every other record in it.** Left in, it poisons its frame's anchor and the next frame's reads as a large backward step: **one step vanished from the row entirely and another came out starting before the step before it had ended.** The parser already excluded gap records from both its backstep measurements **for exactly this reason; the projection was the third place that rule belonged and the only one that had not got it.**

**Three findings of the same shape: a comment that named the right invariant sitting over code that did not implement it.**

- **A lane's spans overlap, and the committed fixture already proved it.** The chart found visible spans by a lower bound plus one step back, **over an explicit comment asserting that a lane's spans never overlap.** They do, exactly when a record was lost: **a dropped switch-out leaves a run open, and this view's own rule draws every still-open span out to the end, so later runs of the same thread sit *inside* it.** The step-back halted on the first nested span and **the enclosing one disappeared from every zoomed window past it** — the exactness property failing on the read side rather than the merge side. The search is now over **the lane's running maximum, non-decreasing by construction and still one binary search.**
- **A thread is never inside itself — a new invariant.** The idle lane already closed an open run when a second entry arrived; **nothing applied that rule to threads, so two switch-ins with no switch-out left both runs open and drew the first across every later run of itself. One CPU runs one thread, so this is a scheduler invariant rather than a claim about any firmware.** *Deliberately not extended to ISRs:* the unidentified-ISR lane is a **bucket** for every vector the manifest could not name, **so two of its spans overlapping is a higher-priority vector nesting inside a lower one — real, and a stack is the right shape for it.**
- **The step row's clipping rule was decided by the wrong test.** Bands were kept by whether each edge could be projected, **which drops a step *enclosing* the capture — neither edge inside the window — and that is the ordinary shape of a tap opened and closed inside one long step. The single step running for the whole trace was the one step the row never drew.** Decided by overlap first now, then clipped. **Same class: the delay split read an unplaceable delay end as "past the far edge" in *both* directions, where before the near edge is the common case** — the delay runs first, so a tap opening partway into a step opens *after* it — **and those bands were drawn as though the whole visible span were a sleep, precisely the misreading the split exists to prevent, arriving from the other end.**

**Rendering the tab in a browser found a defect a Rust test could not.** The Load button and the load table's body carried **the same element id**, so **every summary row had been rendering into the button: the table had never once displayed, and its Rust tests all passed.** **Recorded because "tested in Rust, never looked at" is the exact shape of thing that hides this, and this view is the most Rust-tested and least looked-at surface in the UI.**
