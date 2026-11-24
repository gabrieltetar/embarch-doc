# 113 — The Desk tab draws Promptu's weekly sheet, with its ✓/✕, notes, feel line and Apply

**State:** open
**Source:** `embarch-desk` decision 65 (the Desk tab's spot left empty for a Promptu section, and the four `/promptu` routes `desk/042` added); `embarch-promptu` decisions 14 and 30 and `docs/contract.md` §9 (`promptu desk --json`) and §10 (the sheet); the Desk row of `spec/tabs.md`
**Issue:** EMB-283
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

The Desk tab keeps an empty spot in `.desk-bar` for a Promptu section. The
owner approves the weekly sheet there. When this is done:

- **The bar**: this week and how many lines wait, from `GET /promptu`
  (`{promptu, open, ...}`), shown only while `open` is above zero. With
  `open: 0`, or no Promptu, the section takes no space on the tab.
- **The panel**, opened from the bar, drawn from `GET /promptu/sheet`
  (`week show --json`, contract §10): the numbers first, read-only (a `null`
  value shown as no data, never zero); then each group with its own ✕ and its
  line count; each line with ✓/✕ and a note field; then the
  *better · same · worse* feel line.
- **Marks**: a line's or a group's ✓/✕ posts
  `POST /promptu/sheet/{week}/{id}` with `{"verdict": "approve" | "cut",
  "note"?}` (a group id is `g1`, a line id `l1`); a note goes with its line's
  mark. **The feel line** posts `POST /promptu/feel/{week}` with
  `{"feel": "better" | "same" | "worse"}` — a route `desk/043` adds in the
  same wave, so build against this shape and a stubbed desk.
- **Apply ✓ (n)** posts `POST /promptu/apply/{week}` and shows each line's
  result. A line that failed stays open with its `error` shown.
- **An error is shown in the desk's words**: a 400 carries Promptu's own
  message, a 503 names the missing binary, and the panel stays usable.
- Every call goes through this server's `/api/desk/{*rest}`, as the rest of
  the tab does.

Where to start: `assets/index.html` (the comment "Left empty for a Promptu
section" in `.desk-bar`), `assets/desk.js`, `assets/style.css`,
`tests/browser/drive_desk.py`, and the promptu contract §10 for the sheet's
fields. Read `embarch-desk` and `embarch-promptu`; edit neither.

## Why now

`desk/042` landed the routes the section reads, so the empty spot can be
filled. EMB-283.

**Burndown leg: no new numbered decision.** Amend the Desk tab's decision in
place where it changes, and the Desk row of `spec/tabs.md`. If the work needs
a new decision, stop and say so in this file and in your report.

**Doc size, a dispatch note (supervisor):** no `embarch-ui` file is in
reserve. Decisions within 256 B of their limit, so name them if you touch
them: `tab-folders` 100 (113 B left), `launcher` 28 (22 B), `topology-tab`
10 and 43, `trace-*`, `gatt-capture` 17.

## Done when

- [ ] With `open: 0` the section takes no space on the tab.
- [ ] The browser drive marks a line ✕, adds a note, cuts a group, sets the feel line and applies, against a stubbed desk, and checks each request's path and body.
- [ ] A failed line shows its error and stays open after Apply.
- [ ] `spec/tabs.md`'s Desk row says what the section does.
- [ ] Gate green (`../../embarch-fleet/gate.md`), with `cargo test` and `cargo clippy --all-targets -- -D warnings`.
- [ ] `changelog.d/` fragment dropped.
