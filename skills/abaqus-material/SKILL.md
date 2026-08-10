---
name: abaqus-material
description: Use when defining or reviewing Abaqus density, elasticity, plasticity, permeability, damping, sections, or geotechnical constitutive inputs that require units and provenance.
---

# Abaqus Materials

## Overview

Build a traceable material contract before creating Abaqus material or section
objects. Values without provenance, units, conditions, and model interpretation
remain unresolved inputs.

## When to use

Use for new definitions, unit conversions, section assignment, constitutive
table review, or suspicious stiffness, yielding, density, or permeability.

## Inputs

- Constitutive model and applicable material state
- Parameter values, units, source, and uncertainty
- Temperature, field, drainage, rate, or pressure dependence
- Section type and named assignment region
- Expected calibration or benchmark response

## Outputs

Return a parameter ledger, unit audit, constitutive-table plan, section assignment
map, and verification tests with unresolved fields clearly marked.

## Workflow

1. Select the constitutive family from approved physics.
2. Record each value with source, units, conditions, and conversion.
3. Check Abaqus ordering and dependency variables.
4. Assign sections only to verified named regions.
5. Define a material-point, element, or benchmark response check.

## Safety gates

- Never fill missing values with generic handbook defaults.
- Never mix effective and total stress parameters without an approved model.
- Never infer calibration from solver convergence.
- Never hide unit conversion inside unexplained arithmetic.

## Example prompts

> Review this soil material table for unit and provenance completeness. Identify
> unresolved parameters and propose a single-element verification; do not invent values.

## Common failures

- Density and gravity units belong to different unit systems.
- Dependency columns are supplied in the wrong order.
- A section exists but is not assigned to the intended cells.
- Calibrated parameters are reused outside their stress or drainage range.

## Acceptance checklist

- [ ] Model choice and applicable state are justified.
- [ ] Every value has source, units, conditions, and conversion evidence.
- [ ] Abaqus table ordering is checked.
- [ ] Section assignments cover exactly the intended regions.
- [ ] Independent response checks are defined.

