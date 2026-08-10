# Public adaptation example

This synthetic walkthrough shows how the expanded skills compose without
requiring Abaqus, a CAE file, or an ODB. It is a contract exercise, not a
solver benchmark.

## Scenario

Review a small tunnel-and-soil model plan whose purpose is to compare a
displacement response at a named lining region. The package contains only a
coordinate convention, units, region names, intended steps, and synthetic
observations.

## Skill sequence

1. `abaqus-geometry` checks source dimensions, instances, partitions, sets, and
   surfaces.
2. `abaqus-mesh` records element choices, local controls, interface rhythm, and
   the sensitivity question.
3. `abaqus-interaction` separates contact, tie, and coupling constraints and
   records activation and parameter provenance.
4. `abaqus-bc`, `abaqus-load`, `abaqus-material`, and `abaqus-step` bind the
   physical intent to regions, units, signs, and step history.
5. `abaqus-field` and `abaqus-output` define any mapped initial state and the
   minimum variables and frames needed for the claim.
6. `abaqus-odb` and `abaqus-export` specify read-only inspection and a digestable
   result artifact without changing the source database.

## Stop conditions

Stop with a blocked or conditional review when a coordinate system, unit,
region, frame, mapping rule, interaction parameter, or expected observation is
missing. Do not fill the gap with plausible dimensions or a solver exit code.

## Public boundary

Keep the scenario synthetic. Do not attach real CAE/ODB files, private paths,
manuscripts, credentials, or proprietary material data to reproduce it.
