import os
import re
import subprocess
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
    "abaqus-mapped-load-provenance-auditor",
    "abaqus-odb",
    "abaqus-output",
    "abaqus-parametric-project-starter",
    "abaqus-script-debugging-checklist",
    "abaqus-shared-naming-manifest-builder",
    "abaqus-staged-construction-auditor",
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
TEXT_SUFFIXES = {".cff", ".json", ".md", ".py", ".yml", ".yaml", ".txt"}
TEXT_FILENAMES = {"LICENSE", "NOTICE"}
INTERNAL_SCRATCH_PARTS = frozenset(
    {".git", ".worktrees", "worktrees", "build", "dist", "__pycache__", ".superpowers"}
)
SENSITIVE_PATTERNS = {
    "absolute Windows path": re.compile(r"(?i)(?<![A-Za-z])[C-Z]:[\\/]"),
    "email address": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    "private project term": re.compile(
        "(?i)" + "Paper" + "Writing" + "|" + "Condition" + "Analysis_TwinLine"
    ),
    "credential": re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*[^\s`]+"),
}


def is_internal_scratch(path: Path) -> bool:
    return any(part.casefold() in INTERNAL_SCRATCH_PARTS for part in path.parts)


def _git_tracked_files(root: Path):
    if not (root / ".git").exists():
        return None
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
            ],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    paths = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        path = root / raw_path.decode("utf-8")
        if path.is_file() and not path.is_symlink():
            paths.append(path)
    return tuple(sorted(paths, key=lambda path: path.relative_to(root).as_posix()))


def release_files(root: Path = ROOT):
    root = Path(root)
    tracked = _git_tracked_files(root)
    if tracked is not None:
        yield from tracked
        return
    candidates = sorted(root.rglob("*"), key=lambda path: path.relative_to(root).as_posix())
    for path in candidates:
        if (
            path.is_file()
            and not path.is_symlink()
            and not is_internal_scratch(path)
        ):
            yield path


def _is_utf8_text(path: Path) -> bool:
    try:
        payload = path.read_bytes()
        if b"\x00" in payload:
            return False
        payload.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return True


def text_files(root: Path = ROOT):
    for path in release_files(root):
        if (
            (
                path.suffix.lower() in TEXT_SUFFIXES
                or path.name.upper() in TEXT_FILENAMES
                or not path.suffix
            )
            and _is_utf8_text(path)
        ):
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

    def test_git_checkout_scan_uses_tracked_files_and_catches_tracked_sensitive_blob(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            (root / ".gitignore").write_text("build/\n.worktrees/\n", encoding="utf-8")
            notice = root / "NOTICE"
            notice.write_text("Public attribution", encoding="utf-8")
            tracked_test = root / "tests" / "fixture.txt"
            tracked_test.parent.mkdir()
            tracked_test.write_text("C:" + "\\private\\tracked-value", encoding="utf-8")
            ignored_worktree = root / ".worktrees" / "local" / "secret.md"
            ignored_worktree.parent.mkdir(parents=True)
            ignored_worktree.write_text("C:" + "\\private\\ignored-value", encoding="utf-8")
            ignored_build = root / "build" / "report.md"
            ignored_build.parent.mkdir()
            ignored_build.write_text("C:" + "\\private\\ignored-build", encoding="utf-8")
            subprocess.run(["git", "add", ".gitignore", "NOTICE", "tests/fixture.txt"], cwd=root, check=True)
            tracked = set(release_files(root))
            self.assertIn(notice, tracked)
            self.assertIn(tracked_test, tracked)
            self.assertNotIn(ignored_worktree, tracked)
            self.assertNotIn(ignored_build, tracked)
            text_paths = set(text_files(root))
            self.assertIn(tracked_test, text_paths)
            self.assertIsNotNone(SENSITIVE_PATTERNS["absolute Windows path"].search(tracked_test.read_text()))

    def test_fallback_scan_excludes_worktrees_build_dist_and_python_cache(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            public = root / "README.md"
            public.write_text("public", encoding="utf-8")
            tests_file = root / "tests" / "test_public.py"
            tests_file.parent.mkdir()
            tests_file.write_text("public", encoding="utf-8")
            excluded = (
                root / ".git" / "metadata.txt",
                root / ".worktrees" / "scratch.md",
                root / "worktrees" / "scratch.md",
                root / "build" / "report.md",
                root / "dist" / "package.md",
                root / "__pycache__" / "module.py",
            )
            for path in excluded:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("internal", encoding="utf-8")
            paths = set(release_files(root))
            self.assertEqual({public, tests_file}, paths)

    def test_git_checkout_scan_covers_tracked_staged_and_untracked_public_text(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            (root / ".gitignore").write_text("ignored.json\nbuild/\n", encoding="utf-8")
            tracked = {
                root / "NOTICE": "Public notice\n",
                root / "LICENSE": "Public license\n",
                root / "CITATION.cff": "cff-version: 1.2.0\n",
                root / "contract.json": "{}\n",
                root / "README": "UTF-8 text without an extension\n",
            }
            for path, contents in tracked.items():
                path.write_text(contents, encoding="utf-8")
            subprocess.run(["git", "add", ".gitignore", *[str(path.name) for path in tracked]], cwd=root, check=True)

            staged = root / "staged.json"
            staged.write_text('{"staged": true}\n', encoding="utf-8")
            subprocess.run(["git", "add", staged.name], cwd=root, check=True)

            untracked = {
                root / "untracked.json": "{\"untracked\": true}\n",
                root / "untracked.cff": "message: public\n",
                root / "UNTRACKED": "another UTF-8 text file\n",
            }
            for path, contents in untracked.items():
                path.write_text(contents, encoding="utf-8")
            ignored = root / "ignored.json"
            ignored.write_text("{\"ignored\": true}\n", encoding="utf-8")
            binary_json = root / "binary.json"
            binary_json.write_bytes(b"{\x00binary\x00}\n")

            release_paths = set(release_files(root))
            text_paths = set(text_files(root))
            expected_text = set(tracked) | {staged} | set(untracked)
            for path in expected_text:
                self.assertIn(path, release_paths)
                self.assertIn(path, text_paths)
            self.assertNotIn(ignored, release_paths)
            self.assertNotIn(binary_json, text_paths)

    def test_archive_fallback_excludes_symlinks_and_is_sorted(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "z.txt").write_text("z", encoding="utf-8")
            (root / "a.txt").write_text("a", encoding="utf-8")
            nested = root / "nested"
            nested.mkdir()
            (nested / "m.txt").write_text("m", encoding="utf-8")
            link = root / "linked.txt"
            try:
                os.symlink(root / "a.txt", link)
            except OSError as error:
                self.skipTest(f"symlink creation denied: {error}")

            paths = list(release_files(root))
            self.assertEqual(
                sorted(paths, key=lambda path: path.relative_to(root).as_posix()),
                paths,
            )
            self.assertNotIn(link, paths)
            self.assertTrue(all(not path.is_symlink() for path in paths))

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
