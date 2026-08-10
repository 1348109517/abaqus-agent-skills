---
name: abaqus-output
description: Use when defining or reviewing Abaqus field or history output variables, regions, frequency, and result-file size controls.
---

# Abaqus Output Requests

## Overview

Design output from the claim or acceptance gate backward. Record variable
availability, position, region, frequency, and expected post-processing so the
result is sufficient but not an unexplained data dump.

## When to use

Use when defining or reviewing field output, history output, diagnostic output,
regions, sampling frequency, or file-size controls. Use the ODB skill for
read-only result extraction and an evidence audit for claim readiness.

## Inputs

- Engineering quantity or acceptance gate to be tested
- Analysis procedure, element type, position, region, and step
- Required variables, sampling frequency, history points, and storage limits
- Expected post-processing keys, units, frames, and claim/evidence mapping

## Outputs

Return a minimum-output table, variable availability checks, named-region and
step audit, frequency rationale, expected file-size or sampling trade-off, and
unverified variable or interpretation risks.

## Workflow

1. Start from the quantity or claim, not a generic variable list.
2. Confirm variable availability for the procedure, element type, position,
   region, and step.
3. Separate full-field evidence from history monitoring and choose the minimum
   useful frame or increment frequency.
4. Cross-check named sets, surfaces, steps, and downstream post-processing keys.
5. Record what output configuration can establish and what still requires an
   ODB, physical, or engineering review.

## Safety gates

- Do not add exhaustive output by default or to conceal an unclear claim.
- Do not treat variable availability as evidence that the result is correct.
- Do not alter a read-only source model or historical output request.
- Do not use output configuration to bypass boundary, material, or evidence gates.

## Example prompts

> Design the minimum field and history output for a synthetic displacement and
> contact-reaction claim. Include regions, variables, positions, frames,
> frequency rationale, and post-processing checks.

## Common failures

- Requesting a variable unavailable for the procedure or element position.
- Sampling too sparsely to resolve a transient or contact event.
- Recording output without units, frame, region, or coordinate metadata.
- Treating a large ODB as a substitute for a clear evidence contract.

## Acceptance checklist

- [ ] Each variable maps to a quantity, claim, or acceptance gate.
- [ ] Availability, region, position, step, units, and frequency are explicit.
- [ ] Full-field and history output are intentionally separated.
- [ ] Storage and post-processing risks are recorded.
- [ ] Solver completion and engineering interpretation remain separate.
