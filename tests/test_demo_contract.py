import hashlib
import json
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path
from tempfile import TemporaryDirectory

from abaqus_agent_demo.contract import ContractError, input_digest, load_contract
from abaqus_agent_demo.findings import AuditReport, Finding
from tests.demo_fixtures import complete_contract


class ContractLoadingTests(unittest.TestCase):
    def test_load_contract_returns_json_mapping(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "contract.json"
            path.write_text(json.dumps(complete_contract()), encoding="utf-8")
            self.assertEqual("complete", load_contract(path)["scenario_id"])

    def test_load_contract_rejects_non_object_json(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "contract.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaisesRegex(ContractError, "top-level JSON object"):
                load_contract(path)

    def test_input_digest_matches_file_bytes(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "contract.json"
            path.write_bytes(b"{}\n")
            self.assertEqual(hashlib.sha256(b"{}\n").hexdigest(), input_digest(path))


class FindingModelTests(unittest.TestCase):
    def test_finding_is_immutable(self):
        finding = Finding("C-TEST", "PASS", "message", "location", "skill", "next")
        with self.assertRaises(FrozenInstanceError):
            finding.status = "WARNING"

    def test_audit_report_is_immutable_and_summarizes_valid_statuses(self):
        findings = (
            Finding("C-PASS", "PASS", "", "", "", ""),
            Finding("C-WARNING", "WARNING", "", "", "", ""),
            Finding("C-REVIEW-1", "REVIEW_REQUIRED", "", "", "", ""),
            Finding("C-REVIEW-2", "REVIEW_REQUIRED", "", "", "", ""),
        )
        report = AuditReport("1.0", "0.3.0", "complete", "digest", findings)
        self.assertEqual(
            {"PASS": 1, "WARNING": 1, "REVIEW_REQUIRED": 2}, report.summary()
        )
        with self.assertRaises(FrozenInstanceError):
            report.scenario_id = "changed"


if __name__ == "__main__":
    unittest.main()
