# 015 — The retired-`[[projects.targets]]` load error tells a `zephyr-west` project to store the three fields decision 12 removed

**State:** claimed by agent/api/015-retired-targets-error-misadvises-zephyr, 2026-09-05 18:10
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

- [ ] A `zephyr-west` project declaring `[[projects.targets]]` is refused with
      advice it can actually follow — not "set build_command/chip/artifact_path",
      which the same `validate()` rejects on the next branch.
- [ ] A `static` project's message is unchanged, or equivalently truthful.
- [ ] `a_zephyr_west_project_is_refused_the_retired_menu_too` asserts on the
      advice, not only on the word "retired", so the two branches cannot drift.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
