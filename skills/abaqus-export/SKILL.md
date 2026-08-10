---
name: abaqus-export
description: Use when an approved Abaqus geometry, mesh, input-deck, image, or read-only result export needs a traceable destination and format.
---

# Abaqus Export

## Overview

Treat an export as a controlled transformation with an explicit source,
purpose, format, units, and destination. A successful export is an artifact
record, not automatic engineering evidence.

## When to use

Use when exporting geometry, mesh, input data, images, or selected result data
from an approved Abaqus model or ODB. Use a separate review before exporting
anything that contains private project or manuscript material.

## Inputs

- Approved source model or ODB and read/write status
- Object, step, frame, region, variable, or geometry scope
- Target format, units, coordinate system, and evidence purpose
- Destination directory, overwrite policy, and expected consumers

## Outputs

Return the exported artifact path, source scope, format and unit metadata,
selection rules, validation result, and a SHA-256 or equivalent manifest entry.
State whether the artifact is scoping material, a reproducibility package, or
an engineering-review input.

## Workflow

1. Confirm the source, object scope, format, destination, and authorization.
2. Inspect result exports read-only and record step, frame, variable, region,
   position, aggregation, and coordinate information.
3. Use a no-write preview for geometry, mesh, or input-deck exports.
4. Refuse silent overwrite; create a task-specific destination when approved.
5. Verify existence, size, parseability, metadata, and digest after export.

## Safety gates

- Never overwrite a source model, ODB, existing export, or formal asset.
- Do not export credentials, private data, or proprietary geometry.
- Do not call a guessed or partial export a formal engineering result.
- Do not bypass dry-run, read-only inspection, or human authorization.

## Example prompts

> Prepare a read-only export manifest for the displacement field at the final
> frame on a named synthetic region. List units, coordinates, selection rules,
> destination, and validation checks; do not modify the ODB.

## Common failures

- Omitting the frame or region and exporting an ambiguous result.
- Mixing local and global coordinates or silently changing units.
- Writing an export beside the source and overwriting an earlier artifact.
- Treating an image or input deck as proof of physical correctness.

## Acceptance checklist

- [ ] Source, scope, format, units, coordinates, and destination are explicit.
- [ ] Read-only or no-write behavior was preserved where required.
- [ ] Overwrite and privacy checks passed.
- [ ] Artifact is parseable and its digest is recorded.
- [ ] Evidence status and remaining engineering review are stated.
