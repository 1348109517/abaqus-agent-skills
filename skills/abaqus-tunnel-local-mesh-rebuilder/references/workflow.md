# Tunnel local mesh rebuilding workflow

## 1. Diagnose

Record geometry partitions, mesh controls, element assignments, global and
local seeds, interface divisions, failed mapping operations, and current
quality statistics. Classify the dominant defect as topology, technique,
seeding, transition, or interface compatibility.

## 2. Design partitions

Prefer partitions that create sweepable or mappable cells around the tunnel.
Use radial bands to control grading, circumferential sectors to align interfaces,
and longitudinal slices to match staged construction or output locations.
Avoid narrow slivers and sector angles that collapse near geometric details.

## 3. Define controls and seeds

Assign mesh techniques per cell and element families per analysis requirement.
State the target interface division count, near-field size, far-field size,
growth limit, and longitudinal division logic. A seed schedule is evidence only
when the resulting cells accept the intended technique.

## 4. Pilot and propagate

Rebuild one representative bounded region. Verify cell technique, connectivity,
interface compatibility, region names, element assignment, Jacobian or shape
quality, aspect ratio, and transition smoothness. Propagate only after the pilot
meets every approved threshold.

## 5. Evidence package

Store the source revision, rebuild script or replay steps, partition inventory,
seed schedule, quality table, interface audit, named-region audit, and images
from consistent views. Keep solver convergence and physical validation as later,
separate gates.
