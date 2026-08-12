# Synthetic tunnel review scenarios

These three small contracts demonstrate deterministic static review of a
tunnel-and-soil model plan. They contain independently created synthetic names
and values only; they do not require Abaqus/CAE, a solver, an ODB, or private
model files.

Run the committed scenario integration test from the repository root:

```text
python -m unittest tests.test_demo_scenarios -v
```

This test directly loads and audits `complete`, `naming-drift`, and
`evidence-overreach`, then compares each actual non-PASS finding with its
literal `expected-findings.json` file. A future one-command CLI may expose
individual scenario selection; the focused test is the current runnable path.

## Scenarios

| Scenario | Demonstrates | Expected static result |
|---|---|---|
| `complete` | Internally consistent names, references, steps, outputs, and evidence declarations | All checks pass; the contract still stops at the static-review boundary |
| `naming-drift` | The `Gravity` load refers to `ExcavationFaceRenamed` instead of a declared region | `C-REF-001` at `loads.Gravity.region` is `REVIEW_REQUIRED` |
| `evidence-overreach` | An engineering claim is marked `approved` while solver and physical-review gates remain incomplete | `C-EVIDENCE-001` at `evidence.engineering_claim` is `REVIEW_REQUIRED` |

Each directory contains the input contract and a literal expected non-pass
finding list:

- [complete contract](complete/model-contract.json) and [expected findings](complete/expected-findings.json)
- [naming-drift contract](naming-drift/model-contract.json) and [expected findings](naming-drift/expected-findings.json)
- [evidence-overreach contract](evidence-overreach/model-contract.json) and [expected findings](evidence-overreach/expected-findings.json)

## Evidence boundary

`PASS` means only that the declared static contract satisfies a bounded check.
It does not mean that a solver ran, that an ODB was inspected, that the model
is physically valid, or that an engineering claim is approved. A broken name
or an evidence-gate shortcut remains `REVIEW_REQUIRED` until a human resolves
the relevant dependency or evidence gap.
