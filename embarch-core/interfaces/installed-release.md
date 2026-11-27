# embarch-core: the installed-release record

**Status:** active, 2026-11-26 ([decision 157](../decisions/platform.md)). Index: [../interfaces.md](../interfaces.md).

`<data dir>/installed-release.json` (`%ProgramData%\embarch\` on Windows, `/var/lib/embarch/` elsewhere). Written by `embarch install-core` (`embarch-umbrella` decisions 61 and 69), whose record carries more fields than this; Core only reads it.

```json
{"binary_sha256": ["<64 lowercase hex>", "..."]}
```

`binary_sha256` lists the SHA-256 of every `embarch-core` binary a signed release installed, as `GET /status` reports it. `install --service` refuses unless the SHA-256 of its own executable is an entry, or the file is missing or not JSON with that array. Unknown fields are ignored.
