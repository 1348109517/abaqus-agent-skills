---
name: abaqus-dependency-preflight-validator
description: Use when an Abaqus scripting project spans multiple files and model, part, instance, region, step, job, output, or ODB identifiers may have drifted before execution.
---

# Abaqus Dependency Preflight Validator

## Overview

Perform a static, read-only audit of cross-file contracts before Abaqus is
started. Report mismatches with source locations and downstream consumers.

## When to use

Use after a rename, configuration change, script split, output-path change, or
failed lookup that may cross module boundaries.

## Inputs

- Project root and intended entry point
- Configuration files and naming manifest
- Build-stage order and supported execution mode
- Expected job, input, and result artifacts

## Outputs

Return a dependency table with producer, identifier, consumer, source location,
status, severity, and a smallest-fix recommendation. Separate definite errors
from warnings that require runtime evidence.

## Workflow

1. Inventory configuration, Python, input, and manifest files.
2. Extract declared and consumed identifiers without executing project code.
3. Compare repository names, paths, step order, and job/output relationships.
4. Flag risky patterns such as positional repository assumptions, implicit
   working directories, and CPU/domain disagreement.
5. Stop before edits and present the dependency chain.

## Safety gates

- Do not import project modules when import has side effects.
- Do not open or alter model/result databases during static preflight.
- Do not guess that similar spellings identify the same region.
- Do not advance from warning to confirmed defect without evidence.

## Example prompts

> Preflight this multi-file project after `LINING_SURFACE` was renamed. Show
> every producer and consumer, including output extraction. Diagnose only.

## Common failures

- Searching only Python while the authoritative value lives in configuration.
- Treating dictionary order as a stable repository contract.
- Checking job names without checking their expected result paths.
- Reporting matches without line-level provenance.

## Acceptance checklist

- [ ] Every high-risk identifier has one identified producer.
- [ ] Every consumer resolves to the intended declaration.
- [ ] Step and artifact dependencies are ordered.
- [ ] Findings include file and line evidence.
- [ ] No project code or solver job ran during preflight.

