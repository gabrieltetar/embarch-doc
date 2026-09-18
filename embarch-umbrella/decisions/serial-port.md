# embarch-umbrella decisions: Serial port assignment stays out of `init`

**Status:** active, 2026-09-17.

**Split out of [projects.md](projects.md) on 2026-09-17 (`tasks/umbrella/081`), decision 55 moved
verbatim.** That file held 13, 17, 26, 41 and 55 at 12,286/12,288 B — 2 B left — and 55 is the
newest and most self-contained entry: unlike 13/17/41's shared subject (what `init` derives for
board and chip) and 26's (`doctor --prune`), 55 is the one place this sub-project states why a
*volatile, OS-assigned* fact gets different treatment from a hardware fact that merely needs
confirming. **Verification, and what it can't see.** A grep for the `[decision N](path)` link
shape found no inbound reference elsewhere in the suite naming `projects.md` for decision 55, so
the move looked like it needed no redirect. That grep cannot see the suite's other citation shape:
inline code with a parenthetical, ``` `embarch-umbrella decision 55` (`embarch-umbrella/decisions/projects.md`) ```.
One of those existed — `tasks/api/114`'s `**Source:**` line, since retired in this repo's
`ca564376` fold — and had cited `projects.md` this way since before this split ran.
`scripts/check-decision-refs.py`'s topic-file arm inspects only the link shape; its plain
per-reference arm resolves a bare `decision 55` against the sub-project, which still passes no
matter which file inside it holds the entry, so the gate stayed green over the stale pointer the
whole time. The supervisor repointed that citation at this file in this split's own fold, so it now
names the right file by accident rather than by having been checked; `tasks/doc/044` names the
general defect — a verbatim split is the one move this check structurally cannot see — and is
still open.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md); the referral
this closes is [`embarch-api/open.md`](../../embarch-api/open.md).

### 55 — `init` never writes `serial_port`: not a repo fact, present-tense state

`embarch-api`'s referral (`open.md`) names the gap correctly but as unowned. **It stays out, deliberately.** Decisions 17 and 41 refuse to scaffold board and chip as fact because both are hardware truths `init` cannot observe. A serial port fails that test *harder*: board and chip name a property of a unit that persists across a session; a `serial_port` is assigned by the host OS at enumeration and can renumber on a replug, a hub power cycle, or a reboot — no cable move needed to invalidate a value correct an hour earlier. Scaffolding it would be worse than the board-guessing 17 replaced: that guess went wrong only on the wrong repo build; a written port goes wrong on a schedule `init` cannot predict, and TOML cannot say "as of enumeration N."

**The remedy already exists on the other side of this boundary.** `embarch-api` decision 70's `list_serial_ports` answers this at call time; its interface doc already names the case: discover a value for `serial_log`'s `port` when a project has none configured. `serial_log` takes `port` per call, falling back to the configured value only when set — the shape decision 17 gave `chip`: resolved per call, not stored. Setting `serial_port` stays available for a caller wanting a stable default willing to re-edit after a replug; `init` just never guesses it in.
