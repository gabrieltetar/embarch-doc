# 013 — `promptu week pack` writes the week's per-run events for the drafter

**State:** done — promptu week pack writes the run events; chat and terminal runs found, edit diffs, tests green
**Source:** `embarch-promptu` `docs/contract.md` §14 (the weekly pass, written by `promptu/011`); decisions 14 and 42 (`decisions/learning.md`)
**Issue:** EMB-273
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

The weekly pass needs a pack of the week's Promptu runs that is built without a
model: what each run's footer says, and how the owner changed the prompt before
he sent it. No command reads a week of runs yet. A run's record is split in two:
`log/<run>.json` holds the original and what landed (`rendered`), and the
transcript holds what was sent. Decision 14, amended by 42, compares the sent
prompt against `rendered`, and nothing makes that comparison.

When this is done, `promptu week pack` writes the week's pack in the week
folder, in the shape and at the path `docs/contract.md` §14 fixes, with one
record per rendered run in the window, carrying:

- **From the footer**: questions skipped, answers other than the
  recommendation, "Other" text, fills the owner changed (`!`), a pattern he
  switched (`pick=owner`), and assumptions left by Esc.
- **From the comparison**: his edit, as a diff against `rendered`. An unedited
  send has no diff.
- **A terminal `/promptu` run as well as a chat-sent one.** A terminal run never
  appears as an owner message. Its prompt runs after "Send as is", or from the
  edited draft after "Edit first", so the pack finds it through the
  `AskUserQuestion` answer. The contract's match rule says how a sent prompt is
  matched to its run (decision 44).

Where to start: `src/state.rs` (`all_logs`, `LogEntry`: the run list and
`rendered`), `src/footer.rs` (`parse`), `src/used.rs` (`transcripts`,
`footers`: the transcript walk and what counts as an owner's message),
`src/prior.rs` (`scan`: reading `AskUserQuestion` answers), and
`docs/contract.md` §14 for the pack's shape, the week folder and the match rule.

Friction, unmatched task starts and outcomes are a separate unit (EMB-274) and
are not part of this one. Leave room for them in the pack, as the contract's
record shapes already do.

## Why now

The pack is the input to everything else in step 4: the drafter (EMB-276),
`week run` (EMB-277), the sheet's numbers (EMB-278) and `week apply` (EMB-279)
all wait on it.

**Burndown leg: no new numbered decision.** If the contract's record shapes turn
out to be wrong once they meet real code, fix the contract in this unit and say
so. A choice the contract and forks W1 to W9 leave open goes to
`docs/forks.md` as a new open fork with a provisional default, not to
`decisions/`.

## Done when

- [x] `promptu week pack` writes the week's pack in the week folder, one record per rendered run in the window.
- [x] A chat-sent run and a terminal run are each found, in invented transcript fixtures.
- [x] An edited send yields its diff against `rendered`; an unedited one yields none.
- [x] It makes no model call and no network call; tests use a scratch `CLAUDE_CONFIG_DIR`, `PROMPTU_STATE_DIR` and `PROMPTU_TODAY`.
- [x] `cargo test --all-targets` and `cargo clippy --all-targets -- -D warnings` pass. On a machine with a crowded `/tmp`, a failure of `claude::tests::a_folder_name_decodes_back_to_the_checkout_on_disk` is `promptu/012`'s (EMB-286), not this unit's: say so if it appears.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`open.md`/`interfaces.md` updated, and a `changelog.d/` fragment dropped.

## Result

Built `promptu week pack` for the `run` events (`src/week.rs`, `tests/week.rs`). Choices the task left open, all recorded as open forks with provisional defaults in the repo's `docs/forks.md`: W10 (the "Other" text is read from `runs/<run>.json` while it survives its 7 days), W11 (a draft counts as an edit only when it differs from `rendered`). Contract §14.4/14.5 amended: `edit` and `diff` sit on the run record, plus `skipped_questions`, `assumed_questions`, `not_recommended`, `other_text`; `sent.source` gains `terminal`. `prep`'s prune now keeps a draft until a pack covers its date, at most 35 days (W8).

**Not built here (EMB-274):** `session`, `unmatched`, `outcome`, `carried` events; they are counted 0.

**Known red, not this unit's:** `claude::tests::a_folder_name_decodes_back_to_the_checkout_on_disk` fails with the default `/tmp` (promptu/012, EMB-286); with `TMPDIR=/var/tmp/<own folder>` the whole suite passes (78 + 20 + 32 + 4).

**Unverified against real data:** the terminal match (a tool result showing the run id, then the next `Send as is` question) and the chat match were tested on invented transcripts only. The prune change has no test.
