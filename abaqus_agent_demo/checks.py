"""Deterministic, read-only checks for the synthetic Abaqus demo contract.

The checks in this module validate names and relationships described by the
contract.  They do not load Abaqus, run a solver, or infer physical results.
"""

from collections.abc import Mapping
import re
from typing import Any

from .findings import Finding


_SUPPORTED_SCHEMA_VERSIONS = frozenset({"1.0", "1.1"})
_OPTIONAL_SCHEMA_FIELDS = ("construction_events", "mapped_loads")


def finding(code, status, message, location, skill, next_action):
    return Finding(code, status, message, location, skill, next_action)


def declared_names(items):
    """Return the non-empty names declared by a sequence of mappings."""

    if not isinstance(items, list):
        return set()
    return {
        str(item["name"])
        for item in items
        if isinstance(item, Mapping) and item.get("name")
    }


def _item_name(item):
    if isinstance(item, Mapping) and item.get("name"):
        return str(item["name"])
    return "<unnamed>"


def _items(contract, path):
    """Read a list at a known path without allowing malformed input to raise."""

    value: Any = contract
    for key in path:
        if not isinstance(value, Mapping):
            return []
        value = value.get(key)
    return value if isinstance(value, list) else []


def _check_type(problems, contract, path, expected, skill, next_action):
    value: Any = contract
    for key in path:
        if not isinstance(value, Mapping):
            value = None
            break
        value = value.get(key)
    location = ".".join(path)
    if not isinstance(value, expected):
        expected_name = " or ".join(item.__name__ for item in expected)
        problems.append(
            finding(
                "C-CONTRACT-001",
                "REVIEW_REQUIRED",
                f"Contract field {location} must be a {expected_name}.",
                location,
                skill,
                next_action,
            )
        )


def _check_nonempty_string(problems, value, location, skill, next_action):
    if not isinstance(value, str) or not value.strip():
        problems.append(
            finding(
                "C-CONTRACT-001",
                "REVIEW_REQUIRED",
                f"Contract field {location} must be a non-empty string.",
                location,
                skill,
                next_action,
            )
        )


def _check_bounded_string(problems, value, location, allowed, skill, next_action):
    if not isinstance(value, str) or value not in allowed:
        states = ", ".join(sorted(allowed))
        problems.append(
            finding(
                "C-CONTRACT-001",
                "REVIEW_REQUIRED",
                f"Contract field {location} must be one of: {states}.",
                location,
                skill,
                next_action,
            )
        )


def check_contract_shape(contract: Mapping[str, Any]):
    """Validate the collection/object boundary before running other checks."""

    skill = "abaqus-parametric-project-starter"
    next_action = "Repair the contract shape before running dependent checks."
    if not isinstance(contract, Mapping):
        return [
            finding(
                "C-CONTRACT-001",
                "REVIEW_REQUIRED",
                "Contract must be a top-level object.",
                "contract",
                skill,
                next_action,
            )
        ]

    problems = []
    for key in ("schema_version", "scenario_id"):
        _check_nonempty_string(problems, contract.get(key), key, skill, next_action)
    schema_version = contract.get("schema_version")
    if (
        isinstance(schema_version, str)
        and schema_version.strip()
        and schema_version not in _SUPPORTED_SCHEMA_VERSIONS
    ):
        problems.append(
            finding(
                "C-CONTRACT-001",
                "REVIEW_REQUIRED",
                "Contract field schema_version must be 1.0 or 1.1.",
                "schema_version",
                skill,
                next_action,
            )
        )
    for key in _OPTIONAL_SCHEMA_FIELDS:
        if key in contract and schema_version != "1.1":
            problems.append(
                finding(
                    "C-CONTRACT-001",
                    "REVIEW_REQUIRED",
                    f"Contract field {key} requires schema_version 1.1.",
                    key,
                    skill,
                    next_action,
                )
            )

    top_level_types = {
        "units": Mapping,
        "model": Mapping,
        "materials": list,
        "sections": list,
        "steps": list,
        "boundary_conditions": list,
        "loads": list,
        "interactions": list,
        "mesh_intents": list,
        "outputs": list,
        "review_intent": Mapping,
        "evidence": Mapping,
    }
    for key in sorted(top_level_types):
        _check_type(problems, contract, (key,), (top_level_types[key],), skill, next_action)
    for key in _OPTIONAL_SCHEMA_FIELDS:
        if key in contract:
            _check_type(problems, contract, (key,), (list,), skill, next_action)

    model = contract.get("model")
    if isinstance(model, Mapping):
        _check_nonempty_string(problems, model.get("name"), "model.name", skill, next_action)
        for key in ("parts", "instances", "sets", "surfaces"):
            _check_type(problems, contract, ("model", key), (list,), skill, next_action)

    units = contract.get("units")
    if isinstance(units, Mapping):
        for key in ("length", "force"):
            _check_nonempty_string(problems, units.get(key), f"units.{key}", skill, next_action)

    review_intent = contract.get("review_intent")
    if isinstance(review_intent, Mapping):
        _check_type(
            problems,
            contract,
            ("review_intent", "requires_outputs"),
            (list,),
            skill,
            next_action,
        )

    evidence = contract.get("evidence")
    if isinstance(evidence, Mapping):
        evidence_states = {
            "static_review": {"required", "complete"},
            "solver": {"not_run", "complete", "failed"},
            "physical_review": {"required", "complete"},
            "engineering_claim": {"blocked", "approved"},
        }
        for key, allowed in evidence_states.items():
            _check_bounded_string(
                problems,
                evidence.get(key),
                f"evidence.{key}",
                allowed,
                skill,
                next_action,
            )

    # The other checks expect lists of objects.  Report malformed entries here
    # so a partially edited contract cannot turn a static audit into a crash.
    list_paths = (
        ("materials",),
        ("sections",),
        ("steps",),
        ("boundary_conditions",),
        ("loads",),
        ("construction_events",),
        ("mapped_loads",),
        ("interactions",),
        ("mesh_intents",),
        ("outputs",),
        ("model", "parts"),
        ("model", "instances"),
        ("model", "sets"),
        ("model", "surfaces"),
    )
    for path in list_paths:
        values = _items(contract, path)
        for index, value in enumerate(values):
            if not isinstance(value, Mapping):
                location = ".".join(path) + f"[{index}]"
                problems.append(
                    finding(
                        "C-CONTRACT-001",
                        "REVIEW_REQUIRED",
                        f"Contract item {location} must be an object.",
                        location,
                        skill,
                        next_action,
                    )
                )

    named_collections = (
        ("materials",),
        ("sections",),
        ("steps",),
        ("boundary_conditions",),
        ("loads",),
        ("interactions",),
        ("outputs",),
        ("model", "parts"),
        ("model", "instances"),
        ("model", "sets"),
        ("model", "surfaces"),
    )
    for path in named_collections:
        for index, item in enumerate(_items(contract, path)):
            if isinstance(item, Mapping):
                _check_nonempty_string(
                    problems,
                    item.get("name"),
                    ".".join(path) + f"[{index}].name",
                    skill,
                    next_action,
                )

    reference_fields = (
        (("model", "instances"), ("part",)),
        (("model", "sets"), ("instance",)),
        (("model", "surfaces"), ("instance",)),
        (("sections",), ("material", "part")),
        (("boundary_conditions",), ("region", "step")),
        (("loads",), ("region", "step")),
        (("interactions",), ("main", "secondary")),
        (("mesh_intents",), ("part", "element_family")),
    )
    for path, fields in reference_fields:
        for index, item in enumerate(_items(contract, path)):
            if isinstance(item, Mapping):
                for field in fields:
                    _check_nonempty_string(
                        problems,
                        item.get(field),
                        ".".join(path) + f"[{index}].{field}",
                        skill,
                        next_action,
                    )

    for index, item in enumerate(_items(contract, ("steps",))):
        if isinstance(item, Mapping):
            order = item.get("order")
            if not isinstance(order, int) or isinstance(order, bool) or order < 0:
                problems.append(
                    finding(
                        "C-CONTRACT-001",
                        "REVIEW_REQUIRED",
                        f"Contract field steps[{index}].order must be a nonnegative integer.",
                        f"steps[{index}].order",
                        skill,
                        next_action,
                    )
                )

    for index, item in enumerate(_items(contract, ("outputs",))):
        if not isinstance(item, Mapping):
            continue
        variables = item.get("variables")
        location = f"outputs[{index}].variables"
        if not isinstance(variables, list):
            problems.append(
                finding(
                    "C-CONTRACT-001",
                    "REVIEW_REQUIRED",
                    f"Contract field {location} must be a list.",
                    location,
                    skill,
                    next_action,
                )
            )
            continue
        if not variables:
            _check_nonempty_string(problems, None, location, skill, next_action)
        for variable_index, variable in enumerate(variables):
            _check_nonempty_string(
                problems,
                variable,
                f"{location}[{variable_index}]",
                skill,
                next_action,
            )

    if isinstance(review_intent, Mapping):
        required_outputs = review_intent.get("requires_outputs")
        if isinstance(required_outputs, list):
            for index, output_name in enumerate(required_outputs):
                _check_nonempty_string(
                    problems,
                    output_name,
                    f"review_intent.requires_outputs[{index}]",
                    skill,
                    next_action,
                )

    if problems:
        return sorted(problems, key=lambda item: (item.location, item.code))
    return [
        finding(
            "C-CONTRACT-001",
            "PASS",
            "Required contract fields have the expected JSON types.",
            "contract",
            skill,
            "Preserve the contract shape while extending the demo.",
        )
    ]


def check_units(contract):
    units = contract.get("units", {}) if isinstance(contract, Mapping) else {}
    problems = []
    for key in ("length", "force"):
        value = units.get(key) if isinstance(units, Mapping) else None
        if not isinstance(value, str) or not value.strip():
            problems.append(
                finding(
                    "C-UNITS-001",
                    "WARNING",
                    f"The declared {key} unit is missing or empty.",
                    f"units.{key}",
                    "abaqus-parametric-project-starter",
                    "Declare the unit before interpreting model values.",
                )
            )
    if problems:
        return problems
    return [
        finding(
            "C-UNITS-001",
            "PASS",
            "Length and force units are declared.",
            "units",
            "abaqus-parametric-project-starter",
            "Preserve the unit declaration through later script stages.",
        )
    ]


_NAME_COLLECTIONS = (
    ("parts", ("model", "parts")),
    ("instances", ("model", "instances")),
    ("sets", ("model", "sets")),
    ("surfaces", ("model", "surfaces")),
    ("materials", ("materials",)),
    ("sections", ("sections",)),
    ("steps", ("steps",)),
    ("boundary_conditions", ("boundary_conditions",)),
    ("loads", ("loads",)),
    ("interactions", ("interactions",)),
    ("outputs", ("outputs",)),
)


def check_unique_names(contract):
    problems = []
    for namespace, path in _NAME_COLLECTIONS:
        seen = set()
        for item in _items(contract, path):
            name = _item_name(item)
            location = f"{namespace}.{name}"
            valid_name = name != "<unnamed>"
            if not valid_name:
                problems.append(
                    finding(
                        "C-NAME-001",
                        "REVIEW_REQUIRED",
                        f"{namespace} contains an item without a non-empty name.",
                        location,
                        "abaqus-shared-naming-manifest-builder",
                        "Declare a stable, non-empty unique name before model edits.",
                    )
                )
            elif name in seen:
                problems.append(
                    finding(
                        "C-NAME-001",
                        "REVIEW_REQUIRED",
                        f"The name {name!r} is duplicated in namespace {namespace}.",
                        location,
                        "abaqus-shared-naming-manifest-builder",
                        "Reconcile the shared naming manifest before model edits.",
                    )
                )
            seen.add(name)
    if problems:
        return problems
    return [
        finding(
            "C-NAME-001",
            "PASS",
            "Declared names are non-empty and unique within their namespaces.",
            "names",
            "abaqus-shared-naming-manifest-builder",
            "Preserve these names across all generated artifacts.",
        )
    ]


def _reference_problem(group_name, item_name, field, value, namespace, skill, action):
    return finding(
        "C-REF-001",
        "REVIEW_REQUIRED",
        f"{group_name} {item_name} references undeclared {namespace} {value!r}.",
        f"{group_name}.{item_name}.{field}",
        skill,
        action,
    )


def check_references(contract):
    model = contract.get("model", {}) if isinstance(contract, Mapping) else {}
    if not isinstance(model, Mapping):
        model = {}
    parts = declared_names(model.get("parts", []))
    instances = declared_names(model.get("instances", []))
    regions = declared_names(model.get("sets", [])) | declared_names(model.get("surfaces", []))
    surfaces = declared_names(model.get("surfaces", []))
    steps = declared_names(contract.get("steps", []))
    materials = declared_names(contract.get("materials", []))
    problems = []

    for item in sorted(model.get("instances", []), key=lambda value: _item_name(value)):
        name = _item_name(item)
        if not isinstance(item, Mapping) or item.get("part") not in parts:
            value = item.get("part") if isinstance(item, Mapping) else None
            problems.append(
                _reference_problem(
                    "instances",
                    name,
                    "part",
                    value,
                    "part",
                    "abaqus-dependency-preflight-validator",
                    "Declare the part or correct the consumer reference.",
                )
            )

    for group_name, values in (("sets", model.get("sets", [])), ("surfaces", model.get("surfaces", []))):
        for item in sorted(values, key=lambda value: _item_name(value)):
            name = _item_name(item)
            if not isinstance(item, Mapping) or item.get("instance") not in instances:
                value = item.get("instance") if isinstance(item, Mapping) else None
                problems.append(
                    _reference_problem(
                        group_name,
                        name,
                        "instance",
                        value,
                        "instance",
                        "abaqus-dependency-preflight-validator",
                        "Declare the instance or correct the consumer reference.",
                    )
                )

    for item in sorted(contract.get("sections", []), key=lambda value: _item_name(value)):
        name = _item_name(item)
        if not isinstance(item, Mapping) or item.get("material") not in materials:
            value = item.get("material") if isinstance(item, Mapping) else None
            problems.append(
                _reference_problem(
                    "sections",
                    name,
                    "material",
                    value,
                    "material",
                    "abaqus-dependency-preflight-validator",
                    "Declare the material or correct the consumer reference.",
                )
            )
        if not isinstance(item, Mapping) or item.get("part") not in parts:
            value = item.get("part") if isinstance(item, Mapping) else None
            problems.append(
                _reference_problem(
                    "sections",
                    name,
                    "part",
                    value,
                    "part",
                    "abaqus-dependency-preflight-validator",
                    "Declare the part or correct the consumer reference.",
                )
            )

    for group_name in ("boundary_conditions", "loads"):
        for item in sorted(contract.get(group_name, []), key=lambda value: _item_name(value)):
            name = _item_name(item)
            if not isinstance(item, Mapping) or item.get("region") not in regions:
                value = item.get("region") if isinstance(item, Mapping) else None
                problems.append(
                    _reference_problem(
                        group_name,
                        name,
                        "region",
                        value,
                        "region",
                        "abaqus-dependency-preflight-validator",
                        "Reconcile the shared naming manifest before model edits or execution.",
                    )
                )
            if not isinstance(item, Mapping) or item.get("step") not in steps:
                value = item.get("step") if isinstance(item, Mapping) else None
                problems.append(
                    _reference_problem(
                        group_name,
                        name,
                        "step",
                        value,
                        "step",
                        "abaqus-dependency-preflight-validator",
                        "Declare the step or correct the consumer reference.",
                    )
                )

    for item in sorted(contract.get("interactions", []), key=lambda value: _item_name(value)):
        name = _item_name(item)
        for field in ("main", "secondary"):
            if not isinstance(item, Mapping) or item.get(field) not in surfaces:
                value = item.get(field) if isinstance(item, Mapping) else None
                problems.append(
                    _reference_problem(
                        "interactions",
                        name,
                        field,
                        value,
                        "surface",
                        "abaqus-dependency-preflight-validator",
                        "Declare the surface or correct the interaction reference.",
                    )
                )

    for item in sorted(contract.get("mesh_intents", []), key=lambda value: str(value.get("part", "")) if isinstance(value, Mapping) else ""):
        part = item.get("part") if isinstance(item, Mapping) else None
        if part not in parts:
            name = str(part) if part else "<unnamed>"
            problems.append(
                finding(
                    "C-REF-001",
                    "REVIEW_REQUIRED",
                    f"mesh_intents {name} references undeclared part {part!r}.",
                    f"mesh_intents.{name}.part",
                    "abaqus-dependency-preflight-validator",
                    "Declare the part or correct the consumer reference.",
                )
            )

    if problems:
        return problems
    return [
        finding(
            "C-REF-001",
            "PASS",
            "Declared consumer references resolve.",
            "references",
            "abaqus-dependency-preflight-validator",
            "Preserve these identifiers through later script stages.",
        )
    ]


def check_step_order(contract):
    problems = []
    seen_orders = {}
    steps = _items(contract, ("steps",))
    for item in steps:
        name = _item_name(item)
        order = item.get("order") if isinstance(item, Mapping) else None
        location = f"steps.{name}.order"
        valid_order = isinstance(order, int) and not isinstance(order, bool) and order >= 0
        if not valid_order:
            problems.append(
                finding(
                    "C-STEP-001",
                    "REVIEW_REQUIRED",
                    f"Step {name} must have a unique nonnegative integer order.",
                    location,
                    "abaqus-step",
                    "Assign a unique nonnegative order before model execution.",
                )
            )
            continue
        seen_orders.setdefault(order, []).append((name, location))

    for order, entries in seen_orders.items():
        if len(entries) > 1:
            for name, location in entries:
                problems.append(
                    finding(
                        "C-STEP-001",
                        "REVIEW_REQUIRED",
                        f"Step order {order} is shared by multiple steps.",
                        location,
                        "abaqus-step",
                        "Assign a unique nonnegative order to every step.",
                    )
                )

    if problems:
        return problems
    return [
        finding(
            "C-STEP-001",
            "PASS",
            "Step orders are unique nonnegative integers.",
            "steps",
            "abaqus-step",
            "Preserve this order when generating analysis steps.",
        )
    ]


def check_mesh_intent(contract):
    model = contract.get("model", {}) if isinstance(contract, Mapping) else {}
    parts = declared_names(model.get("parts", [])) if isinstance(model, Mapping) else set()
    intents = _items(contract, ("mesh_intents",))
    by_part = {}
    for item in intents:
        if isinstance(item, Mapping):
            by_part.setdefault(item.get("part"), []).append(item)

    problems = []
    for part in sorted(parts):
        matches = by_part.get(part, [])
        valid = (
            len(matches) == 1
            and isinstance(matches[0].get("element_family"), str)
            and bool(matches[0]["element_family"].strip())
        )
        if not valid:
            if not matches:
                message = f"Part {part} has no mesh intent."
            elif len(matches) != 1:
                message = f"Part {part} must have exactly one mesh intent."
            else:
                message = f"Part {part} has an empty mesh element family."
            problems.append(
                finding(
                    "C-MESH-001",
                    "WARNING",
                    message,
                    f"mesh_intents.{part}",
                    "abaqus-mesh",
                    "Declare one non-empty element family for every part.",
                )
            )

    if problems:
        return problems
    return [
        finding(
            "C-MESH-001",
            "PASS",
            "Every declared part has one mesh intent with an element family.",
            "mesh_intents",
            "abaqus-mesh",
            "Preserve the mesh intent through mesh generation and review.",
        )
    ]


def check_output_coverage(contract):
    outputs = declared_names(_items(contract, ("outputs",)))
    review_intent = contract.get("review_intent", {}) if isinstance(contract, Mapping) else {}
    requires = review_intent.get("requires_outputs", []) if isinstance(review_intent, Mapping) else []
    problems = []
    if isinstance(requires, list):
        for required in sorted(requires, key=lambda value: str(value)):
            name = str(required)
            if required not in outputs and name not in outputs:
                problems.append(
                    finding(
                        "C-OUTPUT-001",
                        "REVIEW_REQUIRED",
                        f"Review intent requires undeclared output {required!r}.",
                        f"review_intent.requires_outputs.{name}",
                        "abaqus-output",
                        "Declare the output request before relying on review evidence.",
                    )
                )
    if problems:
        return problems
    return [
        finding(
            "C-OUTPUT-001",
            "PASS",
            "Every required review output is declared.",
            "review_intent.requires_outputs",
            "abaqus-output",
            "Preserve output coverage through result extraction and review.",
        )
    ]


def check_evidence_boundary(contract):
    evidence = contract.get("evidence", {}) if isinstance(contract, Mapping) else {}
    if not isinstance(evidence, Mapping):
        evidence = {}
    approved = evidence.get("engineering_claim") == "approved"
    gates_complete = (
        evidence.get("solver") == "complete"
        and evidence.get("physical_review") == "complete"
    )
    if approved and not gates_complete:
        return [
            finding(
                "C-EVIDENCE-001",
                "REVIEW_REQUIRED",
                "Engineering approval skips solver evidence or physical review.",
                "evidence.engineering_claim",
                "abaqus-output",
                "Keep the claim blocked until solver evidence and physical review are complete.",
            )
        ]
    return [
        finding(
            "C-EVIDENCE-001",
            "PASS",
            "The declared claim respects the evidence gates.",
            "evidence",
            "abaqus-output",
            "Continue to keep static, solver, physical, and claim stages separate.",
        )
    ]


_CONSTRUCTION_ACTIONS = frozenset({"activate", "deactivate"})
_MAPPED_COUNT_FIELDS = (
    "expected_face_count",
    "mapped_face_count",
    "duplicate_face_count",
    "unmapped_face_count",
)
_MAPPED_TEXT_FIELDS = (
    "source_id",
    "coordinate_system",
    "source_units",
    "target_units",
    "sign_convention",
)


def _optional_problem(code, message, location, skill, next_action):
    return finding(code, "REVIEW_REQUIRED", message, location, skill, next_action)


def _optional_name(item):
    return _item_name(item)


def _declared_sets_and_steps(contract):
    model = contract.get("model", {}) if isinstance(contract, Mapping) else {}
    if not isinstance(model, Mapping):
        model = {}
    regions = declared_names(model.get("sets", []))
    steps = declared_names(contract.get("steps", []))
    return regions, steps


def _valid_nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def check_staged_construction(contract):
    """Check optional construction activation/deactivation events."""

    events = _items(contract, ("construction_events",))
    regions, steps = _declared_sets_and_steps(contract)
    problems = []
    names = {}
    event_keys = {}
    skill = "abaqus-staged-construction-auditor"
    next_action = "Reconcile the staged construction event before model execution."
    if not events:
        return [
            _optional_problem(
                "C-STAGE-001",
                "construction_events is present but contains no events.",
                "construction_events",
                skill,
                next_action,
            )
        ]

    for item in events:
        name = _optional_name(item)
        prefix = f"construction_events.{name}"
        if not _valid_nonempty_string(item.get("name") if isinstance(item, Mapping) else None):
            problems.append(
                _optional_problem(
                    "C-STAGE-001",
                    "Construction event must have a non-empty name.",
                    f"{prefix}.name",
                    skill,
                    next_action,
                )
            )
        elif name in names:
            problems.append(
                _optional_problem(
                    "C-STAGE-001",
                    f"Construction event name {name!r} is duplicated.",
                    f"{prefix}.name",
                    skill,
                    next_action,
                )
            )
        else:
            names[name] = prefix

        action = item.get("action") if isinstance(item, Mapping) else None
        if action not in _CONSTRUCTION_ACTIONS:
            problems.append(
                _optional_problem(
                    "C-STAGE-001",
                    "Construction event action must be activate or deactivate.",
                    f"{prefix}.action",
                    skill,
                    next_action,
                )
            )

        region = item.get("region") if isinstance(item, Mapping) else None
        if not _valid_nonempty_string(region):
            problems.append(
                _optional_problem(
                    "C-STAGE-001",
                    "Construction event region must be a non-empty declared region.",
                    f"{prefix}.region",
                    skill,
                    next_action,
                )
            )
        elif region not in regions:
            problems.append(
                _optional_problem(
                    "C-STAGE-001",
                    f"Construction event {name} references undeclared region {region!r}.",
                    f"{prefix}.region",
                    skill,
                    next_action,
                )
            )

        step = item.get("step") if isinstance(item, Mapping) else None
        if not _valid_nonempty_string(step):
            problems.append(
                _optional_problem(
                    "C-STAGE-001",
                    "Construction event step must be a non-empty declared step.",
                    f"{prefix}.step",
                    skill,
                    next_action,
                )
            )
        elif step not in steps:
            problems.append(
                _optional_problem(
                    "C-STAGE-001",
                    f"Construction event {name} references undeclared step {step!r}.",
                    f"{prefix}.step",
                    skill,
                    next_action,
                )
            )

        if _valid_nonempty_string(region) and _valid_nonempty_string(step) and action in _CONSTRUCTION_ACTIONS:
            event_keys.setdefault((region, step), []).append((action, name, prefix))

    for (region, step), entries in event_keys.items():
        if len(entries) > 1:
            for action, name, prefix in sorted(entries, key=lambda value: value[1]):
                problems.append(
                    _optional_problem(
                        "C-STAGE-001",
                        f"Construction events conflict for region {region!r} in step {step!r}: multiple events are declared.",
                        f"{prefix}.conflict",
                        skill,
                        next_action,
                    )
                )

    if problems:
        return sorted(problems, key=lambda item: (item.location, item.message))
    return [
        finding(
            "C-STAGE-001",
            "PASS",
            "Construction activation and deactivation events are valid and non-conflicting.",
            "construction_events",
            skill,
            "Preserve the reviewed event sequence through model generation.",
        )
    ]


def check_mapped_load_provenance(contract):
    """Check optional face-mapped load provenance and mapping counts."""

    mapped_loads = _items(contract, ("mapped_loads",))
    _, steps = _declared_sets_and_steps(contract)
    model = contract.get("model", {}) if isinstance(contract, Mapping) else {}
    surfaces = declared_names(model.get("surfaces", [])) if isinstance(model, Mapping) else set()
    problems = []
    names = {}
    skill = "abaqus-mapped-load-provenance-auditor"
    next_action = "Repair mapped-load provenance or mapping counts before using the load."
    if not mapped_loads:
        return [
            _optional_problem(
                "C-MAPLOAD-001",
                "mapped_loads is present but contains no mapped loads.",
                "mapped_loads",
                skill,
                next_action,
            )
        ]

    for item in mapped_loads:
        name = _optional_name(item)
        prefix = f"mapped_loads.{name}"
        if not _valid_nonempty_string(item.get("name") if isinstance(item, Mapping) else None):
            problems.append(
                _optional_problem(
                    "C-MAPLOAD-001",
                    "Mapped load must have a non-empty name.",
                    f"{prefix}.name",
                    skill,
                    next_action,
                )
            )
        elif name in names:
            problems.append(
                _optional_problem(
                    "C-MAPLOAD-001",
                    f"Mapped load name {name!r} conflicts with another declared load.",
                    f"{prefix}.name",
                    skill,
                    next_action,
                )
            )
        else:
            names[name] = prefix

        target_surface = item.get("target_surface") if isinstance(item, Mapping) else None
        if not _valid_nonempty_string(target_surface):
            problems.append(
                _optional_problem(
                    "C-MAPLOAD-001",
                    "Mapped load target_surface must be a non-empty declared surface.",
                    f"{prefix}.target_surface",
                    skill,
                    next_action,
                )
            )
        elif target_surface not in surfaces:
            problems.append(
                _optional_problem(
                    "C-MAPLOAD-001",
                    f"Mapped load {name} references undeclared target surface {target_surface!r}.",
                    f"{prefix}.target_surface",
                    skill,
                    next_action,
                )
            )

        step = item.get("step") if isinstance(item, Mapping) else None
        if not _valid_nonempty_string(step):
            problems.append(
                _optional_problem(
                    "C-MAPLOAD-001",
                    "Mapped load step must be a non-empty declared step.",
                    f"{prefix}.step",
                    skill,
                    next_action,
                )
            )
        elif step not in steps:
            problems.append(
                _optional_problem(
                    "C-MAPLOAD-001",
                    f"Mapped load {name} references undeclared step {step!r}.",
                    f"{prefix}.step",
                    skill,
                    next_action,
                )
            )

        for field in _MAPPED_TEXT_FIELDS:
            value = item.get(field) if isinstance(item, Mapping) else None
            if not _valid_nonempty_string(value):
                problems.append(
                    _optional_problem(
                        "C-MAPLOAD-001",
                        f"Mapped load field {field} must be a non-empty string.",
                        f"{prefix}.{field}",
                        skill,
                        next_action,
                    )
                )

        digest = item.get("source_sha256") if isinstance(item, Mapping) else None
        if not isinstance(digest, str) or re.fullmatch(r"[0-9a-fA-F]{64}", digest) is None:
            problems.append(
                _optional_problem(
                    "C-MAPLOAD-001",
                    "Mapped load source_sha256 must be exactly 64 hexadecimal characters.",
                    f"{prefix}.source_sha256",
                    skill,
                    next_action,
                )
            )

        counts = {}
        valid_counts = True
        for field in _MAPPED_COUNT_FIELDS:
            value = item.get(field) if isinstance(item, Mapping) else None
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                valid_counts = False
                problems.append(
                    _optional_problem(
                        "C-MAPLOAD-001",
                        f"Mapped load count {field} must be a nonnegative integer.",
                        f"{prefix}.{field}",
                        skill,
                        next_action,
                    )
                )
            else:
                counts[field] = value
        if valid_counts and counts["duplicate_face_count"] != 0:
            problems.append(
                _optional_problem(
                    "C-MAPLOAD-001",
                    "Mapped load duplicate_face_count must be zero.",
                    f"{prefix}.duplicate_face_count",
                    skill,
                    next_action,
                )
            )
        if valid_counts and counts["mapped_face_count"] + counts["unmapped_face_count"] != counts["expected_face_count"]:
            problems.append(
                _optional_problem(
                    "C-MAPLOAD-001",
                    "Mapped and unmapped face counts must sum to expected_face_count.",
                    f"{prefix}.face_counts",
                    skill,
                    next_action,
                )
            )

    if problems:
        return sorted(problems, key=lambda item: (item.location, item.message))
    return [
        finding(
            "C-MAPLOAD-001",
            "PASS",
            "Mapped-load provenance, references, digest, and face counts are consistent.",
            "mapped_loads",
            skill,
            "Preserve the source digest and mapping counts through load generation and review.",
        )
    ]


CHECKS = (
    check_units,
    check_unique_names,
    check_references,
    check_step_order,
    check_mesh_intent,
    check_output_coverage,
    check_evidence_boundary,
)


def audit_contract(contract: Mapping[str, Any]) -> tuple[Finding, ...]:
    shape_findings = tuple(check_contract_shape(contract))
    if any(item.status != "PASS" for item in shape_findings):
        return shape_findings
    findings = list(shape_findings)
    for check in CHECKS:
        findings.extend(sorted(check(contract), key=lambda item: (item.location, item.code)))
    if "construction_events" in contract:
        findings.extend(sorted(check_staged_construction(contract), key=lambda item: (item.location, item.code)))
    if "mapped_loads" in contract:
        findings.extend(sorted(check_mapped_load_provenance(contract), key=lambda item: (item.location, item.code)))
    return tuple(findings)
