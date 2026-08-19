import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
ROUTING_CASES = ROOT / "examples" / "skill-routing-cases.json"
BASELINE_NOTE = ROOT / "docs" / "evaluation" / "v0.4.0-routing-baseline.md"

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
EXPECTED_OVERLAPS = {
    "staged-vs-step": {
        "primary": "abaqus-staged-construction-auditor",
        "related": ["abaqus-step"],
    },
    "mapped-vs-load": {
        "primary": "abaqus-mapped-load-provenance-auditor",
        "related": ["abaqus-load"],
    },
    "mapped-vs-output": {
        "primary": "abaqus-mapped-load-provenance-auditor",
        "related": ["abaqus-output"],
    },
}


class Version040RepositoryTests(unittest.TestCase):
    def test_exact_skill_set_is_nineteen(self):
        actual = {
            path.name
            for path in SKILLS_ROOT.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        }
        self.assertEqual(EXPECTED_SKILLS, actual)

    def test_every_skill_has_required_openai_metadata(self):
        for name in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=name):
                path = SKILLS_ROOT / name / "agents" / "openai.yaml"
                self.assertTrue(path.is_file(), path)
                text = path.read_text(encoding="utf-8")
                self.assertIn("interface:", text)
                display = re.search(r'(?m)^  display_name:\s*"([^"]+)"$', text)
                short = re.search(r'(?m)^  short_description:\s*"([^"]+)"$', text)
                prompt = re.search(r'(?m)^  default_prompt:\s*"([^"]+)"$', text)
                self.assertIsNotNone(display)
                self.assertIsNotNone(short)
                self.assertIsNotNone(prompt)
                self.assertGreaterEqual(len(short.group(1)), 25)
                self.assertLessEqual(len(short.group(1)), 64)
                self.assertNotIn("Help with", short.group(1))
                self.assertIn(f"${name}", prompt.group(1))
                self.assertNotRegex(text, r"(?i)brand_color|icon_small|icon_large|openai|simulia|Dassault")

    def test_routing_corpus_covers_three_positive_and_two_negative_cases(self):
        corpus = json.loads(ROUTING_CASES.read_text(encoding="utf-8"))
        self.assertEqual(EXPECTED_SKILLS, set(corpus["skills"]))
        for name, cases in corpus["skills"].items():
            with self.subTest(skill=name):
                self.assertEqual(3, len(cases["positive"]))
                self.assertEqual(2, len(cases["negative"]))
                self.assertTrue(all(isinstance(item, str) and item.strip() for item in cases["positive"]))
                self.assertTrue(all(isinstance(item, str) and item.strip() for item in cases["negative"]))
        self.assertEqual(
            {"staged-vs-step", "mapped-vs-load", "mapped-vs-output"},
            {item["name"] for item in corpus["overlap"]},
        )

    def test_overlap_corpus_has_exact_routes_and_nonempty_references(self):
        corpus = json.loads(ROUTING_CASES.read_text(encoding="utf-8"))
        overlaps = {item["name"]: item for item in corpus["overlap"]}
        self.assertEqual(set(EXPECTED_OVERLAPS), set(overlaps))
        for name, expected in EXPECTED_OVERLAPS.items():
            with self.subTest(overlap=name):
                item = overlaps[name]
                self.assertIsInstance(item.get("prompt"), str)
                self.assertTrue(item["prompt"].strip())
                self.assertEqual(expected["primary"], item.get("primary"))
                self.assertEqual(expected["related"], item.get("related"))
                self.assertIn(item["primary"], EXPECTED_SKILLS)
                self.assertTrue(item["related"])
                self.assertTrue(all(skill in EXPECTED_SKILLS for skill in item["related"]))

    def test_routing_corpus_is_public_safe_and_baseline_note_is_present(self):
        corpus_text = ROUTING_CASES.read_text(encoding="utf-8")
        baseline_text = BASELINE_NOTE.read_text(encoding="utf-8")
        private_terms = ("Paper" + "Writing", "Condition" + "Analysis" + "_" + "TwinLine")
        for text in (corpus_text, baseline_text):
            for term in private_terms:
                self.assertNotIn(term.casefold(), text.casefold())
            self.assertNotRegex(text, r"(?i)(?:[A-Z]:\\|/Users/|/home/)")
        self.assertIn("dependency-preflight", baseline_text)
        self.assertIn("abaqus-step", baseline_text)
        self.assertIn("abaqus-load", baseline_text)
        self.assertIn("abaqus-export", baseline_text)
        self.assertIn("primary route", baseline_text.lower())


if __name__ == "__main__":
    unittest.main()
