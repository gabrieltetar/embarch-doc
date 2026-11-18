# 077 — Turn a fetched web page into readable text, and say when it is a bot challenge

**State:** done
**Source:** Fleet Ready issue: agents doing web research keep rewriting a one-off HTML-stripping script when the page fetch tool is blocked or returns raw bytes.
**Issue:** EMB-135
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

One `embarch-atlas` verb, for example `embarch-atlas fetch-text <url|file>`, takes a URL or an HTML file already downloaded and prints the page body as plain text (or Markdown): `<script>` and `<style>` blocks removed, remaining tags stripped, entities unescaped, whitespace collapsed. A response that is a bot challenge, captcha or rate-limit page (a "Just a moment" interstitial, a proof-of-work challenge page, a "Sorry... automated queries" page, an HTTP 403/429/503 with such a body) is reported as blocked, with `blocked: true` in a machine-readable form, never printed as content. A PDF response, or a local PDF, goes through the text extraction the atlas already uses (`pdftotext`). The research note `embarch-atlas/research/14-llm-browsing-format.md` is related background, not a design to follow.

## Why now

The owner moved the issue to Fleet Ready. Every session that hits a blocked fetch writes the same script, and one recently read a rate-limit page as if it were the patent it asked for.

## Dispatch notes

- `embarch-atlas` keeps no numbered decisions; record the verb in its `DESIGN.md`/`README.md` and `embarch-doc/embarch-atlas/` as the recent `q` verbs were.
- **Tests never touch the network.** Use local HTML and PDF fixtures, and a stubbed or local HTTP server for the URL path. Fixtures are written for the suite, not copied from a real site.
- Use the standard library's HTML parser or a dependency the atlas already has; a new one needs a reason in the changelog fragment.
- If an MCP tool is added too, update every lookup count and the test that pins the tool count, as `atlas/075` did.
- No file of this sub-project is in reserve.

## Done when

- [x] One command takes a URL or a local HTML file and prints the page body as plain text with scripts, styles and tags removed and entities unescaped.
- [x] The command reports a bot-challenge or rate-limit response as blocked instead of printing it as content.
- [x] A PDF response is converted to text by the same command.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); docs updated, `changelog.d/` fragment dropped.
