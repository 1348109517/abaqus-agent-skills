import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from abaqus_agent_demo import __version__
from abaqus_agent_demo.checks import audit_contract
from abaqus_agent_demo.report import (
    build_report,
    render_json,
    render_markdown,
    report_payload,
    write_reports,
)
from tests.demo_fixtures import complete_contract


class ReportTests(unittest.TestCase):
    def make_report(self):
        contract = complete_contract()
        with TemporaryDirectory() as directory:
            path = Path(directory) / "model-contract.json"
            path.write_text(json.dumps(contract, sort_keys=True), encoding="utf-8")
            return build_report(path, contract, audit_contract(contract))

    def test_build_report_contains_contract_identity_and_findings(self):
        report = self.make_report()

        self.assertEqual("1.0", report.schema_version)
        self.assertEqual(__version__, report.runner_version)
        self.assertEqual("complete", report.scenario_id)
        self.assertEqual(8, len(report.findings))
        self.assertEqual({"PASS": 8, "WARNING": 0, "REVIEW_REQUIRED": 0}, report.summary())

    def test_payload_contains_serializable_canonical_fields(self):
        report = self.make_report()
        payload = report_payload(report)

        self.assertEqual(
            {
                "boundary",
                "findings",
                "input_digest",
                "runner_version",
                "scenario_id",
                "schema_version",
                "summary",
            },
            set(payload),
        )
        self.assertEqual(report.summary(), payload["summary"])
        self.assertEqual(8, len(payload["findings"]))
        self.assertTrue(all(isinstance(item, dict) for item in payload["findings"]))

    def test_json_and_markdown_use_the_same_summary(self):
        report = self.make_report()
        payload = json.loads(render_json(report))
        markdown = render_markdown(report)
        self.assertEqual(report.summary(), payload["summary"])
        for status, count in report.summary().items():
            self.assertIn(f"| {status} | {count} |", markdown)

    def test_rendered_json_is_sorted_and_newline_terminated(self):
        report = self.make_report()
        rendered = render_json(report)

        self.assertTrue(rendered.endswith("\n"))
        self.assertEqual(
            json.dumps(report_payload(report), indent=2, sort_keys=True) + "\n",
            rendered,
        )

    def test_rendered_markdown_is_newline_terminated(self):
        self.assertTrue(render_markdown(self.make_report()).endswith("\n"))

    def test_report_has_no_runtime_timestamp(self):
        rendered = render_json(self.make_report())
        self.assertNotIn("timestamp", rendered.lower())
        self.assertNotIn("generated_at", rendered.lower())

    def test_rendering_is_deterministic(self):
        report = self.make_report()
        self.assertEqual(render_json(report), render_json(report))
        self.assertEqual(render_markdown(report), render_markdown(report))

    def test_writer_creates_both_reports_and_accepts_identical_rerun(self):
        report = self.make_report()
        with TemporaryDirectory() as directory:
            output = Path(directory) / "reports"
            paths = write_reports(report, output)
            first_contents = tuple(path.read_text(encoding="utf-8") for path in paths)

            self.assertEqual((output / "report.json", output / "report.md"), paths)
            self.assertEqual(render_json(report), first_contents[0])
            self.assertEqual(render_markdown(report), first_contents[1])
            self.assertEqual(paths, write_reports(report, output))
            self.assertEqual(
                first_contents,
                tuple(path.read_text(encoding="utf-8") for path in paths),
            )

    def test_writer_refuses_non_identical_existing_report(self):
        report = self.make_report()
        with TemporaryDirectory() as directory:
            output = Path(directory)
            (output / "report.json").write_text("different", encoding="utf-8")
            with self.assertRaisesRegex(FileExistsError, "non-identical report"):
                write_reports(report, output)
            self.assertFalse((output / "report.md").exists())

    def test_writer_preflights_markdown_collision_before_writing_json(self):
        report = self.make_report()
        with TemporaryDirectory() as directory:
            output = Path(directory)
            (output / "report.md").write_text("different", encoding="utf-8")
            with self.assertRaisesRegex(FileExistsError, "non-identical report"):
                write_reports(report, output)
            self.assertFalse((output / "report.json").exists())
            self.assertEqual("different", (output / "report.md").read_text(encoding="utf-8"))

    def test_writer_does_not_rewrite_json_when_markdown_differs(self):
        report = self.make_report()
        with TemporaryDirectory() as directory:
            output = Path(directory)
            (output / "report.json").write_text(render_json(report), encoding="utf-8")
            (output / "report.md").write_text("different", encoding="utf-8")
            with self.assertRaisesRegex(FileExistsError, "non-identical report"):
                write_reports(report, output)
            self.assertEqual(render_json(report), (output / "report.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
