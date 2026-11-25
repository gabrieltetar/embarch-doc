**Target:** suite/hil-guide.md, "Words" section, the `Study` bullet (apply these exact bytes; the api's pinned copy `guide/hil-guide.md` already carries them, and the drift guard needs the suite copy equal)
**Was:** "- **Study** (the mode): a custom question answered by measurement on exactly one bench. **A study** (the file) is the steps a runner executes: `run_study` on the dev bench, or `run_host_study` on Core's own runner."
**Now:** "- **Study** (the mode; **a study** is its file): a custom question answered by measurement on one bench, run by `run_study` or `run_host_study`. EmbArch's glossary row **Study** is the definition."

Only Study has a glossary row today, so Bench, Test, Run, Measurement and Verdict keep their gloss in place. The bullet is 18 bytes shorter than before. Re-point the others when the glossary gains rows.
