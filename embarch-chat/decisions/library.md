# embarch-chat decisions: The prompt library

**Status:** active, 2026-10-23.

What an entry is, where entries live, how the library is seeded, where it sits at the input, and what became of `embarch-promptu`'s install pieces.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 7 — An entry is a Claude Code command or skill

A `.md` file with frontmatter: it works in the terminal, the official panel and the fleet, and gets its work item from `desk_whoami`, so nothing is templated. **Rejected:** panel-only templates with `{{issue}}` placeholders (usable nowhere else), a button file choosing which commands show (a second file to keep in step).

### 13 — The library is two folders

Generic entries in a plugin in the `embarch-chat` repo (`plugin/`, the repo root its marketplace); **an entry naming a client, a client project or a client internal in `~/.claude/commands`, never in a repo**. Both become buttons. The extension ships a copy of the plugin for the 📚, but a chat runs an entry only once the plugin is installed in Claude Code; until then a started chat shows its entries greyed. **Rejected:** the public plugin only, the open firmware repo's commands too (the client team's, not the owner's).

### 14 — It is seeded from the owner's past prompts, and the owner cuts

682 prompts in 145 local transcripts; the only exact repeats are one-word replies (done ×20, continue ×15, yes ×12, go ×11, push ×7), so one `claude -p` groups them by intent and drafts entries, each ✓ or ✕; about $0.30 on Sonnet [assumed]. **Rejected:** promptu's three then add-as-you-go, starting empty.

### 38 — Entries sit behind a 📚 by the input, Haiku's cards behind a 💡 beside it, one submenu per category each

A library entry's category is `category:` in its own frontmatter (none is Other); a click puts `/<name> ` at the head of the draft, as the session knows it (`/embarch-chat:<name>` for the plugin's), and `/` completes them too. The 💡 is VS Code's Quick Fix bulb: missing context, improvements, context handling, lit with a count when Haiku has something ([assistant.md](assistant.md)). **Rejected:** one bulb holding both; the library inside the 💡 with Haiku as a dot; cards stacked above the input; a `/` list plus a pinned row; a toolbar of every entry; the `/` list only; a folder per category (`/bench:flash-log` names), Haiku grouping them (stored somewhere new, and drifts).

### 39 — promptu's two install pieces became commands that apply them

`/embarch-permissions` and `/embarch-claude-md` show what they would write into the open repo (`settings.local.json`, `CLAUDE.md`) and write it on a yes — never silent (`embarch-umbrella` decision 12). The rule the permission split follows is [suite/user-guide.md](../../suite/user-guide.md) §7.1's; the command carries its tool lists dated and checks them against the server's live tool list, a tool in neither going to ask. **Rejected:** leaving them to umbrella's `init`, template files copied by hand.
