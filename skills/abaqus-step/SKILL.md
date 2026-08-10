---
name: abaqus-step
description: Use when defining or reviewing an Abaqus procedure, analysis step, increment controls, nonlinear settings, stabilization, construction sequence, or restart relationship.
---

# Abaqus Analysis Steps

## Overview

Represent the intended physical and construction sequence explicitly. Choose a
procedure and controls that produce interpretable evidence, not merely a job
that reaches the final increment.

## When to use

Use when starting an analysis sequence or diagnosing time-increment, activation,
convergence, stabilization, or restart behavior.

## Inputs

- Physical process and required procedure
- Step order, time meaning, and activation events
- Initial, minimum, maximum, and total increment controls
- Nonlinearity, stabilization, damping, and solver choices
- Expected convergence and response evidence

## Outputs

Return a step table, state-transition audit, control rationale, output plan, and
criteria separating numerical completion from physical acceptance.

## Workflow

1. Express each physical stage and state transition.
2. Select the Abaqus procedure from the required physics.
3. Set time and increment controls with documented scale reasoning.
4. Audit loads, boundaries, interactions, and model changes per step.
5. Define convergence, energy, state, and response evidence.

## Safety gates

- Never change procedure or stabilization solely to hide a modeling defect.
- Never treat automatic incrementation as a physical time model by default.
- Never assume a completed step validates boundary conditions or material data.
- Preserve restart compatibility before changing an established sequence.

## Example prompts

> Review a staged excavation sequence with automatic incrementation. Explain
> state transitions, control risks, and evidence needed; do not submit the job.

## Common failures

- Loads or supports are modified in the wrong step.
- Minimum increments are reduced without identifying the failing mechanism.
- Stabilization energy is not compared with relevant strain energy.
- Step completion is reported as engineering validation.

## Acceptance checklist

- [ ] Procedure matches the intended physics.
- [ ] Step order and activation history are explicit.
- [ ] Increment controls have scale-based rationale.
- [ ] Convergence and energy evidence are defined.
- [ ] Solver, physical, and engineering verdicts remain separate.
