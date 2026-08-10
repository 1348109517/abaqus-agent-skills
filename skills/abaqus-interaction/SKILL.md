---
name: abaqus-interaction
description: Use when defining or reviewing Abaqus contact, tie, surface interaction, coupling constraints, or connectors between named regions.
---

# Abaqus Interactions

## Overview

Translate a physical interface into an explicit interaction contract. Distinguish
mechanical contact and constraints from analytical theory-to-CAE coupling, and
keep every parameter tied to an approved assumption or source.

## When to use

Use when a model includes contact, tie, cohesive or surface behavior, connectors,
or kinematic/distributing coupling constraints. Use a boundary-condition review
for supports and a mesh review for interface discretization.

## Inputs

- Physical interface and participating named surfaces or regions
- Separation, sliding, adhesion, friction, connector, or constraint intent
- Normal direction, initial clearance or overclosure, and activation step
- Discretization compatibility, parameter sources, and sensitivity assumptions

## Outputs

Return an interface table, Abaqus object plan, activation history, parameter
provenance, conflict audit, and unresolved physical risks. State which behavior
is checked statically and which needs an approved runtime or engineering review.

## Workflow

1. Identify the physical interface and named regions before selecting an API.
2. Distinguish tie, contact, connector, and kinematic/distributing coupling.
3. Check normal direction, initial clearance, discretization, activation, and
   dependency names.
4. Treat friction, penalty stiffness, tolerance, and stabilization as explicit
   inputs or sensitivity assumptions, never unexplained defaults.
5. Define interface observations: status, relative motion, reaction, or energy
   measures appropriate to the claim.

## Safety gates

- Do not infer friction, stiffness, clearance, or contact behavior from an example.
- Do not use an interaction to hide a geometry, support, or convergence defect.
- Do not modify source surfaces or constraints without authorization.
- Do not call a valid interaction definition physical validation.

## Example prompts

> Audit a synthetic soil-structure contact plan. Separate contact, tie, and
> coupling constraints; check surface names, normal direction, activation step,
> friction provenance, and required interface observations.

## Common failures

- Reversing master/slave or normal orientation without checking the interface.
- Activating a tie or contact before the surfaces exist or after they change.
- Treating penalty defaults as calibrated material behavior.
- Confusing analytical-to-CAE coupling with an Abaqus mechanical constraint.

## Acceptance checklist

- [ ] Physical interface and named regions are explicit.
- [ ] Interaction type and activation history match the intent.
- [ ] Parameters, units, signs, and sources are recorded.
- [ ] Interface observations and sensitivity risks are defined.
- [ ] Static, runtime, and engineering-review boundaries are separated.
