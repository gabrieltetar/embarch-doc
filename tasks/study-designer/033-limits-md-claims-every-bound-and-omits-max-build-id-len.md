# 033 — `interfaces/limits.md` claims "every bound the crate declares" and omits `MAX_BUILD_ID_LEN`

**State:** open
**Source:** leg 101's refill sweep, 2026-09-12. Verified by diffing all 47 `pub const MAX_*` in
`src/` against both tables.
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-study-designer/interfaces/limits.md:5` states its own contract:

> **Every bound the crate declares**, each marked `[measured <date>]` or `[assumed]`.

and `spec.md:29` restates it: *"Every bound is disclosed, and exceeding one is a named error naming
the bound actually exceeded."*

Its two tables list **46** constants. The crate declares **47**. The one with no row is
`embarch-study-designer/src/outpost.rs:77-79`:

```rust
/// The longest string the firmware will put in a header frame
/// (`CONFIG_EMBARCH_OUTPOST_BUILD_ID_MAX`'s own range maximum).
pub const MAX_BUILD_ID_LEN: usize = 128;
```

It is not an internal detail: it sizes two **public wire fields** on `OutpostHeader`
(`src/outpost.rs:211-212`), `pub outpost_version: HString<MAX_BUILD_ID_LEN>` and
`pub build_id: HString<MAX_BUILD_ID_LEN>` — a frame a host decodes. It appears nowhere in
`embarch-doc/embarch-study-designer/`.

Every *other* row was checked in both directions: each doc row has a matching constant at the stated
value, and every other constant has a row.

## Why now

`limits.md` is one of the few docs in this suite that makes a **completeness** claim rather than a
descriptive one, which is what makes a single omission a defect rather than a gap. A reader trusting
that sentence concludes there is no bound on the build-ID string, and the bound is the one that
matters most to a decoder, because a header frame is the first thing it reads.

## Done when

- [ ] `MAX_BUILD_ID_LEN` has a row in the first table of `interfaces/limits.md`, naming the two
      `OutpostHeader` fields it sizes.
- [ ] **Its provenance marker is right, and this is the judgement call in the unit.** It is neither
      `[measured]` nor plainly `[assumed]` — it mirrors `CONFIG_EMBARCH_OUTPOST_BUILD_ID_MAX`'s range
      maximum, i.e. it is **derived from another repo's Kconfig**, which no other row is. Read how
      `limits.md` marks the closest existing case before inventing a fourth marker; if none fits,
      say the derivation in the row's own text rather than in a new marker, and say in your report
      that you chose that. **Do not author a new numbered decision for this** — it is a table row.
- [ ] Confirm the value against `embarch-outpost`'s Kconfig rather than trusting the comment: the
      comment says "range maximum", and a mirrored constant that has drifted is the more interesting
      version of this defect. Say which you found.
- [ ] The two sets match with nothing left over on either side:
      ```
      grep -rhoE "pub const MAX_[A-Z0-9_]+" src/ | sort -u
      ```
      against the constant column of `interfaces/limits.md`.
- [ ] `embarch-study-designer` `cargo build` / `test` / `clippy --all-targets -- -D warnings` green.
- [ ] `changelog.d/` fragment.

**Doc-size note:** `embarch-study-designer/spec.md` (91.3%, 890 B left) and `open.md` (91.0%, 461 B
left) are both in reserve, filed against the **blocked** `tasks/study-designer/032` and `026`.
`interfaces/limits.md` is not in reserve, so one table row is affordable — check it against its cap
before you write. If your row leaves any `embarch-study-designer` doc in reserve unfiled, file
`tasks/study-designer/NNN-compact-study-designer.md` in the same commit. Your own scope only, never
`tasks/doc/`.
