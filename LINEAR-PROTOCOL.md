# embarch-doc: Linear issues and comments

**Status:** active, 2026-11-05. The shapes every issue and comment in the EmbArch Linear workspace (team `EMB`) takes, whoever writes it: the owner, an interactive session, a fleet leg, a worker, a reviewer, an audit. `scripts/fleet-linear.py` in the framework repo enforces it: `file` and `rewrite` refuse a body that breaks §2–3, and `lint` checks every open issue. **Nothing it sends names a client** (owner's call, 2026-11-10): every issue, edit and comment is read against the client-name denylist first, since the fleet copies an issue into public task files, and a hit or a dark denylist sends nothing. A client's workspace is not covered; text going there follows the `gabriel-voice` skill alone.

## 1. Three rules behind every shape

**An issue carries everything its worker needs, so nobody reads around it.** An agent picking one up reads the body first and should need nothing else to start: every file path, function, command, verbatim error, decision number and measurement it would otherwise go and find is in the body. A reference points at something an agent can open — a repo path, `<sub-project>` decision N, an issue key — never a chat, a Slack thread or a screenshot (the desk cannot read attachments).

**The body is the current ask; comments are its history.** A comment that changes the ask comes with an edit to the body in the same step (`linear_draft_edit`, or `fleet-linear.py rewrite`), and is a **Changed** comment saying what moved. So an agent reads the body and the latest comment, never the whole discussion to rebuild the ask.

**Two voices.** The summary — a body's opening lines, a comment's head line — is in the owner's voice (the `gabriel-voice` skill: plain words, first person, a space before `?` and `:`), for the owner scanning a list. Everything after it is this repo's doc register — markdown headers, no first person — for the agent doing the work.

## 2. An issue

**The title states the problem or the missing thing**, under 80 characters, with no prefix (`Bug:`, `[desk]`): the Project names the sub-project and `Type` the kind. A title may open with a lowercase command or symbol name (`atlas build fails …`).

**The body, in this order:**

```markdown
<Summary: one to three sentences, under 400 characters, in the owner's voice.>

**Type:** bug
**Scope:** desk
**Hardware:** none
**Filed by:** owner

## <the type's sections, §3>

## Done when

- [ ] A checkable property, not an implementation.
```

- **`Type`** — one of §3's six.
- **`Scope`** — the sub-project without `embarch-` (`desk`, `atlas`, `ui`, `doc` for embarch-doc), or `suite` for one change that must land across several repos at once, which the supervisor runs itself ([the protocol](../embarch-fleet/protocol.md) §8). Any other clone in the suite root is a scope too, such as `private`; the fleet never works one. A repo scope matches the issue's Project, `embarch-<scope>`.
- **`Hardware`** — `none`, `verify-only`, `bench`, `toolchain` or `required`: an honest claim about **the fix**, with [tasks/README.md](tasks/README.md)'s meanings. Anything only the owner can do — a phone, a bench, a login — is `required`.
- **`Filed by`** — `owner`, `session`, `worker`, `reviewer`, `audit` or `decision`. It replaces the old *"Filed by the fleet (…)"* footer, and `fleet-linear.py file` writes it from `--from` when the body leaves it out.
- **`Done when`** — at least one `- [ ]` item, each checkable by reading code or running something.

**Where a section names code, it names it exactly:** `` `embarch-desk/src/linear.rs` `gql_detail` ``, one location per line, with the line's role after a dash. **Put file names and code in backticks, and name a domain in words:** Linear turns a bare `store.rs` into a link to `http://store.rs`, and links a domain such as Claude's web app even inside backticks [measured 2026-11-05, EMB-11].

**Size is not capped at filing.** The supervisor splits an issue into task files when it takes it ([the protocol](../embarch-fleet/protocol.md) §4), and sends back one it cannot state a `Done when` for. A filer writes the issue as big as the problem.

## 3. The six types

Each type's sections sit between the fields and `## Done when`, as `##` headers. **Required** ones must be there, in the order listed; **optional** ones may sit anywhere among them; no other header is accepted, and no text sits between the fields and the first header.

| Type | When | Required | Optional |
|---|---|---|---|
| `bug` | Something does the wrong thing | What happens · Expected · Where | Reproduce · Why it matters · Found while |
| `change` | It works as built, and should behave differently — a default, a layout, a wording | Today · Wanted · Where | Why · Found while |
| `gap` | Something needed does not exist — a tool, a verb, a field, a check | What is missing · Who needs it | Direction · Where · Found while |
| `doc` | A doc is wrong or silent, or contradicts another | Where · What it says · What it should say | Found while |
| `decision` | A choice only the owner makes, and work waits on it | Question · Options · Blocks | Where · Found while |
| `investigation` | A symptom whose cause nobody knows yet | Symptom · Known · Next check | Hypotheses · Where · Found while |

- **`decision`**: `Options` holds two to four, the recommendation first, each with its trade-off in one line. Its `Done when` is the choice recorded in the sub-project's `decisions.md` and the blocked issues moved on.
- **`investigation`**: `Next check` is the one measurement or reading that splits the hypotheses. Its `Done when` is the cause named, then fixed or filed as a `bug`.
- **`Found while`** says what the filer was doing — a unit, a review, an atlas build — in one line, so the owner can weigh how the finding was reached.

## 4. A comment

**The head line opens with its kind in bold, then one sentence in the owner's voice:**

```markdown
**Question** — should a second UI instance hand focus to the first, or refuse to start ?

<detail, in doc register>
```

| Kind | Who writes it | What it holds |
|---|---|---|
| **Split** | the fleet (`filed`) | the task files the issue became; the issue moves to Fleet Working |
| **Sent back** | the fleet (`send-back`) | why it could not be split, and what the body lacks; back to Backlog |
| **Closed** | the fleet (`finish`), a session | the commits or folds that closed it |
| **Question** | anyone | one question, its options with a recommendation first |
| **Answer** | the owner, mostly | a reply **in the Question's thread**, never a new top-level comment |
| **Progress** | a session, the fleet | what landed, by SHA, and what is left |
| **Handoff** | a session | the state, the next step, and what not to retry — for the next session |
| **Blocked** | anyone | what it waits on: an issue key, a decision, hardware |
| **Changed** | anyone | the body was edited: what changed and why |
| **Finding** | anyone | something learned while working that does not change the ask |

**A comment longer than its point is a thread.** The head comment holds the kind and the point, under 600 characters; detail goes in replies under it, one topic each, under 1,500 characters, posted by the same Send (`replies` on `linear_draft_comment`, or `---` lines in `fleet-linear.py comment`'s body). A reader skims the heads for the story and opens a thread only for its detail. A reply opens with a kind only when it is an **Answer**.

**Never in a comment:** what the body already says, tool output beyond the lines that matter, or a recap of earlier comments.

## 5. Who writes, and through what

- **Everything reaches `EMB` through the desk** that `fleet.toml`'s `[linear]` names, never the claude.ai Linear connector or the work desk: a fleet agent and an interactive session alike use `scripts/fleet-linear.py` — `file`, `rewrite`, `comment`, and the fleet's own `filed`, `send-back`, `finish`. An interactive session files with `--from session`, or `--from owner` for the owner's own notes.
- **The desk's draft tools** (`linear_draft_issue`, `linear_draft_comment`, `linear_draft_edit`, `embarch-desk` decisions 30 and 75) are the route on any other desk; the shapes here apply to whatever they send to `EMB`.
- **The owner typing in Linear** follows the same shapes; `fleet-linear.py lint` finds what drifted.

## 6. Who works an issue

**The status is the lane; no label or field says it** (owner's call, 2026-11-05). Every issue starts in Backlog, and the owner moves it on:

| Lane | Statuses | Who moves it |
|---|---|---|
| The fleet | Backlog → **Fleet Ready** → Fleet Working → Done | the owner marks it ready; `filed` and `finish` move the rest |
| The owner's window | Backlog → **Todo** → In Progress → In Review → Done | the owner picks it; the desk's Start work moves it to In Progress |

**Three fields make an issue the owner's, whatever its status:** a `Scope` the fleet does not work — `fleet` (reserved; `check-ownership.py` refuses it as a worker scope) or a clone with no directory here, such as `private` — `Hardware: required` (the owner's hands), and `Type: decision` (the owner's call). `fleet-linear.py ready` moves such an issue out of Fleet Ready to Todo with a **Sent back** comment naming the field, unless a task on `main` already names it. So a field set honestly at filing is the guard, and anything that needs the owner — a phone, a bench, a choice — says `required` or `decision` rather than prose. Until a leg runs `ready`, the listener's count still includes such an issue: one leg may start and find nothing.

