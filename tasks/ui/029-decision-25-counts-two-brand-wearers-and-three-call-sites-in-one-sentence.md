# 029 — Decision 25 counts two `--brand` wearers and three call sites in the same sentence

**State:** claimed — leg 089, 2026-09-11.

**Doc-size reserve for `ui`:** nothing in this sub-project is in reserve. If your work pushes a file
into its last 10%, file `tasks/ui/<NNN>-compact-ui.md` in the same commit.
**Source:** refill sweep, leg 088, 2026-09-11. `embarch-ui/decisions/shell.md` decision 25 against
`embarch-ui/assets/style.css` and `assets/index.html`.
**Scope:** ui
**Hardware:** none.
**Owner:** no

## What

Decision 25 says: *"**`--brand` carries the mark's red and is worn by exactly two things** — the
sidebar wordmark and the header glyph — while `--accent` keeps every interactive surface. One token,
three call sites, no semantic collision."*

`var(--brand)` is referenced in exactly **two** places in the shipped assets:

- `assets/style.css:124` — `.sidebar-header .word { color: var(--brand); }`
- `assets/index.html:34` — the inline glyph's second `<path … fill="var(--brand)">`

The token is *declared* twice (`style.css:44` dark, `:73` light), which is the likeliest origin of
the three; `assets/brand/embarch-mark.svg` uses the literal `#e74c3c` rather than the token, and
`app.js` never mentions brand at all. So the sentence contradicts itself: two wearers, two call
sites.

## What to do

Fix the count, and **make it say which two it means** — a declaration and a use are different things
and conflating them is what produced the error. Decide and state whether the `.svg`'s literal
`#e74c3c` is a deliberate exception (a standalone file has no cascade to inherit a custom property
from) or a third site that should be the token; **say which in this file either way**, because a
future auditor will stop on it exactly as this sweep did.

## Why now

The decision's entire argument is that the brand token's blast radius is small and auditable. A
reader auditing for a third call site either hunts one that does not exist or concludes the token
leaked somewhere it did not — the audit the decision promises is the thing the wrong number breaks.

## Done when

- [x] The sentence's two counts agree with each other and with the source.
- [x] Declaration sites and call sites are not conflated.
- [x] The `.svg`'s literal colour is named as an exception or as work, with a reason.
- [x] No rendered colour changes.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.

## Resolution

Decision 25 rewritten: two declarations (`style.css:44` dark, `:73` light), two call sites
(`style.css:124` sidebar wordmark, `index.html:34` header glyph). `embarch-mark.svg`'s literal
`#e74c3c` is named explicitly as a deliberate exception, not a third call site — a standalone SVG
file has no cascade to inherit a custom property from. No CSS/HTML/SVG asset touched; doc-only
change.
