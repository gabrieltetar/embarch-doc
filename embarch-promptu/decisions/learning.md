# embarch-promptu decisions: Learning

**Status:** active, 2026-10-30.

The weekly sheet and what it learns from. Moved verbatim from `decisions.md` on 2026-10-30, when step 3's fork answers took it past its 25 KB cap ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 14 — A weekly ✓/✕ sheet, drafted locally
A systemd user timer runs a stripped Opus `claude -p` every Wednesday at 08:00 (`Persistent=true`), about $1.5–3 a week [assumed]. Its inputs: friction in sessions, his edits, skipped and overridden questions, prompts no pattern matched, outcomes, and a quarterly or new-model refresh of published practice. **Every event becomes a proposal**; a specific fact becomes a memory entry, so patterns stay generic. He approves the sheet in a Promptu section of the Desk tab, the spot `embarch-desk` decision 65 kept, hidden while it has nothing open. **The ping is the Desk section alone**: no Slack message, since the desk's Slack connector is gone (`embarch-desk` decision 66). **Rejected:** 👍/👎 clicks and memory corrections as inputs, cloud routines (the data stays local), the fleet, a session cron (it skips while the session is busy).

### 30 — The weekly sheet works without the Desk
Decided by the owner on 2026-10-29; **not built** (build step 4). Without the Desk, the weekly ✓/✕ sheet is a Markdown file applied with `promptu week apply`, and a `/promptu:review` skill walks it in the terminal. With the Desk present, its Promptu section shows the same sheet (14). **Rejected:** a sheet only the Desk can show.

### 15 — Success after four weeks
Reported on each sheet: corrections per prompt at or below 0.10 against non-Promptu sessions as a control, redirected messages per task start down about 30%, at least 90% of pre-filled answers kept, at least 85% of picked patterns kept, questions per run falling, and a one-key "better · same · worse" line.
