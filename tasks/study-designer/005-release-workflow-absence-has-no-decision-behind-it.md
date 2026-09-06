# 005 — `crate.md` says the missing `release.yml` has "a separate decision behind it"; there is no such decision

**State:** claimed by agent/study-designer/005-release-workflow-decision, 2026-09-06 00:47
**Source:** `embarch-study-designer/open.md`'s last bullet — "**No `release.yml`**, so
`embarch-umbrella` decisions 27/29's `verify-version` job does not run here … unaddressed,
not deferred" — and `embarch-study-designer/decisions/crate.md:63`, which says the same
absence is "a separate absence with a separate decision behind it". Swept by leg 015,
2026-09-06.
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

Two files in this sub-project point at a decision about the missing release workflow. **The
decision does not exist**, and the other half of the pointer already answers it —
`embarch-umbrella/decisions/release.md` (27/29) closes with:

> The four sub-projects with no release workflow at all — `embarch-study-designer`,
> `embarch-dev-bench`, `embarch-outpost`, `embarch-ui` — still have none, so **"every repo"
> means every repo that releases.** Whichever gains a release workflow first inherits the
> obligation to copy this job.

So the umbrella side does *not* treat this as an outstanding obligation on this crate.
`open.md` says "unaddressed, not deferred"; `crate.md` says a decision explains it. **Both
cannot be right, and one of them is a reader's cue to go looking for something that is not
there.**

**Settle it inside this sub-project, with the argument written down.** The facts to weigh —
check each rather than taking them from here:

- `embarch-study-designer` has no `.github/workflows/release.yml` and **no git tags at
  all**; `Cargo.toml` is `version = "0.1.0"`.
- It is consumed only as a **sibling path dependency** — `embarch-core`, `embarch-api`,
  `embarch-ui`, `embarch-umbrella` and dev-bench firmware all reach it by relative path, not
  by a published version. Confirm this with
  `grep -rn 'path *= *"\.\.' --include=Cargo.toml` in the suite root.
- Decision 27/29's `verify-version` job asserts that a **pushed tag** agrees with
  `Cargo.toml`. A repo that never pushes a tag has nothing for it to assert.
- It *did* gain its first workflow ever last night (`test.yml`, decision 64), so "this crate
  has no CI" is no longer the reason.

## What the outcome has to look like

**Either** a decision saying this crate does not release, why, and the **reversal condition**
that would make it release — publication to crates.io, a consumer that depends on it by
version rather than by path, or a tag pushed for any reason — **and** the obligation
decision 27/29 already names, restated here so whoever pushes the first tag meets it at the
point they act. `open.md`'s bullet then closes and `crate.md:63` points at a real entry.

**Or** the workflow, if the argument comes out the other way — in which case copy
`verify-version` from `embarch-umbrella/decisions/release.md` and honour its three
deliberate choices (`awk` not `cargo metadata`; leading `v` stripped rather than required;
`workflow_dispatch` exits 0 with a reason).

**Do not resolve it by deleting the `open.md` bullet.** An absence that was argued about is
worth a reader knowing; an absence silently removed reads as an absence nobody noticed.
**And do not reach into `embarch-umbrella`** — 27/29 is another sub-project's entry and
already says what it needs to say. If you find it genuinely wrong, drop that in `inbox/`.

## Why now

`study-designer/004` just gave this crate its first CI and its `open.md` bullet on the
feature matrix; this is the sibling bullet in the same file, left explicitly "unaddressed,
not deferred". It is the last release-shaped loose end in the crate every other repo in the
suite compiles, and it is cheap — the expensive half is deciding, and the material to decide
with is listed above.

## Done when

- [ ] `embarch-study-designer` carries a decision that answers whether it releases, with the
      losing option argued against rather than merely listed, and a reversal condition.
- [ ] `decisions/crate.md:63`'s "a separate decision behind it" resolves to that entry.
- [ ] `open.md`'s `release.yml` bullet is closed by the decision, not deleted.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/study-designer-*`
      fragment dropped.
