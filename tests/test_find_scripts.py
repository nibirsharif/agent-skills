"""Tests for the lookup scripts: implement-task and build-phase's find_tasks.py and verify-spec's
find_requirements.py. A named feature is looked up at one path only, and the three copies stay the same."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent / "skills"
SCRIPTS = {
    "implement-task": SKILLS / "implement-task" / "scripts" / "find_tasks.py",
    "verify-spec": SKILLS / "verify-spec" / "scripts" / "find_requirements.py",
    "build-phase": SKILLS / "build-phase" / "scripts" / "find_tasks.py",
}
MARKER = "# Everything below this line is the same in every skill's copy of this script"


def load(skill):
    spec = importlib.util.spec_from_file_location(f"find_{skill.replace('-', '_')}", SCRIPTS[skill])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Project(unittest.TestCase):
    """A project folder and a home folder, both temporary, so the user's own config is never read."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root, self.home = Path(tmp.name) / "project", Path(tmp.name) / "home"
        self.root.mkdir()
        self.home.mkdir()

    def project(self, *features, files=("tasks.md", "requirements.md"), config="spec_output_dir: docs/specs\n"):
        if config is not None:
            (self.root / ".agent-skills-config.yaml").write_text(config)
        for name in features:
            folder = self.root / "docs" / "specs" / name
            folder.mkdir(parents=True, exist_ok=True)
            for file in files:
                (folder / file).write_text("# File\n")


class SharedCore(unittest.TestCase):
    def test_the_three_copies_are_identical_below_the_marker(self):
        cores = {}
        for skill, path in SCRIPTS.items():
            text = path.read_text()
            self.assertEqual(text.count(MARKER), 1, skill)
            cores[skill] = text.split(MARKER)[1]
        self.assertEqual(len(set(cores.values())), 1)


class OneLineSkills(Project):
    """implement-task and verify-spec: a stop is one line."""

    CASES = {
        "implement-task": ("tasks.md", "stop No tasks file found at {}. Run write-tasks first, then run implement-task again."),
        "verify-spec": ("requirements.md", "stop No requirements file found at {}. Run write-spec first, then run verify-spec again."),
    }

    def each(self):
        for skill, (file, stop) in self.CASES.items():
            with self.subTest(skill=skill):
                module = load(skill)
                yield file, stop, lambda module=module, **kwargs: module.find(self.root, self.home, **kwargs)

    def test_named_feature_is_found(self):
        self.project("reading-time", "invoice-export")
        for file, _, find in self.each():
            self.assertEqual(find(feature="reading-time"), f"found docs/specs/reading-time/{file}")

    def test_named_feature_without_the_file_stops_even_when_another_feature_has_it(self):
        self.project("reading-time")
        (self.root / "docs" / "specs" / "invoice-export").mkdir()
        for file, stop, find in self.each():
            self.assertEqual(find(feature="invoice-export"), stop.format(f"docs/specs/invoice-export/{file}"))
            self.assertEqual(find(feature="no-folder"), stop.format(f"docs/specs/no-folder/{file}"))

    def test_no_feature_uses_the_only_one(self):
        self.project("reading-time")
        for file, _, find in self.each():
            self.assertEqual(find(), f"found docs/specs/reading-time/{file}")

    def test_no_feature_with_several_or_none_asks(self):
        self.project()
        for file, _, find in self.each():
            self.assertTrue(find().startswith(f"ask No {file} under docs/specs"))
        self.project("b-feature", "a-feature", config=None)
        for _, _, find in self.each():
            self.assertEqual(find(), "ask Which feature: a-feature, b-feature")

    def test_a_named_path(self):
        self.project("reading-time")
        for file, stop, find in self.each():
            self.assertEqual(find(path=f"docs/specs/reading-time/{file}"), f"found docs/specs/reading-time/{file}")
            self.assertEqual(find(path=f"notes/{file}"), stop.format(f"notes/{file}"))

    def test_config_project_wins_then_home_then_ask(self):
        self.project(config=None)
        for file, stop, find in self.each():
            config = self.root / ".agent-skills-config.yaml"
            config.unlink(missing_ok=True)
            (self.home / ".agent-skills-config.yaml").unlink(missing_ok=True)
            self.assertTrue(find(feature="x").startswith("ask No spec_output_dir is set"))
            (self.home / ".agent-skills-config.yaml").write_text("spec_output_dir: specs   # shared\n")
            self.assertEqual(find(feature="x"), stop.format(f"specs/x/{file}"))
            config.write_text("test_command: make test\nspec_output_dir: 'docs/specs/'\n")
            self.assertEqual(find(feature="x"), stop.format(f"docs/specs/x/{file}"))
            config.write_text("spec_output_dir:\n")
            self.assertEqual(find(feature="x"), stop.format(f"specs/x/{file}"))

    def test_absolute_spec_output_dir(self):
        self.project("reading-time", config=None)
        absolute = self.root / "docs" / "specs"
        (self.root / ".agent-skills-config.yaml").write_text(f"spec_output_dir: {absolute}\n")
        for file, _, find in self.each():
            self.assertEqual(find(feature="reading-time"), f"found {absolute}/reading-time/{file}")

    def test_command_line(self):
        self.project("reading-time")
        for skill, (file, stop) in self.CASES.items():
            run = lambda *args: subprocess.run([sys.executable, str(SCRIPTS[skill]), "--root", str(self.root), *args],
                                               capture_output=True, text=True)
            out = run("--feature", "invoice-export")
            self.assertEqual((out.returncode, out.stdout.strip()), (0, stop.format(f"docs/specs/invoice-export/{file}")))
            self.assertEqual(run("--feature", "../x").returncode, 2)
            self.assertEqual(run("--feature", "a", "--path", "b").returncode, 2)


class BuildPhase(Project):
    """build-phase: a stop is the whole stopped summary, and requirements.md must be beside tasks.md."""

    def setUp(self):
        super().setUp()
        self.module = load("build-phase")
        git = ["git", "-c", "user.name=T", "-c", "user.email=t@example.com", "-c", "commit.gpgsign=false"]
        for cmd in (["git", "init", "-q", "-b", "main"], git + ["commit", "-q", "--allow-empty", "-m", "Initial commit"]):
            subprocess.run(cmd, cwd=self.root, check=True, capture_output=True)

    def find(self, **kwargs):
        return self.module.find(self.root, self.home, **kwargs)

    def summary(self, feature, stopped, branch="main"):
        return "\n".join(["stop", f"Phase ? of {feature}: stopped", f"Branch: {branch}",
                          "Tasks: 0 implemented, 0 reworked", "Verify: not run", f"Stopped: {stopped}"])

    def test_found_needs_requirements_beside_it(self):
        self.project("reading-time")
        self.assertEqual(self.find(feature="reading-time"), "found docs/specs/reading-time/tasks.md\nrounds 2")
        self.project("no-reqs", files=("tasks.md",))
        self.assertEqual(self.find(feature="no-reqs"), self.summary(
            "no-reqs", "No requirements file found at docs/specs/no-reqs/requirements.md. Run write-spec first, then run build-phase again."))

    def test_rounds_is_the_configured_limit_or_the_default(self):
        config = "spec_output_dir: docs/specs\nbuild_max_rework_rounds:{}\n"
        for written, line in (("", "rounds 2"), (" 0", "rounds 0"), (" 3  # more", "rounds 3")):
            self.project("reading-time", config=config.format(written))
            self.assertEqual(self.find(feature="reading-time").split("\n")[1], line)
        (self.root / ".agent-skills-config.yaml").write_text("spec_output_dir: docs/specs\n")
        (self.home / ".agent-skills-config.yaml").write_text("build_max_rework_rounds: 1\n")
        self.assertEqual(self.find(feature="reading-time").split("\n")[1], "rounds 1")
        self.project("reading-time", config=config.format(" two"))
        self.assertTrue(self.find(feature="reading-time").startswith("ask build_max_rework_rounds"))

    def test_missing_tasks_is_the_whole_stopped_summary(self):
        self.project("reading-time")
        stopped = "No tasks file found at docs/specs/invoice-export/tasks.md. Run write-tasks first, then run build-phase again."
        self.assertEqual(self.find(feature="invoice-export"), self.summary("invoice-export", stopped))
        self.assertEqual(self.find(path="docs/specs/invoice-export/tasks.md"), self.summary("invoice-export", stopped))

    def test_the_summary_passes_the_eval_hook(self):
        sys.path.insert(0, str(SKILLS.parent / "evals"))
        import grading
        self.project("reading-time")
        reply = self.find(feature="invoice-export").split("\n", 1)[1]
        self.assertEqual(grading.load_hooks("build-phase").check(reply), [])

    def test_branch_is_the_current_one_or_none(self):
        self.project("reading-time")
        subprocess.run(["git", "switch", "-q", "-c", "reading-time/phase-1"], cwd=self.root, check=True)
        self.assertIn("\nBranch: reading-time/phase-1\n", self.find(feature="x"))
        subprocess.run(["git", "switch", "-q", "--detach"], cwd=self.root, check=True)
        self.assertIn("\nBranch: none\n", self.find(feature="x"))


if __name__ == "__main__":
    unittest.main()
