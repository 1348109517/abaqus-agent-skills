---
name: abaqus-bc
description: Use when defining or reviewing Abaqus displacement, rotation, symmetry, support, pore-pressure, temperature, or other prescribed boundary conditions on named regions and steps.
---

# Abaqus Boundary Conditions

## Overview

Translate an approved physical support or prescribed field into an auditable
region, degree-of-freedom, magnitude, amplitude, and activation contract.

## When to use

Use before creating or changing a boundary condition, or when reactions,
rigid-body motion, symmetry, or step activation suggest a support error.

## Inputs

- Physical restraint or prescribed-field statement
- Named region and coordinate system
- Active degrees of freedom, units, and magnitude
- Creation step, later modifications, and amplitude behavior
- Expected reactions or symmetry evidence

## Outputs

Return a boundary-condition table, Abaqus object plan, conflict audit, and
verification observations. State every unconstrained degree of freedom.

## Workflow

1. Express the physical intent without Abaqus syntax.
2. Resolve the exact region and local/global coordinate system.
3. Map intent to active degrees of freedom and step history.
4. Check duplicate, conflicting, or over-constraining conditions.
5. Define reaction, displacement, or symmetry evidence.

## Safety gates

- Never add a restraint only to suppress convergence trouble.
- Never infer symmetry from visual appearance alone.
- Never prescribe an unknown magnitude or sign.
- Keep support adequacy separate from solver completion.

## Example prompts

> Review the base and side supports for a three-dimensional soil model. List
> constrained degrees of freedom, coordinate systems, conflicts, and reaction
> checks. Do not edit the model.

## Common failures

- Applying a global direction where the region uses a rotated system.
- Leaving an obsolete condition active in later steps.
- Constraining both members of an intended relative motion.
- Reporting a fixed node set without its physical justification.

## Acceptance checklist

- [ ] Region, step, coordinate system, and units are explicit.
- [ ] Every constrained degree of freedom has physical justification.
- [ ] Conflicts and rigid-body modes were checked.
- [ ] Activation history matches the construction sequence.
- [ ] Verification variables and regions are defined.

