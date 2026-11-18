"""Tests for implement-task's pick_task.py and verify-spec's check_scope.py: each stop line a script can decide."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PICK = ROOT / "skills" / "implement-task" / "scripts" / "pick_task.py"
SCOPE = ROOT / "skills" / "verify-spec" / "scripts" / "check_scope.py"
sys.path.insert(0, str(ROOT / "skills" / "build-phase" / "scripts"))
import parse_reply  # noqa: E402

TASKS = "docs/specs/reading-time/tasks.md"
REQS = "docs/specs/reading-time/requirements.md"


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def task(tid, status, depends="None.", covers="FR-001", files="`a.py`"):
    status_line = f"**Status:** {status}\n\n" if status else ""
    return (f"#### {tid}: Title of {tid}\n\n**Covers:** {covers}\n\n**Files:** {files}\n\n"
            f"**Depends on:** {depends}\n\n**Done when:** {covers}: a test\n\n{status_line}")


class Project(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root, self.home = Path(tmp.name) / "project", Path(tmp.name) / "home"
        (self.root / "docs" / "specs" / "reading-time").mkdir(parents=True)
        self.home.mkdir()
        (self.root / ".agent-skills-config.yaml").write_text("spec_output_dir: docs/specs\n")

    def git(self, *args):
        cmd = ["git", "-c", "user.name=T", "-c", "user.email=t@example.com", "-c", "commit.gpgsign=false", *args]
        subprocess.run(cmd, cwd=self.root, check=True, capture_output=True)

    def commit_all(self, subject="Initial commit"):
        if not (self.root / ".git").exists():
            self.git("init", "-q", "-b", "main")
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", subject)


class PickTask(Project):
    def setUp(self):
        super().setUp()
        self.module = load(PICK)

    def tasks(self, *tasks):
        text = "# Implementation Tasks: X\n\n## 2. Tasks\n\n### Phase 1: One\n\n" + "".join(tasks)
        (self.root / TASKS).write_text(text + "## 3. Blocked Requirements\n\nBlocked by Q-001: topic\n")

    def run_pick(self, **kwargs):
        return self.module.run(self.root, self.home, feature="reading-time", **kwargs)

    def assert_stop(self, out, line):
        self.assertEqual(out, "stop " + line)
        self.assertEqual(parse_reply.parse_implement(line, strict=True)["kind"], "stop", "the skill's own stop line")

    def fixture(self):
        self.tasks(task("T-1.1", "Done"), task("T-1.2", "Todo", "T-1.1", "FR-002"), task("T-1.3", "Todo", "T-1.1", "FR-003"),
                   task("T-1.4", "Todo", "T-1.2, T-1.3", "FR-001, FR-002, FR-003", "None."))

    def test_next_task_is_the_first_todo_with_its_dependencies_done(self):
        self.fixture()
        self.assertEqual(self.run_pick(), f"found {TASKS}\ntask T-1.2")

    def test_named_task(self):
        self.fixture()
        self.assertEqual(self.run_pick(task="T-1.3"), f"found {TASKS}\ntask T-1.3")
        self.assert_stop(self.run_pick(task="T-9.9"), f"No task T-9.9 in {TASKS}.")
        self.assert_stop(self.run_pick(task="T-1.1"), "T-1.1 is already Done.")
        self.assert_stop(self.run_pick(task="T-1.4"), "T-1.4 depends on T-1.2, T-1.3, not yet Done. Implement those first.")

    def test_only_the_dependencies_not_done_are_named(self):
        self.tasks(task("T-1.1", "Done"), task("T-1.2", "Todo"), task("T-1.3", "Todo", "T-1.1, T-1.2"))
        self.assert_stop(self.run_pick(task="T-1.3"), "T-1.3 depends on T-1.2, not yet Done. Implement those first.")

    def test_a_requirement_stands_for_its_build_task(self):
        self.fixture()
        self.assertEqual(self.run_pick(requirement="FR-003"), f"found {TASKS}\ntask T-1.3")
        self.assert_stop(self.run_pick(requirement="FR-001"), "T-1.1 is already Done.")
        self.assert_stop(self.run_pick(requirement="FR-004"),
                         f"FR-004 has no task in {TASKS}. Add it with write-tasks, then run implement-task again.")

    def test_every_task_done_and_none_ready(self):
        self.tasks(task("T-1.1", "Done"), task("T-1.2", "Done"))
        self.assert_stop(self.run_pick(), f"Every task in {TASKS} is Done.")
        self.tasks(task("T-1.1", "Todo", "T-1.2"), task("T-1.2", "Todo", "T-1.1"))
        self.assert_stop(self.run_pick(), "T-1.1 depends on T-1.2, not yet Done. Implement those first.")

    def test_no_status_lines_and_a_task_without_one(self):
        self.tasks(task("T-1.1", None), task("T-1.2", None))
        line = f"{TASKS} has no task Status lines. Re-run write-tasks to add them, then run implement-task again."
        self.assert_stop(self.run_pick(), line)
        self.tasks(task("T-1.1", "Done"), task("T-1.2", None))
        self.assert_stop(self.run_pick(), "T-1.2 has no Status of Todo or Done. Fix the task with write-tasks, then run implement-task again.")
        self.tasks(task("T-1.1", "Todo", "T-7.7"))
        self.assert_stop(self.run_pick(), "T-1.1 depends on T-7.7, which is not in the file. Fix the task with write-tasks, then run implement-task again.")

    def test_missing_tasks_file_is_the_lookup_stop(self):
        out = self.module.run(self.root, self.home, feature="invoice-export")
        self.assert_stop(out, "No tasks file found at docs/specs/invoice-export/tasks.md. Run write-tasks first, then run implement-task again.")

    def test_uncommitted_changes_outside_the_feature_folder_stop_first(self):
        self.fixture()
        (self.root / "a.py").write_text("x = 1\n")
        self.commit_all()
        self.assertEqual(self.run_pick(), f"found {TASKS}\ntask T-1.2")
        (self.root / "docs" / "specs" / "reading-time" / "plan.md").write_text("# Plan\n")
        self.assertEqual(self.run_pick(), f"found {TASKS}\ntask T-1.2", "the feature's own spec files may be uncommitted")
        (self.root / "a.py").write_text("x = 2\n")
        (self.root / "new.py").write_text("y = 1\n")
        self.assert_stop(self.run_pick(task="T-9.9"), "Uncommitted changes in a.py, new.py. Commit or stash them, then run implement-task again.")

    def test_an_uncommitted_config_file_is_not_a_change(self):
        self.fixture()
        (self.root / "a.py").write_text("x = 1\n")
        self.commit_all()
        self.git("rm", "-q", "--cached", ".agent-skills-config.yaml")
        self.commit_all("Stop tracking the config")
        (self.root / ".agent-skills-config.yaml").write_text("spec_output_dir: docs/specs\nbase_branch: main\n")
        self.assertEqual(self.run_pick(), f"found {TASKS}\ntask T-1.2", "the skills' own settings file may stay untracked")
        (self.root / "sub").mkdir()
        (self.root / "sub" / ".agent-skills-config.yaml").write_text("x: 1\n")
        self.assert_stop(self.run_pick(), "Uncommitted changes in sub/. Commit or stash them, then run implement-task again.")

    def test_a_spec_folder_that_is_wholly_untracked_is_allowed(self):
        (self.root / "a.py").write_text("x = 1\n")
        (self.root / ".gitignore").write_text(".agent-skills-config.yaml\n")
        spec = self.root / "docs"
        import shutil
        shutil.rmtree(spec)
        self.commit_all()
        (spec / "specs" / "reading-time").mkdir(parents=True)
        self.fixture()
        self.assertEqual(self.run_pick(), f"found {TASKS}\ntask T-1.2")

    def test_rework_is_a_todo_task_that_already_has_a_commit(self):
        self.fixture()
        self.commit_all()
        self.commit_all("T-1.2: Title of T-1.2")
        self.assertEqual(self.run_pick(), f"found {TASKS}\ntask T-1.2 rework")
        self.assertEqual(self.run_pick(task="T-1.3"), f"found {TASKS}\ntask T-1.3")

    def test_command_line(self):
        self.fixture()
        run = lambda *args: subprocess.run([sys.executable, str(PICK), "--root", str(self.root), *args], capture_output=True, text=True)
        out = run("--feature", "reading-time", "--task", "T-1.4")
        self.assertEqual((out.returncode, out.stdout.strip()), (0, "stop T-1.4 depends on T-1.2, T-1.3, not yet Done. Implement those first."))
        self.assertEqual(run("--task", "1.4").returncode, 2)
        self.assertEqual(run("--task", "T-1.4", "--requirement", "FR-001").returncode, 2)


class CheckScope(Project):
    def setUp(self):
        super().setUp()
        self.module = load(SCOPE)
        (self.root / REQS).write_text("# Requirements\n\n## 1. Functional Requirements\n\nFR-001: The x shall y.\n\n"
                                      "FR-002: The x shall z. Blocked by Q-001.\n\n## 2. Non-Functional Requirements\n\nNFR-001: The x shall be quick.\n")

    def plan(self):
        (self.root / "docs" / "specs" / "reading-time" / "plan.md").write_text(
            "# Plan\n\n**Requirements:** requirements.md, version 1.0\n\n## 2. Phases\n\n### Phase 1: One\n\n**Requirements:** FR-001, NFR-001\n\n"
            "**Verify:**\n\n- FR-001: a test\n\n### Phase 2: Two\n\n**Requirements:** FR-002\n\n## 3. Blocked Requirements\n\nNone.\n")

    def run_scope(self, **kwargs):
        return self.module.run(self.root, self.home, feature="reading-time", **kwargs)

    def assert_stop(self, out, line):
        self.assertEqual(out, "stop " + line)
        self.assertEqual(parse_reply.parse_verify(line, strict=True)["kind"], "stop", "the skill's own stop line")

    def test_scopes(self):
        self.plan()
        self.assertEqual(self.run_scope(), f"found {REQS}\nscope all")
        self.assertEqual(self.run_scope(req_id="NFR-001"), f"found {REQS}\nscope NFR-001")
        self.assertEqual(self.run_scope(phase="1"), f"found {REQS}\nscope phase 1: FR-001, NFR-001")
        self.assertEqual(self.run_scope(phase="2"), f"found {REQS}\nscope phase 2: FR-002")

    def test_stops(self):
        self.assert_stop(self.run_scope(req_id="FR-009"), f"No requirement FR-009 in {REQS}.")
        plan = "docs/specs/reading-time/plan.md"
        self.assert_stop(self.run_scope(phase="1"), f"No plan file found at {plan}, so phase 1 has no requirements list. Run write-plan first, then run verify-spec again.")
        self.plan()
        self.assert_stop(self.run_scope(phase="7"), f"No phase 7 in {plan}.")
        (self.root / REQS).write_text("# Requirements\n\nNothing yet. See FR-001: later.\n")
        self.assert_stop(self.run_scope(), f"{REQS} has no FR or NFR requirements. Run write-spec first, then run verify-spec again.")
        out = self.module.run(self.root, self.home, feature="invoice-export", req_id="FR-001")
        self.assert_stop(out, "No requirements file found at docs/specs/invoice-export/requirements.md. Run write-spec first, then run verify-spec again.")

    def test_command_line(self):
        run = lambda *args: subprocess.run([sys.executable, str(SCOPE), "--root", str(self.root), *args], capture_output=True, text=True)
        out = run("--feature", "reading-time", "--id", "FR-009")
        self.assertEqual((out.returncode, out.stdout.strip()), (0, f"stop No requirement FR-009 in {REQS}."))
        self.assertEqual(run("--id", "9").returncode, 2)
        self.assertEqual(run("--phase", "one").returncode, 2)


if __name__ == "__main__":
    unittest.main()
