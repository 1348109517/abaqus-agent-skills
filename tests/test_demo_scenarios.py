import json
import unittest
from pathlib import Path

from abaqus_agent_demo.checks import audit_contract
from abaqus_agent_demo.contract import load_contract


ROOT = Path(__file__).resolve().parents[1]


class ScenarioIntegrationTests(unittest.TestCase):
    def test_scenarios_match_expected_non_pass_findings(self):
        root = ROOT / "examples" / "synthetic-tunnel-review"
        for name in ("complete", "naming-drift", "evidence-overreach"):
            with self.subTest(scenario=name):
                contract = load_contract(root / name / "model-contract.json")
                expected = json.loads(
                    (root / name / "expected-findings.json").read_text(encoding="utf-8")
                )
                actual = [
                    {"code": item.code, "status": item.status, "location": item.location}
                    for item in audit_contract(contract)
                    if item.status != "PASS"
                ]
                self.assertEqual(expected["non_pass"], actual)


if __name__ == "__main__":
    unittest.main()
