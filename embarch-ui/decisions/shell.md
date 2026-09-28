# embarch-ui decisions: The shell

**Status:** active, 2026-09-20.

One app behind a persistent sidebar. The visual design system that renders it
is in [design-system.md](design-system.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 4 — One app, not linked-but-separate pages

A persistent left sidebar plus a top status bar, with **six** sections behind it as designed: Dashboard, Topology, Study Designer, Enroll, Trace, Debug — the last two present in none of the three surfaces this replaces. **It is five now**, by two changes in opposite directions that cancelled: Trace folded into the Live Study tab that replaced the run card (decision 31), and Enroll folded into Topology's own diagram (decision 43). Client-side navigation, one shared header throughout, **so it reads as one product rather than a pile of tools that happen to share a port.**

**Trace is its own section rather than a panel inside the Study Designer's run card**, for one reason: **a trace belongs to a *completed* study, which is not necessarily the one this tab currently has in its table** — a run from an hour ago, or one a terminal submitted, is exactly as valid a thing to open, and a per-run panel could only ever show the run you just did. The run card links into it, handing over the study id, so the common case costs no typing.

**One title per tab, and the topbar owns it.** Every tab used to open with an `<h1>` and a one-line subtitle, directly under a topbar that already named the tab — and named it from the nav item's own label, so the heading could only ever be the same word one line lower (removed 2026-09-19). The five static subtitles went with their headings: each described the tab in a sentence a reader has already passed twice, in the sidebar and in the topbar. **The Debug tab keeps its one line, because it never was a restatement** — it describes the log *source* currently selected and changes with it ("Live-tailed embarch-api log — every MCP session and one-shot CLI run on this machine"), so it now sits under that tab's chip row rather than beside a heading.

**Navigation is by URL fragment, and the fragment carries parameters where a section needs them** — `#topology` is already `embarch-topology`'s own fix-it destination. Parameters in the fragment rather than the query string, because **the fragment already selects the section, so an address is one mechanism rather than two**, and because **a fragment never reaches the server**: linking somebody to a trace costs no round trip and puts no study id in a log.

### 46 — The open project belongs to the shell, not to the Study Designer

**One firmware repo is open at a time, and it always was** — the server holds exactly one, and the catalog, the saved benches, the studies, the Build card and half this binary's error messages are relative to it. What was wrong was where it was *stated*: a card on the Study Designer, so "which repo am I looking at?" was answered on one of five tabs, and the Topology tab's refusals ended with "open one on the Study Designer tab first", pointing a reader off the tab that needed it.

The control sits at the foot of the sidebar now, under the nav: the word Project, the repo's directory name, and under that **where it is** — its last two parent directories, in mono. *Not the path again*: the name line already carries the last segment, the sidebar is 236 px wide, and a full path there is a string cut off at whichever end the CSS chooses. Two checkouts of one firmware differ exactly in their parent, which is what makes that the useful half; the whole path is on the tooltip and in the dialog. Computed in JS rather than left to `direction: rtl`, which truncates on the right side but reorders an absolute path's leading `/` to the far end — rendering a trailing slash that is not in the path, as the live control did for one deploy. Nothing open reads *none open* in the warning colour — a state, not an error.

**One picker, two doors.** The control opens the dialog, and the Study Designer's card keeps a **Change project…** button onto the *same* dialog rather than a second copy of the fields. The dialog is decision 14's panel unchanged in substance, for unchanged reasons: a browser directory picker yields no usable path, and the path is resolved server-side anyway, because the server is what reads the files.

**What stays on that tab is the half that is only its own**: the summary of what the open project holds, and the static analysis of its source. *Rejected: leaving the picker there and mirroring the state into the sidebar.* Two renderers of one fact is how a footer comes to name a repo a tab has already left; there is one render function over one state object, and the sidebar, the summary line and the dialog are its three outputs.

**A switch now reloads the board catalog and the saved benches too** — project files that would otherwise show one repo's bench under another repo's name, survivable before only because the switch happened on a tab that does not render them. The server's refusals were re-pointed in the same change, so a message that says what to do names something on screen wherever the reader is.
