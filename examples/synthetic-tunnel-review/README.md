# Synthetic tunnel review scenarios

These five small contracts demonstrate deterministic static review of a
tunnel-and-soil model plan. They contain independently created synthetic names
and values only; they do not require Abaqus/CAE, a solver, an ODB, or private
model files.

Run any committed scenario from the repository root:

```text
python scripts/run_demo.py --scenario <name>
```

Replace `<name>` with `complete`, `naming-drift`, `evidence-overreach`,
`staged-conflict`, or `mapped-load-gap`. The
command writes `report.json` and `report.md` under `build/demo/<name>/` by
default. It performs static contract review only: it does not start Abaqus, run
a solver, inspect an ODB, or establish physical engineering validity.

## Scenarios

| Scenario | Demonstrates | Expected static result |
|---|---|---|
| `complete` | Internally consistent schema-1.1 names, references, construction event, mapped load, outputs, and evidence declarations | 10 static checks pass; the contract still stops at the static-review boundary |
| `naming-drift` | The `Gravity` load refers to `ExcavationFaceRenamed` instead of a declared region | `C-REF-001` at `loads.Gravity.region` is `REVIEW_REQUIRED` |
| `evidence-overreach` | An engineering claim is marked `approved` while solver and physical-review gates remain incomplete | `C-EVIDENCE-001` at `evidence.engineering_claim` is `REVIEW_REQUIRED` |
| `staged-conflict` | Two events target `LiningVolume` in `Excavation` | Two `C-STAGE-001` conflict findings are `REVIEW_REQUIRED` |
| `mapped-load-gap` | Mapped and unmapped faces do not equal expected faces | `C-MAPLOAD-001` at `mapped_loads.MappedFacePressure.face_counts` is `REVIEW_REQUIRED` |

Each directory contains the input contract and a literal expected non-pass
finding list:

- [complete contract](complete/model-contract.json) and [expected findings](complete/expected-findings.json)
- [naming-drift contract](naming-drift/model-contract.json) and [expected findings](naming-drift/expected-findings.json)
- [evidence-overreach contract](evidence-overreach/model-contract.json) and [expected findings](evidence-overreach/expected-findings.json)
- [staged-conflict contract](staged-conflict/model-contract.json) and [expected findings](staged-conflict/expected-findings.json)
- [mapped-load-gap contract](mapped-load-gap/model-contract.json) and [expected findings](mapped-load-gap/expected-findings.json)

## Evidence boundary

`PASS` means only that the declared static contract satisfies a bounded check.
It does not mean that a solver ran, that an ODB was inspected, that the model
is physically valid, or that an engineering claim is approved. A broken name
or an evidence-gate shortcut remains `REVIEW_REQUIRED` until a human resolves
the relevant dependency or evidence gap.
