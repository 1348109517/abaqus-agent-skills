import unittest

from abaqus_agent_demo.checks import audit_contract
from tests.demo_fixtures import complete_contract


class AuditCheckTests(unittest.TestCase):
    def test_complete_contract_emits_one_pass_for_each_check_code(self):
        findings = audit_contract(complete_contract())
        self.assertEqual(8, len(findings))
        self.assertEqual(
            {
                "C-CONTRACT-001",
                "C-UNITS-001",
                "C-NAME-001",
                "C-REF-001",
                "C-STEP-001",
                "C-MESH-001",
                "C-OUTPUT-001",
                "C-EVIDENCE-001",
            },
            {item.code for item in findings},
        )
        self.assertTrue(all(item.status == "PASS" for item in findings))

    def test_complete_contract_has_no_non_pass_findings(self):
        findings = audit_contract(complete_contract())
        self.assertTrue(findings)
        self.assertEqual([], [item for item in findings if item.status != "PASS"])

    def test_missing_region_is_review_required(self):
        contract = complete_contract()
        contract["loads"][0]["region"] = "ExcavationFaceRenamed"
        findings = audit_contract(contract)
        problem = [
            item
            for item in findings
            if item.code == "C-REF-001" and item.status == "REVIEW_REQUIRED"
        ]
        self.assertEqual(1, len(problem))
        self.assertEqual("loads.Gravity.region", problem[0].location)
        self.assertEqual("abaqus-dependency-preflight-validator", problem[0].skill)

    def test_engineering_claim_without_solver_and_physical_review_is_blocked(self):
        contract = complete_contract()
        contract["evidence"]["engineering_claim"] = "approved"
        findings = audit_contract(contract)
        problem = [item for item in findings if item.code == "C-EVIDENCE-001"]
        self.assertEqual("REVIEW_REQUIRED", problem[0].status)

    def test_findings_are_deterministic(self):
        contract = complete_contract()
        contract["loads"].append(
            {"name": "A_Load", "region": "MissingB", "step": "Excavation"}
        )
        contract["loads"].append(
            {"name": "B_Load", "region": "MissingA", "step": "Excavation"}
        )
        first = audit_contract(contract)
        second = audit_contract(contract)
        self.assertEqual(first, second)

    def test_malformed_contract_returns_contract_finding_instead_of_crashing(self):
        findings = audit_contract({"schema_version": "1.0"})
        self.assertEqual("C-CONTRACT-001", findings[0].code)
        self.assertEqual("REVIEW_REQUIRED", findings[0].status)

    def test_findings_follow_registry_then_lexical_location_order(self):
        contract = complete_contract()
        contract["loads"].append(
            {"name": "A_Load", "region": "MissingB", "step": "MissingStepB"}
        )
        contract["loads"].append(
            {"name": "B_Load", "region": "MissingA", "step": "MissingStepA"}
        )
        findings = audit_contract(contract)
        refs = [item for item in findings if item.code == "C-REF-001"]
        self.assertEqual(
            [
                "loads.A_Load.region",
                "loads.A_Load.step",
                "loads.B_Load.region",
                "loads.B_Load.step",
            ],
            [item.location for item in refs],
        )
        self.assertLess(
            [item.code for item in findings].index("C-REF-001"),
            [item.code for item in findings].index("C-STEP-001"),
        )


if __name__ == "__main__":
    unittest.main()
