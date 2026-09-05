**Target:** suite/user-guide.md — the `--snippet` / `--extra-arg` bullet under the build section
**Was:** "Omitting `--snippet` uses the project's `default_snippets`, and there is currently **no way to force zero snippets** over a configured default."
**Now:** `--snippet none` (the reserved literal, alone) forces zero snippets over a configured default, as of 2026-09-04. Mixing it with real snippet names, or using it where the app really declares a snippet called `none`, is refused naming the ambiguity.

The same guide section may also want `[projects.default_target]`, now built: a `zephyr-west` project's base (board, variant, revision, app) selection that a call narrows from per field. Both are [embarch-api/decisions/zephyr.md](../embarch-api/decisions/zephyr.md) 20 and 21, with the surface in [embarch-api/interfaces/config.md](../embarch-api/interfaces/config.md).
