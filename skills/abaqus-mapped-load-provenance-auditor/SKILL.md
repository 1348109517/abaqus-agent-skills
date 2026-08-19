---
name: abaqus-mapped-load-provenance-auditor
description: Use when a clean-room model contract declares mapped_loads and source-to-surface provenance, digest, units, sign, or face-count consistency needs a dedicated static audit.
---

# Abaqus Mapped Load Provenance Auditor

## Overview

Audit the optional `mapped_loads` contract before a mapped load is generated or
used as evidence. This is a provenance-and-count route, not a replacement for
ordinary load magnitude review or approved artifact export.

## When to use

Use when a schema-1.1 contract records source-to-surface mapping with
`source_sha256`, coordinate system, units, sign convention, and face counts.
Use `abaqus-load` for ordinary force, pressure, amplitude, or direction review;
use `abaqus-export` for an approved file or result leaving the model.

## Inputs

- Contract `schema_version` set to `1.1`.
- `mapped_loads` entries with `name`, `target_surface`, `step`, `source_id`,
  `source_sha256`, `coordinate_system`, `source_units`, `target_units`, and
  `sign_convention`.
- Nonnegative `expected_face_count`, `mapped_face_count`,
  `duplicate_face_count`, and `unmapped_face_count`.
- Declared target surfaces and analysis steps.

## Outputs

Return deterministic `C-MAPLOAD-001` findings for unresolved references,
provenance defects, invalid digests, nonzero duplicate counts, or count gaps.
Accept counts only when `expected_face_count` equals
`mapped_face_count + unmapped_face_count` and `duplicate_face_count` is zero.

## Workflow

1. Confirm the optional section is present as a non-empty list in schema 1.1.
2. Resolve `target_surface` and `step` against declared model entities.
3. Check non-empty provenance strings and an exactly 64-character hexadecimal `source_sha256`.
4. Check nonnegative integer counts, zero duplicates, and mapped/unmapped consistency.
5. Report `C-MAPLOAD-001` with the failing location and a bounded review action.

## Safety gates

- Keep this audit static and read-only; do not edit a CAE, ODB, input deck, source file, or mapped result.
- Do not recompute or invent source values, units, signs, coordinates, or face counts.
- Do not treat a digest match or a passing count check as proof of physical load correctness.
- Do not submit a solver job, export an artifact, or approve an engineering claim from this audit.

## Example prompts

> Audit this synthetic schema-1.1 `mapped_loads` section. Verify surface and
> step references, source digest, units, sign, and face-count consistency;
> report `C-MAPLOAD-001` and do not modify files or run Abaqus.

## Common failures

- A source digest is copied with fewer or more than 64 hexadecimal characters.
- Source and target units or coordinate systems are omitted during mapping.
- Duplicate faces are hidden by folding them into the mapped count.
- A static mapping audit is reported as load equilibrium or physical validation.
- A normal pressure-direction question is routed here instead of to `abaqus-load`.

## Acceptance checklist

- [ ] The contract uses schema version 1.1 when `mapped_loads` is present.
- [ ] Every mapped load resolves to a declared target surface and step.
- [ ] Provenance strings and source digest are present and valid.
- [ ] All four counts are nonnegative integers; duplicates are zero.
- [ ] Mapped plus unmapped faces equals expected faces.
- [ ] Findings remain static, deterministic, and separate from solver or engineering approval.
