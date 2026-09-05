# 015 — The retired-`[[projects.targets]]` load error tells a `zephyr-west` project to store the three fields decision 12 removed

**State:** done, 2026-09-05, on agent/api/015-retired-targets-error-misadvises-zephyr
**Source:** review of `api/010-static-project-target-menu` (`embarch-api` `863f187`, `embarch-doc` `f46fb80`) against `embarch-api` decision 12
**Scope:** api
**Hardware:** none

## What

`embarch-api/src/config.rs:395-411` — decision 53's new load-time refusal — bails
for **either** discovery kind with:

> project '{}' declares [[projects.targets]], which is retired. […] **Declare one
> [[projects]] entry per target instead, each with its own
> name/build_command/chip/artifact_path**; a Zephyr/west repo can set
> discovery = "zephyr-west" and have its targets discovered live per call

That check sits *above* the `match project.discovery` block, so a
`discovery = "zephyr-west"` project carrying rows gets this text. Its advice is
refused thirty lines later by the same function
(`src/config.rs`, `Discovery::ZephyrWest` arm):

> project '{}' (discovery = "zephyr-west") must not set
> build_command/chip/artifact_path — these are resolved per call instead

and its escape clause ("a Zephyr/west repo can set `discovery = "zephyr-west"`")
is a no-op for a reader who already has.

The fix is the message, not the check: branch the advice on `project.discovery`,
or move the `retired_targets` check inside the existing `match`. Both refusals
should stay.

## Why now

**Which decision.** `embarch-api` decision 12
(`embarch-api/decisions/zephyr.md`), left standing and untouched by this diff:

> a `zephyr-west` project stores only what cannot be derived from the repo, and
> board, variant, revision, app, **chip, build directory and artifact path all
> resolve live per call, never cached**: caching would reintroduce the exact
> staleness this exists to eliminate.

**Which hunk.** `embarch-api/src/config.rs:395-411` (added by `863f187`), the
`bail!` inside `if !project.retired_targets.is_empty()`.

**Why a contradiction rather than a refinement.** Decision 12 exists to stop a
Zephyr repo's targets being snapshotted into config as
`build_command`/`chip`/`artifact_path` rows, and this message instructs a Zephyr
repo's operator to do exactly that, one `[[projects]]` entry per target — the
hand-authored static schema decision 12 removed, re-proposed as remediation
advice. Decision 53 itself does not contradict 12; only the text a caller reads
does, which is the half decision 51 closed by making surface text mechanical
("the tool descriptions, CLI help and `config.example.toml` now say *refused*
rather than *ignored* — decision 44's own lesson that the surface text is what a
caller reads").

**Why the gate could not see it.** The commit's own
`a_zephyr_west_project_is_refused_the_retired_menu_too`
(`embarch-api/src/config.rs`) asserts only `contains("retired")`, so the
zephyr-west branch is covered for *that it refuses* and not for *what it advises*
— reversals shape 8, the comment naming the right invariant while the text does
not implement it.

**What it would take to undo.** Merge SHA `863f187`
(`embarch-api`); `git revert --no-commit 863f187` applies cleanly against
current `main` (`863f187` is tip). **A revert is the wrong remedy** — it would
restore the menu decision 53 correctly retired. This is a message-only fix.

## Done when

- [x] A `zephyr-west` project declaring `[[projects.targets]]` is refused with
      advice it can actually follow — not "set build_command/chip/artifact_path",
      which the same `validate()` rejects on the next branch.
- [x] A `static` project's message is unchanged, or equivalently truthful.
- [x] `a_zephyr_west_project_is_refused_the_retired_menu_too` asserts on the
      advice, not only on the word "retired", so the two branches cannot drift.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## What shipped

`embarch-api/src/config.rs` — the `retired_targets` refusal stays **one check
above** the `match project.discovery`, and only its remediation branches. Chosen
over moving the check into the two arms: the refusal is one invariant of decision
53, it must fire before the per-kind field errors so a config carrying both hears
about the retired menu first, and duplicating the `is_empty()` condition into two
arms is exactly how the two texts drift apart again.

A `zephyr-west` caller now reads: *"…which is retired. Nothing ever selected a
row. This project already discovers its targets live from the repo on every call,
so the rows were a second, stale copy of what west reports. Delete them: a caller
picks a target with board/variant/revision/app on the call itself, and
[projects.default_target] sets the one used when a call names none. Do not move
them into build_command/chip/artifact_path — a discovery = \"zephyr-west\"
project is refused those three fields outright, because caching them is the
staleness this discovery kind exists to eliminate."* The `static` message is
unchanged in substance; its first clause is re-punctuated by the split.

Both tests now assert the **advice**. `a_retired_projects_targets_menu_is_refused_by_name`
pins `Declare one [[projects]] entry per target` and
`name/build_command/chip/artifact_path`;
`a_zephyr_west_project_is_refused_the_retired_menu_too` pins `discovers its
targets live`, `board/variant/revision/app on the call itself` and
`[projects.default_target]`, asserts the **absence** of the static remedy's
pinned phrase, and — stronger than a phrase check — asserts that if the message
names `build_command` at all it does so only under the explicit prohibition. A
future shared tail therefore fails a test rather than shipping.

Docs: decision 53 (`embarch-api/decisions/shape.md`) records the branched
remediation, why the check stays above the match, and why the gate was blind;
`embarch-api/interfaces/config.md`'s `[[projects.targets]]` row now branches its
advice too (row shortened to keep that file out of the doc-size reserve — 11,040
of 12,288 B, 89.8%). `spec.md` needed no edit and was not touched: its sentence
says the menu is retired and refused at load, which stays true.

**A reversals row may be owed** and is not a worker's to write — reported to the
supervisor rather than filed here.
