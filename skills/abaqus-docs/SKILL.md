---
name: abaqus-docs
description: Use when an Abaqus Python API symbol, method signature, argument, module location, or release compatibility needs verification.
---

# Abaqus API Documentation

## Overview

Use documentation lookup to separate a versioned API fact from runtime behavior
that still requires an Abaqus/CAE check. The result should be precise enough to
review without claiming that a static signature proves a model is correct.

## When to use

Use before authoring or reviewing an Abaqus Python call when the symbol, module,
argument, return type, or supported release is uncertain. Do not use this skill
as a substitute for an authorized model run or an engineering review.

## Inputs

- Object, method, symbol, or error message to verify
- Target Abaqus/CAE or abqpy release and Python context
- Expected behavior and the model operation that depends on it
- Available official manual, installed reference, or type information

## Outputs

Return the module path, callable signature, relevant argument constraints,
release notes, and a short separation of static facts from runtime uncertainty.
Record the source and any unresolved version or licensing limitation.

## Workflow

1. Identify the exact object and operation rather than searching a broad keyword.
2. Check the reference for the target release and execution context.
3. Compare embedded Abaqus Python behavior with any external abqpy type hints.
4. Mark arguments that require a runtime check, model state, or named region.
5. Give a minimal, read-only example and state what it does not establish.

## Safety gates

- Do not invent a signature from a similarly named API object.
- Do not execute an unreviewed snippet against a source model or ODB.
- Do not treat a valid import or signature as solver or physical validation.
- Do not download or redistribute restricted manuals or project data.

## Example prompts

> Verify the release-specific signature for the field-output region accessor.
> Compare the external type hint with the embedded Python context, and list
> which behavior still needs a read-only runtime check.

## Common failures

- Mixing the embedded Python release with a separately installed abqpy package.
- Copying an argument from a neighboring object with a different contract.
- Assuming a static API check changed the model or proved the result.
- Omitting the release, object path, or source of the documented signature.

## Acceptance checklist

- [ ] Object, method, release, and Python context are explicit.
- [ ] Signature and argument constraints have a traceable source.
- [ ] Static facts and runtime observations are separated.
- [ ] No model, ODB, or solver mutation was performed implicitly.
- [ ] Remaining compatibility uncertainty is stated.
