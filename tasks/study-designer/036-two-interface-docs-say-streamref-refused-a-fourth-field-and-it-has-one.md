# 036 — Two interface docs say `StreamRef` refused a fourth field, and it grew exactly that field

**State:** done — landed by agent/study-designer/036-streamref-fourth-field, 2026-09-13
**Source:** leg 106 refill sweep, 2026-09-13, scout-verified on both sides. Every file:line below was
read by the scout; re-check them rather than trusting the quotes.
**Scope:** study-designer
**Hardware:** none — two documentation paragraphs. No code change, no wire change, no board.
**Owner:** no

## What

`StreamRef` has **four** fields. `src/streams.rs:330-352` carries `name`, `bytes_written`,
`truncated` and — added 2026-09-08, `git log -1 -S "pub records" -- src/streams.rs` → `7f168fd` —
`pub records: Option<crate::records::RecordReport>` at `:351`.

Two interface docs still describe the three-field type, and the first does more than omit the
fourth: it states that growing one was **refused**.

**(a) `embarch-study-designer/interfaces/taps.md:21`** — *"**`StreamRef` deliberately did not grow a
`note` field** … `truncated` stays the one thing this type says about incompleteness."*

That is now false in the one way that matters. `records`' own doc comment at `src/streams.rs:346`
reads *"This is the end-to-end statement `truncated` cannot make"* — precisely the shape the
paragraph says was turned down. A reader who trusts taps.md concludes the field does not exist and
that asking for it has already been answered no.

**(b) `embarch-study-designer/interfaces/types.md:69`** — *"`streams` carries one `StreamRef { name,
bytes_written, truncated }` per declared tap"*. A plain enumeration that is one short.

## Why now

`taps.md` carries `Status: active, 2026-09-02` and the field landed 2026-09-08, so the paragraph
pre-dates the change rather than disagreeing with it on purpose. No gate can see this:
`check-decision-refs.py` resolves decision numbers and `check-links.py` resolves links — a prose
claim about a struct's field list is neither.

## Done when

- [x] `taps.md`'s paragraph no longer says the type refused a fourth field. **Keep the reasoning**,
      which is the durable half — why a free-text `note` was the wrong shape is still true, and
      `records` is not a `note`. The honest amendment says what was refused (an unstructured note)
      and what was later accepted instead (a structured `RecordReport`), and why those are
      different answers rather than a reversal. If on reading it you conclude it genuinely *is* a
      reversal, `embarch-decision-reversals.md` is **not this scope's to write** (`protocol.md`
      §3) — drop the row to `/home/gabriel/Github/embarch/embarch-doc/inbox/` by absolute path
      and say so in the task file.

      **Not a reversal.** No numbered decision refused a `note` field — only this file's own
      prose did — so there is nothing for `embarch-decision-reversals.md` to record and nothing
      dropped to `inbox/`. The amended paragraph keeps the original reasoning (free text with no
      defined shape isn't a fact a caller can rely on the way it relies on `truncated`, and Core's
      own index is where that kind of ad hoc thing belongs) and adds that `records` answers a
      different question — a structured, checksum-backed verdict `truncated` cannot make, decided
      by decision 70 — rather than the same question decided the other way.
- [x] `types.md:69`'s enumeration names all four fields. Also added a one-sentence gloss on what
      `records`/`None` means, cross-referencing `taps.md` and decision 70.
- [x] Both claims re-derived from `src/streams.rs` as it is now (`:330-352`), not from this task's
      quotes. `records: Option<crate::records::RecordReport>` at `:351` confirmed; doc comment at
      `:346-349` ("This is the end-to-end statement `truncated` cannot make...") is what the
      amended `taps.md` paragraph now paraphrases.
- [x] Check whether any other doc in `embarch-study-designer/` enumerates `StreamRef`'s fields —
      `grep -rn 'StreamRef' embarch-doc/embarch-study-designer/` — and fix every instance or say
      why one was left. Only three hits total: `taps.md:21` and `types.md:69` (both fixed) and
      `interfaces/limits.md:24`, which cites `StreamRef.name` for `MAX_STREAM_NAME_LEN` and does
      not enumerate the type's fields — left as is.
- [x] Gate green; `changelog.d/` fragment. `cargo build`/`test`/`clippy --all-targets -- -D
      warnings` all green in `embarch-study-designer` (unchanged by this doc-only task, single
      `Cargo.toml`, no nested crate to miss); `check-client-names.py`, `check-docs.py` (11/11) and
      `check-ownership.py --scope study-designer` all green on this branch.

`types.md` crossed into its last-10% reserve (91.6%, 1037 B left) from the field-list fix and
gloss added here; filed `tasks/study-designer/037-compact-study-designer.md` (blocked, `In flux:
yes`) in this same commit per the task brief.

## Do not

Do not add, rename or reorder a field. This is a documentation correction to a type that is already
on the wire; changing the type is a different task with a different blast radius.
