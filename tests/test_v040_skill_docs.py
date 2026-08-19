import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StagedConstructionSkillTests(unittest.TestCase):
    def test_staged_skill_is_narrow_static_and_has_repository_headings(self):
        path = ROOT / "skills" / "abaqus-staged-construction-auditor" / "SKILL.md"
        self.assertTrue(path.is_file(), path)
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        self.assertRegex(frontmatter, r"(?m)^name:\s*abaqus-staged-construction-auditor\s*$")
        description = re.search(r"(?m)^description:\s*(.+)$", frontmatter)
        self.assertIsNotNone(description)
        self.assertTrue(description.group(1).startswith("Use when "))
        for heading in (
            "When to use",
            "Inputs",
            "Outputs",
            "Safety gates",
            "Example prompts",
            "Common failures",
            "Acceptance checklist",
        ):
            self.assertIn(f"## {heading}", text)
        self.assertIn("construction_events", text)
        self.assertIn("C-STAGE-001", text)
        self.assertIn("activate", text)
        self.assertIn("deactivate", text)
        self.assertRegex(text, r"(?i)static|read-only")
        self.assertRegex(text, r"(?i)do not|never")
        private_terms = ("Paper" + "Writing", "Condition" + "Analysis" + "_" + "TwinLine")
        self.assertTrue(all(term.casefold() not in text.casefold() for term in private_terms))
        self.assertNotRegex(text, r"[A-Z]:\\")
        self.assertIn("ordinary", text.lower())
        self.assertIn("abaqus-step", text)


class MappedLoadSkillTests(unittest.TestCase):
    def test_mapped_load_skill_is_narrow_static_and_has_repository_headings(self):
        path = ROOT / "skills" / "abaqus-mapped-load-provenance-auditor" / "SKILL.md"
        self.assertTrue(path.is_file(), path)
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        self.assertRegex(frontmatter, r"(?m)^name:\s*abaqus-mapped-load-provenance-auditor\s*$")
        description = re.search(r"(?m)^description:\s*(.+)$", frontmatter)
        self.assertIsNotNone(description)
        self.assertTrue(description.group(1).startswith("Use when "))
        for heading in (
            "When to use",
            "Inputs",
            "Outputs",
            "Safety gates",
            "Example prompts",
            "Common failures",
            "Acceptance checklist",
        ):
            self.assertIn(f"## {heading}", text)
        self.assertIn("mapped_loads", text)
        self.assertIn("C-MAPLOAD-001", text)
        for field in ("source_sha256", "expected_face_count", "mapped_face_count", "duplicate_face_count", "unmapped_face_count"):
            self.assertIn(field, text)
        self.assertRegex(text, r"(?i)static|read-only")
        self.assertRegex(text, r"(?i)do not|never")
        private_terms = ("Paper" + "Writing", "Condition" + "Analysis" + "_" + "TwinLine")
        self.assertTrue(all(term.casefold() not in text.casefold() for term in private_terms))
        self.assertNotRegex(text, r"[A-Z]:\\")
        self.assertIn("abaqus-load", text)
        self.assertIn("abaqus-export", text)


if __name__ == "__main__":
    unittest.main()
