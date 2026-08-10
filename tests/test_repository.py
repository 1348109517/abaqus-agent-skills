import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "abaqus-bc",
    "abaqus-dependency-preflight-validator",
    "abaqus-load",
    "abaqus-material",
    "abaqus-odb",
    "abaqus-parametric-project-starter",
    "abaqus-script-debugging-checklist",
    "abaqus-shared-naming-manifest-builder",
    "abaqus-step",
    "abaqus-tunnel-local-mesh-rebuilder",
}
REQUIRED_HEADINGS = {
    "When to use",
    "Inputs",
    "Outputs",
    "Safety gates",
    "Example prompts",
    "Common failures",
    "Acceptance checklist",
}
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".txt"}
SENSITIVE_PATTERNS = {
    "absolute Windows path": re.compile(r"(?i)(?<![A-Za-z])[C-Z]:[\\/]"),
    "email address": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    "private project term": re.compile(r"(?i)PaperWriting|ConditionAnalysis_TwinLine"),
    "credential": re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*[^\s`]+"),
}


def text_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES and ".git" not in path.parts:
            yield path


class RepositoryContractTests(unittest.TestCase):
    def test_exact_skill_set(self):
        skills_root = ROOT / "skills"
        actual = {path.name for path in skills_root.iterdir() if path.is_dir()} if skills_root.exists() else set()
        self.assertEqual(EXPECTED_SKILLS, actual)

    def test_skill_frontmatter_and_sections(self):
        for name in EXPECTED_SKILLS:
            with self.subTest(skill=name):
                path = ROOT / "skills" / name / "SKILL.md"
                self.assertTrue(path.is_file(), path)
                text = path.read_text(encoding="utf-8")
                match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
                self.assertIsNotNone(match, f"invalid front matter: {path}")
                frontmatter = match.group(1)
                self.assertRegex(frontmatter, rf"(?m)^name:\s*{re.escape(name)}\s*$")
                description = re.search(r"(?m)^description:\s*(.+)$", frontmatter)
                self.assertIsNotNone(description)
                self.assertTrue(description.group(1).startswith("Use when "))
                headings = set(re.findall(r"(?m)^## (.+?)\s*$", text))
                self.assertFalse(REQUIRED_HEADINGS - headings, f"missing headings in {path}: {REQUIRED_HEADINGS - headings}")

    def test_relative_markdown_links_resolve(self):
        pattern = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
        for path in text_files():
            if path.suffix.lower() != ".md":
                continue
            for target in pattern.findall(path.read_text(encoding="utf-8")):
                clean = target.split("#", 1)[0]
                if clean:
                    self.assertTrue((path.parent / clean).resolve().exists(), f"broken link {target} in {path}")

    def test_release_files_contain_no_sensitive_text(self):
        excluded = {ROOT / "tests" / "test_repository.py"}
        for path in text_files():
            if path in excluded or "superpowers" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for label, pattern in SENSITIVE_PATTERNS.items():
                self.assertIsNone(pattern.search(text), f"{label} found in {path}")

    def test_no_large_or_binary_release_files(self):
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
                continue
            self.assertLessEqual(path.stat().st_size, 1024 * 1024, f"file exceeds 1 MiB: {path}")
            if "superpowers" not in path.parts:
                sample = path.read_bytes()[:4096]
                self.assertNotIn(b"\x00", sample, f"binary file: {path}")


if __name__ == "__main__":
    unittest.main()
