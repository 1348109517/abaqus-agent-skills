# Abaqus Agent Skills

[中文说明](README.zh-CN.md) · [Quickstart](docs/quickstart.md) · [Demo guide](docs/demo.md) · [Choose a skill](docs/skill-selection.md) · [Compatibility](docs/compatibility.md)

Nineteen reusable workflow skills for AI coding agents that help plan, review, and
audit Abaqus automation. The collection focuses on traceable inputs, stable
naming, diagnosis-first debugging, and an explicit boundary between a solver
run and engineering validation.

## Three-minute quickstart

The runnable demo uses only the Python standard library. It reviews a small,
synthetic tunnel-and-soil contract and writes deterministic Markdown and JSON
reports; it does not install Abaqus or run a solver.

```bash
git clone https://github.com/1348109517/abaqus-agent-skills.git
cd abaqus-agent-skills
python scripts/run_demo.py
```

If a Windows checkout reports `Filename too long`, clone into a short working
directory close to the filesystem root; the
[compatibility guide](docs/compatibility.md) explains the boundary.

The default command reports the `complete` scenario and writes:

```text
build/demo/complete/report.json
build/demo/complete/report.md
```

The five scenario names can also be selected explicitly:

```bash
python scripts/run_demo.py --scenario complete
python scripts/run_demo.py --scenario naming-drift
python scripts/run_demo.py --scenario evidence-overreach
python scripts/run_demo.py --scenario staged-conflict
python scripts/run_demo.py --scenario mapped-load-gap
```

The schema-1.1 `complete` scenario has ten static passes, including staged
construction and mapped-load provenance checks. `naming-drift` identifies an
unresolved region reference, and `evidence-overreach` identifies an engineering
claim that skips solver evidence or physical review. `staged-conflict` and
`mapped-load-gap` demonstrate the two new dedicated findings. These scenarios
are completed static audits and intentionally return exit status 0 while
recording `REVIEW_REQUIRED` findings.

To preview a skill installation without copying files:

```bash
python scripts/install_skill.py abaqus-mesh --target build/install-check
```

The installer is dry-run by default. Add `--apply` only after reviewing the
printed source, destination, and collision state.

Validate the checkout with:

```bash
python -m unittest discover -s tests -v
```

The demo and repository tests do not require Abaqus, an ODB, a license, or
third-party Python packages.

## Evidence handoff

The deterministic `report.json` can be converted into an evidence-contract
0.2 handoff with the stable
[Engineering Evidence Toolkit v0.2.0](https://github.com/1348109517/engineering-evidence-toolkit/releases/tag/v0.2.0).
That adapter records a static audit and its source digests; it deliberately
keeps solver and physical-review lifecycle states gated rather than turning a
static report into an engineering conclusion.

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
| `abaqus-staged-construction-auditor` | Auditing schema-1.1 construction activation and deactivation events |
| `abaqus-mapped-load-provenance-auditor` | Auditing mapped-load source provenance and face counts |
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

See the [demo guide](docs/demo.md) for the schema-1.1 contract data flow, report schema,
scenario details, and finding codes. See the [architecture](docs/architecture.md)
for the boundary between static checks, optional solver evidence, physical
review, and an engineering claim.

## Contributing and citation

Please read [CONTRIBUTING](CONTRIBUTING.md) before opening an issue or pull
request. Contributions must use synthetic or clean-room material and state what
evidence was actually inspected. If this repository is useful in your work,
please use the metadata in [CITATION.cff](CITATION.cff).

## Scope and independence

This repository contains workflow guidance, not Abaqus, solver binaries,
official documentation, engineering data, or a substitute for qualified
engineering review. Abaqus is a trademark of Dassault Systemes or its
affiliates. This independent project is not affiliated with or endorsed by
Dassault Systemes or SIMULIA.

The demo performs static contract checks only. A passing report does not mean
that a solver completed, that an ODB was inspected, that the model is
physically valid, or that an engineering claim is approved. Licensed under
Apache-2.0. See [NOTICE](NOTICE), [CONTRIBUTING](CONTRIBUTING.md), and the
[community launch guide](docs/community-launch.md).
