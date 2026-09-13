# 036 — Two interface docs say `StreamRef` refused a fourth field, and it grew exactly that field

**State:** open
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

- [ ] `taps.md`'s paragraph no longer says the type refused a fourth field. **Keep the reasoning**,
      which is the durable half — why a free-text `note` was the wrong shape is still true, and
      `records` is not a `note`. The honest amendment says what was refused (an unstructured note)
      and what was later accepted instead (a structured `RecordReport`), and why those are
      different answers rather than a reversal. If on reading it you conclude it genuinely *is* a
      reversal, `embarch-decision-reversals.md` is **not this scope's to write** (`protocol.md`
      §3) — drop the row to `/home/gabriel/Github/embarch/embarch-doc/inbox/` by absolute path
      and say so in the task file.
- [ ] `types.md:69`'s enumeration names all four fields.
- [ ] Both claims re-derived from `src/streams.rs` as it is now, not from this task's quotes.
- [ ] Check whether any other doc in `embarch-study-designer/` enumerates `StreamRef`'s fields —
      `grep -rn 'StreamRef' embarch-doc/embarch-study-designer/` — and fix every instance or say
      why one was left.
- [ ] Gate green; `changelog.d/` fragment.

## Do not

Do not add, rename or reorder a field. This is a documentation correction to a type that is already
on the wire; changing the type is a different task with a different blast radius.
