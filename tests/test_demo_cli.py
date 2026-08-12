import json
import subprocess
import sys
import unittest
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_demo.py"
SCENARIOS = ROOT / "examples" / "synthetic-tunnel-review"
NO_SOLVER_REMINDER = (
    "Static contract review only. No Abaqus solver execution or physical "
    "engineering validation was performed."
)


class DemoCliTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_default_command_writes_both_reports(self):
        with TemporaryDirectory() as directory:
            result = self.run_cli("--output-dir", directory)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((Path(directory) / "report.json").is_file())
            self.assertTrue((Path(directory) / "report.md").is_file())
            self.assertIn("Scenario: complete", result.stdout)
            self.assertIn("Input:", result.stdout)
            self.assertIn("PASS: 8", result.stdout)
            self.assertIn("WARNING: 0", result.stdout)
            self.assertIn("REVIEW_REQUIRED: 0", result.stdout)
            self.assertIn(str(Path(directory) / "report.json"), result.stdout)
            self.assertIn(str(Path(directory) / "report.md"), result.stdout)
            self.assertIn(NO_SOLVER_REMINDER, result.stdout)

    def test_review_required_scenario_is_a_completed_demo(self):
        with TemporaryDirectory() as directory:
            result = self.run_cli(
                "--scenario", "naming-drift", "--output-dir", directory
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Scenario: naming-drift", result.stdout)
            self.assertIn("REVIEW_REQUIRED: 1", result.stdout)
            self.assertIn(NO_SOLVER_REMINDER, result.stdout)
            payload = json.loads((Path(directory) / "report.json").read_text())
            self.assertEqual(1, payload["summary"]["REVIEW_REQUIRED"])

    def test_invalid_contract_returns_two(self):
        with TemporaryDirectory() as directory:
            contract = Path(directory) / "invalid.json"
            contract.write_text("[]", encoding="utf-8")
            result = self.run_cli(
                "--contract",
                str(contract),
                "--output-dir",
                str(Path(directory) / "out"),
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("top-level JSON object", result.stderr)
            self.assertEqual("", result.stdout)
            self.assertFalse((Path(directory) / "out").exists())

    def test_custom_contract_with_contract_finding_returns_two_without_reports(self):
        with TemporaryDirectory() as directory:
            contract = json.loads(
                (SCENARIOS / "complete" / "model-contract.json").read_text(
                    encoding="utf-8"
                )
            )
            contract["model"]["instances"][0]["part"] = []
            contract_path = Path(directory) / "invalid-shape.json"
            output = Path(directory) / "out"
            contract_path.write_text(json.dumps(contract), encoding="utf-8")

            result = self.run_cli(
                "--contract", str(contract_path), "--output-dir", str(output)
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("C-CONTRACT-001", result.stderr)
            self.assertEqual("", result.stdout)
            self.assertFalse(output.exists())

    def test_scenario_and_contract_are_mutually_exclusive(self):
        with TemporaryDirectory() as directory:
            result = self.run_cli(
                "--scenario",
                "complete",
                "--contract",
                str(SCENARIOS / "complete" / "model-contract.json"),
                "--output-dir",
                directory,
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("not allowed with argument", result.stderr)
            self.assertEqual("", result.stdout)
            self.assertFalse((Path(directory) / "report.json").exists())

    def test_unknown_scenario_is_invalid_input(self):
        with TemporaryDirectory() as directory:
            result = self.run_cli("--scenario", "missing", "--output-dir", directory)
            self.assertEqual(2, result.returncode)
            self.assertIn("scenario", result.stderr.lower())
            self.assertEqual("", result.stdout)
            self.assertFalse((Path(directory) / "report.json").exists())

    def test_traversal_shaped_scenario_is_invalid_input(self):
        with TemporaryDirectory() as directory:
            result = self.run_cli(
                "--scenario", "../synthetic-tunnel-review/complete", "--output-dir", directory
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("scenario", result.stderr.lower())
            self.assertEqual("", result.stdout)
            self.assertFalse((Path(directory) / "report.json").exists())

    def test_custom_contract_uses_contract_scenario_for_default_output(self):
        with TemporaryDirectory() as directory:
            custom = Path(directory) / "custom-contract.json"
            source = SCENARIOS / "complete" / "model-contract.json"
            scenario = f"custom-{uuid.uuid4().hex}"
            contract = json.loads(source.read_text(encoding="utf-8"))
            contract["scenario_id"] = scenario
            custom.write_text(json.dumps(contract), encoding="utf-8")
            result = self.run_cli("--contract", str(custom))
            self.assertEqual(0, result.returncode, result.stderr)
            output = ROOT / "build" / "demo" / scenario
            try:
                self.assertTrue((output / "report.json").is_file())
                self.assertTrue((output / "report.md").is_file())
                self.assertIn(f"Scenario: {scenario}", result.stdout)
                self.assertIn(str(output / "report.json"), result.stdout)
            finally:
                for path in (output / "report.json", output / "report.md"):
                    if path.exists():
                        path.unlink()
                if output.exists():
                    output.rmdir()

    def test_report_collision_is_an_io_error_without_partial_output(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "out"
            output.mkdir()
            (output / "report.json").write_text("different", encoding="utf-8")
            result = self.run_cli(
                "--scenario", "complete", "--output-dir", str(output)
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("non-identical report", result.stderr)
            self.assertEqual("different", (output / "report.json").read_text())
            self.assertFalse((output / "report.md").exists())

    def test_output_directory_file_is_an_io_error(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            output.write_text("not a directory", encoding="utf-8")
            result = self.run_cli("--scenario", "complete", "--output-dir", str(output))
            self.assertEqual(2, result.returncode)
            self.assertIn("output", result.stderr.lower())
            self.assertEqual("", result.stdout)


if __name__ == "__main__":
    unittest.main()
