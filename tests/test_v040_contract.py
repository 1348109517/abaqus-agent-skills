import unittest

from abaqus_agent_demo.checks import audit_contract
from tests.demo_fixtures import complete_contract, complete_v11_contract


class Version11ContractTests(unittest.TestCase):
    def test_schema_version_accepts_only_1_0_or_1_1(self):
        for version in ("0.9", "2.0"):
            with self.subTest(version=version):
                contract = complete_contract()
                contract["schema_version"] = version
                findings = audit_contract(contract)
                self.assertTrue(
                    any(
                        item.code == "C-CONTRACT-001"
                        and item.location == "schema_version"
                        for item in findings
                    )
                )

    def test_optional_sections_require_schema_version_1_1(self):
        for field in ("construction_events", "mapped_loads"):
            with self.subTest(field=field):
                contract = complete_contract()
                contract[field] = []
                findings = audit_contract(contract)
                self.assertTrue(
                    any(
                        item.code == "C-CONTRACT-001"
                        and item.location == field
                        for item in findings
                    )
                )

    def test_v10_contract_without_optional_sections_retains_eight_passes(self):
        findings = audit_contract(complete_contract())
        self.assertEqual(8, len(findings))
        self.assertNotIn("C-STAGE-001", {item.code for item in findings})
        self.assertNotIn("C-MAPLOAD-001", {item.code for item in findings})

    def test_complete_v11_contract_emits_two_additional_passes(self):
        findings = audit_contract(complete_v11_contract())
        self.assertEqual(10, len(findings))
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
                "C-STAGE-001",
                "C-MAPLOAD-001",
            },
            {item.code for item in findings},
        )
        self.assertTrue(all(item.status == "PASS" for item in findings))

    def test_invalid_construction_action_and_conflict_require_review(self):
        contract = complete_v11_contract()
        contract["construction_events"][0]["action"] = "replace"
        contract["construction_events"].append(
            {
                "name": "DeactivateLining",
                "action": "deactivate",
                "region": "LiningOuter",
                "step": "Excavation",
            }
        )
        findings = audit_contract(contract)
        problems = [item for item in findings if item.code == "C-STAGE-001"]
        self.assertTrue(problems)
        self.assertTrue(all(item.status == "REVIEW_REQUIRED" for item in problems))
        self.assertIn("construction_events.ActivateLining.action", [item.location for item in problems])

    def test_construction_event_references_are_checked(self):
        contract = complete_v11_contract()
        contract["construction_events"][0]["region"] = "MissingSet"
        contract["construction_events"][0]["step"] = "MissingStep"
        findings = audit_contract(contract)
        locations = {
            item.location
            for item in findings
            if item.code == "C-STAGE-001" and item.status == "REVIEW_REQUIRED"
        }
        self.assertIn("construction_events.ActivateLining.region", locations)
        self.assertIn("construction_events.ActivateLining.step", locations)

    def test_construction_region_must_resolve_to_a_model_set(self):
        contract = complete_v11_contract()
        contract["construction_events"][0]["region"] = "LiningOuter"
        findings = audit_contract(contract)
        self.assertIn(
            "construction_events.ActivateLining.region",
            {
                item.location
                for item in findings
                if item.code == "C-STAGE-001" and item.status == "REVIEW_REQUIRED"
            },
        )

    def test_repeated_construction_events_for_same_set_and_step_conflict(self):
        contract = complete_v11_contract()
        contract["construction_events"].append(
            {
                "name": "ActivateLiningAgain",
                "action": "activate",
                "region": "LiningVolume",
                "step": "Excavation",
            }
        )
        findings = audit_contract(contract)
        conflict_locations = {
            item.location
            for item in findings
            if item.code == "C-STAGE-001" and item.status == "REVIEW_REQUIRED"
        }
        self.assertIn("construction_events.ActivateLining.conflict", conflict_locations)
        self.assertIn("construction_events.ActivateLiningAgain.conflict", conflict_locations)

    def test_empty_present_optional_sections_require_review(self):
        for field, code in (
            ("construction_events", "C-STAGE-001"),
            ("mapped_loads", "C-MAPLOAD-001"),
        ):
            with self.subTest(field=field):
                contract = complete_contract()
                contract["schema_version"] = "1.1"
                contract[field] = []
                findings = audit_contract(contract)
                problems = [item for item in findings if item.code == code]
                self.assertEqual(1, len(problems))
                self.assertEqual("REVIEW_REQUIRED", problems[0].status)

    def test_mapped_load_digest_counts_and_consistency_require_review(self):
        contract = complete_v11_contract()
        mapped = contract["mapped_loads"][0]
        mapped["source_sha256"] = "not-a-digest"
        mapped["expected_face_count"] = 4
        mapped["mapped_face_count"] = 2
        mapped["duplicate_face_count"] = 1
        mapped["unmapped_face_count"] = 0
        findings = audit_contract(contract)
        problems = [item for item in findings if item.code == "C-MAPLOAD-001"]
        self.assertGreaterEqual(len(problems), 2)
        self.assertTrue(all(item.status == "REVIEW_REQUIRED" for item in problems))
        locations = {item.location for item in problems}
        self.assertIn("mapped_loads.MappedFacePressure.source_sha256", locations)
        self.assertIn("mapped_loads.MappedFacePressure.face_counts", locations)

    def test_mapped_load_counts_must_be_nonnegative_integers(self):
        contract = complete_v11_contract()
        contract["mapped_loads"][0]["duplicate_face_count"] = True
        findings = audit_contract(contract)
        locations = {
            item.location
            for item in findings
            if item.code == "C-MAPLOAD-001" and item.status == "REVIEW_REQUIRED"
        }
        self.assertIn("mapped_loads.MappedFacePressure.duplicate_face_count", locations)

    def test_duplicate_mapped_faces_must_be_zero_and_are_not_part_of_expected_sum(self):
        contract = complete_v11_contract()
        mapped = contract["mapped_loads"][0]
        mapped["mapped_face_count"] = 3
        mapped["unmapped_face_count"] = 1
        mapped["duplicate_face_count"] = 1
        findings = audit_contract(contract)
        problems = [item for item in findings if item.code == "C-MAPLOAD-001"]
        self.assertEqual(1, len(problems))
        self.assertEqual(
            "mapped_loads.MappedFacePressure.duplicate_face_count",
            problems[0].location,
        )

    def test_distinct_mapped_loads_on_same_surface_and_step_are_allowed(self):
        contract = complete_v11_contract()
        second = dict(contract["mapped_loads"][0])
        second["name"] = "MappedFacePressureSecond"
        second["source_id"] = "synthetic-source-2"
        contract["mapped_loads"].append(second)
        findings = audit_contract(contract)
        self.assertEqual(
            [],
            [
                item
                for item in findings
                if item.code == "C-MAPLOAD-001" and item.status == "REVIEW_REQUIRED"
            ],
        )

    def test_mapped_load_namespace_is_independent_from_ordinary_loads(self):
        contract = complete_v11_contract()
        contract["mapped_loads"][0]["name"] = "Gravity"
        findings = audit_contract(contract)
        self.assertEqual(
            [],
            [
                item
                for item in findings
                if item.code == "C-MAPLOAD-001" and item.status == "REVIEW_REQUIRED"
            ],
        )

    def test_mapped_load_surface_and_step_references_are_checked(self):
        contract = complete_v11_contract()
        contract["mapped_loads"][0]["target_surface"] = "MissingSurface"
        contract["mapped_loads"][0]["step"] = "MissingStep"
        findings = audit_contract(contract)
        locations = {
            item.location
            for item in findings
            if item.code == "C-MAPLOAD-001" and item.status == "REVIEW_REQUIRED"
        }
        self.assertIn("mapped_loads.MappedFacePressure.target_surface", locations)
        self.assertIn("mapped_loads.MappedFacePressure.step", locations)

    def test_optional_section_must_be_a_list_before_optional_checks_run(self):
        contract = complete_contract()
        contract["construction_events"] = {}
        findings = audit_contract(contract)
        self.assertTrue(findings)
        self.assertTrue(all(item.code == "C-CONTRACT-001" for item in findings))
        self.assertNotIn("C-STAGE-001", {item.code for item in findings})


if __name__ == "__main__":
    unittest.main()
