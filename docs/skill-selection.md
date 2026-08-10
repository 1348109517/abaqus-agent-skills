# Skill selection

| Symptom or request | Start with | Add when needed |
|---|---|---|
| New multi-file automation project | `abaqus-parametric-project-starter` | naming manifest, preflight |
| A name or region works in one file but not another | `abaqus-dependency-preflight-validator` | debugging checklist |
| Repeated model, set, surface, job, or output names | `abaqus-shared-naming-manifest-builder` | preflight |
| Traceback, empty region, job-build failure | `abaqus-script-debugging-checklist` | relevant domain skill |
| Tunnel mesh is asymmetric or poorly mapped | `abaqus-tunnel-local-mesh-rebuilder` | boundary-condition review |
| Supports or symmetry are uncertain | `abaqus-bc` | step review |
| Magnitude, direction, amplitude, or sign is uncertain | `abaqus-load` | step review |
| Constitutive inputs lack provenance | `abaqus-material` | step review |
| Procedure, sequence, or increments are uncertain | `abaqus-step` | output/ODB review |
| Results must be extracted without altering the database | `abaqus-odb` | claim-specific audit |

Use the smallest set that covers the decision. A domain skill does not replace
the preflight validator when names and dependencies span files.

