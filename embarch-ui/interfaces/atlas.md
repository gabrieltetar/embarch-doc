# embarch-ui interfaces: the Atlas tab's routes

**Status:** active, 2026-10-01.

Reference for [decisions/atlas-tab.md](../decisions/atlas-tab.md) (52-54). Index: [../interfaces.md](../interfaces.md).

Under `/api/atlas`, all `GET`, all files in the open project (`404` naming the project control when none is open). Ids are validated before they touch the filesystem (`<target>@<hex>`; a doc id has no separators).

| Path | Notes |
|---|---|
| `atlas` | The atlases under `embarch/atlas/atlases/`, newest first: commit, whether it has a `graph.json`, at HEAD or how many commits behind, the default to open, the page render DPI |
| `atlas/{id}/graph` | `graph.json` byte for byte |
| `atlas/doc/{doc}/{file}` | A translated document's `card.md`, `toc.md` or `s/<section>.md`, nothing else |
| `atlas/{id}/page/{doc}/{n}` | Page `n` as a PNG, `pdftoppm` on first request, cached under `cache/pages/` (54) |
| `atlas/{id}/pdf/{doc}` | The source PDF, for the browser's viewer at `#page=N` |
| `atlas/code?id&root&path&line` | The cited lines at the atlas's commit (`git show`), `unchanged`/`changed` since (`git diff --quiet`), a VS Code link |
