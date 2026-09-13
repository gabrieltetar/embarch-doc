# 036 — `GET /dev-bench/hello` serves the bench's build as `firmware_version`, the one rename `embarch-core` decision 47 already made on this exact route

**State:** open — **half done.** Leg 105 announced this in `#embarch-fleet`
(`ts 1789317643.030479`, 2026-09-13 10:40, window closed 11:10 unobjected) and took only the
documentation half; see "What leg 105 did and did not do" below. **The rename itself is still
open and needs its own announcement window** — leg 105's covered documenting the field, and
the rename is a breaking change to a served field in three repos.
**Source:** leg 104, 2026-09-13, while running `tasks/suite/010`. Split out rather than taken,
because it changes a served field and `suite/010`'s announcement window covered the `clamp_version`
fix and the doc comments, not an API rename.
**Scope:** suite
**Hardware:** none — an HTTP response field and its consumers; nothing reaches a board.
**Owner:** no

## What

`embarch-core`'s `GET /dev-bench/hello` returns `firmware_version`
(`embarch-core/interfaces/studies.md`). That value is the **bench's** build. A `Study`'s
`requires.firmware_version` is the **DUT's**. The field a caller should copy this into is
`requires.dev_bench_version` — and `embarch-api`'s reflash gate and `embarch-core`'s study start
both do that crossing by hand.

`embarch-study-designer` decision 74 (landed by `suite/010`) settles the two *wire-and-storage*
spellings: they keep their names, and every reader is told whose build the value is. It explicitly
leaves this third surface open, because the argument that decided the other two does not apply
here.

## Why this one is different

**The rename is cheap on HTTP.** No reflash, no schema bump, no saved study or `StudyResult` on
disk changes — only Core's response body and its consumers.

**And this suite has already made exactly this rename, on exactly this route.** `embarch-core`
decision 47 (2026-09-07, `tasks/core/020`) renamed this endpoint's `hardware_id` to
`self_reported_hardware_id`, because a caller comparing `hardware_id` from here against
`hardware_id` from `/probes/enrolled` got **a near-miss byte-swap rather than a category error**.
That is the same defect shape as this one, one field over, and it was judged worth a breaking
rename.

## The counter-argument as first written, and why it does not hold

**Superseded 2026-09-13, leg 105.** This task originally argued that the rename would leave the
suite with **three** spellings for the bench's build instead of two — wire `firmware_version`,
HTTP `dev_bench_version`, study `dev_bench_version`. **That arithmetic is wrong and the conclusion
it supported should not be inherited.** `dev_bench_version` is one spelling used on two surfaces,
so the count is two either way:

| | wire (`HelloAck`) | HTTP (`/dev-bench/hello`) | study (`Requirements`) | distinct |
|---|---|---|---|---|
| today | `firmware_version` | `firmware_version` | `dev_bench_version` | **2** |
| renamed | `firmware_version` | `dev_bench_version` | `dev_bench_version` | **2** |

What the rename actually moves is **where the crossing happens**, and that cuts *for* it. Today the
crossing is between HTTP and the study — which is to say, in the caller's hands, at the exact point
where the HTTP name collides with `Requirements.firmware_version`, a field on the same struct
holding a **different board's** version. A caller matching name to name does the wrong thing and it
looks right. After the rename the crossing is between the wire and HTTP, *inside Core*, where Core
composes the response and no caller crosses anything; the caller sees `dev_bench_version` →
`dev_bench_version`. That is decision 47's shape exactly: Core relabels a value it serves so that a
caller's name-matching instinct produces the correct action.

## The real cost, which is not a spelling count

**The rename needs old-Core tolerance, and that is what makes it not cheap.** `embarch-api`
decision 58 exists because of decision 47's rename: against a Core predating it, the identity
fields come back absent, so the client types them `Option<String>` and `dev_bench_hello` renders an
**unavailable** cross-check naming which fields this Core did not send, rather than a partial pass.
A `firmware_version` → `dev_bench_version` rename needs the same treatment, and it is worse-placed:
`firmware_version` is a plain `String` on the client today, and `embarch-api`'s reflash gate
compares it (`src/reflash.rs:259-270`). A client that silently reads an absent field as empty would
turn a real version check into a vacuous one.

**And the Core actually running on this machine is already behind `main`** — `core/015`'s
outstanding native Windows build — so "old Core" here is not hypothetical, it is the bench.

That is the argument whoever takes this has to answer: not *how many spellings*, but *what the
client does when the field it asks for is not there*.

## Consumers to move if it is taken

- `embarch-core` — the response type for `GET /dev-bench/hello`, and `interfaces/studies.md`.
- `embarch-api` — `dev_bench_hello()`'s response struct and `src/reflash.rs`'s use of it; the
  `dev_bench_hello` MCP tool's output shape.
- `embarch-ui` — **checked, leg 105: it consumes the value and already crosses correctly.**
  `src/study_designer.rs:1581` maps `hello.firmware_version` into `BenchStateResponse.dev_bench`,
  and `:1645` into `MismatchResponse.dev_bench`; the DUT's version reaches the same responses as
  `dut`. So the UI's own surface is already spelled `dev_bench`, no `embarch-ui` doc mentions the
  field, and **a rename here would be a two-line deserialization change, not a rendering change.**
- `suite/user-guide.md` / `suite/studies-guide.md` — check for the field name in a worked example.

## What leg 105 did and did not do

**Did — the documentation half, which is decision 74's own principle applied to the one surface
that did not state it.** Two readers now say whose build the value is and which `Study` field it
corresponds to:

- `embarch-api/interfaces/tools-dev-bench.md` — the `dev_bench_hello` row listed
  `firmware_version` among the returned fields and said nothing about whose build it is.
- `embarch-api/crates/embarch-core-client/src/client.rs` — the response type's doc comment said
  the value is "what the bench currently running actually reports", which is true and does not
  warn anybody off `requires.firmware_version`.

`embarch-core/interfaces/studies.md` already said it (landed with `suite/010`), and no
`embarch-ui` doc and neither suite guide mentions the field at all, so those needed nothing. **The
served field, the MCP tool's output keys, the CLI's `--json` keys and the human rendering are all
unchanged.**

**Did not — the rename**, and not because the argument against it holds. It does not (see above).
It was left because leg 105's announcement covered documenting the field, because the rename needs
the old-Core tolerance work described above rather than a mechanical field rename, and because
executing a breaking change to a served field across three code repos unattended, as a leg's last
unit, is the wrong shape for it.

**Decision 74 was not amended and does not need to be.** It already says, in its own words, that
this surface *"is a genuinely open question and this decision does not close it"* — the previous
leg's worry that 74 reads as settling the question is answered by reading 74.

## Done when

- [x] Every reader of `/dev-bench/hello`'s `firmware_version` is told whose build it is and which
      `Study` field it corresponds to. (leg 105)
- [ ] Either the rename lands across every consumer above — **with the old-Core tolerance
      question answered**, not just the field renamed — **or** this task is closed with the
      reasoning recorded in `embarch-study-designer` decision 74 as the answer that stands.
- [ ] Whichever happens, it gets its **own** `#embarch-fleet` announcement window: leg 105's
      covered documenting the field, not renaming it.
- [ ] Gate green in every repo touched; `changelog.d/` fragments for each.
