import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "abaqus-bc",
    "abaqus-dependency-preflight-validator",
    "abaqus-docs",
    "abaqus-export",
    "abaqus-field",
    "abaqus-geometry",
    "abaqus-interaction",
    "abaqus-load",
    "abaqus-material",
    "abaqus-mesh",
    "abaqus-odb",
    "abaqus-output",
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
INTERNAL_SCRATCH_PARTS = frozenset({".superpowers"})
SENSITIVE_PATTERNS = {
    "absolute Windows path": re.compile(r"(?i)(?<![A-Za-z])[C-Z]:[\\/]"),
    "email address": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    "private project term": re.compile(r"(?i)PaperWriting|ConditionAnalysis_TwinLine"),
    "credential": re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*[^\s`]+"),
}


def is_internal_scratch(path: Path) -> bool:
    return any(part.casefold() in INTERNAL_SCRATCH_PARTS for part in path.parts)


def release_files(root: Path = ROOT):
    for path in root.rglob("*"):
        if (
            path.is_file()
            and ".git" not in path.parts
            and "__pycache__" not in path.parts
            and not is_internal_scratch(path)
        ):
            yield path


def text_files(root: Path = ROOT):
    for path in release_files(root):
        if path.suffix.lower() in TEXT_SUFFIXES:
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
            if path in excluded:
                continue
            text = path.read_text(encoding="utf-8")
            for label, pattern in SENSITIVE_PATTERNS.items():
                self.assertIsNone(pattern.search(text), f"{label} found in {path}")

    def test_release_scan_is_self_contained_for_internal_scratch_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            public_text = root / "README.md"
            public_text.write_text("public", encoding="utf-8")
            public_binary = root / "public.bin"
            public_binary.write_bytes(b"\x00public")
            (root / ".superpowers" / "scratch.md").parent.mkdir(parents=True)
            (root / ".superpowers" / "scratch.md").write_text("scratch", encoding="utf-8")
            (root / ".superpowers" / "scratch.bin").write_bytes(b"\x00scratch")
            (root / "docs" / "superpowers" / "scratch.md").parent.mkdir(parents=True)
            (root / "docs" / "superpowers" / "scratch.md").write_text("scratch", encoding="utf-8")
            (root / "docs" / "superpowers" / "scratch.bin").write_bytes(b"\x00scratch")
            (root / ".git" / "metadata.txt").parent.mkdir(parents=True)
            (root / ".git" / "metadata.txt").write_text("internal", encoding="utf-8")
            (root / "__pycache__" / "module.pyc").parent.mkdir(parents=True)
            (root / "__pycache__" / "module.pyc").write_bytes(b"\x00internal")
            release_paths = set(release_files(root))
            text_paths = set(text_files(root))
            self.assertEqual(
                {
                    public_text,
                    public_binary,
                    root / "docs" / "superpowers" / "scratch.md",
                    root / "docs" / "superpowers" / "scratch.bin",
                },
                release_paths,
            )
            self.assertEqual(
                {public_text, root / "docs" / "superpowers" / "scratch.md"},
                text_paths,
            )

    def test_no_large_or_binary_release_files(self):
        for path in release_files():
            self.assertLessEqual(path.stat().st_size, 1024 * 1024, f"file exceeds 1 MiB: {path}")
            sample = path.read_bytes()[:4096]
            self.assertNotIn(b"\x00", sample, f"binary file: {path}")

    def test_public_compatibility_contract_is_documented(self):
        compatibility = ROOT / "docs" / "compatibility.md"
        self.assertTrue(compatibility.is_file(), compatibility)
        text = compatibility.read_text(encoding="utf-8")
        for term in ("Abaqus/CAE", "abqpy", "read-only", "dry-run", "engineering review"):
            self.assertIn(term, text, term)


if __name__ == "__main__":
    unittest.main()
