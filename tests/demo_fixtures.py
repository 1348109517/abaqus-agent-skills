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
