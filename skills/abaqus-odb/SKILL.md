---
name: abaqus-odb
description: Use when reading an Abaqus ODB to inspect steps, frames, field outputs, history outputs, regions, coordinates, units, extrema, paths, or bounded result exports without modification.
---

# Abaqus ODB Read-Only Inspection

## Overview

Extract bounded, reproducible evidence from a result database. Every reported
value carries database identity, step, frame or time, region, variable,
component or invariant, coordinate interpretation, and units.

## When to use

Use for result inspection, claim audits, monitoring extraction, or diagnosing a
missing field/history output. Do not use it to repair the source model.

## Inputs

- Approved ODB and expected job identity
- Step, frame or time, and named region
- Field or history variable and component/invariant
- Position, coordinate system, units, and aggregation rule
- Export destination and requested evidence format

## Outputs

Return an inventory, extraction table, provenance header, missing-data findings,
and a bounded export plan. Open with `readOnly=True` and close deterministically.

## Workflow

1. Confirm file identity, size, timestamp, and expected job relationship.
2. Inventory steps, frames, instances, sets, surfaces, and available outputs.
3. Resolve the requested region and variable before reading values.
4. Apply explicit component, invariant, position, and aggregation rules.
5. Record provenance and close the database in a guaranteed cleanup path.

## Safety gates

- Always open the database read-only.
- Never infer units from variable names alone.
- Never compare values from different frames, positions, or coordinate systems silently.
- Never overwrite the source database or export into its source directory by default.

## Example prompts

> Read the last converged frame and extract vertical displacement for a named
> monitoring set. Report time, coordinates, units, extrema rule, and provenance.

## Common failures

- Selecting the last frame without checking whether it is the intended state.
- Mixing nodal, integration-point, and extrapolated values.
- Reporting an invariant when a signed component was requested.
- Leaving the database open after an exception.

## Acceptance checklist

- [ ] ODB identity and job relationship are confirmed.
- [ ] Step, frame/time, region, variable, and position are explicit.
- [ ] Component/invariant, coordinates, units, and aggregation are recorded.
- [ ] Missing outputs are reported rather than fabricated.
- [ ] Database closure and export boundaries are verified.

