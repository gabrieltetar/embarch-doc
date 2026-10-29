# embarch-ui decisions: Building a study's own firmware

**Status:** active, 2026-09-18.

The Build card, the ordered snippet picker, the outpost mode declaration, the build as a phase of a run, and where a build log is read afterwards. The half of [study-designer.md](study-designer.md) decision 11 this reverses is stated there and in [reversals](../../embarch-decision-reversals.md) row 113.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The shared crate this rests on: [`embarch-api` decision 78](../../embarch-api/decisions/firmware-build-crate.md). What a study stores: [`embarch-study-designer` decision 77](../../embarch-study-designer/decisions.md). What Core checks before step 1: [`embarch-core` decision 74](../../embarch-core/decisions.md).

### 38 — A study carries a build spec, the picker is ordered, and the mode is three-state

**Off by default, and stated as a choice.** Flashing is the destructive half, and a study that only observes a board somebody just flashed by hand must not silently overwrite it — the same posture `ReflashTarget::None` already takes in the CLI.

**Three places a project config is looked for, and the third is what makes the card work at all**: this UI's own `[build].config_path`, then `EMBARCH_API_CONFIG`, then the **open repo's own `embarch/embarch.toml`** — `embarch-api`'s documented fallback, asked of the repo this tab has open rather than of a working directory. The VS Code extension sets only `EMBARCH_UI_CONFIG`, so without the third the card was unavailable on every bench not hand-edited for it: **the feature shipped inert**, [reversals](../../embarch-decision-reversals.md) row 33's shape, caught by launching the binary.

**An unbuildable bench gets the reason, not a dead toggle.** The configured project is matched **by path**: this tab already knows which repo is open (decision 14) and `embarch-api`'s config says which repo each project is, so asking again would mean keeping two answers in step, and getting it wrong builds a different repo than the one whose studies are on screen. No match or no config is `available: false` with a sentence — a `500` from a survey would take the tab down over a feature nobody asked for. **The survey runs even with no project open**, because "no project" is an answer; without it the card sat on "checking…" forever, reading as a hung request.

**The snippet picker is an ordered list with move-up/move-down, not checkboxes.** West applies `-S` in order, and [reversals](../../embarch-decision-reversals.md) row 114 is where order is the whole difference: the BLE-shell snippet re-points the shell backend and switches the traced UART off, so an outpost overlay applied first loses the tracer its UART. **This lands after the resolver stopped sorting** — on a sorting resolver a set-shaped picker would be a control that does nothing, and an ordered one a lie.

**The outpost mode is three states per flag** — don't care, must be set, must be clear — because a clear flag can be the requirement, `trace_self` the standing case. Flag names come from the server, out of `HeaderFlags::NAMED`, so the picker cannot disagree with the refusal an engineer reads. **A mode requirement is sent whether or not the build toggle is on**: it states the firmware a study needs, not who built it.

**A run with a build phase cannot be one request.** `POST …/run` returns `{build_id}` at once and the build runs in a background task publishing to `GET /api/build/events`: tens of seconds of `west` behind a spinner is not a progress display, and the owner asked for the log to be a *phase of the run*, which it can only be if it arrives live. The browser follows the stream and takes the study id from its terminal frame. A run with no build spec is unchanged — synchronous, `{study_id}`.

**The build card stays on screen after the study starts**, because what was flashed is part of reading the run. A browser that falls behind the broadcast is told so and pointed at the whole log, not left with a card that looks complete.

**A failed build leaves its error on screen, and the banner names it.** The console's cap drops oldest-first, so a trailing compiler error is never the line scrolled away — confirmed by breaking a real build. That run found the banner reading *"west exited Some(1)"* with the compiler's error 35 lines up; it now quotes that error via `BuildOutcome::failure_reason` (`embarch-api` decision 79), so the line read first is the line worth reading.

### 39 — A build log is kept locally and read as a third Debug source, not uploaded to Core

Two places, because they answer different questions: live, so a build in progress is watchable; durably, so a build from an hour ago is readable at all.

**The durable copy is a file under the per-user data directory, beside `embarch-api`'s own rolling logfile, and this tab reads it directly.** That is decision 13's exception applied unchanged — decision 7's never-read-a-logfile rule is about **Core**, which can run on another machine; this file's writer is this process, on the machine the browser is open on.

***Rejected: uploading it to Core with the study's results.*** It would make provenance complete, at the cost of a new route, a new on-disk artifact and a retention rule — and what actually establishes which firmware a run used is the outpost header Core reads in its own pre-flight, not the text of a compiler's output. The build ran here; Core never saw it.

**A third source on the Debug tab, not a Builds tab.** That tab is already the thing that switches between log sources, and a build log is a log; another section in a shell whose section list is decision 4's would be a larger change than the feature. It is **stored, not tailed** — a finished build's log does not change — so it carries no SSE stream and brings its own picker, which the other two sources have nothing to pick with. Pruned to fifty: a log is evidence about a run that already happened, and an unbounded directory is a slow leak nobody notices.

### 40 — A saved study's `firmware_version` is rewritten only when a mismatch was waved through, and never over `any`

The build refuses before it starts when the working tree is not at the revision the study requires — so in the ordinary case the two already agree and there is nothing to write. What is left is the case worth automating: a study pinned to a revision the tree has moved past, run anyway on purpose. Writing the built version back is what stops that study asking the same stale question tomorrow.

**`any` is exempt, and that is decision 11's own rule rather than a special case.** `any` is a deliberate statement that the build does not matter; silently converting it into a pin would erase the distinction the whole of `embarch-study-designer` decision 40 rests on — the same harm as promoting a blank field to `any`, in the other direction.

**The file is edited as parsed JSON, not re-serialized from the `Study`.** It also carries `_embarch_ui_rows` and `_embarch_ui_taps`, the sidecars that make it loadable back into the table, and rewriting it from the runnable study alone would quietly turn an editable study into one the editor refuses with a `409`. None of the three seals cover `requires`, so nothing needs resealing. **An authored study that was never saved gets no write**, because there is no file, and inventing one would be saving a study nobody asked to save.

### 62 — The build log says which board it built and why, on every path, and the stored log keeps what the run said

Decision 45 says the role wins "and the build log says so". It said so only when the role resolved. `role_target` returned `None` for three different causes — no board type in the role, a board type the catalog does not list, a catalog that would not load — and the caller then built the study's own board with no line at all. It now returns the cause (`RoleMiss`), and `choose_board` writes **one line for every path**: what the study stored, what the role holds, what is built, and which won. A role that agrees with the study says so; a role on the same board that replaced the study's variant or revision names the axis it replaced (the case the old "building for the DUT role's board" hid); a role that could not decide says why and that the study's own board is used.

**The stored log keeps the run's own lines.** Every `info` line (version, board choice, flashing, flashed, reset, and a flash or reset failure) goes into the file with an `[embarch-ui] ` marker, so a log read an hour later says why it built what it did. Lines before the build are in the body written after it; lines after it (flash, reset, their failures) are appended.

**The file name and header keep the build's own verdict** (`ok`/`failed`), as decision 39 says a build log is a log. How the run *ended* is told in the last lines of the body, not in the name: a build that compiled and then failed to flash is `-ok.log` ending in `flash failed: …`. The alternative, renaming the file after the flash, would make the listing's `ok` mean "the run worked" while the header still said "result: ok" for a build, two meanings for one word.

Measured: unit tests for each branch, and `tests/browser/drive_build.py` drives a real run through a stub `west` and stub Core and reads the line back from the Debug tab's builds source.
