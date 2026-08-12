# Runnable demo

The v0.3.0 demo is a small, deterministic reference workflow. It loads a
synthetic JSON contract, checks names and relationships that are useful during
an Abaqus automation review, and writes the same findings as Markdown and JSON.
It uses Python's standard library and does not require Abaqus, an ODB, a
license, network access, or third-party packages.

## Run it

From the repository root:

```bash
python scripts/run_demo.py
```

The default `complete` scenario writes
`build/demo/complete/report.json` and `build/demo/complete/report.md`.
Choose a committed scenario explicitly when teaching or debugging:

```bash
python scripts/run_demo.py --scenario complete
python scripts/run_demo.py --scenario naming-drift
python scripts/run_demo.py --scenario evidence-overreach
```

The CLI also accepts a small, explicitly selected contract and output target:

```bash
python scripts/run_demo.py --contract path/to/model-contract.json --output-dir build/demo/custom
```

The output directory is not a substitute for a project data-management plan;
keep real model files and confidential paths out of public examples.

## Data flow

```text
model-contract.json
        |
        v
contract loader -> static checks -> ordered findings -> report writer
                                                   |             |
                                                   v             v
                                             report.json    report.md
```

The contract declares units, model names, materials, sections, steps, boundary
conditions, loads, interactions, mesh intent, output requests, review intent,
and evidence statuses. The checker verifies the declared shape and references;
it does not open a `.cae`, `.odb`, or `.inp` file and does not infer a physical
result.

The JSON report is the machine-readable artifact. It contains the runner and
scenario identity, an input SHA-256 digest, summary counts, ordered findings,
and the evidence-boundary disclaimer. The Markdown report is rendered from the
same finding objects. Reports contain no runtime timestamp by default, so a
repeat run is deterministic and the writer refuses to replace a different
existing report.

See the [synthetic scenario README](../examples/synthetic-tunnel-review/README.md)
for the committed contracts and literal expected non-pass findings.

## Scenarios

| Scenario | What it demonstrates | Expected static result |
|---|---|---|
| `complete` | Consistent synthetic names, references, steps, outputs, and evidence declarations | 8 `PASS`, 0 `WARNING`, 0 `REVIEW_REQUIRED` |
| `naming-drift` | `Gravity` refers to `ExcavationFaceRenamed`, which is not declared | 7 `PASS`, 0 `WARNING`, 1 `REVIEW_REQUIRED` (`C-REF-001`) |
| `evidence-overreach` | An engineering claim is marked approved while solver and physical-review gates are incomplete | 7 `PASS`, 0 `WARNING`, 1 `REVIEW_REQUIRED` (`C-EVIDENCE-001`) |

Expected teaching findings are still successful demo runs. A nonzero exit is
reserved for invalid input or an I/O failure, not for a finding that tells a
human to review a dependency or evidence gate.

## Finding codes

| Code | Static check |
|---|---|
| `C-CONTRACT-001` | Required top-level and collection fields have the expected JSON types |
| `C-UNITS-001` | Length and force units are declared |
| `C-NAME-001` | Names are non-empty and unique within their namespaces |
| `C-REF-001` | Parts, instances, regions, materials, steps, surfaces, and other consumer references resolve |
| `C-STEP-001` | Step orders are unique nonnegative integers |
| `C-MESH-001` | Every declared part has one mesh intent and an element-family declaration |
| `C-OUTPUT-001` | Every output required by the review intent is declared |
| `C-EVIDENCE-001` | An engineering claim does not skip the declared solver and physical-review gates |

Statuses have a narrow meaning:

- `PASS` means that one declared static check passed.
- `WARNING` means that static information is incomplete but the contract can
  still be reviewed.
- `REVIEW_REQUIRED` means that a dependency is broken or an evidence boundary
  is crossed and a person must resolve it before a later workflow stage.

No status means that an Abaqus solver completed, that an ODB was interpreted,
that the model is physically valid, or that an engineering claim is approved.
The [architecture guide](architecture.md) shows the complete stage boundary.

## Validation

Run the focused scenario test and then the complete repository suite:

```bash
python -m unittest tests.test_demo_scenarios -v
python -m unittest discover -s tests -v
```

The tests compare the actual non-pass findings with the committed expected
files. They are packaging and workflow checks, not finite-element validation.
