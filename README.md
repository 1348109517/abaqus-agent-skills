# Abaqus Agent Skills

[中文说明](README.zh-CN.md) · [Quickstart](docs/quickstart.md) · [Choose a skill](docs/skill-selection.md) · [Compatibility](docs/compatibility.md)

Seventeen reusable workflow skills for AI coding agents that help plan, review, and
audit Abaqus automation. The collection focuses on traceable inputs, stable
naming, diagnosis-first debugging, and an explicit boundary between a solver
run and engineering validation.

## Skill catalog

| Skill | Use it for |
|---|---|
| `abaqus-parametric-project-starter` | Starting a maintainable scripting project |
| `abaqus-dependency-preflight-validator` | Finding cross-file naming and dependency drift |
| `abaqus-shared-naming-manifest-builder` | Defining one naming contract |
| `abaqus-script-debugging-checklist` | Diagnosing scripting and region failures |
| `abaqus-tunnel-local-mesh-rebuilder` | Repairing tunnel-neighborhood topology and mapping |
| `abaqus-bc` | Reviewing supports, symmetry, and prescribed fields |
| `abaqus-load` | Reviewing forces, pressures, gravity, and amplitudes |
| `abaqus-material` | Reviewing traceable material and section definitions |
| `abaqus-step` | Reviewing procedures, increments, and step sequences |
| `abaqus-odb` | Inspecting result databases without modifying them |
| `abaqus-docs` | Verifying release-specific API symbols and signatures |
| `abaqus-export` | Planning approved, traceable geometry and result exports |
| `abaqus-field` | Reviewing initial and predefined field contracts |
| `abaqus-geometry` | Reviewing parts, assemblies, partitions, sets, and surfaces |
| `abaqus-interaction` | Reviewing contact, tie, connectors, and constraints |
| `abaqus-mesh` | Reviewing element choices, controls, quality, and mapping |
| `abaqus-output` | Designing claim-driven field and history output |

## Install

Copy one directory from `skills/` into the skills directory recognized by your
agent, preserving the `SKILL.md` filename. See the [quickstart](docs/quickstart.md)
for examples and the [selection matrix](docs/skill-selection.md) when several
skills appear relevant.

## Validate

```bash
python -m unittest discover -s tests -v
```

The checks require Python 3.10 or newer and do not require Abaqus. See the
[compatibility boundary](docs/compatibility.md) before porting a skill to a
different Abaqus/CAE or embedded Python release.

## Scope and independence

This repository contains workflow guidance, not Abaqus, solver binaries,
official documentation, engineering data, or a substitute for qualified
engineering review. Abaqus is a trademark of Dassault Systemes or its
affiliates. This independent project is not affiliated with or endorsed by
Dassault Systemes or SIMULIA.

Licensed under Apache-2.0. See [NOTICE](NOTICE) and [CONTRIBUTING](CONTRIBUTING.md).
