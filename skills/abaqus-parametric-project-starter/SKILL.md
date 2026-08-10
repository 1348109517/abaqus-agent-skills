---
name: abaqus-parametric-project-starter
description: Use when starting a new multi-file Abaqus Python automation project that needs explicit configuration, naming, execution, and output boundaries before model code is written.
---

# Abaqus Parametric Project Starter

## Overview

Establish a small project contract before generating model logic. Keep inputs,
names, build stages, and evidence outputs separate so a failed run can be
diagnosed without reconstructing hidden assumptions.

## When to use

Use for a new reusable project or a clean migration. Do not use it to restructure
an established project without an approved migration plan.

## Inputs

- Analysis purpose and acceptance evidence
- Abaqus release and supported Python execution mode
- Geometry source, coordinate system, and units
- Parameter ranges and immutable baseline values
- Intended jobs, outputs, and destination boundary

## Outputs

Produce a layout with `configs/`, `src/`, `tests/`, and `outputs/`; a single
entry point; a naming manifest; one example configuration; and a dry-run or
static-validation command.

## Workflow

1. Freeze the units and coordinate convention.
2. Separate configuration data from Abaqus repository operations.
3. Order stages as geometry, properties, assembly, steps, interactions, loads,
   mesh, outputs, and job creation.
4. Make every stage consume named inputs and return an evidence summary.
5. Add a preflight check before any Abaqus execution.

## Safety gates

- Never invent dimensions, material values, loads, or step controls.
- Keep generated files outside source directories.
- Make destructive rebuilds explicit and opt-in.
- Treat a created job as neither a completed solve nor a validated model.

## Example prompts

> Scaffold a parametric soil-block project with SI units, JSON configuration,
> stable region names, a dry-run preflight, and separate generated outputs. Do
> not create material values or submit a job.

## Common failures

- Configuration contains Abaqus objects instead of serializable values.
- Names are repeated across scripts rather than imported from one manifest.
- The entry point performs irreversible cleanup before validation.
- Output paths depend on the current working directory.

## Acceptance checklist

- [ ] Units, coordinates, version, and execution mode are explicit.
- [ ] One configuration drives one deterministic build path.
- [ ] Shared names have one source of truth.
- [ ] Static validation runs before model mutation.
- [ ] Generated outputs cannot overwrite source files by default.
