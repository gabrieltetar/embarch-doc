# HIL notes: the goals every review is held to

**Status:** draft, 2026-11-15.

**What the HIL design must achieve, in the owner's words, and what each goal asks of a review.** A reviewer reads this first and judges every note against it; a finding that serves no goal here is out of scope. The owner's words are quoted from the review session of 2026-11-15; **what each one asks of a review is the reviewer's reading**, marked as such, and the owner may correct it.

## The goals

| # | The owner's words | What a review checks (reviewer's reading) |
|---|---|---|
| G1 | "the most critical part of the EmbArch solution" | Nothing in the design is "later" by default: a gap in HIL is a gap in EmbArch. A deferred piece says why it can wait |
| G2 | "very well engineered for other eng to like and adopt it" | **An engineer new to EmbArch** can run a first Study or Test without building an atlas, writing a suite, or reading the suite's history. Every concept has one name, one file shape, one place. The first hour is short |
| G3 | "professional, ground breaking, sound logic good solution" | **Professional**: the vocabulary and the report match what a test lab would expect (verdicts, limits, units, decision rule, coverage, records enough to repeat a test). **Sound logic**: no rule contradicts another, or a decision of the suite. **Ground-breaking**: what EmbArch does that no prior art does is named, and checked against the prior-art survey before it is claimed |
| G4 | "solves the LLM-HIL problematic" | **The trust model holds** ([09-trust-model.md](09-trust-model.md)): the agent does to the hardware only what the engineer allowed, what it reports is true, and a reader can check that without trusting the agent. Every failure an LLM at a bench is prone to has a row, a mitigation and an enforcing layer |
| G5 | "the main reason EmbArch might become a big open source project instead of a one man show" | **A contributor can add to it**: a premade suite, a reducer, a bench app, without touching the core. The public docs and suites carry no client detail. Nothing depends on the owner's own machine or setup |
| G6 | "ship the solution to real clients but only if the HIL part is very well designed and professional quality" | **A client can rely on a report**: it states what it does not prove (not a certification, what was not run, what is a claim and what is measured), and a client can check it with an open-source tool. A client's prototype is not put at risk by the procedure |
| G7 | "this can be a work spanning weeks" | Depth over speed: a review round may reopen an answered question when a later finding shows it was answered on wrong facts, and says so |

## How a review uses this

- **Each finding names the goal it serves** (G1 to G7), and its severity follows from it: a finding that breaks G4 or G6 is a must.
- **A review round ends with a line per goal**: met, met with named gaps, or not met, and why.
- **The lenses for an independent round** follow from the goals: evidence integrity (G4, G6), hardware safety (G4, G6), adoption by a new engineer (G2, G5), professional practice against prior art (G3), consistency with the suite's decisions (G3).

## Open

- **Whether the reviewer's readings in the table say what the owner meant**, goal by goal.
- **What "ground-breaking" is measured against**: the prior-art survey of review round 1 ([11-prior-art.md](11-prior-art.md)), once it lands.
