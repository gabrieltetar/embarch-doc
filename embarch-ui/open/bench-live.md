# embarch-ui open: making a bench live

**Status:** active, 2026-11-02.

Unresolved in phases 4 and 5 of the bench editor: making a bench live, which config is live, and a prompt naming one. Current truth: [../spec/bench-live.md](../spec/bench-live.md). The rest of the editor: [bench.md](bench.md). Index: [../open.md](../open.md).

- **Whether a null `config` should mean every config.** A make-live with none counts the bench-level cables alone, where the old apply searches every config's leads (75). The page sends null only for a bench with no config, so only an API caller meets the difference. **Trigger:** an API caller making a bench with configs live and naming none.

- **The dev-bench link waits for a second apply after its enrolment is confirmed.** Core amends the link onto the dev-bench row, so a make-live that finds the role empty defers it; the page applies the live bench again after every Confirm, but a caller enrolling through `/api/enroll` alone must make the bench live again itself (decision 93). By design for now. **Trigger:** an agent's flow that enrols dev-bench and expects the link without a second call.

- **A late make-live answer can replace a newer *unknown* on the bar.** A read of the record that fails after a write was sent is overwritten when the write's answer lands, since the server orders neither: the bar then says *live* from the write while the record may be unreadable. It stays so until the record is read again. **Trigger:** an unreadable record seen to flip back to *live* — then the server stamps its answers.

- **A saved study naming a config the bench lacks is not re-pointed when it is opened.** The design was that it asks for a config on open and keeps the answer, but host studies have no saved files yet to keep it in, so only the per-run pick exists (99). **Trigger:** host studies saved in a repo — then opening one checks its `bench_config` names against the live bench.

- **The per-run pick lives in page memory.** A config picked, or text only, for a name the live bench lacks is kept by study and name in the open page (99), so a reload or a second browser asks again. A prompt waits for a person anyway, so a lost pick costs one click. **Trigger:** an operator asked twice in one run — then the pick moves to the server.
