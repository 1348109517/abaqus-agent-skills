---
name: abaqus-shared-naming-manifest-builder
description: Use when multiple Abaqus scripts or configurations repeat model, part, instance, set, surface, step, job, or result identifiers and require one authoritative naming contract.
---

# Abaqus Shared Naming Manifest Builder

## Overview

Create a small, stable manifest that separates semantic roles from literal
Abaqus repository keys. A name change should occur once and be detected before
runtime if any consumer remains stale.

## When to use

Use when identifiers cross files, stages, or post-processing scripts. Skip it
for a disposable single-file exploration with no reused output.

## Inputs

- Inventory of declared models, parts, instances, regions, steps, jobs, and outputs
- Semantic purpose of every shared identifier
- Configuration format already used by the project
- Compatibility aliases that must remain temporarily readable

## Outputs

Produce a human-readable manifest, a language-level access layer, and a report
of duplicate literals or unresolved aliases.

## Workflow

1. Group names by model, geometry, regions, analysis, jobs, and artifacts.
2. Assign semantic keys such as `excavation_surface`, not numbered placeholders.
3. Preserve Abaqus spelling and case in manifest values.
4. Replace consumers incrementally and run preflight after each group.
5. Remove an alias only after searches and tests find no consumer.

## Safety gates

- Do not rename live repository objects as a side effect of building the manifest.
- Do not merge two regions because their names look similar.
- Do not store machine-specific absolute paths in the manifest.
- Keep configuration values separate from engineering evidence.

## Example prompts

> Build a YAML-neutral naming manifest for the model, soil part, lining
> instance, excavation sets, analysis steps, job, and ODB. Report duplicate
> literals but do not edit the Abaqus model.

## Common failures

- A manifest mirrors file structure instead of semantic ownership.
- Output scripts keep hidden string literals.
- Aliases have no removal criterion.
- Case changes silently break repository lookup.

## Acceptance checklist

- [ ] Each shared identifier has one semantic key and one owner.
- [ ] Literal values preserve required case.
- [ ] Consumers access the manifest rather than repeat strings.
- [ ] Compatibility aliases are documented and tested.
- [ ] No local machine path is part of the naming contract.
