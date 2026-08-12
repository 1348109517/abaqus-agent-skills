"""Deterministic, read-only checks for the synthetic Abaqus demo contract.

The checks in this module validate names and relationships described by the
contract.  They do not load Abaqus, run a solver, or infer physical results.
"""

from collections.abc import Mapping
from typing import Any

from .findings import Finding


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
    string_fields = ("schema_version", "scenario_id")
    for key in string_fields:
        _check_type(problems, contract, (key,), (str,), skill, next_action)

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

    model = contract.get("model")
    if isinstance(model, Mapping):
        _check_type(problems, contract, ("model", "name"), (str,), skill, next_action)
        for key in ("parts", "instances", "sets", "surfaces"):
            _check_type(problems, contract, ("model", key), (list,), skill, next_action)

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

    # The other checks expect lists of objects.  Report malformed entries here
    # so a partially edited contract cannot turn a static audit into a crash.
    list_paths = (
        ("materials",),
        ("sections",),
        ("steps",),
        ("boundary_conditions",),
        ("loads",),
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
    return tuple(findings)
