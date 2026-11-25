# embarch-ui decisions: Confirm tab

**Status:** active, 2026-11-25.

The tab where the engineer confirms a test input on Core's own card. The prompt modal it sits beside: [operator-prompt.md](operator-prompt.md) (69). The person's token: [core-token.md](core-token.md) (103). Index: [../decisions.md](../decisions.md).

### 110 — The Confirm tab draws Core's card for each pending definition as text and confirms with the person's token and the card's nonce

A confirmation is the engineer's act, on exactly what Core recorded (`notes/hil/12-prevention.md` item 4), so the UI has a tab for it, **Confirm**, beside the prompt modal.

- **`GET /api/confirmations`** reads `GET /confirmations/pending` and joins each item with `GET /confirmations/{hash}/card`: `{items: [{hash, kind, name, card, confirmation, nonce, expires_utc_ms}]}`. A card Core refused is `{..., error}` with Core's reason, so one refusal hides no other item. **`POST /api/confirmations`** takes `{hash, nonce}` and relays it as surface `ui` through the one client, which sends the person's token (103); Core's `400`, `403`, `404` and `409` come back as their own status with the reason alone, never a success.
- **Every string the agent wrote is text**: `confirm.js` builds the cards with `textContent` only, and a test refuses `innerHTML` and its kin in the file. A test name holding markup shows as the characters.
- **The card shows what Core rendered, whole**: the diff against the premade test when the copy has one, and the definition in full, with derived-from, prompts, provenance, limits, mapping and inputs drawn first as their own sections when the definition has them. Nothing is summarised away, so what is shown is what is confirmed. *Rejected:* a hand-built layout per kind, a second copy of Core's schema.
- **Confirm one, or all shown**: *Confirm all shown* posts each item with its own nonce, one after another. The nonce is spent by the attempt, so after any refusal the page keeps Core's reason on the item and reloads the cards for fresh nonces; a confirmation is never retried by the page.
- **No push**: the list loads when the tab opens and on Reload. It does not poll and does not raise a modal; a pending item is not an interrupt the way a running study's prompt is.

Measured: unit tests against a stub Core (one input confirmed, the stub receiving `Bearer` person token, the nonce and `ui`; markup in a name served untouched; a `403` coming back with Core's reason). **Not measured:** the page in a browser, and a real Core's card shape for a capability, hook or limit: the sections are drawn by key name from the definition and may not match what Core sends.
