---
name: abaqus-mesh
description: Use when generating or reviewing Abaqus element types, seeding, mesh controls, local refinement, mesh quality, or interface mapping.
---

# Abaqus Mesh

## Overview

Choose discretization from the engineering quantity and interface behavior it
must resolve. A mesh review records topology, element formulation, controls,
quality observations, and mapping or convergence risks without claiming mesh
independence automatically.

## When to use

Use when selecting element types, seeds, mesh controls, local refinement,
quality checks, or integration-point mapping. Use a dedicated geometry or
tunnel-topology review when the defect begins before meshing.

## Inputs

- Geometry, sections, named regions, interfaces, and analysis procedure
- Engineering quantity, gradients, contact behavior, and expected scales
- Element formulation, seed strategy, local controls, and quality criteria
- Mapping or convergence objective and available synthetic or measured evidence

## Outputs

Return a mesh decision table, element and control plan, region-specific quality
observations, interface rhythm or mapping audit, and unresolved convergence or
physical-review risks.

## Workflow

1. Confirm geometry, sections, regions, interfaces, and procedure first.
2. Define what quantity the mesh must resolve before choosing seed sizes.
3. Select element formulation and local controls with documented reasons.
4. Check interface node rhythm, topology, aspect/skew/quality observations, and
   spatial-field or integration-point mapping assumptions.
5. Record the audit and identify what a mesh-sensitivity study still must test.

## Safety gates

- Do not use global refinement to conceal missing geometry or bad topology.
- Do not infer a universal quality threshold or a solver edition limit.
- Do not equate mesh generation or one converged run with mesh independence.
- Do not alter a read-only source model without explicit authorization.

## Example prompts

> Review a synthetic tunnel-soil mesh plan. Check element choices, local seeds,
> interface node rhythm, quality observations, mapping risks, and the minimum
> sensitivity study needed; do not edit the model.

## Common failures

- Choosing a global seed from a generic table instead of the target quantity.
- Refining a contact interface without checking surface discretization.
- Reporting a quality score without element type, region, or criterion.
- Calling a single mesh result mesh-independent without a comparison plan.

## Acceptance checklist

- [ ] Engineering quantity, procedure, region, and interface objectives are explicit.
- [ ] Element types and local controls have traceable reasons.
- [ ] Quality, topology, mapping, and convergence risks are recorded.
- [ ] Source model and authorization boundaries are respected.
- [ ] Mesh-independence work is separated from solver completion.
