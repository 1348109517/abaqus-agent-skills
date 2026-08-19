---
name: abaqus-staged-construction-auditor
description: Use when a clean-room model contract declares construction_events for staged activation or deactivation and the event set, action, step, or conflict status needs a dedicated static audit.
---

# Abaqus Staged Construction Auditor

## Overview

Audit the optional `construction_events` contract before model generation. This
is a dedicated staged-state route, not a replacement for ordinary procedure,
increment, or step-control review.

## When to use

Use when a contract contains `construction_events` entries with activation or
deactivation of named model sets. Use `abaqus-step` for ordinary procedure,
increment, stabilization, or step-control questions without staged-event
contract evidence.

## Inputs

- Contract `schema_version` set to `1.1`.
- `construction_events` list with `{name, action, region, step}` objects.
- Declared model sets and analysis steps.
- Any approved construction-sequence intent and evidence boundary.

## Outputs

Return a deterministic finding list for `C-STAGE-001` and identify each field
or conflict requiring review. A passing finding means only that the declared
static contract is internally consistent; it does not establish activation
behavior in Abaqus.

## Workflow

1. Confirm the optional section is present as a non-empty list in schema 1.1.
2. Resolve every `region` against model sets only and every `step` against declared steps.
3. Accept only `activate` or `deactivate` actions and non-empty names.
4. Mark any multiple events for the same set and step as a conflict, including repeated actions.
5. Report `C-STAGE-001` findings with locations and the smallest human review action.

## Safety gates

- Keep this audit static and read-only; do not open, mutate, or regenerate a CAE, ODB, or input deck.
- Do not infer physical construction behavior from names, ordering, or a passing finding.
- Do not submit a solver job or approve an engineering claim from this audit.
- Preserve the source contract and separate solver, physical-review, and engineering-claim evidence.

## Example prompts

> Audit this synthetic schema-1.1 `construction_events` section. Check set and
> step references, allowed actions, repeated set-step conflicts, and report
> `C-STAGE-001`; do not modify files or run Abaqus.

## Common failures

- A surface name is supplied where the staged region must be a model set.
- The same set is activated twice in one step or activated and deactivated in one step.
- A missing or misspelled step is treated as an implicit Abaqus step.
- A static pass is reported as proof that the staged model is physically valid.

## Acceptance checklist

- [ ] The contract uses schema version 1.1 when `construction_events` is present.
- [ ] The event list is non-empty and every event has a unique non-empty name.
- [ ] Every region resolves to a declared model set.
- [ ] Every step resolves and every action is `activate` or `deactivate`.
- [ ] No set-step pair has multiple construction events.
- [ ] Findings remain static, deterministic, and separate from solver or engineering approval.
