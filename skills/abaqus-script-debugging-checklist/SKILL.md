---
name: abaqus-script-debugging-checklist
description: Use when an Abaqus Python script raises a traceback, resolves an empty region, misses a repository key, fails to create a job, or cannot open an expected result database.
---

# Abaqus Script Debugging Checklist

## Overview

Establish the first failing boundary before proposing a fix. Capture execution
context, exact error text, repository state, and artifact state separately.

## When to use

Use for reproducible scripting failures and surprising empty selections. Pair
it with a domain skill only after the failing boundary is localized.

## Inputs

- Exact command or GUI action and interpreter context
- Complete traceback or message
- Relevant configuration and source revision
- Expected and observed repository keys or artifacts

## Outputs

Return a diagnosis containing reproduction, first failing operation, evidence,
root cause confidence, smallest reversible fix, and verification command.

## Workflow

1. Reproduce with the smallest read-only or build-only command available.
2. Confirm the intended Python interpreter and Abaqus execution mode.
3. Inspect repository keys before indexing or selecting regions.
4. Trace the failed value backward to its producer.
5. Write a regression check before applying a code fix.

## Safety gates

- Do not rerun an expensive or destructive job merely to obtain a traceback.
- Do not delete databases, lock files, or generated models during diagnosis.
- Do not replace an empty region with a broader region without geometry evidence.
- A successful import proves neither model construction nor solver correctness.

## Example prompts

> Diagnose why a surface lookup is empty after partitioning. Record repository
> keys and the producer-consumer chain. Do not broaden the selection or run a job.

## Common failures

- Fixing the last exception instead of the first invalid state.
- Testing in regular Python when the script requires Abaqus modules.
- Indexing repositories without inspecting available keys.
- Confusing a missing result file with a failed field extraction.

## Acceptance checklist

- [ ] Exact execution context and error text are recorded.
- [ ] The first failing boundary is identified.
- [ ] Root cause is separated from downstream symptoms.
- [ ] Proposed change is minimal and reversible.
- [ ] Verification can distinguish the fix from an unrelated success.
