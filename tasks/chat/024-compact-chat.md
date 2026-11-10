# 024 — `embarch-chat/spec.md` is in reserve

**State:** open — unparked by the supervisor 2026-11-10 as a verbatim split; see the update below
**Source:** `chat/023` added a spec line for an ended issue's chat and left spec.md at 9,373 of 10,240 B.
**Scope:** chat
**Hardware:** none
**Owner:** no

**Compacts:** embarch-chat/spec.md
**Size debt due:** 2026-11-24
**In flux:** no, for the verbatim split this task now asks for. The end-of-issue behaviour (decision 104) has not met a real desk and window, and the chat's spec has taken a line a week since 2026-10-25, so a squeeze would restate what the next unit changes. A split by mission moves text whole and restates nothing (`DOC-BUDGET.md`, "a split is the default remedy"), so that objection does not apply to it.
**Must not delete:** the `§2` bullet on an ended issue (decision 104) and the one on what a reload restores (63), which state behaviour no decision file's summary repeats.

## Update (supervisor, 2026-11-10)

Unparked as a split, not a squeeze, on the reasoning that unparked `outpost/029` and `promptu/004` the same afternoon: the park waited on a live run nobody has scheduled, and `DOC-BUDGET.md` makes a split the default remedy. **Reword nothing** in what moves. `spec.md` is 9,373 B and leaves reserve at <= 9,039 B. §2, "How it works", is 4,770 of those bytes; the seam is inside it, by feature. `spec/constants.md` is the precedent for a `spec/<topic>.md` file. Leave a one-line pointer where text left, keep both `Must not delete:` bullets readable (moved whole is fine), and check inbound links (`grep -rn 'chat/spec.md'`) before cutting. If no seam leaves `spec.md` able to say what the chat is and how it works, say so and re-file with the plan instead.

## What

Split `spec.md` by mission, verbatim, so it leaves reserve.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; `chat/023` spent the reserve.

## Done when

- [ ] `spec.md` is clear of reserve (`scripts/check-doc-size.py --pressure` shows it not at all), or a successor re-files with a concrete plan.
- [ ] Moved text matches the original apart from headers and pointer lines.
- [ ] Every `Must not delete:` item is still readable.
- [ ] Can `spec.md` alone answer what someone needs to work on this component today? Answered in the commit message.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
