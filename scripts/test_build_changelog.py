#!/usr/bin/env python3
"""A history roll must leave every relative link resolving (tasks/doc/092).

    python3 scripts/test_build_changelog.py

The first real roll copied a window into `history/archive/` verbatim, and its
19 `](../embarch-api/...)` links, right from `history/`, pointed one directory
short. Replayed against that file (`2ffe19ec^:history/api.md`, cap 18,000 B),
the fixed roll writes the same bytes the supervisor fixed by hand. This test
keeps that true without the repo's history: a temporary tree, one window
holding every link shape a fragment uses, rolled, each target resolved.
"""
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("build_changelog", HERE / "build_changelog.py")
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)

OLD = ("## 2026-09\n\n### Changed\n"
       "- [spec](../embarch-api/spec.md#3-wire), [core](core.md), [prior](archive/x.md), "
       "[web](https://example.com/a), [here](#top)\n\n")
NEW = "## 2026-10\n\n### Added\n- " + "x" * 300 + "\n\n"


class RollRebasesLinks(unittest.TestCase):
    def test_every_relative_link_resolves_after_a_roll(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            for f in ("embarch-api/spec.md", "history/core.md", "history/archive/x.md"):
                (repo / f).parent.mkdir(parents=True, exist_ok=True)
                (repo / f).write_text("x\n")
            hist = repo / "history" / "api.md"
            hist.write_text("# api: history\n\n" + NEW + OLD)
            saved = (bc.REPO, bc.HISTORY, bc.ARCHIVE, bc.CAP_BYTES)
            bc.REPO, bc.HISTORY, bc.ARCHIVE = repo, repo / "history", repo / "history" / "archive"
            bc.CAP_BYTES = len(hist.read_bytes()) - 1
            try:
                rolled = bc.roll_if_over_cap(hist, "api")
            finally:
                bc.REPO, bc.HISTORY, bc.ARCHIVE, bc.CAP_BYTES = saved
            self.assertIsNotNone(rolled)
            text = (repo / rolled).read_text()
            targets = [m.group(2) for m in bc.LINK_RE.finditer(text)]
            self.assertIn("https://example.com/a", targets)
            self.assertIn("#top", targets)
            local = [t.partition("#")[0] for t in targets if not t.startswith(("#", "http"))]
            self.assertEqual(len(local), 4)      # back-link to api.md + spec, core, prior
            for t in local:
                self.assertTrue(os.path.exists(repo / "history" / "archive" / t), t)
            self.assertIn("../../embarch-api/spec.md#3-wire", targets)


if __name__ == "__main__":
    unittest.main()
