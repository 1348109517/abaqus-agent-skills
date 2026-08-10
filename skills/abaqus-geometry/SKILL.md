---
name: abaqus-geometry
description: Use when creating or reviewing Abaqus parts, sketches, assemblies, instances, partitions, sets, surfaces, or CAD-import geometry from approved inputs.
---

# Abaqus Geometry

## Overview

Plan geometry from explicit source evidence, units, coordinates, and naming
contracts. Separate source geometry, derived construction geometry, and
temporary scoping geometry so a valid API call cannot be mistaken for a valid
engineering model.

## When to use

Use before creating or reviewing parts, sketches, assemblies, instances,
partitions, sets, surfaces, or CAD imports. Use a mesh or interaction review
when the decision depends on discretization or interfaces.

## Inputs

- Approved geometry source, coordinate convention, and unit system
- Part, instance, set, surface, and partition naming contract
- Required dimensions, tolerances, interfaces, and analysis purpose
- Read-only or no-write status of source CAE and reference files

## Outputs

Return a geometry intent table, object and region plan, dependency graph,
uncertainty list, and no-write verification observations. Identify which
dimensions are sourced, derived, assumed, or still missing.

## Workflow

1. Read the source evidence, coordinate convention, units, and naming manifest.
2. Define stable part, instance, set, and surface names before downstream use.
3. Separate source, derived, and temporary geometry and label uncertainty.
4. Prefer named regions and documented geometric predicates over unexplained
   coordinate picks.
5. Produce a no-write preview, then recheck dimensions, orientation, instances,
   regions, and dependency names after any approved change.

## Safety gates

- Do not infer a missing origin, unit system, dimension, or interface.
- Do not modify a read-only source CAE/ODB or delete an existing instance.
- Do not substitute plausible literature dimensions for missing project inputs.
- Do not treat geometry creation as mesh, solver, or physical validation.

## Example prompts

> Review a synthetic tunnel-and-soil assembly plan. Check coordinate systems,
> part/instance names, interface surfaces, partitions, and missing dimensions;
> return a no-write geometry audit.

## Common failures

- Naming a set before its instance or partition dependency is stable.
- Selecting regions with brittle coordinates that fail after a partition.
- Mixing source and derived dimensions without recording the transform.
- Deleting and recreating an instance to hide a dependency error.

## Acceptance checklist

- [ ] Source, units, coordinates, and geometry purpose are explicit.
- [ ] All downstream names and dependencies are stable and traceable.
- [ ] Source, derived, and temporary geometry are distinguished.
- [ ] Region selection predicates are documented and reviewable.
- [ ] No-write or authorization boundaries are respected.
