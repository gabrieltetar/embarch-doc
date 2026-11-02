# embarch-ui open: making a bench live

**Status:** active, 2026-11-02.

Unresolved in phase 4 of the bench editor. Current truth: [../spec/bench-live.md](../spec/bench-live.md). The rest of the editor: [bench.md](bench.md). Index: [../open.md](../open.md).

- **A bench board drawn on the canvas is never proposed.** Its chip is looked up from its board type, as every chip is (decision 48), a template carries none (71), and the inspector offers a board type only on a part holding a role (86), so a role-less board says *not proposed* unless its file names a `board` by hand. **Trigger:** the first bench board someone wants enrolled from the canvas — then either the inspector offers it a board type or a template states a chip.

- **Whether a null `config` should mean every config.** A make-live with none counts the bench-level cables alone, where the old apply searches every config's leads (75). The page sends null only for a bench with no config, so only an API caller meets the difference. **Trigger:** an API caller making a bench with configs live and naming none.

- **The dev-bench link waits for a second apply after its enrolment is confirmed.** Core amends the link onto the dev-bench row, so a make-live that finds the role empty defers it; the page applies the live bench again after every Confirm, but a caller enrolling through `/api/enroll` alone must make the bench live again itself (decision 93). By design for now. **Trigger:** an agent's flow that enrols dev-bench and expects the link without a second call.

- **A late make-live answer can replace a newer *unknown* on the bar.** A read of the record that fails after a write was sent is overwritten when the write's answer lands, since the server orders neither: the bar then says *live* from the write while the record may be unreadable. It stays so until the record is read again. **Trigger:** an unreadable record seen to flip back to *live* — then the server stamps its answers.
