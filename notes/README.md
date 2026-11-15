# notes: research intake

**Raw intake, not a doc tier.** A folder per design being shaped (`notes/<topic>/`), one file per subtopic (`NN-<slug>.md`). A note records what was found in the suite and what the owner answered while the design took shape. **It folds into a proposal or a sub-project's four files once accepted, and is deleted then** ([DOC-PROTOCOL.md](../DOC-PROTOCOL.md) §3). The precedent is [embarch-atlas/research/](../embarch-atlas/research/README.md), which is the same thing for one sub-project.

## Rules

- **Each file carries `**Status:** draft, <date>`**; a README carries none.
- **Say whose a claim is.** An owner's answer is recorded as decided. A recommendation the owner has not answered sits under **Open**. An inference is marked as one, and a claim about the suite's own code cites the doc or file it came from.
- **Each file ends with Open**: what is still undecided, longest list first, for the owner to cut.
- **This repo is public.** No client names, client project names, client issue keys or client internals. An example taken from client work keeps the generalised finding and replaces the specifics with placeholders (`<dut>`, `<service>`, `<board>`).
- **No size cap is enforced here**, so keep a file to one subtopic and split it when it grows past one.

## Topics

| Folder | What is being shaped | Folds into |
|---|---|---|
| [hil/](hil/README.md) | How an agent runs hardware-in-the-loop: a Study, a Test, or Live access | [embarch-hil-proposal.md](../embarch-hil-proposal.md) |
