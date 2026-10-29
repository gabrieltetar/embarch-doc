`fold-commit.py` deletes a landed unit's local `agent/*` branches with its pushed ones, so `git worktree remove` no longer leaks one per unit (`tasks/doc/066`).
