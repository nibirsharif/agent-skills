"""Tests for skills/write-spec/scripts/target.py: where spec_output_dir comes from, how the folder is
printed, and that the location question is the same line everywhere it is written."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "write-spec"
SCRIPT = SKILL / "scripts" / "target.py"
spec = importlib.util.spec_from_file_location("write_spec_target", SCRIPT)
target = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target)

CONFIG = ".agent-skills-config.yaml"


class Project(unittest.TestCase):
    """A project folder and a home folder, both temporary, so the user's own config is never read."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = Path(tmp.name).resolve()
        self.root, self.home = base / "project", base / "home"
        self.root.mkdir()
        self.home.mkdir()

    def printed(self, cwd=None):
        return target.target(self.root, self.home, cwd or self.root)


class NoFolder(Project):
    def test_no_config_file_is_the_question(self):
        self.assertEqual(self.printed(), "ask " + target.ASK)

    def test_an_empty_value_is_the_question(self):
        (self.root / CONFIG).write_text("spec_output_dir:\n")
        self.assertEqual(self.printed(), "ask " + target.ASK)

    def test_a_commented_value_is_the_question(self):
        (self.root / CONFIG).write_text("spec_output_dir: # docs/specs\n# spec_output_dir: docs/specs\n")
        self.assertEqual(self.printed(), "ask " + target.ASK)

    def test_another_key_is_not_the_folder(self):
        (self.root / CONFIG).write_text("tasks_max_per_phase: 16\n")
        self.assertEqual(self.printed(), "ask " + target.ASK)


class Folder(Project):
    def test_a_relative_folder_is_resolved_against_the_project_root(self):
        (self.root / CONFIG).write_text("spec_output_dir: docs/specs\n")
        self.assertEqual(self.printed(), "dir docs/specs")

    def test_from_a_subfolder_the_path_is_printed_in_full(self):
        (self.root / CONFIG).write_text("spec_output_dir: docs/specs\n")
        sub = self.root / "src"
        sub.mkdir()
        self.assertEqual(self.printed(cwd=sub), f"dir {self.root}/docs/specs")

    def test_the_home_config_is_used_when_the_project_has_none(self):
        (self.home / CONFIG).write_text("spec_output_dir: specs\n")
        self.assertEqual(self.printed(), "dir specs")

    def test_the_project_config_wins_over_the_home_config(self):
        (self.root / CONFIG).write_text("spec_output_dir: docs/specs\n")
        (self.home / CONFIG).write_text("spec_output_dir: elsewhere\n")
        self.assertEqual(self.printed(), "dir docs/specs")

    def test_an_empty_project_value_falls_back_to_the_home_config(self):
        (self.root / CONFIG).write_text("spec_output_dir:\n")
        (self.home / CONFIG).write_text("spec_output_dir: specs\n")
        self.assertEqual(self.printed(), "dir specs")

    def test_quotes_and_a_trailing_comment_are_not_part_of_the_folder(self):
        for line in ('spec_output_dir: "docs/specs"', "spec_output_dir: 'docs/specs'", "spec_output_dir: docs/specs  # where specs go"):
            with self.subTest(line=line):
                (self.root / CONFIG).write_text(line + "\n")
                self.assertEqual(self.printed(), "dir docs/specs")

    def test_an_absolute_folder_outside_the_project_is_printed_in_full(self):
        outside = self.home / "specs"
        (self.root / CONFIG).write_text(f"spec_output_dir: {outside}\n")
        self.assertEqual(self.printed(), f"dir {outside}")


class CommandLine(Project):
    def run_script(self, *args, cwd):
        env = {"HOME": str(self.home), "PATH": "/usr/bin:/bin"}
        return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd, env=env, capture_output=True, text=True)

    def test_outside_a_repository_the_current_directory_is_the_project_root(self):
        (self.root / CONFIG).write_text("spec_output_dir: docs/specs\n")
        out = self.run_script(cwd=self.root)
        self.assertEqual((out.returncode, out.stdout), (0, "dir docs/specs\n"))

    def test_inside_a_repository_its_root_is_the_project_root(self):
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        (self.root / CONFIG).write_text("spec_output_dir: docs/specs\n")
        sub = self.root / "src"
        sub.mkdir()
        out = self.run_script(cwd=sub)
        self.assertEqual((out.returncode, out.stdout), (0, f"dir {self.root}/docs/specs\n"))

    def test_root_names_the_project_root(self):
        (self.root / CONFIG).write_text("spec_output_dir: docs/specs\n")
        out = self.run_script("--root", str(self.root), cwd=self.home)
        self.assertEqual((out.returncode, out.stdout), (0, f"dir {self.root}/docs/specs\n"))

    def test_the_home_config_is_read_from_the_home_directory(self):
        (self.home / CONFIG).write_text("spec_output_dir: ~/specs\n")
        out = self.run_script(cwd=self.root)
        self.assertEqual((out.returncode, out.stdout), (0, f"dir {self.home}/specs\n"))

    def test_an_unknown_argument_is_a_usage_error(self):
        self.assertEqual(self.run_script("--feature", "x", cwd=self.root).returncode, 2)


class OneQuestion(unittest.TestCase):
    """The location question is written in three places, since each must work without the others."""

    def test_the_rules_for_an_agent_that_cannot_run_commands_hold_the_same_line(self):
        self.assertIn(f"`{target.ASK}`", (SKILL / "references" / "saving.md").read_text())

    def test_the_eval_hook_expects_the_same_line(self):
        hooks = (ROOT / "evals" / "write-spec" / "hooks.py").read_text()
        self.assertIn(target.ASK.replace('"', '\\"'), hooks)

    def test_the_golden_reply_is_the_same_line(self):
        golden = (ROOT / "evals" / "write-spec" / "cases" / "ask-location" / "golden.md").read_text()
        self.assertEqual(golden.strip(), target.ASK)


if __name__ == "__main__":
    unittest.main()
