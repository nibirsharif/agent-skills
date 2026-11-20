"""Tests for the word budget check in validate.py: the words a skill makes the agent read on every run."""

import shutil
import tempfile
import unittest
from pathlib import Path

import validate

ROOT = Path(__file__).resolve().parent.parent


class WordBudgetTest(unittest.TestCase):
    def make_skill(self, skill_words=10, files=None):
        """A skill folder named `demo` whose SKILL.md has skill_words words; files maps a path to its word count."""
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        skill = tmp / "demo"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text("word " * skill_words)
        for name, words in (files or {}).items():
            (skill / name).write_text("word\n" * words)
        return skill

    def test_at_the_budget_passes(self):
        skill = self.make_skill(10, {"references/rules.md": 20})
        self.assertEqual(validate.check_budget(skill, {"demo": (30, ["references/rules.md"])}), [])

    def test_over_the_budget_names_each_file(self):
        skill = self.make_skill(10, {"references/rules.md": 21})
        errors = validate.check_budget(skill, {"demo": (30, ["references/rules.md"])})
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("31 words read on every run, over its budget of 30", errors[0])
        self.assertIn("SKILL.md 10, references/rules.md 21", errors[0])

    def test_unlisted_file_is_not_counted(self):
        skill = self.make_skill(10, {"references/rules.md": 20, "references/rare.md": 500})
        self.assertEqual(validate.check_budget(skill, {"demo": (30, ["references/rules.md"])}), [])

    def test_skill_without_a_budget_fails(self):
        errors = validate.check_budget(self.make_skill(), {})
        self.assertTrue(any("no word budget" in e for e in errors), errors)

    def test_listed_file_must_exist_in_the_skill_folder(self):
        skill = self.make_skill(10)
        (skill.parent / "outside.md").write_text("word")
        for name in ("references/gone.md", "../outside.md"):
            errors = validate.check_budget(skill, {"demo": (30, [name])})
            self.assertTrue(any(f"names '{name}'" in e for e in errors), errors)

    def test_every_real_skill_has_a_budget_and_meets_it(self):
        skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir() and not p.name.startswith("."))
        self.assertEqual(sorted(validate.WORD_BUDGETS), [p.name for p in skills])
        for skill in skills:
            self.assertEqual(validate.check_budget(skill), [])


if __name__ == "__main__":
    unittest.main()
