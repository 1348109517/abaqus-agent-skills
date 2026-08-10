---
name: abaqus-field
description: Use when defining or reviewing Abaqus initial conditions or predefined fields such as stress, temperature, pore pressure, velocity, or approved result mapping.
---

# Abaqus Fields

## Overview

Make an initial or predefined field an explicit contract: source, units, sign
convention, coordinates, target region, step, and mapping evidence. A complete
mapping is an interface result and does not by itself validate the physics.

## When to use

Use when a model starts from a stress, temperature, pore-pressure, velocity,
or other spatial field, or when an approved result must be mapped between
meshes. Use a separate review for constitutive or equilibrium conclusions.

## Inputs

- Field type, source artifact, source step and frame
- Source and target regions, coordinates, units, and sign convention
- Mapping key, tolerance, interpolation or extrapolation rule
- Applicable analysis step and expected compatibility or equilibrium checks

## Outputs

Return a field contract, mapping table or algorithm, coverage and missing-point
counts, duplicate and extrapolation counts, and a list of physical checks that
remain open.

## Workflow

1. Identify the field type, source, target, units, coordinates, and activation
   step before choosing an API object.
2. Define a deterministic source-to-target key and a documented tolerance.
3. Inspect the source read-only and record the selected step and frame.
4. Report coverage, duplicates, missing points, extrapolation, and sign changes.
5. Check equilibrium, compatibility, or conservation requirements appropriate
   to the field before treating it as an engineering input.

## Safety gates

- Do not guess missing coordinates, regions, frames, units, or tolerances.
- Do not write back to a source ODB or alter a read-only historical model.
- Do not treat mapping success as physical validation or solver acceptance.
- Do not hide missing coverage with silent extrapolation.

## Example prompts

> Review a synthetic pore-pressure mapping contract. List source and target
> frames, units, coordinate transforms, coverage, extrapolation, and the
> checks needed before the field can be used in an analysis.

## Common failures

- Applying a field in the wrong step or with an inconsistent sign convention.
- Mapping coordinates from different origins or unit systems.
- Accepting a high coverage percentage while missing a critical interface.
- Confusing a successful API call with equilibrium or compatibility evidence.

## Acceptance checklist

- [ ] Field type, source, step, frame, region, units, and coordinates are explicit.
- [ ] Mapping key, tolerance, and extrapolation policy are reproducible.
- [ ] Coverage, duplicate, missing, and extrapolation counts are recorded.
- [ ] Source data remain read-only.
- [ ] Physical review and unresolved assumptions are visible.
