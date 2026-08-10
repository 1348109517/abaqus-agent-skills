---
name: abaqus-tunnel-local-mesh-rebuilder
description: Use when a tunnel or underpass neighborhood has asymmetric, flower-like, over-dense, poorly swept, or inconsistently mapped soil and lining mesh topology.
---

# Abaqus Tunnel Local Mesh Rebuilder

## Overview

Repair topology before tuning seeds. Build a controllable radial, circumferential,
and longitudinal partition structure whose interfaces and evidence can be audited.

Read [the detailed workflow](references/workflow.md) before changing partitions.

## When to use

Use when local mesh defects arise from partition topology or mapping, not merely
from one incorrect seed value.

## Inputs

- Approved geometry, units, and tunnel alignment
- Existing partition and mesh-control inventory
- Required lining-soil interface and mapping relationships
- Target element families, quality limits, and transition zones

## Outputs

Produce a partition plan, seed schedule, mesh-control map, compatibility audit,
quality summary, before/after evidence, and rollback point.

## Workflow

1. Diagnose topology, controls, and seeds separately.
2. Establish rings or blocks that support structured or sweep meshing.
3. Align circumferential divisions across coupled interfaces.
4. Grade sizes outward with explicit transition ratios.
5. Rebuild one bounded region and verify mapping before propagation.

## Safety gates

- Preserve a recoverable source model or scripted rebuild path.
- Do not infer physical correctness from visual symmetry.
- Do not change interfaces, element formulations, and seeds simultaneously.
- Stop if rebuilt topology invalidates named regions or staged construction.

## Example prompts

> Propose a local tunnel-soil topology repair for a flower-like mesh. Keep the
> tunnel alignment and interface names fixed, define evidence, and do not run a solve.

## Common failures

- Reducing seed size while retaining unsuitable topology.
- Using unmatched circumferential divisions at an interface.
- Judging quality from one screenshot.
- Rebuilding globally before a local pilot passes.

## Acceptance checklist

- [ ] Topology supports the intended mesh technique.
- [ ] Interface divisions and node mapping are compatible.
- [ ] Size transitions meet the approved limits.
- [ ] Named regions and stages remain valid.
- [ ] Quality metrics and rollback evidence are recorded.
