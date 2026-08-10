---
name: abaqus-load
description: Use when defining or reviewing Abaqus force, moment, pressure, gravity, traction, flux, body load, amplitude, direction, sign, region, or step activation.
---

# Abaqus Loads

## Overview

Encode only approved loads. Preserve magnitude provenance, units, sign
convention, spatial distribution, amplitude, region, and step history.

## When to use

Use before authoring a load or when resultant force, direction, amplitude, or
activation sequence is uncertain.

## Inputs

- Load source and approved numerical values
- Units, sign convention, direction, and coordinate system
- Named target region and area or volume interpretation
- Distribution and amplitude definition
- Creation, modification, and removal steps

## Outputs

Return a load contract, resultant audit plan, object mapping, and output requests
needed to test direction, equilibrium, and activation.

## Workflow

1. Record the physical quantity and source before converting it.
2. Resolve sign and direction in the target coordinate system.
3. Confirm whether the value is total, per area, per volume, or per length.
4. Map the load and amplitude through the step sequence.
5. Define force, moment, energy, reaction, or flux balance evidence.

## Safety gates

- Never invent a magnitude, area, direction, or amplitude.
- Never use a nodal force as an undocumented substitute for pressure.
- Never normalize a distribution without checking its resultant.
- Keep numerical application separate from physical validation.

## Example prompts

> Audit a pressure load whose resultant appears too large. Check units, loaded
> area, normal direction, amplitude, and step history. Diagnose only.

## Common failures

- Confusing total force with pressure.
- Reversing a surface-normal sign after geometry changes.
- Applying gravity twice through separate stages.
- Comparing peak values without time or amplitude context.

## Acceptance checklist

- [ ] Source, units, sign, direction, and coordinate system are explicit.
- [ ] Target region and measure interpretation are correct.
- [ ] Step and amplitude history are complete.
- [ ] Resultant force and moment have an audit method.
- [ ] No unsupported magnitude was introduced.

