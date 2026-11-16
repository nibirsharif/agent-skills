"""Tests for skills/implement-task/scripts/find_tasks.py: a named feature is looked up at one path only."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills" / "implement-task" / "scripts" / "find_tasks.py"
spec = importlib.util.spec_from_file_location("find_tasks", SCRIPT)
find_tasks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(find_tasks)

STOP = "stop No tasks file found at {}. Run write-tasks first, then run implement-task again."


class FindTasks(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root, self.home = Path(tmp.name) / "project", Path(tmp.name) / "home"
        self.root.mkdir()
        self.home.mkdir()

    def project(self, *features, config="spec_output_dir: docs/specs\n"):
        if config is not None:
            (self.root / ".agent-skills-config.yaml").write_text(config)
        for name in features:
            folder = self.root / "docs" / "specs" / name
            folder.mkdir(parents=True)
            (folder / "tasks.md").write_text("# Tasks\n")

    def find(self, **kwargs):
        return find_tasks.find(self.root, self.home, **kwargs)

    def test_named_feature_is_found(self):
        self.project("reading-time", "invoice-export")
        self.assertEqual(self.find(feature="reading-time"), "found docs/specs/reading-time/tasks.md")

    def test_named_feature_without_tasks_stops_even_when_another_feature_has_them(self):
        self.project("reading-time")
        self.assertEqual(self.find(feature="invoice-export"), STOP.format("docs/specs/invoice-export/tasks.md"))

    def test_named_feature_with_a_folder_but_no_tasks_file_stops(self):
        self.project("reading-time")
        (self.root / "docs" / "specs" / "invoice-export").mkdir()
        self.assertEqual(self.find(feature="invoice-export"), STOP.format("docs/specs/invoice-export/tasks.md"))

    def test_no_feature_uses_the_only_one(self):
        self.project("reading-time")
        self.assertEqual(self.find(), "found docs/specs/reading-time/tasks.md")

    def test_no_feature_with_several_or_none_asks(self):
        self.project()
        self.assertTrue(self.find().startswith("ask No tasks.md under docs/specs"))
        self.project("b-feature", "a-feature", config=None)
        self.assertEqual(self.find(), "ask Which feature: a-feature, b-feature")

    def test_a_named_path(self):
        self.project("reading-time")
        self.assertEqual(self.find(path="docs/specs/reading-time/tasks.md"), "found docs/specs/reading-time/tasks.md")
        self.assertEqual(self.find(path="notes/tasks.md"), STOP.format("notes/tasks.md"))

    def test_config_project_wins_then_home_then_ask(self):
        self.project(config=None)
        self.assertTrue(self.find(feature="x").startswith("ask No spec_output_dir is set"))
        (self.home / ".agent-skills-config.yaml").write_text("spec_output_dir: specs   # shared\n")
        self.assertEqual(self.find(feature="x"), STOP.format("specs/x/tasks.md"))
        (self.root / ".agent-skills-config.yaml").write_text("test_command: make test\nspec_output_dir: 'docs/specs/'\n")
        self.assertEqual(self.find(feature="x"), STOP.format("docs/specs/x/tasks.md"))
        (self.root / ".agent-skills-config.yaml").write_text("spec_output_dir:\n")
        self.assertEqual(self.find(feature="x"), STOP.format("specs/x/tasks.md"))

    def test_absolute_spec_output_dir(self):
        self.project("reading-time", config=None)
        absolute = self.root / "docs" / "specs"
        (self.root / ".agent-skills-config.yaml").write_text(f"spec_output_dir: {absolute}\n")
        self.assertEqual(self.find(feature="reading-time"), f"found {absolute}/reading-time/tasks.md")

    def test_command_line(self):
        self.project("reading-time")
        run = lambda *args: subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), *args],
                                           capture_output=True, text=True)
        out = run("--feature", "invoice-export")
        self.assertEqual((out.returncode, out.stdout.strip()), (0, STOP.format("docs/specs/invoice-export/tasks.md")))
        self.assertEqual(run("--feature", "../x").returncode, 2)
        self.assertEqual(run("--feature", "a", "--path", "b").returncode, 2)


if __name__ == "__main__":
    unittest.main()
