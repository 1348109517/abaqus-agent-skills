import copy


def complete_contract():
    return {
        "schema_version": "1.0",
        "scenario_id": "complete",
        "units": {"length": "m", "force": "N"},
        "model": {
            "name": "SyntheticTunnelReview",
            "parts": [{"name": "Soil"}, {"name": "Lining"}],
            "instances": [
                {"name": "Soil-1", "part": "Soil"},
                {"name": "Lining-1", "part": "Lining"},
            ],
            "sets": [
                {"name": "FarField", "instance": "Soil-1"},
                {"name": "SoilVolume", "instance": "Soil-1"},
            ],
            "surfaces": [
                {"name": "TunnelFace", "instance": "Soil-1"},
                {"name": "LiningOuter", "instance": "Lining-1"},
            ],
        },
        "materials": [{"name": "SyntheticSoil"}, {"name": "SyntheticLining"}],
        "sections": [
            {"name": "SoilSection", "material": "SyntheticSoil", "part": "Soil"},
            {"name": "LiningSection", "material": "SyntheticLining", "part": "Lining"},
        ],
        "steps": [{"name": "Initial", "order": 0}, {"name": "Excavation", "order": 1}],
        "boundary_conditions": [
            {"name": "FarFieldFix", "region": "FarField", "step": "Initial"}
        ],
        "loads": [{"name": "Gravity", "region": "SoilVolume", "step": "Excavation"}],
        "interactions": [
            {"name": "SoilLining", "main": "LiningOuter", "secondary": "TunnelFace"}
        ],
        "mesh_intents": [
            {"part": "Soil", "element_family": "continuum"},
            {"part": "Lining", "element_family": "continuum"},
        ],
        "outputs": [
            {"name": "Displacement", "kind": "field", "variables": ["U"]},
            {"name": "Reaction", "kind": "history", "variables": ["RF"]},
        ],
        "review_intent": {"requires_outputs": ["Displacement", "Reaction"]},
        "evidence": {
            "static_review": "complete",
            "solver": "not_run",
            "physical_review": "required",
            "engineering_claim": "blocked",
        },
    }


def complete_v11_contract():
    contract = copy.deepcopy(complete_contract())
    contract["schema_version"] = "1.1"
    contract["model"]["sets"].append(
        {"name": "LiningVolume", "instance": "Lining-1"}
    )
    contract["construction_events"] = [
        {
            "name": "ActivateLining",
            "action": "activate",
            "region": "LiningVolume",
            "step": "Excavation",
        }
    ]
    contract["mapped_loads"] = [
        {
            "name": "MappedFacePressure",
            "target_surface": "TunnelFace",
            "step": "Excavation",
            "source_id": "synthetic-source-1",
            "source_sha256": "a" * 64,
            "coordinate_system": "global",
            "source_units": "kPa",
            "target_units": "kPa",
            "sign_convention": "positive-outward",
            "expected_face_count": 4,
            "mapped_face_count": 4,
            "duplicate_face_count": 0,
            "unmapped_face_count": 0,
        }
    ]
    return contract
