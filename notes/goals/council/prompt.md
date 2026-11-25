# Goals notes: the council prompt

**Status:** draft, 2026-11-23.

**The exact prompts a multi-model review of the goals notes sends.** The method is llm-council's three stages (each member answers alone, the members rank each other anonymously, a chair reports), with prompts rewritten to keep a lone dissent instead of averaging it away: the stock ranking prompt rewards "the most comprehensive answer" and the stock chair writes "the council's collective wisdom". The runner sends each fenced block below verbatim, with the `{placeholders}` filled.

## Stage 1: each member, alone

`{docs}` is [00-goals.md](../00-goals.md), [01-scope.md](../01-scope.md) and [02-phases.md](../02-phases.md), each under its file name.

```text
You are reviewing the goals of an open-source project from outside it. You have never seen the project before. Below are three documents: its goals statement (00-goals.md), the scope answers behind it (01-scope.md) and its phases (02-phases.md). You cannot see the code or the rest of the documentation: judge what is written here, and where a judgment would need the code, say so instead of guessing.

The owner wants disagreement, not reassurance. Skip praise, and skip summaries of what the documents say.

Answer each of these:

1. Read cold. From the Vision and "Built for" sections alone, say in two sentences what you think the project is. Then name the first sentence where the text lost you or assumed knowledge you did not have.
2. Not worth it. Which goal is not worth building, or not worth building now? Why?
3. Conflicts. Which two goals pull against each other? The Open section already names goal 3 against goal 2; find others.
4. Missing. What would a firmware engineer who lets an LLM agent work on their real hardware expect to find here and not find: a goal, a non-goal, a risk, a kind of user?
5. Status. Which "met" or "partly met" reads stronger than the evidence line under it supports?
6. Adoption. What would make an experienced embedded engineer refuse to use this? Which existing tools or practices already cover part of it, and what does this project claim that they do not? Label anything you say about the outside world (other tools, what engineers do) as your belief, since you cannot check it here.
7. Phases. Is "build now, stabilise on the owner's call, scale inside the trinity" a plan or a deferral? What would have to be true for the one-engineer, one-service, one-machine boundary to be the wrong bet?
8. The Open items. For each item under Open in 00-goals.md, your pick in one line.

Then list your findings, most consequential first, at most fifteen. For each finding: the line you are criticising, quoted; what is wrong with it; what you would write instead; your confidence (high, medium or low).

{docs}
```

## Stage 2: each member ranks the others

`{question}` is the whole stage 1 prompt; `{responses}` is every member's answer under an anonymous label, `Response A` onward.

```text
You are one member of a review panel. Every member answered the same question independently; their answers are below, anonymised.

The question:
{question}

The answers:
{responses}

Judge each answer on two things only: are its findings likely to be true, given the documents in the question, and how much would they matter to the project if true? Length, coverage, tone and structure earn nothing. A short answer with one true, consequential finding beats a long answer of safe, generic ones.

1. For each answer, name its strongest finding and any finding you believe is wrong, with the reason.
2. List every finding that only one answer raised and that you believe is true, and say which answer raised it. This is the most important part of your reply.
3. End with your ranking, formatted exactly like this, one line per answer and nothing else after it:

FINAL RANKING:
1. Response X
2. Response Y
```

## Stage 3: the chair reports

`{responses}` carries each member's model name; `{rankings}` is every stage 2 reply, under its member's name.

```text
You chair a review panel. Its members answered a question independently, then judged each other's answers anonymously. Your job is to report what the panel found, not to write a consensus.

The question:
{question}

The members' answers:
{responses}

The members' judgements of each other:
{rankings}

Write four sections, in this order:

1. Agreed: findings that two or more members raised or endorsed. Name the members for each.
2. Raised once: every finding only one member raised, kept in that member's words as far as possible, with the member's name and whether any other member called it wrong. Do not drop a finding because the others did not mention it.
3. Disputed: where members disagree, both positions side by side, with who holds each.
4. The Open items: each member's pick on each item under Open in 00-goals.md, as a table.

Add no findings of your own. Where you think a member is wrong, say so in a line starting "Chair:" under that finding, and leave the finding in.
```
