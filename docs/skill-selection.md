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
| Schema-1.1 construction activation/deactivation is uncertain | `abaqus-staged-construction-auditor` | `abaqus-step` for ordinary procedure and increments |
| Mapped-load source, digest, units, sign, or face counts are uncertain | `abaqus-mapped-load-provenance-auditor` | `abaqus-load` for ordinary load magnitude/direction; `abaqus-output` for response variables |
| Constitutive inputs lack provenance | `abaqus-material` | step review |
| Procedure, sequence, or increments are uncertain | `abaqus-step` | output/ODB review |
| Results must be extracted without altering the database | `abaqus-odb` | claim-specific audit |
| An API symbol or signature is release-sensitive | `abaqus-docs` | static/runtime compatibility check |
| A geometry, mesh, image, or result must leave the model | `abaqus-export` | provenance and digest audit |
| Stress, temperature, pore pressure, or velocity is mapped | `abaqus-field` | ODB and physical review |
| Parts, partitions, instances, sets, or surfaces are uncertain | `abaqus-geometry` | naming manifest, mesh review |
| Contact, tie, connector, or coupling behavior is uncertain | `abaqus-interaction` | geometry, mesh, boundary review |
| Element type, seed, quality, or interface mapping is uncertain | `abaqus-mesh` | geometry or tunnel-local review |
| Output variables, regions, or sampling are unclear | `abaqus-output` | ODB and claim-readiness audit |

Use the smallest set that covers the decision. A domain skill does not replace
the preflight validator when names and dependencies span files.

The two v0.4.0 auditors are dedicated primary routes: staged construction owns
`construction_events` and mapped-load provenance owns `mapped_loads`. Use the
ordinary step/load/output skills only for their adjacent decisions.

