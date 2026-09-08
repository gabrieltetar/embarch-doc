# `ValidateResponse` now hard-requires a Core new enough to send `validated_at_utc_ms`

**State:** claimed by agent/api/046-older-core-parse-rule, 2026-09-07 19:20
**Source:** `tasks/api/045` (leg 043), raised by me at the merge diff and
independently by that unit's reviewer, which found no decision either way and
correctly declined to file it as a contradiction.
**Scope:** api
**Hardware:** none

## What

`api/045` added `validated_at_utc_ms` to
`crates/embarch-core-client/src/client.rs`'s `ValidateResponse` as a **required**
serde field. It mirrors `embarch-core`'s `ValidateOkResponse` exactly, which is
right, and every gate passed.

But this same file carries an explicit precedent going the other way. At least
two fields — `link_port_interface` and `study_designer_schema_version` — are
`#[serde(default)]`, and a test near the end of `client.rs` asserts in so many
words that *an older Core that predates `link_port_interface` still parses*. So
the crate has, at least twice, chosen to keep deserializing a Core that predates
a field. `validate` now does the opposite: against an `embarch-core` older than
`tasks/core/026` (merged `b0bf60d`), **every** `validate` call fails at
deserialization rather than coming back with the one timestamp that Core does
send.

**This is not hypothetical on this machine.** The live Core is a deployed
Windows service and `embarch-api` is built separately; the two are not
guaranteed to move together, and "the MCP binary goes stale after a schema bump"
is already a recorded gotcha. A rebuilt `embarch-api` against a
not-yet-redeployed Core is the exact configuration this breaks, and the failure
is a parse error rather than a missing field — which reads like a broken client,
not a version skew.

## The question, which is the point of the task

**Does `embarch-core-client` promise to parse an older `embarch-core`?** The
reviewer looked in `embarch-api/decisions/core-link.md` and `spec.md` and found
no decision stating one way or the other, so today it is a per-field judgement
call made three times with two different answers. That is the defect: not the
missing `#[serde(default)]`, but that nothing says whether it should be there.

The task as filed offered two honest answers. **The supervisor has decided it,
and the answer is "yes" — do not re-litigate it, implement it.** The reason it
is decided here rather than left to you is that the evidence is not two data
points, it is fourteen, and the filer only had two:

**`client.rs` carries 14 `#[serde(default)]` fields and every single one of them
is `Option<T>`.** Not one is a bare value with a zero default. Alongside them
sits `an_older_core_body_missing_link_port_interface_still_parses`, a test whose
name is the rule stated out loud. `validated_at_utc_ms` as a bare required `u64`
is the **only** anomaly in the file. So this is not a per-field judgement call
that has been made three times with two different answers; it is a convention
expressed fourteen times, one test, and a single field that missed it.

**Verify that count yourself before you write the decision on it** — `grep -c
'serde(default)' crates/embarch-core-client/src/client.rs` and check the shapes.
It was 14 at `a687baf`. If you find it is not, the decision's reasoning changes
and you should say so rather than write a number you did not confirm.

So:

- `ValidateResponse::validated_at_utc_ms` becomes `Option<u64>` with
  `#[serde(default)]`, matching all fourteen precedents in **shape**, not merely
  in having a default. `0` is explicitly rejected: a fabricated "validated at
  1970" is worse than the parse error it replaces, and no other field in the
  file takes that shape.
- The decision names the convention as a **rule of the crate**, not as this
  field's exception, and cites `link_port_interface` and
  `study_designer_schema_version` as the named precedents plus the test as the
  thing that already asserted it.

## Scope, and what is deliberately not in it

- **`tasks/api/044` is out of scope.** It changes the `hardware_id` spelling in
  this same struct in this same file. Two wire-shape changes in one diff is how
  a revert stops being possible. Do not touch it, do not "while I am here" it.
- **Do not change `embarch-core`.** Core is right; it sends the field. This unit
  is entirely about what the client tolerates.
- **Do not add a version-negotiation mechanism.** The decision is "the client
  parses an older Core, field by field, via `Option` + default". Anything larger
  is a different task.

## The two surfaces, and the trap in them

`api/045` added exactly two readers, and both will silently do the wrong thing
if you only change the struct:

- `src/cli.rs:743` puts `resp.validated_at_utc_ms` into a JSON object, and
  `:746-747` formats a human line reading
  `validated_at_utc_ms {}, enrolled/confirmed_at_utc_ms {}`.
- `src/tools.rs:843` puts it into the MCP tool's JSON result.

For the JSON surfaces, an `Option` serialising to `null` is honest and is
probably right — but **decide it and say why**, because a consumer that reads
the key and gets `null` needs to know that means "this Core did not report it"
and not "it validated at an unknown time". For the human line, `None` must never
reach the output: say *not reported by this Core* (or wording you prefer) in
words. Check whether `tools.rs:830`'s long tool description — which currently
tells the caller to "read the latter for freshness" — is still true when the
field can be absent, and amend it if not.

## Why now

Not urgent — nothing is broken against a current Core, and `api/045` is not
wrong. It is filed while the context that produced the question still exists,
which is the only cheap moment to file it.

## Done when

- [ ] An `embarch-api` decision states that `embarch-core-client` parses an
      older Core's responses field-by-field via `#[serde(default)]` on an
      `Option`, on the evidence above — the 14 existing fields, their uniform
      `Option` shape, and the test that already asserts it. Name
      `link_port_interface` and `study_designer_schema_version` explicitly, so
      they stop being precedent nobody cited.
      **Decision numbers are global across `decisions/*.md`, not per file.**
      The directory maximum was **57** at `a687baf`, so yours is **58** — verify
      with `grep -rn '^### [0-9]' decisions/` before you use it.
- [ ] `ValidateResponse::validated_at_utc_ms` is `Option<u64>` with
      `#[serde(default)]`.
- [ ] Neither the CLI nor the MCP tool prints a fabricated timestamp for a Core
      that never sent one, and the human-readable line says so in words.
- [ ] A test pins the **absent** case, mirroring
      `an_older_core_body_missing_link_port_interface_still_parses` — a
      `validate` body with no `validated_at_utc_ms` parses and yields `None`.
      The existing test at `client.rs:1709` pins the present case; leave it
      working (it will need `Some(...)`).

## The reserve, and why the split is not blocked

`embarch-api/decisions/core-link.md` is **12,266 / 12,288 B — 22 bytes**, the
tightest file in the suite, and its compaction task `tasks/api/026` is parked
`In flux: yes`. **You cannot write decision 58 into it as it stands, and
compacting it is part of this unit** (`DOC-COMPACTION.md` §2).

**Read `tasks/api/026` before you do anything to that file.** It has already
worked out the move and it is not a shortening:

> *The move is a split, not a shortening, and the split is not blocked.* … This
> file already carries six unrelated missions … Splitting the event stream
> (48, 49) out is the obvious cut: it is the flux, and it is the half a live run
> will rewrite.

A **verbatim** move states nothing new, so `In flux: yes` does not forbid it —
`api/023` did exactly this to `shape.md`. So: move decisions 48 and 49 verbatim
into a new topic file, update the index, and write 58 into the room that frees.
**Do not shorten any remaining entry** — actual compaction waits on
`tasks/api/001`, and `api/026` carries a `Must not delete:` list you must honour
in full. Close only `core-link.md`'s item in `api/026`; that task stays
`blocked` for `spec.md` and `open.md`.

**Other `api` files in reserve** (do not spend these): `decisions/surface.md`
11,873 / 12,288 — 415 B, parked under `tasks/api/043`. `spec.md` 9,087 / 10,240
and `open.md` 4,734 / 5,120 are both filed under `api/026`. If your work pushes
any file into reserve that nothing has filed, file
`tasks/api/<NNN>-compact-api.md` in the same commit.
