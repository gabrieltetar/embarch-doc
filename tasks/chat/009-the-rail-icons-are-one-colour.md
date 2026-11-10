# 009 — The chat rail's icons are one-colour SVGs, not colour emoji

**State:** claimed by agent/chat/009-the-rail-icons-are-one-colour, 2026-11-09 17:52
**Source:** Linear issue EMB-56, filed by the owner — the owner changing his own earlier pick
**Issue:** EMB-56
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

Each entry on the chat's left rail (the 30 px column, decision 94) is a one-colour inline SVG drawn in `currentColor`, so it follows the theme's foreground colour. Lit and unlit differ by opacity or the theme's active colour, never by a CSS filter on a colour image.

Today the rail draws its entries as emoji text — 📊 Usage, 🧠 Memory, ✨ Promptu, 📚 Library, 💡 Suggestions — and fakes their states with filters: unlit is `grayscale(1)` (and `opacity: .7` for Promptu), Memory `grayscale(0.4)`, lit states add a `drop-shadow`.

## Why now

Decision 94 and `embarch-promptu` decision 40 record the emoji as the owner's pick; this is the owner changing it. Decision 54 already gives the status bar and sidebar a one-colour mark, so the rail is the one coloured spot left, and it clashes with the rest of VS Code.

## Where to look

- `webview/chat/composer.tsx` — the block that portals the rail entries into the rail
- `webview/chat/rail.tsx` `RailEntry` — renders `icon: string` as text today
- `webview/chat/tools.tsx` `Glyph` — already draws a one-colour inline SVG in `currentColor`; reuse its approach
- `webview/shared/style.css` — `.rail-icon`, and the grayscale and drop-shadow rules for `.bulb`, Promptu, Memory and Usage
- `test/webview.e2e.mjs` — the rail tests

## Dispatch notes

- **`embarch-promptu` decision 40 is not yours to amend** — it is another sub-project's doc. `tasks/promptu/003` amends it once this lands. Amend `embarch-chat` decision 94 here, and say in it that the promptu side follows in that task.
- When this lands, `tasks/promptu/003` unparks: the folding supervisor sets it `open` in the same fold.
- No `embarch-chat` doc is in reserve at the split.

## Done when

- [ ] No rail entry renders an emoji; each is an SVG in `currentColor`, readable in a light and a dark theme.
- [ ] Lit and unlit states stay distinguishable without CSS filters.
- [ ] Decision 94 is amended, and `embarch-chat/spec.md` and `interfaces.md` no longer name the emoji.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
