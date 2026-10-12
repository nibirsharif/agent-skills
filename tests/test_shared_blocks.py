"""Tests for repo-wide consistency: release metadata guards and the shared "find the files" rule."""

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import validate

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["write-spec", "write-plan", "implement-task", "verify-spec"]
# The part of the "find the files" step that every skill must word the same way.
CONFIG_RULE_RE = re.compile(r"`spec_output_dir` from `\.agent-skills-config\.yaml`.*?against the project root\.")


class SharedBlockTest(unittest.TestCase):
    def test_config_lookup_rule_is_identical(self):
        found = {}
        for name in SKILLS:
            text = (ROOT / "skills" / name / "SKILL.md").read_text()
            m = CONFIG_RULE_RE.search(text)
            self.assertIsNotNone(m, f"{name}: no spec_output_dir lookup rule")
            found[name] = m.group(0)
        self.assertEqual(len(set(found.values())), 1, found)


class ReleaseCheckTest(unittest.TestCase):
    def make_repo(self, plugin_version="1.0.0", market_version="1.0.0", changelog="## 1.0.0\n", readme_skills=("a",)):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        meta = tmp / ".claude-plugin"
        meta.mkdir()
        (meta / "plugin.json").write_text(json.dumps({"name": "p", "version": plugin_version, "skills": ["./skills/a"]}))
        (meta / "marketplace.json").write_text(json.dumps({"plugins": [{"name": "p", "version": market_version}]}))
        (tmp / "CHANGELOG.md").write_text(changelog)
        (tmp / "README.md").write_text("".join(f"| [{s}](skills/{s}/SKILL.md) | x |\n" for s in readme_skills))
        return tmp

    def test_consistent_repo_passes(self):
        self.assertEqual(validate.check_release(self.make_repo()), [])

    def test_version_mismatch(self):
        errors = validate.check_release(self.make_repo(market_version="0.9.0"))
        self.assertTrue(any("differs from plugin.json" in e for e in errors), errors)

    def test_missing_changelog_heading(self):
        errors = validate.check_release(self.make_repo(changelog="## Unreleased\n"))
        self.assertTrue(any("CHANGELOG.md" in e for e in errors), errors)

    def test_readme_table_mismatch(self):
        errors = validate.check_release(self.make_repo(readme_skills=("a", "b")))
        self.assertTrue(any("'b'" in e for e in errors), errors)
        errors = validate.check_release(self.make_repo(readme_skills=()))
        self.assertTrue(any("'a'" in e for e in errors), errors)

    def test_real_repo_passes(self):
        self.assertEqual(validate.check_release(), [])


if __name__ == "__main__":
    unittest.main()
