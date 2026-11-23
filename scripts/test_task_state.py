#!/usr/bin/env python3
"""task-state.py's claim and close, read back by check-task-state.py (EMB-151).

    python3 scripts/test_task_state.py

A scratch instance holds one task and copies of the checker and the two
framework shims it asks, so the checker's verdict, the claim grammar
`queue-status.py` parses included, is the one the real gate would give.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent.parent

BLOCKED = """# 174 — a parked task

**State:** blocked — waits on the scan

**Unparks when:** the owner says go.
**Scope:** api
**Hardware:** none

## Done when

- [ ] It works.
"""


class TaskState(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / "scripts").mkdir()
        for name in ("check-task-state.py", "task-state.py", "queue-status.py", "check-ownership.py"):
            shutil.copy(HERE / name, self.repo / "scripts" / name)
        self.task = self.repo / "tasks" / "api" / "174-a-parked-task.md"
        self.task.parent.mkdir(parents=True)
        self.task.write_text(BLOCKED)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "add", "-A"], check=True)
        self.env = dict(os.environ, EMBARCH_FLEET_ROOT=str(SUITE))

    def tearDown(self):
        self.tmp.cleanup()

    def run_script(self, name, *args):
        return subprocess.run([sys.executable, str(self.repo / "scripts" / name), *args],
                              capture_output=True, text=True, env=self.env)

    def gate(self):
        r = self.run_script("check-task-state.py")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn("NOTE", r.stdout, "the claim grammar was not asked of queue-status.py")

    def test_claim_writes_the_parsed_prefix_and_drops_the_park(self):
        r = self.run_script("task-state.py", "claim", str(self.task), "--at", "2026-11-23 14:00",
                            "--note", "leg resumed it")
        self.assertEqual(r.returncode, 0, r.stderr)
        text = self.task.read_text()
        self.assertIn("**State:** claimed by agent/api/174-a-parked-task, 2026-11-23 14:00 — leg resumed it",
                      text)
        self.assertNotIn("Unparks when", text)
        self.assertIn("**Scope:** api", text)
        self.gate()

    def test_close_done_then_a_second_close_is_refused(self):
        self.run_script("task-state.py", "claim", str(self.task))
        r = self.run_script("task-state.py", "close", str(self.task), "done", "--why", "landed in abc1234")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("**State:** done — landed in abc1234", self.task.read_text())
        self.gate()
        before = self.task.read_text()
        r = self.run_script("task-state.py", "close", str(self.task), "done", "--why", "again")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.task.read_text(), before)

    def test_close_blocked_needs_and_adds_its_unpark(self):
        self.run_script("task-state.py", "claim", str(self.task))
        before = self.task.read_text()
        r = self.run_script("task-state.py", "close", str(self.task), "blocked", "--why", "board missing")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.task.read_text(), before)
        r = self.run_script("task-state.py", "close", str(self.task), "blocked", "--why", "board missing",
                            "--unparks", "a board is attached.")
        self.assertEqual(r.returncode, 0, r.stderr)
        text = self.task.read_text()
        self.assertIn("**State:** blocked — board missing\n\n**Unparks when:** a board is attached.", text)
        self.gate()

    def test_a_claimed_task_is_not_claimed_again(self):
        self.run_script("task-state.py", "claim", str(self.task))
        before = self.task.read_text()
        r = self.run_script("task-state.py", "claim", str(self.task))
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.task.read_text(), before)


if __name__ == "__main__":
    unittest.main()
